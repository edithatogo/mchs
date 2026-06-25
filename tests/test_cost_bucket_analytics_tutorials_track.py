from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "cost_bucket_analytics_tutorials_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_cost_bucket_analytics_tutorial_archive_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
        TRACK / "tutorial_cost_bucket_analytics.md",
    ]:
        assert path.exists(), path


def test_cost_bucket_analytics_tutorial_records_public_safe_scope():
    tutorial = _read(TRACK / "tutorial_cost_bucket_analytics.md")

    for phrase in [
        "synthetic data",
        "public aggregate NHCDC",
        "not confidential patient-level submissions",
        "cost-versus-NWAU",
        "Local Cost Bucket Mapping Overlays",
    ]:
        assert phrase in tutorial


def test_cost_bucket_analytics_metadata_records_scope_gaps_and_dependencies():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "cost_bucket_analytics_tutorials_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert "cost_bucket_registry_20260512" in metadata["dependencies"]
    assert "ahpcs_costing_process_model_20260512" in metadata["dependencies"]
    assert metadata["support_scope"]
    assert metadata["gap_register"]


def test_cost_bucket_analytics_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "Cost Bucket Analytics Tutorials" in registry
    assert "./archive/cost_bucket_analytics_tutorials_20260512/" in registry
