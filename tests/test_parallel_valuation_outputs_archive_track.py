from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nwau_py import nsw_funding_model, price_registry

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "parallel_valuation_outputs_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "pricing-and-hwau-strategy.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_parallel_valuation_archive_metadata_records_runtime_scope() -> None:
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "parallel_valuation_outputs_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "runtime PriceRegistry API for national, state, local, and discounted rows",
        "public NEP-backed national rows from shared pricing constants",
        "public-safe synthetic state, local, discounted, missing, and blocked fixtures",
        "parallel NSW/national valuation helper combining priced schedules",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "complete official sourced registry for every jurisdiction and year",
        "direct valuation adapters in CLI/file, HTTP API, MCP, and OpenAI surfaces",
        "public claim that synthetic state/local constants are official prices",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "partially-resolved",
        "source-gap",
    }


def test_parallel_valuation_archive_plan_and_registry_are_complete() -> None:
    plan = _read(TRACK / "plan.md")
    registry = _read(TRACKS)
    roadmap = _read(ROADMAP)

    assert "Runtime Registry API" in plan
    assert "[checkpoint:" in plan
    assert "Parallel Valuation Outputs" in registry
    assert (
        "Parallel comparison output across national, state, local, and discounted"
        in roadmap
    )


def test_parallel_valuation_runtime_registry_matches_archive_scope() -> None:
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

    nsw_parallel = nsw_funding_model.apply_parallel_nsw_valuation(
        100.0,
        financial_year="2026",
    )
    assert nsw_parallel["nsw_funding"] == 608100.0
    assert nsw_parallel["national_funding"] == 741800.0
    assert nsw_parallel["state_source_term"] == "NWAU25"
    assert nsw_parallel["national_source_term"] == "NEP"
