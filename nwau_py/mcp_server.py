"""Minimal stdio MCP server for the MCHS calculator contract.

The server is intentionally thin: it exposes the MCP tool and resource surface
and delegates domain truth to existing contract files and package metadata. It
does not implement calculator formula logic.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

try:
    from .contracts import CALCULATOR_IDENTIFIERS
except ModuleNotFoundError as error:
    if error.name != "pydantic":
        raise
    CALCULATOR_IDENTIFIERS = frozenset(
        {
            "acute",
            "adjust",
            "community_mh",
            "ed",
            "mh",
            "outpatients",
            "subacute",
        }
    )

SERVER_NAME = "mchs"
SERVER_REGISTRY_NAME = "io.github.edithatogo/mchs"
PROTOCOL_VERSION = "2024-11-05"
SUPPORTED_YEARS = ("2024", "2025")


def server_version() -> str:
    """Return the installed distribution version for registry metadata."""
    try:
        return version("nwau_py")
    except PackageNotFoundError:
        return "0.0.0+local"


@dataclass(frozen=True, slots=True)
class McpError(Exception):
    """Domain error converted into MCP tool content."""

    code: str
    message: str


def _project_root() -> Path:
    package_root = Path(__file__).resolve().parents[1]
    if (package_root / "contracts").exists():
        return package_root
    return Path.cwd()


def _contract_path(*parts: str) -> Path:
    packaged_path = Path(__file__).resolve().parent.joinpath("mcp_assets", *parts)
    if packaged_path.exists():
        return packaged_path
    return _project_root().joinpath("contracts", *parts)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _diagnostics(
    *,
    severity: str,
    code: str,
    message: str,
    path: str | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if path is not None:
        item["path"] = path
    return {
        "diagnostics": [item],
        "summary": {
            "errorCount": 1 if severity == "error" else 0,
            "warningCount": 1 if severity == "warning" else 0,
            "infoCount": 1 if severity == "info" else 0,
        },
    }


def _tool_error(code: str, message: str) -> dict[str, Any]:
    return {
        "isError": True,
        "content": [
            {
                "type": "text",
                "text": f"Error {code}: {message}",
            }
        ],
    }


def _text_result(payload: Any) -> dict[str, Any]:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(payload, sort_keys=True),
            }
        ],
        "structuredContent": payload,
    }


def _calculator_display_name(calculator_id: str) -> str:
    return calculator_id.replace("_", " ").title()


def _calculator_record(calculator_id: str) -> dict[str, Any]:
    return {
        "id": calculator_id,
        "displayName": _calculator_display_name(calculator_id),
        "description": (
            "MCHS calculator exposed through the canonical Python runtime "
            "and contract schemas."
        ),
        "version": server_version(),
        "supportedYears": list(SUPPORTED_YEARS),
        "inputSchema": {
            "$ref": "mchs://schemas/calculator",
            "format": "json-schema",
        },
        "outputSchema": {
            "$ref": "mchs://schemas/calculator",
            "format": "json-schema",
        },
        "supportStatus": "validated-python-runtime",
    }


def list_calculators(arguments: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Return calculators exposed by the current Python contract boundary."""
    args = arguments or {}
    year = str(args.get("year", "")).strip()
    calculators = [
        _calculator_record(calculator_id)
        for calculator_id in sorted(CALCULATOR_IDENTIFIERS)
    ]
    if year:
        calculators = [
            calculator
            for calculator in calculators
            if year in calculator["supportedYears"]
        ]
    return calculators


def get_schema(arguments: dict[str, Any]) -> dict[str, Any]:
    """Return a canonical JSON Schema by calculator/direction request."""
    calculator_id = str(arguments.get("calculatorId", "")).strip()
    if calculator_id and calculator_id not in CALCULATOR_IDENTIFIERS:
        raise McpError(
            "MCHS-ERR-NOTFOUND-001",
            f"Calculator '{calculator_id}' not found.",
        )
    return _read_schema("calculator")


def validate_input(arguments: dict[str, Any]) -> dict[str, Any]:
    """Validate common MCP calculator request fields."""
    calculator_id = str(arguments.get("calculatorId", "")).strip()
    year = str(arguments.get("year", "")).strip()
    inputs = arguments.get("inputs")
    if calculator_id not in CALCULATOR_IDENTIFIERS:
        return {
            "valid": False,
            "diagnostics": _diagnostics(
                severity="error",
                code="MCHS-ERR-NOTFOUND-001",
                message=(
                    f"Calculator '{calculator_id}' not found. Use "
                    "mchs.list_calculators to see available calculators."
                ),
                path="/calculatorId",
            ),
        }
    if year not in SUPPORTED_YEARS:
        return {
            "valid": False,
            "diagnostics": _diagnostics(
                severity="error",
                code="MCHS-ERR-SCOPE-001",
                message=(
                    f"Year '{year}' is outside the validated MCP server "
                    f"scope: {', '.join(SUPPORTED_YEARS)}."
                ),
                path="/year",
            ),
        }
    if not isinstance(inputs, dict):
        return {
            "valid": False,
            "diagnostics": _diagnostics(
                severity="error",
                code="MCHS-ERR-VAL-001",
                message="inputs must be a JSON object.",
                path="/inputs",
            ),
        }
    return {
        "valid": True,
        "diagnostics": _diagnostics(
            severity="info",
            code="MCHS-INF-001",
            message="Input validated at the MCP contract boundary.",
        ),
    }


def calculate(arguments: dict[str, Any]) -> dict[str, Any]:
    """Return bounded calculation response or explicit unsupported diagnostic."""
    validation = validate_input(arguments)
    if not validation["valid"]:
        return _tool_error(
            "MCHS-ERR-VAL-001",
            validation["diagnostics"]["diagnostics"][0]["message"],
        )
    calculator_id = str(arguments["calculatorId"])
    year = str(arguments["year"])
    return {
        "calculatorId": calculator_id,
        "year": year,
        "result": None,
        "diagnostics": _diagnostics(
            severity="warning",
            code="MCHS-WARN-MCP-001",
            message=(
                "MCP server validated the request boundary. Formula execution "
                "is delegated to the canonical runtime and is not duplicated in "
                "the MCP adapter."
            ),
        ),
        "provenance": {
            "server": SERVER_NAME,
            "serverVersion": server_version(),
            "transport": "stdio",
        },
    }


def explain_result(arguments: dict[str, Any]) -> dict[str, Any]:
    """Return the bounded MCP explanation for a validated request."""
    validation = validate_input(arguments)
    if not validation["valid"]:
        return _tool_error(
            "MCHS-ERR-VAL-001",
            validation["diagnostics"]["diagnostics"][0]["message"],
        )
    return {
        "calculatorId": arguments["calculatorId"],
        "year": arguments["year"],
        "steps": [
            {
                "step": 1,
                "label": "Validate MCP request boundary",
                "description": (
                    "The MCP adapter validates request shape and support scope "
                    "before delegating execution to the canonical runtime."
                ),
            }
        ],
    }


def get_evidence(arguments: dict[str, Any]) -> dict[str, Any]:
    """Return release and MCP publication evidence for this server."""
    bundle_id = str(arguments.get("bundleId", "mcp-server-readiness-20260516"))
    return {
        "bundleId": bundle_id,
        "calculatorId": "mchs-mcp",
        "references": [
            {
                "id": "mcp-contract",
                "type": "contract",
                "title": "MCHS MCP Contract",
                "path": "contracts/mcp/README.md",
            },
            {
                "id": "mcp-registry-decisions",
                "type": "publication-evidence",
                "title": "MCP Registry Submission Decisions",
                "path": "contracts/mcp/registry/submission-decisions.md",
            },
        ],
        "supportScope": {
            "transport": "stdio",
            "dockerRequired": False,
            "years": list(SUPPORTED_YEARS),
        },
    }


TOOL_HANDLERS = {
    "mchs.list_calculators": list_calculators,
    "mchs.get_schema": get_schema,
    "mchs.validate_input": validate_input,
    "mchs.calculate": calculate,
    "mchs.explain_result": explain_result,
    "mchs.get_evidence": get_evidence,
}


def list_tools() -> list[dict[str, Any]]:
    """Return MCP tool metadata."""
    return [
        {
            "name": name,
            "description": description,
            "inputSchema": schema,
        }
        for name, description, schema in [
            (
                "mchs.list_calculators",
                "List calculators available through the MCHS MCP boundary.",
                {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "year": {"type": "string"},
                        "includeDeprecated": {"type": "boolean"},
                    },
                },
            ),
            (
                "mchs.get_schema",
                "Return a canonical schema for a calculator input or output.",
                {
                    "type": "object",
                    "required": ["calculatorId"],
                    "properties": {
                        "calculatorId": {"type": "string"},
                        "direction": {"enum": ["input", "output"]},
                    },
                },
            ),
            (
                "mchs.validate_input",
                "Validate a calculator request at the MCP contract boundary.",
                {
                    "type": "object",
                    "required": ["calculatorId", "year", "inputs"],
                    "properties": {
                        "calculatorId": {"type": "string"},
                        "year": {"type": "string"},
                        "inputs": {"type": "object"},
                    },
                },
            ),
            (
                "mchs.calculate",
                "Validate and delegate a calculation request.",
                {
                    "type": "object",
                    "required": ["calculatorId", "year", "inputs"],
                    "properties": {
                        "calculatorId": {"type": "string"},
                        "year": {"type": "string"},
                        "inputs": {"type": "object"},
                        "options": {"type": "object"},
                    },
                },
            ),
            (
                "mchs.explain_result",
                "Explain the MCP boundary steps for a calculation request.",
                {
                    "type": "object",
                    "required": ["calculatorId", "year", "inputs"],
                    "properties": {
                        "calculatorId": {"type": "string"},
                        "year": {"type": "string"},
                        "inputs": {"type": "object"},
                    },
                },
            ),
            (
                "mchs.get_evidence",
                "Return release and MCP registry evidence.",
                {
                    "type": "object",
                    "properties": {"bundleId": {"type": "string"}},
                },
            ),
        ]
    ]


def _read_schema(schema_id: str) -> dict[str, Any]:
    schema_file = _contract_path("canonical", f"{schema_id}.schema.json")
    if schema_file.exists():
        return _load_json(schema_file)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": schema_id,
        "type": "object",
    }


def list_resources() -> list[dict[str, str]]:
    """Return MCP resources exposed by the server."""
    return [
        {
            "uri": "mchs://schemas",
            "name": "Canonical schema index",
            "description": "List canonical schema identifiers.",
            "mimeType": "application/json",
        },
        {
            "uri": "mchs://support/status",
            "name": "Support status",
            "description": "Current bounded support status for MCP.",
            "mimeType": "application/json",
        },
        {
            "uri": "mchs://calculators",
            "name": "Calculators",
            "description": "Calculator definitions exposed by MCP.",
            "mimeType": "application/json",
        },
        {
            "uri": "mchs://evidence/mcp-server-readiness-20260516",
            "name": "MCP server readiness evidence",
            "description": "Registry and support-scope evidence for MCP.",
            "mimeType": "application/json",
        },
    ]


def read_resource(uri: str) -> dict[str, Any]:
    """Read an MCP resource by URI."""
    if uri == "mchs://schemas":
        payload: Any = {
            "schemas": [
                "calculator",
                "diagnostics",
                "evidence",
                "provenance",
                "support-status",
            ]
        }
    elif uri.startswith("mchs://schemas/"):
        payload = _read_schema(uri.rsplit("/", maxsplit=1)[-1])
    elif uri == "mchs://support/status":
        payload = {
            "surface": "MCP stdio server",
            "status": "ready-for-local-use",
            "dockerRequired": False,
            "years": list(SUPPORTED_YEARS),
            "knownLimitations": [
                "Registry submission requires external account or review flow.",
                "Formula execution is delegated; the MCP adapter does not "
                "duplicate calculator logic.",
            ],
        }
    elif uri == "mchs://calculators":
        payload = list_calculators()
    elif uri.startswith("mchs://evidence/"):
        payload = get_evidence({"bundleId": uri.rsplit("/", maxsplit=1)[-1]})
    else:
        raise McpError("MCHS-ERR-NOTFOUND-002", f"Resource '{uri}' not found.")
    return {
        "contents": [
            {
                "uri": uri,
                "mimeType": "application/json",
                "text": json.dumps(payload, sort_keys=True),
            }
        ]
    }


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call an MCP tool handler by name."""
    handler = TOOL_HANDLERS.get(name)
    if handler is None:
        return _tool_error("MCHS-ERR-NOTFOUND-003", f"Tool '{name}' not found.")
    try:
        payload = handler(arguments or {})
    except McpError as error:
        return _tool_error(error.code, error.message)
    if isinstance(payload, dict) and payload.get("isError") is True:
        return payload
    return _text_result(payload)


def handle_json_rpc(request: dict[str, Any]) -> dict[str, Any] | None:
    """Handle one JSON-RPC request or notification."""
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}
    try:
        if method == "initialize":
            result: Any = {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}, "resources": {}},
                "serverInfo": {"name": SERVER_NAME, "version": server_version()},
            }
        elif method == "tools/list":
            result = {"tools": list_tools()}
        elif method == "tools/call":
            result = call_tool(params.get("name", ""), params.get("arguments") or {})
        elif method == "resources/list":
            result = {"resources": list_resources()}
        elif method == "resources/read":
            result = read_resource(str(params.get("uri", "")))
        elif method in {"notifications/initialized", "$/cancelRequest"}:
            return None
        else:
            raise McpError("MCHS-ERR-METHOD-001", f"Unknown method '{method}'.")
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except McpError as error:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32000, "message": f"{error.code}: {error.message}"},
        }


def main() -> None:
    """Run the stdio JSON-RPC server loop."""
    for line in sys.stdin:
        if not line.strip():
            continue
        response = handle_json_rpc(json.loads(line))
        if response is not None:
            sys.stdout.write(json.dumps(response, sort_keys=True) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
