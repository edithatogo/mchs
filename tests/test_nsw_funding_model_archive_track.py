from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwau_py import nsw_funding_model

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "nsw_funding_model_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "pricing-and-hwau-strategy.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_nsw_archive_metadata_records_runtime_scope() -> None:
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "nsw_funding_model_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "runtime NSWFundingModelRegistry API for source-backed years",
        "public NSW State Price rows for 2025 and 2026",
        "fail-closed missing-year handling for unavailable NSW years",
        "parallel valuation helper combining NSW and national prices",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "full official NSW source coverage for all historical and future years",
        "validated NSW-specific adjustment modelling for every district/network note",
        "redistribution of restricted NSW service-agreement artefacts",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {"source-gap"}


def test_nsw_archive_plan_tracks_runtime_checkpoint() -> None:
    plan = _read(TRACK / "plan.md")
    registry = _read(TRACKS)
    roadmap = _read(ROADMAP)

    assert "Runtime NSW Funding Registry" in plan
    assert "[checkpoint:" in plan
    assert "- [x] **Track: NSW Funding Model**" in registry
    assert "Parallel comparison output" in roadmap
    assert "NSW State Price per NWAU by financial year" in roadmap


def test_nsw_runtime_registry_matches_archive_scope() -> None:
    registry = nsw_funding_model.NSWFundingModelRegistry.default()

    assert registry.require_record("2025").state_price_per_hwau == 5675
    assert registry.require_record("2026").state_price_per_hwau == 6081
    assert registry.get_record("2024") is None
    try:
        registry.require_state_price("2024")
    except nsw_funding_model.NSWFundingModelError as exc:
        assert "No NSW funding" in str(exc)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("missing NSW state price should fail closed")
