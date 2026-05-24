"""Streamable HTTP adapter for the MCHS MCP server.

This module is intentionally small and dependency-free. It exposes the same
JSON-RPC handler used by the stdio MCP server at ``/mcp`` and serves static
metadata needed by registry scanners at ``/.well-known/mcp/server-card.json``.
Formula logic remains in the canonical runtime; this adapter only transports
MCP requests.
"""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from . import mcp_server

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def server_card() -> dict[str, Any]:
    """Return Smithery-compatible static metadata for scanner fallback."""
    return {
        "serverInfo": {
            "name": mcp_server.SERVER_REGISTRY_NAME,
            "version": mcp_server.server_version(),
        },
        "authentication": {"required": False, "schemes": []},
        "tools": mcp_server.list_tools(),
        "resources": mcp_server.list_resources(),
        "prompts": [],
        "metadata": {
            "title": "MCHS NWAU Calculator MCP",
            "transport": "streamable-http",
            "endpoint": "/mcp",
            "stdioEntryPoint": "mchs-mcp",
            "formulaLogicPolicy": (
                "The HTTP adapter delegates to the existing MCP handlers and "
                "does not duplicate calculator formula logic."
            ),
            "dataHandling": (
                "No telemetry or persistence is performed by the adapter. "
                "Private healthcare deployments should use internal hosting."
            ),
        },
    }


def health_payload() -> dict[str, Any]:
    """Return a minimal readiness payload safe for public probes."""
    return {
        "status": "ok",
        "server": mcp_server.SERVER_REGISTRY_NAME,
        "version": mcp_server.server_version(),
        "transport": "streamable-http",
    }


def handle_http_json_rpc(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Handle one HTTP JSON-RPC payload using the shared MCP dispatcher."""
    return mcp_server.handle_json_rpc(payload)


class McpHttpHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MCP JSON-RPC and registry metadata."""

    server_version = "MCHS-MCP-HTTP/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default stderr logging to avoid leaking request context."""

    def _write_json(self, status: HTTPStatus, payload: Any) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        """Serve health and static server-card metadata."""
        if self.path == "/healthz":
            self._write_json(HTTPStatus.OK, health_payload())
        elif self.path == "/.well-known/mcp/server-card.json":
            self._write_json(HTTPStatus.OK, server_card())
        else:
            self._write_json(
                HTTPStatus.NOT_FOUND,
                {"error": "not_found", "message": f"No route for {self.path}"},
            )

    def do_POST(self) -> None:
        """Serve Streamable HTTP JSON-RPC requests at ``/mcp``."""
        if self.path != "/mcp":
            self._write_json(
                HTTPStatus.NOT_FOUND,
                {"error": "not_found", "message": f"No route for {self.path}"},
            )
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "bad_request", "message": "Missing JSON-RPC body."},
            )
            return
        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except json.JSONDecodeError as error:
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "invalid_json", "message": str(error)},
            )
            return
        if not isinstance(payload, dict):
            self._write_json(
                HTTPStatus.BAD_REQUEST,
                {"error": "bad_request", "message": "JSON-RPC body must be object."},
            )
            return
        response = handle_http_json_rpc(payload)
        if response is None:
            self.send_response(HTTPStatus.ACCEPTED)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self._write_json(HTTPStatus.OK, response)


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Run the Streamable HTTP MCP adapter."""
    httpd = ThreadingHTTPServer((host, port), McpHttpHandler)
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


def main() -> None:
    """Run the command-line HTTP MCP adapter."""
    parser = argparse.ArgumentParser(description="Run the MCHS MCP HTTP server")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", default=DEFAULT_PORT, type=int)
    args = parser.parse_args()
    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
