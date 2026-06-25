from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "contract_enforcement_harness_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
PLAN = ROOT / "conductor" / "contract-enforcement.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_contract_enforcement_plan_exists_and_names_required_checks():
    text = _read(PLAN)

    for phrase in [
        "Schema drift check",
        "Fixture conformance check",
        "Negative conformance check",
        "Documentation conformance check",
        "Release conformance check",
        "Stub/fake check",
    ]:
        assert phrase in text


def test_contract_enforcement_track_archive_metadata_is_explicit():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "contract_enforcement_harness_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "conductor/contract-enforcement.md" in metadata["completion_evidence"]
    assert (TRACK / "review.md").exists()


def test_contract_enforcement_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "Contract Enforcement Harness" in registry
    assert "./archive/contract_enforcement_harness_20260513/" in registry
