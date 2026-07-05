from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwau_py import jurisdiction_funding_model_registry as funding_registry

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "jurisdiction_funding_model_registry_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "pricing-and-hwau-strategy.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_jurisdiction_funding_archive_metadata_records_runtime_scope() -> None:
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "jurisdiction_funding_model_registry_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "runtime JurisdictionFundingModelRegistry API",
        "explicit source-status rows for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT",
        "parallel jurisdiction valuation helper for priced rows",
        "fail-closed blocked and missing jurisdiction handling",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "official extracted funding model rows for every state and territory year",
        "redistribution of restricted state and territory funding schedules",
        "full validated adjustment logic for every jurisdiction-specific caveat",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {"source-gap"}


def test_jurisdiction_funding_archive_plan_and_registry_are_complete() -> None:
    plan = _read(TRACK / "plan.md")
    registry = _read(TRACKS)
    roadmap = _read(ROADMAP)

    assert "Runtime Jurisdiction Registry" in plan
    assert "[checkpoint:" in plan
    assert "- [x] **Track: Jurisdiction Funding Model Registry**" in registry
    assert (
        "Parallel comparison output across national, state, local, and discounted"
        in roadmap
    )


def test_jurisdiction_funding_runtime_registry_matches_archive_scope() -> None:
    registry = funding_registry.JurisdictionFundingModelRegistry.default()

    assert registry.require_record("NSW", "2025").support_status is (
        funding_registry.JurisdictionFundingModelStatus.PUBLIC
    )
    assert registry.require_record("VIC", "2025").support_status is (
        funding_registry.JurisdictionFundingModelStatus.LOCAL_ONLY
    )
    assert registry.require_record("WA", "2025").price_per_hwau is None
    assert registry.require_record("TAS", "2025").support_status is (
        funding_registry.JurisdictionFundingModelStatus.BLOCKED
    )
