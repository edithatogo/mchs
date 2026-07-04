from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = (
    ROOT
    / "conductor"
    / "archive"
    / "conductor_requirements_design_authority_20260513"
)
TRACKS = ROOT / "conductor" / "tracks.md"
REQUIREMENTS = ROOT / "conductor" / "requirements.md"
DESIGN = ROOT / "conductor" / "design.md"
WORKFLOW = ROOT / "conductor" / "workflow.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_metadata() -> dict[str, Any]:
    return json.loads(_read(TRACK / "metadata.json"))


def test_conductor_authority_docs_exist_and_define_required_rules():
    requirements = _read(REQUIREMENTS)
    design = _read(DESIGN)
    workflow = _read(WORKFLOW)

    assert "MUST-010" in requirements
    assert "MUST-011" in requirements
    assert "Rust must become the single source of calculator logic" in requirements
    assert "Contract Enforcement Flow" in design
    assert "Multi-Level Agent Execution Model" in design
    assert "Requirements and Design Authority" in workflow


def test_conductor_authority_track_archive_metadata_is_explicit():
    metadata = _load_metadata()

    assert metadata["track_id"] == "conductor_requirements_design_authority_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["completion_policy"].startswith("Complete means")

    support_scope = metadata["support_scope"]
    assert support_scope["state"] == "complete"
    assert support_scope["implemented"] == [
        "Conductor requirements authority in conductor/requirements.md",
        "Conductor design authority in conductor/design.md",
        "workflow rules requiring conductor-review at phase and track boundaries",
        "no-stub completion semantics linked to requirements and workflow evidence",
        "archive evidence contract for this governance track",
    ]
    assert support_scope["not_implemented"] == [
        "automatic completion of dependent implementation tracks",
        "replacement of per-track validation, release, or publication evidence",
        "runtime enforcement outside the repository Conductor workflow",
    ]

    assert metadata["gap_register"]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "deferred",
        "out-of-scope",
    }
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/conductor_requirements_design_authority_20260513/review.md"
    )
    assert "conductor/requirements.md" in metadata["completion_evidence"]
    assert "conductor/design.md" in metadata["completion_evidence"]
    assert (TRACK / "review.md").exists()


def test_conductor_authority_plan_records_archive_review_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "metadata.json" in plan
    assert "plan.md" in plan
    assert "does not complete every dependent implementation track" in plan


def test_conductor_authority_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "Conductor Requirements and Design Authority" in registry
    assert "./archive/conductor_requirements_design_authority_20260513/" in registry
