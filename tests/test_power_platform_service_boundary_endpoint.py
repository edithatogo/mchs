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


def _load_module():
    spec = importlib.util.spec_from_file_location("service_boundary_endpoint", SCRIPT)
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


def test_service_boundary_endpoint_validation_is_blocked_without_base_url() -> None:
    module = _load_module()
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))

    exit_code, summary = module.evaluate_configuration(config)

    assert exit_code == 2
    assert summary["status"] == "blocked_pending_real_https_endpoint"
    assert summary["checks"][0]["status"] == "blocked"


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
