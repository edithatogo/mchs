from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "expert_panel_remediation_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read_text(path))


def test_expert_panel_archive_metadata_uses_archive_paths() -> None:
    metadata = _load_json(TRACK / "metadata.json")

    assert metadata["track_id"] == "expert_panel_remediation_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_evidence"] == [
        "conductor/archive/expert_panel_remediation_20260512/"
        "expert_panel_remediation.md",
        "conductor/archive/expert_panel_remediation_20260512/spec.md",
        "conductor/archive/expert_panel_remediation_20260512/plan.md",
        "conductor/archive/expert_panel_remediation_20260512/index.md",
        "tests/test_tracks_registry.py",
    ]
    gap_register = cast(list[dict[str, Any]], metadata["gap_register"])
    assert gap_register[0]["status"] == "delegated"


def test_expert_panel_archive_review_and_registry_are_consistent() -> None:
    review = _read_text(TRACK / "review.md")
    registry = _read_text(TRACKS)

    assert "archive-ready as `complete-with-gaps`" in review
    assert "keep live as `complete-with-gaps`" not in review
    assert "- [x] **Track: Expert Panel Remediation**" in registry
