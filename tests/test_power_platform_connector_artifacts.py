from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_validation_module():
    spec = importlib.util.spec_from_file_location(
        "pp_connector_validation",
        ROOT / "scripts" / "validate_power_platform_connector_artifacts.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_connector_artifacts_validate_without_errors():
    module = _load_validation_module()
    return_code, errors, _warnings = module.validate_assets()
    assert return_code == 0
    assert errors == []


def test_connector_openapi_includes_required_operations_and_schemas():
    openapi_path = (
        ROOT
        / "power-platform"
        / "connectors"
        / "mchs-service-boundary"
        / "apiDefinition.swagger.json"
    )
    openapi = json.loads(openapi_path.read_text(encoding="utf-8"))
    paths = set(openapi["paths"].keys())
    for required in {
        "/healthz",
        "/v1/calculators",
        "/v1/calculators/{calculator_id}",
        "/v1/schemas/{schema_name}",
        "/v1/validate",
        "/v1/calculations",
        "/v1/evidence/{bundle_id}",
        "/calculators/run",
    }:
        assert required in paths, required

    components = openapi["components"]["schemas"]
    assert "ServiceBoundaryRequest" in components
    assert "ServiceBoundaryResponse" in components


def test_connector_metadata_references_api_definition():
    metadata = json.loads(
        (
            ROOT
            / "power-platform"
            / "connectors"
            / "mchs-service-boundary"
            / "apiProperties.json"
        ).read_text(encoding="utf-8")
    )
    assert metadata["apiDefinition"] == "apiDefinition.swagger.json"
    assert "connectionParameters" in metadata["properties"]
    assert "api_key" in metadata["properties"]["connectionParameters"]
