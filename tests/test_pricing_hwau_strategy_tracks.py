from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "pricing-and-hwau-strategy.md"
AUDIENCE = ROOT / "docs" / "roadmaps" / "audience-language-strategy.md"

TRACK_IDS = [
    "hwau_terminology_migration_20260513",
    "state_local_price_registry_20260513",
    "nsw_funding_model_20260513",
    "jurisdiction_funding_model_registry_20260513",
    "parallel_valuation_outputs_20260513",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _track_root(track_id: str) -> Path:
    archive = ROOT / "conductor" / "archive" / track_id
    if archive.exists():
        return archive
    return ROOT / "conductor" / "tracks" / track_id


def test_hwau_pricing_tracks_exist_and_define_parallel_valuations():
    roadmap = _read(ROADMAP)
    tracks = _read(TRACKS)

    for track_id in TRACK_IDS:
        root = _track_root(track_id)
        assert (root / "index.md").exists()
        assert (root / "spec.md").exists()
        assert (root / "plan.md").exists()
        metadata = json.loads(_read(root / "metadata.json"))
        assert metadata["track_id"] == track_id
        assert metadata["status"] == "completed"
        assert track_id in tracks

    for phrase in [
        "healthcare weighted activity unit",
        "`hwau`",
        "`nwau`",
        "jurisdiction-specific prices by year",
        "discounted_price",
        "NSW",
        "ACT",
        "NT",
        "WAU",
        "Parallel comparison output",
        "Formula execution and pricing application must remain separate",
    ]:
        assert phrase in roadmap

    assert "NSW Funding Model" in tracks
    assert "Jurisdiction Funding Model Registry" in tracks
    assert "NSW, VIC, QLD, WA, SA, TAS, ACT, and NT" in tracks


def test_language_strategy_retains_research_surfaces_and_blocks_sprawl():
    audience = _read(AUDIENCE)
    tracks = _read(TRACKS)

    for retained in [
        "Julia",
        "SAS",
        "Stata",
        "TypeScript/WASM",
        "C#/.NET",
        "MCP contract",
        "OpenAI tool adapter",
    ]:
        assert retained in audience

    for deferred in [
        "Scala/Spark",
        "Swift",
        "Go",
        "MATLAB",
        "SQL/DuckDB",
    ]:
        assert deferred in audience

    assert "audience/owner evidence gate" in tracks
    assert "Historical/deprioritized" in tracks
    assert "Stata evidence case" in tracks
