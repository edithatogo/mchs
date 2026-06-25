from __future__ import annotations

import json
from pathlib import Path

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
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "conductor_requirements_design_authority_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "conductor/requirements.md" in metadata["completion_evidence"]
    assert "conductor/design.md" in metadata["completion_evidence"]
    assert (TRACK / "review.md").exists()


def test_conductor_authority_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "Conductor Requirements and Design Authority" in registry
    assert "./archive/conductor_requirements_design_authority_20260513/" in registry
