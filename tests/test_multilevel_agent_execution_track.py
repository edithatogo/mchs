from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "multilevel_agent_execution_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ORCHESTRATION = ROOT / "conductor" / "subagent-orchestration.md"
DESIGN = ROOT / "conductor" / "design.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_metadata() -> dict[str, Any]:
    return json.loads(_read(TRACK / "metadata.json"))


def test_multilevel_agent_archive_metadata_records_governance_only_scope():
    metadata = _load_metadata()

    assert metadata["track_id"] == "multilevel_agent_execution_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "subagent orchestration governance document",
        "multi-level agent execution model in conductor/design.md",
        "bounded ownership and disjoint write-set rules",
        (
            "handoff requirements for changed files, validation commands, "
            "docs, review findings, residual risks, and next action"
        ),
        (
            "phase-end conductor-review, auto-fix, validation, checkpoint, "
            "commit, and push gate rules"
        ),
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "final archived evidence from actual multilevel subagent handoffs",
        "proof that every active track followed the multilevel execution protocol",
        "per-work-package handoff evidence bundles for delegated tasks",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "deferred",
        "out-of-scope",
    }
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/multilevel_agent_execution_20260513/review.md"
    )


def test_multilevel_agent_plan_records_archive_review_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "metadata.json" in plan
    assert "plan.md" in plan
    assert "governance-only complete-with-gaps scope" in plan


def test_multilevel_agent_governance_contract_names_required_handoffs():
    orchestration = _read(ORCHESTRATION)
    design = _read(DESIGN)

    for phrase in [
        "Track ID and phase",
        "Model preference and fallback rule",
        "Owned files or modules",
        "Files or areas explicitly out of scope",
        "Tests, checks, or validations run",
        "Remaining blockers or risks",
        "Nested subagents inherit the same evidence obligations",
    ]:
        assert phrase in orchestration

    assert "Multi-Level Agent Execution Model" in design


def test_multilevel_agent_registry_points_to_completed_archive():
    registry = _read(TRACKS)

    assert "- [x] **Track: Multi-Level Agent Execution**" in registry
    assert "./archive/multilevel_agent_execution_20260513/" in registry
    assert "./tracks/multilevel_agent_execution_20260513/" not in registry
