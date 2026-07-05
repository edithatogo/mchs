from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwau_py.jurisdiction_price_sources import (
    JURISDICTIONS,
    JurisdictionPriceSourceStatus,
    list_jurisdiction_price_sources,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "jurisdiction_price_source_index_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "jurisdiction-price-source-index.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_jurisdiction_price_source_archive_metadata_records_runtime_scope() -> None:
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "jurisdiction_price_source_index_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["implemented"] == [
        "runtime JurisdictionPriceSourceIndex API",
        (
            "public-safe metadata or blocked rows for NSW, VIC, QLD, WA, SA, "
            "TAS, ACT, and NT"
        ),
        "fail-closed missing source coverage validation",
        "source rows that do not redistribute jurisdiction price values",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "official extracted state and territory price values",
        "redistribution of restricted state or local funding schedules",
        "validated mapping from QWAU, WIES, WAU, or local activity terms to HWAU",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "partially-resolved",
        "source-gap",
    }


def test_jurisdiction_price_source_archive_plan_registry_and_roadmap() -> None:
    plan = _read(TRACK / "plan.md")
    registry = _read(TRACKS)
    roadmap = _read(ROADMAP)

    assert "Runtime Source Index API" in plan
    assert "[checkpoint:" in plan
    assert "- [x] **Track: Jurisdiction Price Source Index**" in registry
    assert "machine-readable runtime source index" in roadmap
    assert (
        "No source-index row contains a committed jurisdiction price value" in roadmap
    )


def test_jurisdiction_price_source_runtime_matches_archive_scope() -> None:
    rows = list_jurisdiction_price_sources(financial_year="2025")

    assert {row.jurisdiction for row in rows} == set(JURISDICTIONS)
    assert all(row.redistribution_status == "metadata_only" for row in rows)
    assert all("not extracted" in row.price_term for row in rows)
    assert {
        row.jurisdiction
        for row in rows
        if row.support_status is JurisdictionPriceSourceStatus.BLOCKED
    } == {"NSW", "TAS", "NT"}
