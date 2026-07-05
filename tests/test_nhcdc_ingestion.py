from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "nhcdc_cost_report_ingestion_20260512"
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / "nhcdc_cost_report_ingestion_20260512"
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
        ROOT / "nwau_py" / "nhcdc_ingestion.py",
        ROOT
        / "tests"
        / "data"
        / "costing_study"
        / "nhcdc_public_appendix"
        / "manifest.yaml",
        ROOT
        / "tests"
        / "data"
        / "costing_study"
        / "nhcdc_public_appendix"
        / "source.csv",
        ROOT
        / "tests"
        / "data"
        / "costing_study"
        / "nhcdc_public_appendix"
        / "normalized_output.csv",
    ]:
        assert path.exists(), path


def test_nhcdc_ingestion_tracks_md_is_open():
    registry = _read_text(TRACKS)
    assert "NHCDC Cost Report Ingestion" in registry
    assert "- [x] **Track: NHCDC Cost Report Ingestion**" in registry


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


def test_public_nhcdc_appendix_fixture_normalizes_with_provenance():
    from nwau_py.nhcdc_ingestion import (
        diagnose_nhcdc_appendix_source,
        load_nhcdc_appendix_manifest,
        normalize_nhcdc_appendix_table,
    )

    manifest_path = (
        ROOT
        / "tests"
        / "data"
        / "costing_study"
        / "nhcdc_public_appendix"
        / "manifest.yaml"
    )
    normalized_path = (
        ROOT
        / "tests"
        / "data"
        / "costing_study"
        / "nhcdc_public_appendix"
        / "normalized_output.csv"
    )

    manifest = load_nhcdc_appendix_manifest(manifest_path)
    diagnostic = diagnose_nhcdc_appendix_source(manifest_path)
    normalized = normalize_nhcdc_appendix_table(manifest_path)
    expected = pd.read_csv(normalized_path)

    assert manifest.appendix_id == "nhcdc-public-sector-2023-24-summary"
    assert manifest.status == "available"
    assert diagnostic["status"] == "available"
    assert diagnostic["gap_id"] is None
    pd.testing.assert_frame_equal(normalized, expected)


def test_public_nhcdc_appendix_diagnostics_record_missing_and_changed_sources(
    tmp_path: Path,
):
    from nwau_py.nhcdc_ingestion import diagnose_nhcdc_appendix_source

    fixture_dir = (
        ROOT / "tests" / "data" / "costing_study" / "nhcdc_public_appendix"
    )
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(
        (fixture_dir / "manifest.yaml")
        .read_text(encoding="utf-8")
        .replace("source.csv", "missing.csv"),
        encoding="utf-8",
    )

    missing = diagnose_nhcdc_appendix_source(manifest_path)
    assert missing["status"] == "missing"
    assert missing["gap_id"] == "missing-source-file"

    changed_manifest_path = tmp_path / "changed-manifest.yaml"
    changed_manifest_path.write_text(
        (fixture_dir / "manifest.yaml")
        .read_text(encoding="utf-8")
        .replace("source.csv", "changed.csv"),
        encoding="utf-8",
    )
    (tmp_path / "changed.csv").write_text(
        "stream,wrong_column\nacute,1\n",
        encoding="utf-8",
    )

    changed = diagnose_nhcdc_appendix_source(changed_manifest_path)
    assert changed["status"] == "format-changed"
    assert changed["gap_id"] == "format-changed-source-schema"
