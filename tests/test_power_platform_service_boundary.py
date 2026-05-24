from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_boundary_module():
    spec = importlib.util.spec_from_file_location(
        "mchs_service_boundary",
        ROOT / "power-platform" / "service" / "boundary.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_health_endpoint_is_unprotected_and_ready():
    module = _load_boundary_module()
    status, payload = module.handle_service_request("GET", "/healthz")
    assert status == 200
    assert payload["status"] == "ok"
    assert payload["service"] == "MCHS Service Boundary"


def test_legacy_calculation_route_alias_and_mcp_delegation():
    module = _load_boundary_module()
    body = json.dumps(
        {
            "contract_version": "2026-05",
            "calculator_id": "acute",
            "pricing_year": "2025",
            "input_payload": {},
            "fixture_id": "fixture-abc",
        }
    ).encode()
    status, payload = module.handle_service_request(
        "POST", "/calculators/run", body=body, headers={}
    )
    assert status == 200
    assert payload["status"] == "success"
    assert payload["result_payload"]["calculator_id"] == "acute"
    assert payload["result_payload"]["pricing_year"] == "2025"
    assert payload["result_payload"]["fixture_id"] == "fixture-abc"
    assert payload["result_payload"]["mcp_payload"]["calculatorId"] == "acute"


def test_validation_route_returns_boundary_validation_result():
    module = _load_boundary_module()
    body = json.dumps(
        {
            "contract_version": "2026-05",
            "calculator_id": "acute",
            "pricing_year": "2025",
            "input_payload": {"dummy": "value"},
        }
    ).encode()
    status, payload = module.handle_service_request(
        "POST", "/v1/validate", body=body, headers={}
    )
    assert status == 200
    assert payload["status"] == "success"
    assert payload["result_payload"]["calculator_id"] == "acute"
    assert payload["result_payload"]["validation"]["valid"] is True


def test_schema_lookup_delegates_to_mcp_resources():
    module = _load_boundary_module()
    status, payload = module.handle_service_request("GET", "/v1/schemas/calculator")
    assert status == 200
    assert payload["status"] == "success"
    assert payload["result_payload"]["schema_name"] == "calculator"
    assert "$schema" in payload["result_payload"]["schema"]


def test_connector_api_key_header_alias_is_accepted(monkeypatch):
    module = _load_boundary_module()
    monkeypatch.setenv("MCHS_SERVICE_BOUNDARY_API_KEY", "synthetic-key")
    status, payload = module.handle_service_request(
        "GET", "/healthz", headers={"x-api-key": "synthetic-key"}
    )
    assert status == 200
    assert payload["status"] == "ok"
