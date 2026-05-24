from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "historical_ihacpa_coverage_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
ARCHIVE_MATRIX = ROOT / "conductor" / "ihacpa-archive-matrix.md"
TOOL_MATRIX = ROOT / "conductor" / "ihacpa-tool-coverage-matrix.md"
SOURCE_ARCHIVE = ROOT / "conductor" / "source-archive.md"
HISTORICAL_INVENTORY = TRACK / "historical_source_inventory.md"
MANIFEST_GAPS = TRACK / "manifest_gap_notes.md"
VALIDATION_ROADMAP = TRACK / "validation_roadmap.md"
VALIDATION_SCRIPT = ROOT / "scripts" / "validate_historical_ihacpa_inventory.py"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_historical_ihacpa_coverage_track_scaffold_is_present():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        HISTORICAL_INVENTORY,
        MANIFEST_GAPS,
        VALIDATION_ROADMAP,
        VALIDATION_SCRIPT,
        ARCHIVE_MATRIX,
        TOOL_MATRIX,
        SOURCE_ARCHIVE,
        TRACKS,
    ]:
        assert path.exists(), path


def test_historical_ihacpa_coverage_track_metadata_and_registry_stay_conservative():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    track_index = _read_text(TRACK / "index.md")
    registry = _read_text(TRACKS)
    plan = _read_text(TRACK / "plan.md")

    assert metadata["track_id"] == "historical_ihacpa_coverage_20260512"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "governance"
    assert metadata["current_state"] == "completed-with-explicit-validation-gaps"
    assert metadata["publication_status"] == "not-applicable"
    assert "NHCDC cost evidence" in metadata["description"]
    assert "calculator support" in metadata["description"]

    assert "historical_ihacpa_coverage_20260512" in track_index
    assert "Historical IHACPA Coverage Audit" in registry
    assert "[x] **Track: Historical IHACPA Coverage Audit**" in registry
    assert (
        "verify how far official NEP, technical specification, calculator" in registry
    )
    assert "historical source inventory from 2012-13 to current year" in plan
    assert "Add separate matrix columns" in plan
    assert (
        "Prioritize 2012-13 specification extraction separately from calculator parity"
    ) in plan
    assert "Add foundational 2012-13 PDF hashes" in plan
    assert "executable historical inventory validation" in metadata["primary_contract"]
    assert "2012-13 NWAU calculator support remains an explicit gap" in track_index


def test_historical_ihacpa_coverage_matrix_separates_support_types():
    matrix = _read_text(TOOL_MATRIX)
    archive_matrix = _read_text(ARCHIVE_MATRIX)

    for phrase in [
        (
            "| Artifact family | Earliest confirmed coverage | Current record | "
            "Validation status | Notes |"
        ),
        "Pricing specifications",
        "Calculator artifacts",
        "Price weights",
        "NHCDC / costing evidence",
        "Validation status",
        "2012-13 is a foundational ABF year and stays caveated",
        "Do not infer 2012-13 support from pricing specs or costing evidence.",
        (
            "Useful for costing studies and provenance, but not calculator "
            "support on its own."
        ),
        "The archive should be read as a layered record",
    ]:
        assert phrase in matrix

    assert "2013-14 through 2026-27" in archive_matrix
    assert "box-html-only" in archive_matrix
    assert "Explicit archive gaps: 2" in archive_matrix


def test_historical_ihacpa_coverage_records_explicit_source_provenance():
    spec = _read_text(TRACK / "spec.md")
    source_archive = _read_text(SOURCE_ARCHIVE)
    inventory = _read_text(HISTORICAL_INVENTORY)
    gaps = _read_text(MANIFEST_GAPS)

    for phrase in [
        "National Pricing Model Technical Specifications 2012-13",
        "National Efficient Price Determination 2012-13",
        "National Efficient Price Determination index",
        "NWAU calculators",
        "NHCDC public sector",
        (
            "Keep source provenance auditable with URLs, publication dates, "
            "and file hashes where downloadable."
        ),
    ]:
        assert phrase in spec

    for phrase in [
        "provenance baseline",
        "The committed manifest should remain conservative about what it claims.",
        "SHA-256 checksum",
        "Source page URL",
        "acquisition status",
        "explicit gaps",
    ]:
        assert phrase in source_archive

    for phrase in [
        "460a69489e2bb4210203d35f5095851f8440d55b6a610afc1d580534c7f1983d",
        "0ef844f901347b13746d9b7cb27ab98f97fb303c93ed497e0f188b0e771c7e9c",
        "gap/unknown; no direct 2012-13 calculator artifact proven",
        "NHCDC materials are recorded as cost evidence only",
        "not calculator parity evidence",
    ]:
        assert phrase in inventory

    assert "Calculator archive evidence starts at 2013-14" in gaps
    assert "No 2012-13 NWAU calculator artifact" in gaps


def test_historical_ihacpa_inventory_has_executable_validation_script():
    script = _read_text(VALIDATION_SCRIPT)
    assert "FOUNDATIONAL_HASHES" in script
    assert "2012-13 must remain an explicit calculator gap" in script
    assert "calculator manifest coverage must span 2013-14 through 2026-27" in script
