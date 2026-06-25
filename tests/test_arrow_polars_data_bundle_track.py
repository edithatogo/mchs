from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "arrow_polars_data_bundle_20260504"
TRACKS = ROOT / "conductor" / "tracks.md"
ADR = ROOT / "docs" / "adr" / "0002-arrow-polars-data-bundle.md"
BUNDLE = ROOT / "tests" / "fixtures" / "bundles" / "acute_2025"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_arrow_polars_track_archive_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
    ]:
        assert path.exists(), path


def test_arrow_polars_registry_points_to_archive():
    registry = _read_text(TRACKS)

    assert "Arrow and Polars Data Bundle Migration" in registry
    assert "./archive/arrow_polars_data_bundle_20260504/" in registry


def test_arrow_polars_metadata_records_scope_gaps_and_evidence():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))

    assert metadata["track_id"] == "arrow_polars_data_bundle_20260504"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "tests/test_bundles.py" in metadata["completion_evidence"]
    assert "nwau_py/bundles.py" in metadata["completion_evidence"]


def test_arrow_polars_adr_and_pilot_bundle_match_track_claims():
    adr = _read_text(ADR)
    manifest = json.loads(_read_text(BUNDLE / "manifest.json"))

    assert "dataframe-neutral" in adr
    assert "Arrow/Parquet" in adr
    assert "Polars" in adr
    assert manifest["backend_neutral"] is True
    assert manifest["payloads"]["input"]["format"] == "parquet"
    assert (BUNDLE / manifest["payloads"]["input"]["path"]).exists()
