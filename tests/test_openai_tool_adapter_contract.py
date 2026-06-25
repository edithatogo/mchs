from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TOOL_DEFINITIONS = ROOT / "contracts" / "openai-adapter" / "tool-definitions.md"
README = ROOT / "contracts" / "openai-adapter" / "README.md"
EXAMPLES = ROOT / "contracts" / "openai-adapter" / "examples.md"
CANONICAL = ROOT / "contracts" / "canonical"
RELATIONSHIP = ROOT / "contracts" / "surfaces" / "api-mcp-openai-relationship.json"
TRACK = ROOT / "conductor" / "tracks" / "openai_tool_adapter_20260513"
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / "openai_tool_adapter_20260513"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(_read(path)))


def _tool_blocks() -> list[dict[str, Any]]:
    blocks = re.findall(r"```json\n(.*?)\n```", _read(TOOL_DEFINITIONS), re.S)
    return [cast(dict[str, Any], json.loads(block)) for block in blocks]


def test_openai_tool_definitions_are_parseable_strict_function_tools():
    tools = _tool_blocks()

    assert {tool["function"]["name"] for tool in tools} == {
        "list_calculators",
        "get_schema",
        "validate_input",
        "calculate",
        "explain_result",
        "get_evidence",
    }

    for tool in tools:
        assert tool["type"] == "function"
        function = cast(dict[str, Any], tool["function"])
        parameters = cast(dict[str, Any], function["parameters"])

        assert function["strict"] is True
        assert isinstance(function["name"], str)
        assert isinstance(function["description"], str)
        assert parameters["type"] == "object"
        assert parameters["additionalProperties"] is False
        assert isinstance(parameters["properties"], dict)
        assert set(parameters["required"]).issubset(parameters["properties"])


def test_openai_adapter_is_generated_from_canonical_surface_boundary():
    relationship = _json(RELATIONSHIP)
    openai_surface = {
        item["surface"]: item for item in relationship["relationships"]
    }["openai-tool-adapter"]
    readme = _read(README)
    examples = _read(EXAMPLES)
    metadata = _json(TRACK / "metadata.json")

    canonical_schemas = {
        path.name for path in CANONICAL.glob("*.schema.json") if path.is_file()
    }
    assert {
        "calculator.schema.json",
        "diagnostics.schema.json",
        "evidence.schema.json",
        "provenance.schema.json",
        "support-status.schema.json",
    }.issubset(canonical_schemas)

    assert openai_surface["schema_source"] == "contracts/canonical"
    assert openai_surface["owns_calculator_logic"] is False
    assert openai_surface["emulates_llm_endpoint"] is False
    assert "generated from" in readme
    assert "contracts/canonical/" in readme
    assert "No formula logic" in readme
    assert "/v1/chat/completions" in _read(TRACK / "spec.md")
    assert "diagnostics" in examples
    assert "evidence" in examples.lower()
    assert "contracts/openai-adapter/tool-definitions.md" in metadata[
        "completion_evidence"
    ]
