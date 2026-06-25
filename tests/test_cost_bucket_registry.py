from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "cost_bucket_registry_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
SCHEMA_DOC = TRACK / "cost_bucket_registry_schema.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_cost_bucket_registry_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
        SCHEMA_DOC,
    ]:
        assert path.exists(), path


def test_cost_bucket_registry_tracks_md_is_open():
    registry = _read_text(TRACKS)
    assert "Cost Bucket Registry" in registry
    assert "- [x] **Track: Cost Bucket Registry**" in registry
    assert "./archive/cost_bucket_registry_20260512/" in registry


def test_schema_doc_defines_required_fields():
    text = _read_text(SCHEMA_DOC)

    for phrase in [
        "CostBucketEntry",
        "bucket_id",
        "bucket_name",
        "description",
        "effective_year",
        "source_document",
        "caveats",
        "LocalOverlay",
        "local_overlay",
        "public",
    ]:
        assert phrase in text, f"Missing field: {phrase}"


def test_schema_doc_distinguishes_public_from_local():
    text = _read_text(SCHEMA_DOC)

    assert "public IHACPA" in text
    assert "local_overlay" in text
    assert "confidential NHCDC submissions" in text
    assert "jurisdiction-specific" in text


def test_schema_doc_covers_ahpcs_concepts():
    text = _read_text(SCHEMA_DOC)

    for concept in [
        "cost centre",
        "line item",
        "production centre",
        "overhead_allocation",
        "final product",
        "intermediate product",
        "cost ledger",
    ]:
        assert concept in text


def test_schema_doc_explains_usage_boundary():
    text = _read_text(SCHEMA_DOC)

    for phrase in [
        "Costing Analysis",
        "NWAU Calculation",
        "costing-study workflows",
        "local costing policy",
    ]:
        assert phrase in text


def test_cost_bucket_registry_metadata_is_conservative():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))

    assert metadata["track_id"] == "cost_bucket_registry_20260512"
    assert metadata["track_class"] == "costing"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "ahpcs_costing_process_model_20260512" in metadata["dependencies"]
    assert "cost" in metadata["description"].lower()


def test_schema_doc_includes_provenance_fields():
    text = _read_text(SCHEMA_DOC)

    for field in [
        "source_document",
        "source_checksum",
        "source_publication_date",
    ]:
        assert field in text
