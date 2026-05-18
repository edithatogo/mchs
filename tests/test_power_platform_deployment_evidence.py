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
        "tenant_client_secret_missing",
        "tenant_service_principal_missing",
        "tenant_environment_id_unknown",
    ]:
        assert blocker in _text(GOVERNANCE)
        assert blocker in bundle_limitations

    assert bundle["coverage"]["threshold"] >= 0.0
    assert bundle["coverage"]["actual"] >= 0.0


def test_power_platform_artifacts_state_no_live_nsw_claim():
    for path in [RUNBOOK, READINESS, GOVERNANCE]:
        text = _text(path).lower()
        assert "do not claim" in text


def test_power_platform_evidence_templates_exist():
    for path in [RUNBOOK, READINESS, GOVERNANCE, BUNDLE]:
        assert path.exists(), path
