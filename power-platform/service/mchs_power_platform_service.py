"""HTTP service boundary for Power Platform orchestration.

This service adapts HTTP requests to the existing MCHS MCP runtime. It is not a
formula engine and does not contain calculator constants.
"""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from nwau_py import mcp_server

SERVICE_VERSION = "0.2.2"


def _json_response(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True).encode("utf-8")


def _diagnostic(code: str, message: str, correlation_id: str = "") -> dict[str, Any]:
    return {
        "status": "error",
        "result_payload": None,
        "warnings": [],
        "diagnostics": [{"severity": "error", "code": code, "message": message}],
        "provenance": {
            "service": "mchs-power-platform-boundary",
            "version": SERVICE_VERSION,
        },
        "trace_id": correlation_id,
    }


def _tool_payload(
    tool: str, arguments: dict[str, Any], correlation_id: str = ""
) -> dict[str, Any]:
    result = mcp_server.call_tool(tool, arguments)
    if result.get("isError"):
        return _diagnostic(
            "MCHS-ERR-MCP-001", result["content"][0]["text"], correlation_id
        )
    return {
        "status": "ok",
        "result_payload": result.get("structuredContent"),
        "warnings": [],
        "diagnostics": result.get("structuredContent", {}).get("diagnostics", {}),
        "provenance": {
            "service": "mchs-power-platform-boundary",
            "version": SERVICE_VERSION,
            "mcpServer": mcp_server.SERVER_REGISTRY_NAME,
            "mcpServerVersion": mcp_server.server_version(),
        },
        "trace_id": correlation_id,
    }


def handle_request(
    path: str, payload: dict[str, Any] | None = None
) -> tuple[HTTPStatus, dict[str, Any]]:
    payload = payload or {}
    correlation_id = str(payload.get("correlation_id", ""))
    if path == "/healthz":
        return HTTPStatus.OK, {
            "status": "ok",
            "service": "mchs-power-platform-boundary",
            "version": SERVICE_VERSION,
            "mcpServer": mcp_server.SERVER_REGISTRY_NAME,
        }
    if path == "/calculators":
        return HTTPStatus.OK, _tool_payload(
            "mchs.list_calculators",
            {"year": payload.get("pricing_year", "")},
            correlation_id,
        )
    if path == "/schemas/calculator":
        return HTTPStatus.OK, _tool_payload(
            "mchs.get_schema",
            {
                "calculatorId": payload.get("calculator_id", ""),
                "direction": payload.get("direction", "input"),
            },
            correlation_id,
        )
    if path == "/validate":
        return HTTPStatus.OK, _tool_payload(
            "mchs.validate_input",
            {
                "calculatorId": payload.get("calculator_id", ""),
                "year": payload.get("pricing_year", ""),
                "inputs": payload.get("input_payload", {}),
            },
            correlation_id,
        )
    if path == "/calculate":
        return HTTPStatus.OK, _tool_payload(
            "mchs.calculate",
            {
                "calculatorId": payload.get("calculator_id", ""),
                "year": payload.get("pricing_year", ""),
                "inputs": payload.get("input_payload", {}),
            },
            correlation_id,
        )
    if path == "/evidence":
        return HTTPStatus.OK, _tool_payload(
            "mchs.get_evidence",
            {"bundleId": payload.get("bundle_id", "")},
            correlation_id,
        )
    return HTTPStatus.NOT_FOUND, _diagnostic(
        "MCHS-ERR-HTTP-404", f"No route for {path}", correlation_id
    )


class Handler(BaseHTTPRequestHandler):
    server_version = "MCHS-PowerPlatform/0.2.2"

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _write(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = _json_response(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        status, payload = handle_request(self.path)
        self._write(status, payload)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = (
                json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
            )
        except json.JSONDecodeError as error:
            self._write(
                HTTPStatus.BAD_REQUEST, _diagnostic("MCHS-ERR-JSON-001", str(error))
            )
            return
        if not isinstance(payload, dict):
            self._write(
                HTTPStatus.BAD_REQUEST,
                _diagnostic("MCHS-ERR-JSON-002", "Request body must be a JSON object."),
            )
            return
        status, response = handle_request(self.path, payload)
        self._write(status, response)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run MCHS Power Platform service boundary"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8770, type=int)
    args = parser.parse_args()
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
