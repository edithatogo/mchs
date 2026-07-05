from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = (
    ROOT
    / "conductor"
    / "archive"
    / "roadmap_portfolio_governance_backfill_20260512"
)
TRACKS = ROOT / "conductor" / "tracks.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read_text(path))


def test_roadmap_backfill_archive_metadata_points_to_archive_paths() -> None:
    metadata = _load_json(TRACK / "metadata.json")

    assert metadata["track_id"] == "roadmap_portfolio_governance_backfill_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_evidence"] == [
        "conductor/archive/roadmap_portfolio_governance_backfill_20260512/"
        "governance_backfill_checklist.md",
        "conductor/archive/roadmap_portfolio_governance_backfill_20260512/spec.md",
        "conductor/archive/roadmap_portfolio_governance_backfill_20260512/plan.md",
        "conductor/archive/roadmap_portfolio_governance_backfill_20260512/index.md",
        "tests/test_tracks_registry.py",
        "tests/test_tooling_configuration.py",
    ]
    assert metadata["gap_register"][0]["status"] == "audit-gap"


def test_roadmap_backfill_archive_review_and_registry_are_consistent() -> None:
    review = _read_text(TRACK / "review.md")
    registry = _read_text(TRACKS)

    assert "archive-ready as `complete-with-gaps`" in review
    assert "Keep live as `complete-with-gaps`" not in review
    assert "- [x] **Track: Roadmap Portfolio Governance Backfill**" in registry
    assert "./archive/roadmap_portfolio_governance_backfill_20260512/" in registry
