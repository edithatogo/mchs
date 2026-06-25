from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "docs_sota_starlight_completion_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
DOCS_SITE = ROOT / "docs-site" / "src" / "content" / "docs"
HOME = DOCS_SITE / "index.mdx"
COVERS = DOCS_SITE / "versions" / "index.mdx"
COVERAGE = DOCS_SITE / "governance" / "calculator-coverage.mdx"
CONTRACT = DOCS_SITE / "governance" / "public-calculator-contract.mdx"
CONTRACT_SCHEMA = (
    ROOT
    / "docs-site"
    / "public"
    / "contracts"
    / "public-calculator-contract.v1.schema.json"
)
EXTENSIONS = DOCS_SITE / "governance" / "starlight-extensions.mdx"
SOURCE_ARCHIVE = DOCS_SITE / "governance" / "source-archive.md"
GOVERNANCE_INDEX = DOCS_SITE / "governance" / "index.mdx"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_docs_site_homepage_positions_the_current_public_contract():
    assert (TRACK / "metadata.json").exists()
    assert (TRACK / "review.md").exists()
    tracks = _read(TRACKS)
    assert "./archive/docs_sota_starlight_completion_20260513/" in tracks
    assert "./tracks/docs_sota_starlight_completion_20260513/" not in tracks

    home = _read(HOME)

    for phrase in [
        "Microcosting Health Services docs",
        "Versioned IHACPA calculator docs",
        "Browse 2025 docs",
        "Review coverage",
        "Versioning guide",
        "Current contract",
        "Source archive",
        "Implemented surface",
        "Delivery surfaces",
        "Public calculator contract",
        "GitHub Pages",
        "Power Platform",
    ]:
        assert phrase in home


def test_docs_site_coverage_page_describes_current_implementation_state():
    coverage = _read(COVERAGE)

    for phrase in [
        "Calculator coverage",
        "Acute, ED, MH, subacute, outpatients, and adjustment logic",
        "HAC, AHR, and complexity",
        "2013-14 through 2026-27",
        "currently has 94",
        "92 of which are downloaded",
        "2021-22 SAS Box page",
        "2022-23 SAS Box page",
        "Documented gap",
    ]:
        assert phrase in coverage


def test_docs_site_versioning_page_explains_the_version_switching_model():
    versioning = _read(COVERS)

    for phrase in [
        "Versioning",
        "Current version",
        "2025 is the active versioned documentation set",
        "version switcher",
        "Available versions",
        "How to read versioned docs",
    ]:
        assert phrase in versioning


def test_docs_site_extensions_page_lists_recommended_starlight_plugins():
    extensions = _read(EXTENSIONS)

    for phrase in [
        "Starlight extensions",
        "starlight-versions",
        "starlight-links-validator",
        "starlight-openapi",
        "starlight-typedoc",
        "starlight-blog",
        "Algolia DocSearch",
    ]:
        assert phrase in extensions


def test_docs_site_contract_page_records_the_runtime_neutral_boundary():
    contract = _read(CONTRACT)

    for phrase in [
        "Public calculator contract",
        "Contract version",
        "Version `1.0`",
        "Calculator identifiers",
        "Required inputs",
        "Required outputs",
        "Generation readiness",
        "OpenAPI",
    ]:
        assert phrase in contract


def test_docs_site_contract_schema_is_published_as_machine_readable_artifact():
    schema = _read(CONTRACT_SCHEMA)

    for phrase in [
        '"title": "Public Calculator Contract"',
        '"schema_version"',
        '"calculator_id"',
        '"pricing_year"',
        '"required_input_columns"',
        '"required_output_columns"',
        '"acute"',
        '"adjust"',
        '"NWAU25"',
    ]:
        assert phrase in schema


def test_docs_site_source_archive_page_records_explicit_gaps():
    source_archive = _read(SOURCE_ARCHIVE)

    assert "Manifest entries: 94" in source_archive
    assert "Downloaded entries: 92" in source_archive
    assert "Explicit gaps: 2" in source_archive
    assert "2021-22" in source_archive
    assert "2022-23" in source_archive
    assert "explicit gap" in source_archive.lower()


def test_docs_site_governance_index_prioritizes_the_curated_paths():
    governance = _read(GOVERNANCE_INDEX)

    assert "Calculator coverage" in governance
    assert "Versioning" in governance
    assert "Starlight extensions" in governance
    assert "Public calculator contract" in governance
    assert "Contract schema" in governance
    assert "Source archive" in governance
    assert "Rust core architecture" in governance
    assert "Public readiness" in governance
    assert "Reading order" in governance
    assert "Web and Power Platform delivery" in governance
    assert "Streamlit delivery" in governance
    assert "Downstream packaging plans" in governance
