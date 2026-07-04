from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "contract_enforcement_harness_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
PLAN = ROOT / "conductor" / "contract-enforcement.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_metadata() -> dict[str, Any]:
    return json.loads(_read(TRACK / "metadata.json"))


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
    metadata = _load_metadata()

    assert metadata["track_id"] == "contract_enforcement_harness_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete means")

    support_scope = metadata["support_scope"]
    assert support_scope["state"] == "complete-with-gaps"
    assert support_scope["implemented"] == [
        "contract enforcement governance plan in conductor/contract-enforcement.md",
        (
            "required checks for schema drift, fixture conformance, negative "
            "conformance, documentation conformance, release conformance, and "
            "stub/fake detection"
        ),
        (
            "completion gate definitions for versioned contracts, examples, "
            "tests, documentation, compatibility notes, and release evidence"
        ),
        "archive evidence contract for the harness governance track",
    ]
    assert support_scope["not_implemented"] == [
        "every surface-specific validator wired into CI by this track",
        "generated schemas for all public surfaces",
        "release-boundary enforcement for every package registry",
        "runtime validation for downstream adapters outside the repository contracts",
    ]

    assert metadata["gap_register"]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "deferred",
        "out-of-scope",
    }
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/contract_enforcement_harness_20260513/review.md"
    )
    assert "conductor/contract-enforcement.md" in metadata["completion_evidence"]
    assert (TRACK / "review.md").exists()


def test_contract_enforcement_plan_records_archive_review_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "metadata.json" in plan
    assert "plan.md" in plan
    assert "not every surface-specific validator is implemented here" in plan


def test_contract_enforcement_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "Contract Enforcement Harness" in registry
    assert "./archive/contract_enforcement_harness_20260513/" in registry
