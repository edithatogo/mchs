from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "no_stub_completion_enforcement_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
REQUIREMENTS = ROOT / "conductor" / "requirements.md"
WORKFLOW = ROOT / "conductor" / "workflow.md"
ARCHIVE_POLICY = ROOT / "conductor" / "track-archive-policy.md"
STUB_DETECTOR = ROOT / "conductor" / "scripts" / "stub_detector.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_no_stub_archive_metadata_records_bounded_enforcement_scope():
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "no_stub_completion_enforcement_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "Conductor workflow no-stub completion rule",
        "phase checkpoint requirement to run the stub detector",
        "archive policy requiring implementation and validation evidence",
        "explicit delegation of detector expansion and backlog burn-down",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "claiming every scaffold/backlog item has been remediated",
        "claiming detector expansion is complete",
        "treating docs-only or placeholder artifacts as completion evidence",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {"delegated"}
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/no_stub_completion_enforcement_20260513/review.md"
    )


def test_no_stub_plan_uses_archive_paths_and_records_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "conductor/archive/no_stub_completion_enforcement_20260513" in plan
    assert "conductor/tracks/no_stub_completion_enforcement_20260513" not in plan
    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "bounded complete-with-gaps scope" in plan


def test_no_stub_contract_is_backed_by_requirements_workflow_and_policy():
    requirements = _read(REQUIREMENTS)
    workflow = _read(WORKFLOW)
    archive_policy = _read(ARCHIVE_POLICY)

    assert STUB_DETECTOR.exists()
    assert "MUST-010" in requirements
    assert "No Stub Completion" in workflow
    assert "stub_detector.py --root . --json" in workflow
    assert "Required tests, validation reports, docs, contracts" in archive_policy
    assert "conductor-review" in archive_policy


def test_no_stub_registry_points_to_completed_archive():
    registry = _read(TRACKS)

    assert "- [x] **Track: No-Stub Completion Enforcement**" in registry
    assert "./archive/no_stub_completion_enforcement_20260513/" in registry
    assert "./tracks/no_stub_completion_enforcement_20260513/" not in registry
