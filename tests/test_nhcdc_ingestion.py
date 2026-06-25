from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "nhcdc_cost_report_ingestion_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
PIPELINE_DOC = TRACK / "nhcdc_ingestion_pipeline.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_nhcdc_ingestion_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        PIPELINE_DOC,
    ]:
        assert path.exists(), path


def test_nhcdc_ingestion_tracks_md_is_open():
    registry = _read_text(TRACKS)
    assert "NHCDC Cost Report Ingestion" in registry
    assert "- [~] **Track: NHCDC Cost Report Ingestion**" in registry


def test_pipeline_doc_defines_source_inventory():
    text = _read_text(PIPELINE_DOC)

    for field in [
        "year",
        "title",
        "url",
        "file_type",
        "checksum",
        "publication_date",
        "retrieval_date",
        "table_categories",
        "status",
    ]:
        assert field in text, f"Missing inventory field: {field}"


def test_pipeline_doc_covers_parser_normalization():
    text = _read_text(PIPELINE_DOC)

    for phrase in [
        "Normalized Output Schema",
        "provenance",
        "Arrow",
        "Parquet",
        "CSV",
        "XLSX",
    ]:
        assert phrase in text


def test_pipeline_doc_records_gap_handling():
    text = _read_text(PIPELINE_DOC)

    for phrase in [
        "gap_id",
        "gap",
        "format-changed",
        "missing",
    ]:
        assert phrase in text


def test_pipeline_doc_describes_interpretation_limits():
    text = _read_text(PIPELINE_DOC)

    lower = text.lower()
    for phrase in [
        "interpretation limits",
        "patient-level",
        "confidential",
        "compliance certification",
    ]:
        assert phrase in lower


def test_pipeline_doc_links_cost_bucket_registry():
    text = _read_text(PIPELINE_DOC)

    for phrase in [
        "Cost Bucket Registry",
        "cost bucket",
    ]:
        assert phrase in text


def test_nhcdc_ingestion_metadata_is_conservative():
    import json

    metadata = json.loads(_read_text(TRACK / "metadata.json"))

    assert metadata["track_id"] == "nhcdc_cost_report_ingestion_20260512"
    assert metadata["track_class"] == "costing"
    assert metadata["publication_status"] == "not-applicable"
    assert "cost" in metadata["description"].lower()


def test_pipeline_doc_includes_provenance_fields():
    text = _read_text(PIPELINE_DOC)

    for phrase in [
        "provenance",
        "checksum",
        "reproducible",
    ]:
        assert phrase in text
