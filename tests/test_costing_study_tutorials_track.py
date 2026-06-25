from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "costing_study_tutorials_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
FIXTURES = ROOT / "tests" / "data" / "costing_study"
DOCS = ROOT / "docs-site" / "src" / "content" / "docs" / "2026" / "tutorials"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_costing_study_track_archive_files_exist():
    for path in [
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "review.md",
    ]:
        assert path.exists(), path


def test_costing_study_metadata_is_bounded_and_evidenced():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "costing_study_tutorials_20260512"
    assert metadata["track_class"] == "costing"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert metadata["publication_status"] == "not-applicable"

    evidence = set(metadata["completion_evidence"])
    for expected in [
        "docs-site/src/content/docs/2026/tutorials/costing-study-nwau-nep.mdx",
        "docs-site/src/content/docs/2026/tutorials/costing-study-cost-vs-price.mdx",
        "docs-site/src/content/docs/2026/tutorials/costing-study-stream-benchmarking.mdx",
        "tests/data/costing_study/README.md",
        "tests/test_costing_study_tutorials_track.py",
    ]:
        assert expected in evidence

    for dependency in [
        "ahpcs_costing_process_model_20260512",
        "cost_bucket_registry_20260512",
        "cost_bucket_analytics_tutorials_20260512",
        "nhcdc_cost_report_ingestion_20260512",
    ]:
        assert dependency in metadata["dependencies"]


def test_costing_study_tracks_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "- [x] **Track: Costing-Study Tutorials and Examples**" in registry
    assert "./archive/costing_study_tutorials_20260512/" in registry
    assert "./tracks/costing_study_tutorials_20260512/" not in registry


def test_costing_study_tutorials_cover_required_concepts():
    required_docs = [
        DOCS / "costing-study-nwau-nep.mdx",
        DOCS / "costing-study-cost-vs-price.mdx",
        DOCS / "costing-study-stream-benchmarking.mdx",
    ]

    combined = "\n".join(_read(path).lower() for path in required_docs)
    for phrase in [
        "synthetic",
        "nwau",
        "nep",
        "observed cost",
        "nhcdc",
        "ahpcs",
        "benchmark",
        "not actual funding",
    ]:
        assert phrase in combined


def test_costing_study_fixtures_are_public_safe_and_linkable():
    readme = _read(FIXTURES / "README.md").lower()
    for phrase in [
        "all data is synthetic",
        "no real patient",
        "fabricated",
        "do not use for policy or funding decisions",
        "official ihacpa outputs",
    ]:
        assert phrase in readme

    expected_columns = {
        "nwau_calculation_inputs.csv": {"episode_id", "stream"},
        "observed_costs.csv": {"episode_id", "total_cost"},
        "nhcdc_benchmarks.csv": {"stream", "average_cost_per_episode"},
    }
    for filename, columns in expected_columns.items():
        with (FIXTURES / filename).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            assert columns.issubset(reader.fieldnames or []), filename
            assert list(reader), filename
