from __future__ import annotations

import json

from nwau_py import mcp_server


def _structured(result):
    return result["structuredContent"]


def test_mcp_lists_contract_tools():
    names = {tool["name"] for tool in mcp_server.list_tools()}

    assert names == {
        "mchs.list_calculators",
        "mchs.get_schema",
        "mchs.validate_input",
        "mchs.calculate",
        "mchs.explain_result",
        "mchs.get_evidence",
    }


def test_mcp_lists_calculators_from_contract_boundary():
    result = mcp_server.call_tool("mchs.list_calculators", {"year": "2025"})
    calculators = _structured(result)

    assert {calculator["id"] for calculator in calculators} >= {"acute", "ed"}
    assert all("2025" in calculator["supportedYears"] for calculator in calculators)


def test_mcp_validate_input_reports_unsupported_calculator():
    result = mcp_server.call_tool(
        "mchs.validate_input",
        {"calculatorId": "bad", "year": "2025", "inputs": {}},
    )

    payload = _structured(result)
    assert payload["valid"] is False
    assert payload["diagnostics"]["diagnostics"][0]["code"] == "MCHS-ERR-NOTFOUND-001"


def test_mcp_calculate_does_not_duplicate_formula_logic():
    result = mcp_server.call_tool(
        "mchs.calculate",
        {"calculatorId": "acute", "year": "2025", "inputs": {"DRG": "A01A"}},
    )

    payload = _structured(result)
    assert payload["result"] is None
    assert payload["diagnostics"]["diagnostics"][0]["code"] == "MCHS-WARN-MCP-001"
    assert "delegated" in payload["diagnostics"]["diagnostics"][0]["message"]


def test_mcp_resource_read_returns_support_scope():
    result = mcp_server.read_resource("mchs://support/status")
    payload = json.loads(result["contents"][0]["text"])

    assert payload["dockerRequired"] is False
    assert payload["status"] == "ready-for-local-use"


def test_mcp_schema_resource_returns_canonical_packaged_schema():
    result = mcp_server.read_resource("mchs://schemas/calculator")
    payload = json.loads(result["contents"][0]["text"])

    assert payload["$id"] == "https://mchs.example.org/schemas/calculator.json"
    assert payload["title"] == "Calculator"


def test_mcp_json_rpc_initialize_and_tool_call():
    init = mcp_server.handle_json_rpc(
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    )
    assert init is not None
    assert init["result"]["serverInfo"]["name"] == "mchs"

    call = mcp_server.handle_json_rpc(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "mchs.get_evidence",
                "arguments": {"bundleId": "mcp-server-readiness-20260516"},
            },
        }
    )
    assert call is not None
    support_scope = call["result"]["structuredContent"]["supportScope"]
    assert support_scope["dockerRequired"] is False


def test_mcp_registry_metadata_is_prepared_but_not_overclaimed():
    metadata = json.loads(
        (
            mcp_server._project_root()
            / "contracts"
            / "mcp"
            / "registry"
            / "server.json"
        ).read_text(encoding="utf-8")
    )

    assert metadata["$schema"].endswith("/2025-12-11/server.schema.json")
    assert metadata["name"] == "io.github.edithatogo/mchs"
    assert metadata["packages"][0]["registryType"] == "pypi"
    assert metadata["packages"][0]["identifier"] == "nwau-py"
    assert metadata["packages"][0]["transport"]["type"] == "stdio"


def test_pypi_readme_contains_mcp_registry_verification_marker():
    readme = (mcp_server._project_root() / "nwau_py" / "README.md").read_text(
        encoding="utf-8"
    )

    assert "<!-- mcp-name: io.github.edithatogo/mchs -->" in readme


def test_mcp_http_server_card_matches_contract_tools():
    from nwau_py import mcp_http_server

    card = mcp_http_server.server_card()

    assert card["serverInfo"]["name"] == "io.github.edithatogo/mchs"
    assert card["authentication"] == {"required": False, "schemes": []}
    assert {tool["name"] for tool in card["tools"]} == {
        "mchs.list_calculators",
        "mchs.get_schema",
        "mchs.validate_input",
        "mchs.calculate",
        "mchs.explain_result",
        "mchs.get_evidence",
    }
    assert card["metadata"]["transport"] == "streamable-http"


def test_mcp_http_dispatch_reuses_json_rpc_handler():
    from nwau_py import mcp_http_server

    response = mcp_http_server.handle_http_json_rpc(
        {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}}
    )

    assert response is not None
    assert response["id"] == 7
    assert response["result"]["tools"][0]["name"].startswith("mchs.")


def test_mcp_registry_readiness_contracts_are_explicit():
    root = mcp_server._project_root()
    smithery = (
        root / "contracts" / "mcp" / "registry" / "smithery-readiness-contract.md"
    ).read_text(encoding="utf-8")
    docker = (
        root
        / "contracts"
        / "mcp"
        / "registry"
        / "docker-mcp-registry-readiness-contract.md"
    ).read_text(encoding="utf-8")

    assert "Streamable HTTP" in smithery
    assert "/.well-known/mcp/server-card.json" in smithery
    assert "Dockerfile" in docker
    assert "task validate -- --name mchs" in docker


def test_docker_registry_candidate_metadata_is_prepared_not_published():
    root = mcp_server._project_root()
    server_yaml = (
        root / "contracts" / "mcp" / "registry" / "docker" / "server.yaml"
    ).read_text(encoding="utf-8")
    tools_json = json.loads(
        (root / "contracts" / "mcp" / "registry" / "docker" / "tools.json").read_text(
            encoding="utf-8"
        )
    )

    assert "name: mchs" in server_yaml
    assert "image: mcp/mchs" in server_yaml
    assert "type: server" in server_yaml
    assert {tool["name"] for tool in tools_json} >= {"mchs.list_calculators"}
