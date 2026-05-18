"""Power Platform service boundary for MCP-delegated calculator orchestration."""

from __future__ import annotations

import argparse
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import uuid4

from nwau_py import mcp_http_server, mcp_server

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8702
SERVICE_NAME = "MCHS Service Boundary"
DEFAULT_CONTRACT_VERSION = "2026-05"


def _required_api_key() -> str | None:
    configured_key = os.getenv("MCHS_SERVICE_BOUNDARY_API_KEY", "").strip()
    if configured_key:
        return configured_key
    return None


def _validate_api_key(headers: Any) -> str | None:
    required_key = _required_api_key()
    if required_key is None:
        return None

    header_value = (
        headers.get("x-mchs-api-key")
        or headers.get("X-MCHS-API-KEY")
        or headers.get("X-Mchs-Api-Key")
    )
    if not header_value:
        return "x-mchs-api-key is required"
    if header_value != required_key:
        return "x-mchs-api-key is invalid"
    return None


def _read_json_body(body: bytes | None) -> dict[str, Any]:
    if not body:
        return {}
    try:
        decoded = body.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"payload is not UTF-8 encoded: {error}") from error

    if not decoded.strip():
        return {}
    try:
        payload: Any = json.loads(decoded)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON payload: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    return payload


def _trace_id(payload: dict[str, Any], correlation: dict[str, str]) -> str:
    return (
        str(payload.get("trace_id"))
        or payload.get("traceId")
        or correlation.get("trace_id")
        or str(correlation.get("x-correlation-id"))
        or str(uuid4())
    )


def _normalize_contract_version(payload: dict[str, Any]) -> str:
    return str(payload.get("contract_version", DEFAULT_CONTRACT_VERSION))


def _ok_payload(
    *,
    trace_id: str,
    status: str,
    result_payload: Any,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    payload = {
        "status": status,
        "result_payload": result_payload,
        "result": result_payload,
        "trace_id": trace_id,
    }
    if warnings is not None:
        payload["warnings"] = warnings
    return payload


def _fail_payload(
    trace_id: str, message: str, *, warnings: list[str] | None = None
) -> dict[str, Any]:
    return _ok_payload(
        trace_id=trace_id,
        status="failure",
        result_payload={"error": message},
        warnings=warnings,
    )


def _validation_payload(
    trace_id: str,
    validation: dict[str, Any],
    *,
    calculator_id: str,
    pricing_year: str,
) -> dict[str, Any]:
    diagnostics = validation.get("diagnostics", {}).get("diagnostics", [])
    warnings = [
        entry.get("message", "") for entry in diagnostics if entry.get("message")
    ]
    status = "success" if validation.get("valid") else "validation_required"
    return _ok_payload(
        trace_id=trace_id,
        status=status,
        result_payload={
            "calculator_id": calculator_id,
            "pricing_year": pricing_year,
            "validation": validation,
        },
        warnings=warnings,
    )


def _list_calculators(
    trace_id: str, query_year: str | None = None
) -> tuple[int, dict[str, Any]]:
    args = {}
    if query_year:
        args["year"] = query_year
    calculators = mcp_server.list_calculators(args)
    return HTTPStatus.OK, _ok_payload(
        trace_id=trace_id,
        status="success",
        result_payload={"calculators": calculators},
        warnings=[
            "Calculator execution is delegated to mcp_server handlers.",
            "This service boundary never executes formula logic directly.",
        ],
    )


def _calculator_detail(trace_id: str, calculator_id: str) -> tuple[int, dict[str, Any]]:
    calculators = mcp_server.list_calculators()
    for calculator in calculators:
        if str(calculator.get("id")) == calculator_id:
            return HTTPStatus.OK, _ok_payload(
                trace_id=trace_id,
                status="success",
                result_payload=calculator,
                warnings=[
                    "Calculator definition sourced from MCP list_calculators tool.",
                    "No formula logic exists in this boundary handler.",
                ],
            )
    return HTTPStatus.NOT_FOUND, _fail_payload(
        trace_id=trace_id,
        message=f"Calculator '{calculator_id}' not found.",
        warnings=[
            "Validate calculator_id with GET /v1/calculators before submission.",
        ],
    )


def _calculator_schema(trace_id: str, schema_name: str) -> tuple[int, dict[str, Any]]:
    try:
        schema_resource = mcp_server.read_resource(f"mchs://schemas/{schema_name}")
    except Exception as error:
        return HTTPStatus.NOT_FOUND, _fail_payload(
            trace_id=trace_id,
            message=f"Schema '{schema_name}' not found.",
            warnings=[str(error)],
        )

    text = schema_resource["contents"][0]["text"]
    schema = json.loads(text)
    return HTTPStatus.OK, _ok_payload(
        trace_id=trace_id,
        status="success",
        result_payload={
            "schema_name": schema_name,
            "schema": schema,
        },
        warnings=[
            "Schemas are sourced from canonical MCP resources.",
        ],
    )


def _validate_payload(
    trace_id: str, payload: dict[str, Any]
) -> tuple[int, dict[str, Any]]:
    contract_version = _normalize_contract_version(payload)
    calculator_id = str(payload.get("calculator_id", "")).strip()
    pricing_year = str(payload.get("pricing_year", "")).strip()
    validation = mcp_server.validate_input(
        {
            "calculatorId": calculator_id,
            "year": pricing_year,
            "inputs": payload.get("input_payload", {}),
            "contractVersion": contract_version,
        }
    )
    return HTTPStatus.OK, _validation_payload(
        trace_id=trace_id,
        validation=validation,
        calculator_id=calculator_id,
        pricing_year=pricing_year,
    )


def _calculate(trace_id: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    contract_version = _normalize_contract_version(payload)
    calculator_id = str(payload.get("calculator_id", "")).strip()
    pricing_year = str(payload.get("pricing_year", "")).strip()
    input_payload = payload.get("input_payload")

    validation = mcp_server.validate_input(
        {
            "calculatorId": calculator_id,
            "year": pricing_year,
            "inputs": input_payload,
            "contractVersion": contract_version,
        }
    )
    if not validation.get("valid"):
        return HTTPStatus.OK, _validation_payload(
            trace_id=trace_id,
            validation=validation,
            calculator_id=calculator_id,
            pricing_year=pricing_year,
        )

    try:
        calculation_result = mcp_server.calculate(
            {
                "calculatorId": calculator_id,
                "year": pricing_year,
                "inputs": input_payload,
            }
        )
    except Exception as error:
        return HTTPStatus.OK, _fail_payload(
            trace_id=trace_id,
            message=f"calculation failed: {error}",
        )

    if (
        isinstance(calculation_result, dict)
        and calculation_result.get("isError") is True
    ):
        return HTTPStatus.OK, _fail_payload(
            trace_id=trace_id,
            message="calculation failed",
            warnings=[
                str(calculation_result.get("content", [{}])[0].get("text", ""))
                if calculation_result.get("content")
                else "calculation handler reported error"
            ],
        )

    return HTTPStatus.OK, _ok_payload(
        trace_id=trace_id,
        status="success",
        result_payload={
            "calculator_id": calculator_id,
            "pricing_year": pricing_year,
            "fixture_id": payload.get("fixture_id"),
            "contract_version": contract_version,
            "mcp_payload": calculation_result,
        },
        warnings=[
            "MCP handler validated boundary inputs.",
            "Computation is delegated to mcp_server.calculate.",
        ],
    )


def _evidence(trace_id: str, bundle_id: str) -> tuple[int, dict[str, Any]]:
    evidence = mcp_server.get_evidence({"bundleId": bundle_id})
    return HTTPStatus.OK, _ok_payload(
        trace_id=trace_id,
        status="success",
        result_payload={"bundle_id": bundle_id, "evidence": evidence},
    )


def _health() -> tuple[int, dict[str, Any]]:
    return HTTPStatus.OK, {
        "status": "ok",
        "service": SERVICE_NAME,
        "server": mcp_http_server.server_card()["serverInfo"]["name"],
        "transport": "delegated-http",
        "contract_version": DEFAULT_CONTRACT_VERSION,
    }


def _server_card() -> tuple[int, dict[str, Any]]:
    return HTTPStatus.OK, mcp_http_server.server_card()


def handle_service_request(
    method: str,
    path: str,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, Any]]:
    """Handle one API request against the in-process service dispatcher."""
    headers = headers or {}
    parsed = urlparse(path)
    route = parsed.path
    method_upper = method.upper()

    if route != "/healthz" and route != "/.well-known/mcp/server-card.json":
        auth_error = _validate_api_key(headers)
        if auth_error is not None:
            trace_id = _trace_id({}, {})
            return HTTPStatus.UNAUTHORIZED, _fail_payload(
                trace_id=trace_id,
                message=auth_error,
            )

    if method_upper == "GET":
        if route == "/healthz":
            return _health()
        if route == "/.well-known/mcp/server-card.json":
            return _server_card()
        if route == "/v1/calculators":
            query_year = None
            raw_year = parse_qs(parsed.query).get("pricing_year", [])
            if raw_year:
                query_year = raw_year[0]
            return _list_calculators(_trace_id({}, {}), query_year)
        if route.startswith("/v1/calculators/"):
            calculator_id = route.split("/", 3)[-1]
            return _calculator_detail(_trace_id({}, {}), calculator_id)
        if route.startswith("/v1/schemas/"):
            schema_name = route.split("/", 3)[-1]
            if not schema_name:
                return HTTPStatus.BAD_REQUEST, _fail_payload(
                    _trace_id({}, {}), "schema_name required"
                )
            return _calculator_schema(_trace_id({}, {}), schema_name)
        if route.startswith("/v1/evidence/"):
            bundle_id = route.split("/", 3)[-1] or "mcp-server-readiness-20260516"
            return _evidence(_trace_id({}, {}), bundle_id)
        return HTTPStatus.NOT_FOUND, _fail_payload(_trace_id({}, {}), "route not found")

    if method_upper == "POST":
        try:
            payload = _read_json_body(body)
        except ValueError as error:
            trace_id = _trace_id({}, dict(headers))
            return HTTPStatus.BAD_REQUEST, _fail_payload(
                trace_id=trace_id,
                message=f"bad request: {error}",
            )
        trace_id = _trace_id(payload, dict(headers))
        if route == "/v1/validate":
            return _validate_payload(trace_id, payload)
        if route in {"/v1/calculations", "/calculators/run"}:
            return _calculate(trace_id, payload)
        return HTTPStatus.NOT_FOUND, _fail_payload(
            trace_id=trace_id,
            message="route not found",
        )

    return HTTPStatus.METHOD_NOT_ALLOWED, _fail_payload(
        _trace_id({}, {}),
        f"method {method_upper} not supported",
        warnings=["Use GET or POST for this boundary"],
    )


class PowerPlatformServiceHandler(BaseHTTPRequestHandler):
    """HTTP handler for the secure service boundary."""

    server_version = "MCHS-Service-Boundary/0.1"

    def log_message(self, format: str, *args: Any) -> None:
        return None

    def _write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        status, payload = handle_service_request(
            self.command,
            self.path,
            headers=dict(self.headers),
        )
        self._write_json(status, payload)

    def do_POST(self) -> None:
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length) if content_length > 0 else b""
        try:
            status, payload = handle_service_request(
                self.command,
                self.path,
                body=body,
                headers=dict(self.headers),
            )
        except ValueError as error:
            status = HTTPStatus.BAD_REQUEST
            trace_id = _trace_id({}, {})
            payload = _fail_payload(trace_id=trace_id, message=f"bad request: {error}")
        self._write_json(status, payload)


def run(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Run the service boundary."""
    httpd = ThreadingHTTPServer((host, port), PowerPlatformServiceHandler)
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the MCHS Power Platform service boundary."
    )
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
