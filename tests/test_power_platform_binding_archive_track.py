from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "power_platform_binding_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
VALIDATOR = ROOT / "scripts" / "validate_power_platform_capabilities.py"

spec = importlib.util.spec_from_file_location(
    "validate_power_platform_capabilities",
    VALIDATOR,
)
assert spec is not None
validate_power_platform_capabilities = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validate_power_platform_capabilities
spec.loader.exec_module(validate_power_platform_capabilities)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_power_platform_binding_archive_metadata_records_runtime_scope() -> None:
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "power_platform_binding_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("complete-with-gaps means")
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["included"] == [
        "Local Power Platform binding contract and connector-boundary validation.",
        (
            "Calculator capability matrix for 2013 through 2026 source and "
            "implementation states."
        ),
        "App-surface model and local validator for orchestration-only behavior.",
        "ALM workflow documentation and local-safe contract tests.",
    ]
    assert metadata["support_scope"]["excluded"] == [
        "Tenant-exported managed solution zip.",
        (
            "Credentialed Power Platform solution checker, import, publish, "
            "and environment validation proof."
        ),
        "Live Power Apps, Dataverse, or custom connector runtime evidence.",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "external-tenant-gate"
    }
    assert metadata["archive_evidence"]["archive_ready"] is True


def test_power_platform_binding_archive_plan_and_registry_are_complete() -> None:
    plan = _read(TRACK / "plan.md")
    review = _read(TRACK / "review.md")
    registry = _read(TRACKS)

    assert "Integration Contract" in plan
    assert "[checkpoint:" in plan
    assert "archive-ready as `complete-with-gaps`" in review
    assert "- [x] **Track: Power Platform Binding**" in registry


def test_power_platform_validator_matches_archive_scope() -> None:
    validate_power_platform_capabilities.validate()
