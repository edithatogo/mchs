from __future__ import annotations

import json
from http import HTTPStatus
from io import BytesIO, StringIO

from nwau_py import mcp_http_server, mcp_server


def _structured(result):
    return result["structuredContent"]


class _FakeHttpHandler(mcp_http_server.McpHttpHandler):
    def __init__(self, *, path="/", body=b"", headers=None):
        self.path = path
        self.headers = dict(headers or {})
        self.headers.setdefault("Content-Length", str(len(body)))
        self.rfile = BytesIO(body)
        self.wfile = BytesIO()
        self.responses = []
        self.sent_headers = []

    def send_response(self, status):  # noqa: D401
        self.responses.append(status)

    def send_header(self, key, value):  # noqa: D401
        self.sent_headers.append((key, value))

    def end_headers(self):  # noqa: D401
        self.sent_headers.append(("__end__", ""))

    def address_string(self):  # noqa: D401
        return "127.0.0.1"


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


def test_mcp_validate_input_reports_year_and_shape_errors():
    unsupported_year = mcp_server.call_tool(
        "mchs.validate_input",
        {"calculatorId": "acute", "year": "2030", "inputs": {}},
    )
    bad_inputs = mcp_server.call_tool(
        "mchs.validate_input",
        {"calculatorId": "acute", "year": "2025", "inputs": []},
    )

    assert _structured(unsupported_year)["diagnostics"]["diagnostics"][0]["code"] == "MCHS-ERR-SCOPE-001"
    assert _structured(bad_inputs)["diagnostics"]["diagnostics"][0]["code"] == "MCHS-ERR-VAL-001"


def test_mcp_calculate_does_not_duplicate_formula_logic():
    result = mcp_server.call_tool(
        "mchs.calculate",
        {"calculatorId": "acute", "year": "2025", "inputs": {"DRG": "A01A"}},
    )

    payload = _structured(result)
    assert payload["result"] is None
    assert payload["diagnostics"]["diagnostics"][0]["code"] == "MCHS-WARN-MCP-001"
    assert "delegated" in payload["diagnostics"]["diagnostics"][0]["message"]


def test_mcp_calculate_and_explain_surface_validation_errors():
    calculate = mcp_server.call_tool(
        "mchs.calculate",
        {"calculatorId": "bad", "year": "2025", "inputs": {}},
    )
    explain = mcp_server.call_tool(
        "mchs.explain_result",
        {"calculatorId": "bad", "year": "2025", "inputs": {}},
    )

    assert calculate["isError"] is True
    assert "Calculator 'bad' not found" in calculate["content"][0]["text"]
    assert explain["isError"] is True
    assert "Calculator 'bad' not found" in explain["content"][0]["text"]


def test_mcp_explain_result_returns_boundary_steps():
    result = mcp_server.call_tool(
        "mchs.explain_result",
        {"calculatorId": "acute", "year": "2025", "inputs": {}},
    )
    payload = _structured(result)

    assert payload["steps"][0]["label"] == "Validate MCP request boundary"
    assert payload["calculatorId"] == "acute"


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


def test_mcp_schema_index_calculators_evidence_and_unknown_resource_paths():
    schemas = json.loads(mcp_server.read_resource("mchs://schemas")["contents"][0]["text"])
    calculators = json.loads(
        mcp_server.read_resource("mchs://calculators")["contents"][0]["text"]
    )
    evidence = json.loads(
        mcp_server.read_resource("mchs://evidence/custom-bundle")["contents"][0]["text"]
    )

    assert "calculator" in schemas["schemas"]
    assert {item["id"] for item in calculators} >= {"acute", "ed"}
    assert evidence["bundleId"] == "custom-bundle"

    try:
        mcp_server.read_resource("mchs://missing")
    except mcp_server.McpError as error:
        assert error.code == "MCHS-ERR-NOTFOUND-002"
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("unknown resource should raise McpError")


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


def test_mcp_json_rpc_lists_reads_notifications_and_errors():
    tools = mcp_server.handle_json_rpc(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
    )
    resources = mcp_server.handle_json_rpc(
        {"jsonrpc": "2.0", "id": 2, "method": "resources/list", "params": {}}
    )
    read = mcp_server.handle_json_rpc(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/read",
            "params": {"uri": "mchs://support/status"},
        }
    )
    notification = mcp_server.handle_json_rpc(
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
    )
    unknown = mcp_server.handle_json_rpc(
        {"jsonrpc": "2.0", "id": 4, "method": "bad/method", "params": {}}
    )

    assert tools is not None and tools["result"]["tools"]
    assert resources is not None and resources["result"]["resources"]
    assert read is not None and read["result"]["contents"][0]["uri"] == "mchs://support/status"
    assert notification is None
    assert unknown is not None and unknown["error"]["code"] == -32000


def test_mcp_unknown_tool_and_schema_error_are_reported_as_tool_errors():
    unknown_tool = mcp_server.call_tool("mchs.missing", {})
    missing_schema = mcp_server.call_tool("mchs.get_schema", {"calculatorId": "bad"})

    assert unknown_tool["isError"] is True
    assert "MCHS-ERR-NOTFOUND-003" in unknown_tool["content"][0]["text"]
    assert missing_schema["isError"] is True
    assert "MCHS-ERR-NOTFOUND-001" in missing_schema["content"][0]["text"]


def test_mcp_stdio_main_skips_blank_lines_and_writes_json(monkeypatch):
    stdin = StringIO(
        "\n"
        + json.dumps({"jsonrpc": "2.0", "id": 11, "method": "tools/list", "params": {}})
        + "\n"
    )
    stdout = StringIO()
    monkeypatch.setattr(mcp_server.sys, "stdin", stdin)
    monkeypatch.setattr(mcp_server.sys, "stdout", stdout)

    mcp_server.main()

    payload = json.loads(stdout.getvalue())
    assert payload["id"] == 11
    assert payload["result"]["tools"][0]["name"].startswith("mchs.")


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
    response = mcp_http_server.handle_http_json_rpc(
        {"jsonrpc": "2.0", "id": 7, "method": "tools/list", "params": {}}
    )

    assert response is not None
    assert response["id"] == 7
    assert response["result"]["tools"][0]["name"].startswith("mchs.")


def test_mcp_http_get_paths_return_health_card_and_not_found():
    health = _FakeHttpHandler(path="/healthz")
    card = _FakeHttpHandler(path="/.well-known/mcp/server-card.json")
    missing = _FakeHttpHandler(path="/missing")

    health.do_GET()
    card.do_GET()
    missing.do_GET()

    health_payload = json.loads(health.wfile.getvalue().decode("utf-8"))
    card_payload = json.loads(card.wfile.getvalue().decode("utf-8"))

    assert health.responses == [HTTPStatus.OK]
    assert health_payload["transport"] == "streamable-http"
    assert card.responses == [HTTPStatus.OK]
    assert card_payload["serverInfo"]["name"] == "io.github.edithatogo/mchs"
    assert missing.responses == [HTTPStatus.NOT_FOUND]


def test_mcp_http_post_paths_validate_json_rpc_body_and_notifications():
    missing_route = _FakeHttpHandler(path="/missing", body=b"{}")
    empty = _FakeHttpHandler(path="/mcp", body=b"", headers={"Content-Length": "0"})
    bad_json = _FakeHttpHandler(path="/mcp", body=b"{")
    array_body = _FakeHttpHandler(path="/mcp", body=b"[]")
    notification = _FakeHttpHandler(
        path="/mcp",
        body=json.dumps(
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
        ).encode("utf-8"),
    )
    request = _FakeHttpHandler(
        path="/mcp",
        body=json.dumps(
            {"jsonrpc": "2.0", "id": 9, "method": "resources/list", "params": {}}
        ).encode("utf-8"),
    )

    missing_route.do_POST()
    empty.do_POST()
    bad_json.do_POST()
    array_body.do_POST()
    notification.do_POST()
    request.do_POST()

    assert missing_route.responses == [HTTPStatus.NOT_FOUND]
    assert empty.responses == [HTTPStatus.BAD_REQUEST]
    assert bad_json.responses == [HTTPStatus.BAD_REQUEST]
    assert array_body.responses == [HTTPStatus.BAD_REQUEST]
    assert notification.responses == [HTTPStatus.ACCEPTED]
    assert request.responses == [HTTPStatus.OK]
    assert json.loads(request.wfile.getvalue().decode("utf-8"))["id"] == 9


def test_mcp_http_run_closes_server_after_serving(monkeypatch):
    events = []

    class _Server:
        def __init__(self, address, handler):
            events.append(("init", address, handler))

        def serve_forever(self):
            events.append(("serve",))

        def server_close(self):
            events.append(("close",))

    monkeypatch.setattr(mcp_http_server, "ThreadingHTTPServer", _Server)

    mcp_http_server.run(host="127.0.0.2", port=9876)

    assert events == [
        ("init", ("127.0.0.2", 9876), mcp_http_server.McpHttpHandler),
        ("serve",),
        ("close",),
    ]


def test_mcp_http_main_parses_host_and_port(monkeypatch):
    calls = []
    monkeypatch.setattr(mcp_http_server, "run", lambda **kwargs: calls.append(kwargs))
    monkeypatch.setattr(
        "sys.argv",
        ["mchs-mcp-http", "--host", "0.0.0.0", "--port", "9999"],
    )

    mcp_http_server.main()

    assert calls == [{"host": "0.0.0.0", "port": 9999}]


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
