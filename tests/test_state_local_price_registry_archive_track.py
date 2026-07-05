from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwau_py import price_registry

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "state_local_price_registry_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "pricing-and-hwau-strategy.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_state_local_price_archive_metadata_records_runtime_scope():
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "state_local_price_registry_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "runtime PriceRegistry API for national, state, local, and discounted rows",
        "public NEP-backed national rows from shared pricing constants",
        "local-only synthetic state, local, discounted, missing, and blocked fixtures",
        "fail-closed lookup behavior for unavailable or non-redistributable schedules",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "complete official sourced registry for every jurisdiction and year",
        "redistribution of restricted local or licensed price schedules",
        "public claim that synthetic state/local constants are official prices",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "partially-resolved",
        "source-gap",
    }


def test_state_local_price_archive_plan_and_registry_are_complete():
    plan = _read(TRACK / "plan.md")
    registry = _read(TRACKS)

    assert "[checkpoint:" in plan
    assert "Runtime Registry API" in plan
    assert "conductor/archive/state_local_price_registry_20260513" in plan
    assert "conductor/tracks/state_local_price_registry_20260513" not in plan
    assert "- [x] **Track: State and Local Price Registry**" in registry


def test_state_local_price_runtime_api_matches_archive_scope():
    registry = price_registry.PriceRegistry.default()

    assert price_registry.get_national_price("2026").price_per_hwau == 7418
    assert price_registry.get_state_price("NSW", "2025").price_per_hwau == 7300
    assert price_registry.get_local_price("Sydney_LHN", "2025").price_per_hwau == 7100
    assert (
        price_registry.get_discounted_price("NSW_rural_multiplier", "2025")
        .price_per_hwau
        == 8395
    )
    assert registry.require_price("WA_blocked_local_source", "2025").support_status is (
        price_registry.PriceSourceStatus.BLOCKED
    )


def test_state_local_price_roadmap_preserves_public_source_boundary():
    roadmap = _read(ROADMAP)

    assert "public-source data and local-only/licensed data" in roadmap
    assert "no public sourced state/local pricing support claim" in roadmap
