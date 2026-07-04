from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "strict_quality_gates_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
REQUIREMENTS = ROOT / "conductor" / "requirements.md"
WORKFLOW = ROOT / "conductor" / "workflow.md"
CONTRACT = ROOT / "contracts" / "quality-gates" / "strict-quality-gates.contract.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_strict_quality_gates_archive_metadata_records_bounded_completion():
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "strict_quality_gates_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "strict quality-gate contract with >=90% coverage threshold",
        "Conductor workflow requirements for strict coverage and no-stub checks",
        "local contract tests for quality gate classes and workflow thresholds",
        "explicit gap records for Rust formatting and external release gates",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "claiming the full Rust quality chain is currently green",
        "claiming external registry or release publication gates are complete",
        "treating generic Conductor plan text as executable gate evidence",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "blocked-external-track",
        "external-or-release-gate",
    }
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/strict_quality_gates_20260513/review.md"
    )


def test_strict_quality_gates_plan_records_archive_review_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "metadata.json" in plan
    assert "plan.md" in plan
    assert "bounded complete-with-gaps scope" in plan


def test_strict_quality_gates_contract_is_backed_by_requirements_and_workflow():
    requirements = _read(REQUIREMENTS)
    workflow = _read(WORKFLOW)
    contract = _json(CONTRACT)

    assert "MUST-004" in requirements
    assert "MUST-005" in requirements
    assert "Strict Coverage" in workflow
    assert "No Stub Completion" in workflow
    assert contract["minimumCoveragePercent"] == 90
    assert "security" in contract["requiredGateClasses"]
    assert "versioning" in contract["requiredGateClasses"]


def test_strict_quality_gates_registry_points_to_completed_archive():
    registry = _read(TRACKS)

    assert "- [x] **Track: Strict Quality Gates**" in registry
    assert "./archive/strict_quality_gates_20260513/" in registry
    assert "./tracks/strict_quality_gates_20260513/" not in registry
