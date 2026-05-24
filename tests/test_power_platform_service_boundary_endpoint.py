from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT / "power-platform" / "evidence" / "service-boundary-endpoint-template.json"
)
SCRIPT = ROOT / "scripts" / "validate_power_platform_service_boundary_endpoint.py"
PRECHECK = (
    ROOT
    / "scripts"
    / "preflight_power_platform_service_boundary_endpoint_operator_package.py"
)
OPERATOR_INPUT = (
    ROOT
    / "power-platform"
    / "evidence"
    / "examples"
    / "service-boundary-endpoint-operator-input.example.json"
)
PROBE_RESULT = (
    ROOT
    / "power-platform"
    / "evidence"
    / "examples"
    / "service-boundary-probe-result.example.json"
)


def _load_module():
    spec = importlib.util.spec_from_file_location("service_boundary_endpoint", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_precheck_module():
    spec = importlib.util.spec_from_file_location(
        "service_boundary_preflight",
        PRECHECK,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_service_boundary_endpoint_template_is_blocked() -> None:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    assert data["status"] == "blocked_pending_real_https_endpoint"
    assert data["serviceBoundary"]["httpsBaseUrl"] is None
    assert data["serviceBoundary"]["baseUrlEnvironmentVariable"] == "mchs_api_base_url"
    assert data["claimBoundary"]["endpointConfigured"] is False
    assert data["claimBoundary"]["productionReadinessClaimed"] is False
    assert data["handoff"]["status"] == "blocked_pending_real_https_endpoint"
    assert data["handoff"]["requiredInputs"][0]["logicalName"] == "mchs_api_base_url"
    assert data["handoff"]["requiredInputs"][0]["valueStatus"] == "missing"
    assert data["handoff"]["requiredChecks"][0]["path"] == "/healthz"
    assert data["handoff"]["requiredChecks"][1]["path"] == (
        "/.well-known/mcp/server-card.json"
    )


def test_service_boundary_endpoint_validation_is_blocked_without_base_url() -> None:
    module = _load_module()
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    exit_code, summary = module.evaluate_configuration(config)

    assert exit_code == 2
    assert summary["status"] == "blocked_pending_real_https_endpoint"
    assert summary["checks"][0]["status"] == "blocked"
    assert summary["handoff"]["requiredInputs"][0]["logicalName"] == "mchs_api_base_url"
    assert summary["handoff"]["requiredChecks"][0]["path"] == "/healthz"
    assert (
        summary["handoff"]["requiredChecks"][1]["expectedContentType"]
        == "application/json"
    )


def test_service_boundary_endpoint_normalization_rejects_non_https() -> None:
    module = _load_module()

    with pytest.raises(ValueError):
        module.normalize_https_base_url("http://example.org")


def test_service_boundary_endpoint_normalization_rejects_path_segments() -> None:
    module = _load_module()

    with pytest.raises(ValueError):
        module.normalize_https_base_url("https://example.org/api")


def test_service_boundary_endpoint_normalization_strips_trailing_slash() -> None:
    module = _load_module()

    assert (
        module.normalize_https_base_url("https://example.org/") == "https://example.org"
    )


def test_service_boundary_endpoint_preflight_blocks_example_payloads() -> None:
    module = _load_precheck_module()
    operator_input = json.loads(OPERATOR_INPUT.read_text(encoding="utf-8"))
    probe_result = json.loads(PROBE_RESULT.read_text(encoding="utf-8"))

    exit_code, summary = module.evaluate_package(operator_input, probe_result)

    assert exit_code == 2
    assert summary["status"] == "blocked_placeholder_detected"
    assert (
        summary["operatorInput"]["httpsBaseUrl"] == "https://service-boundary.example"
    )
    assert summary["operatorInput"]["valueStatus"] == "blocked"
    assert summary["probe"]["placeholderDetected"] is True
    assert summary["probe"]["selectedChecks"]["healthz"]["error"].startswith(
        "Example only"
    )


def test_service_boundary_endpoint_preflight_accepts_non_placeholder_probe_json() -> (
    None
):
    module = _load_precheck_module()
    operator_input = {
        "baseUrlEnvironmentVariable": "mchs_api_base_url",
        "healthzPath": "/healthz",
        "httpsBaseUrl": "https://api.mchs.example.com",
        "logicalConnectionReference": "mchs_service_boundary",
        "serverCardPath": "/.well-known/mcp/server-card.json",
        "apiKeySecretConfigured": True,
    }
    probe_result = {
        "status": "probe_passed",
        "checks": [
            {"name": "healthz", "status": "passed", "statusCode": 200},
            {
                "name": "server-card",
                "status": "passed",
                "statusCode": 200,
                "contentType": "application/json",
            },
        ],
    }

    exit_code, summary = module.evaluate_package(operator_input, probe_result)

    assert exit_code == 0
    assert summary["status"] == "operator_package_ready"
    assert summary["probe"]["requiredChecksPassed"] is True
