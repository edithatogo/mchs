from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "cross_language_golden_tests_20260504"
TRACKS = ROOT / "conductor" / "tracks.md"
FIXTURE = ROOT / "tests" / "fixtures" / "golden" / "acute_2025"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_cross_language_golden_track_archive_files_exist():
    for path in [
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "review.md",
    ]:
        assert path.exists(), path


def test_cross_language_golden_metadata_records_real_scope():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "cross_language_golden_tests_20260504"
    assert metadata["current_state"] == "complete"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert metadata["publication_status"] == "not-applicable"

    evidence = set(metadata["completion_evidence"])
    for expected in [
        "tests/fixtures/golden/acute_2025/manifest.json",
        "tests/fixtures/golden/acute_2025/input.csv",
        "tests/fixtures/golden/acute_2025/expected.csv",
        "nwau_py/fixtures.py",
        "tests/test_fixture_manifest.py",
        "tests/test_fixture_consumption.py",
        "tests/test_fixture_cross_engine.py",
        "tests/test_fixture_runner.py",
        "tests/test_cross_language_golden_tests_track.py",
    ]:
        assert expected in evidence


def test_cross_language_golden_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "**Track: Cross-Language Golden Test Suite**" in registry
    assert "./archive/cross_language_golden_tests_20260504/" in registry
    assert "./tracks/cross_language_golden_tests_20260504/" not in registry


def test_acute_2025_fixture_manifest_is_runner_neutral():
    manifest = json.loads(_read(FIXTURE / "manifest.json"))

    assert manifest["fixture_id"] == "acute_2025"
    assert manifest["calculator"] == "acute"
    assert manifest["pricing_year"] == "2025"
    assert manifest["cross_language_ready"] is True
    assert manifest["privacy_classification"] == "synthetic"
    assert manifest["payloads"]["input"]["format"] == "csv"
    assert manifest["payloads"]["expected_output"]["format"] == "csv"
    assert not Path(manifest["payloads"]["input"]["path"]).is_absolute()
    assert not Path(manifest["payloads"]["expected_output"]["path"]).is_absolute()

    encoded = json.dumps(manifest)
    assert "__" not in encoded
    assert "pytest" not in encoded.lower()
    assert "nwau_py" not in encoded.lower()
