from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "release" / "evidence-bundle.schema.json"
BUNDLE = (
    ROOT
    / "power-platform"
    / "evidence"
    / "nsw-operational-readiness-bundle-template.json"
)
RUNBOOK = (
    ROOT / "power-platform" / "deployment" / "nsw-managed-solution-promotion-runbook.md"
)
READINESS = (
    ROOT / "power-platform" / "deployment" / "nsw-deployment-readiness-template.md"
)
GOVERNANCE = ROOT / "power-platform" / "governance" / "nsw-power-platform-governance.md"
RUNTIME_SMOKE = (
    ROOT / "power-platform" / "evidence" / "runtime-smoke-evidence-template.json"
)
CONNECTIONS = (
    ROOT / "power-platform" / "evidence" / "connection-reference-evidence-template.json"
)
MONITORING = (
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-evidence-template.json"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _required_fields(schema: dict) -> set[str]:
    return set(schema.get("required", []))


def test_power_platform_evidence_bundle_contains_required_fields_and_blockers():
    schema = _json(SCHEMA)
    bundle = _json(BUNDLE)

    for field in _required_fields(schema):
        assert field in bundle, f"Missing required evidence field: {field}"

    bundle_limitations = "\n".join(bundle.get("known_limitations", []))
    for blocker in [
        "service_boundary_production_endpoint_missing",
        "connection_reference_values_missing",
        "real_dataverse_app_component_smoke_missing",
        "real_power_automate_flow_component_smoke_missing",
    ]:
        assert blocker in bundle_limitations

    assert bundle["coverage"]["threshold"] >= 0.0
    assert bundle["coverage"]["actual"] >= 0.0


def test_power_platform_artifacts_state_no_live_nsw_claim():
    for path in [RUNBOOK, READINESS, GOVERNANCE]:
        text = _text(path).lower()
        assert "do not claim" in text


def test_power_platform_evidence_templates_exist():
    for path in [
        RUNBOOK,
        READINESS,
        GOVERNANCE,
        BUNDLE,
        RUNTIME_SMOKE,
        CONNECTIONS,
        MONITORING,
    ]:
        assert path.exists(), path


def test_power_platform_operational_evidence_contracts_are_precise():
    runtime = _json(RUNTIME_SMOKE)
    connections = _json(CONNECTIONS)
    monitoring = _json(MONITORING)

    assert runtime["claimBoundary"]["runtimeSmokePassed"] is False
    assert runtime["claimBoundary"]["productionReadinessClaimed"] is False
    assert connections["claimBoundary"]["connectionsConfigured"] is False
    assert monitoring["claimBoundary"]["monitoringConfigured"] is False
    assert monitoring["claimBoundary"]["dlpEvidenceCaptured"] is False


def test_power_platform_operational_evidence_validator_passes():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_operational_evidence.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform operational evidence contracts passed." in result.stdout
