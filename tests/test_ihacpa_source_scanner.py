from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, cast

import yaml
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import nwau_py.provenance as provenance
import nwau_py.reference_manifest as reference_manifest
import nwau_py.source_scanner as source_scanner
from nwau_py.cli.main import cli
from nwau_py.source_scanner import (
    SourceDocument,
    SourceDraftManifest,
    SourceGapRecord,
    manifest_to_json,
    render_dry_run,
    scan_sources,
    scan_sources_dry_run,
)
from scripts import archive_ihacpa_sources as scanner

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "source_scanner"


def _read_text(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def _load_json(name: str):
    return json.loads(_read_text(name))


def _load_yaml(name: str):
    return yaml.safe_load(_read_text(name))


def _load_contract(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _parse_listing():
    parser = scanner.NwauCalculatorPageParser(scanner.PAGE_URL)
    parser.feed(_read_text("nwau_scanner_listing.html"))
    return parser.items


def _source_signature(record: dict[str, object]) -> tuple[object, ...]:
    return (
        record["artifact_url"],
        record["final_url"],
        record["content_type"],
        record["checksum"],
        record["bytes"],
    )


def test_parser_fixture_groups_years_and_source_categories():
    items = _parse_listing()

    assert [
        (
            item.year_label,
            item.year_start,
            item.artifact_type,
            item.service_stream,
            item.source_host.value,
            item.label,
        )
        for item in items
    ] == [
        (
            "2027-28",
            2027,
            "excel",
            "2027 Acute calculator workbook",
            "ihacpa",
            "2027 Acute calculator workbook",
        ),
        (
            "2027-28",
            2027,
            "sas",
            "SAS-based calculators",
            "ihacpa",
            "2027 SAS calculator package",
        ),
        (
            "2027-28",
            2027,
            "sas",
            "SAS-based calculators",
            "box",
            "2027 SAS calculator package on Box",
        ),
        (
            "2026-27",
            2026,
            "excel",
            "2026 Acute calculator workbook",
            "ihacpa",
            "2026 Acute calculator workbook",
        ),
    ]


def test_dry_run_output_stays_review_only(monkeypatch, capsys, tmp_path):
    items = _parse_listing()
    snapshot = provenance.SourcePageSnapshot(
        path=str(tmp_path / "source-page.html"),
        sha256="snapshot",
        byte_count=1,
        captured_at="2026-05-12T00:00:00+00:00",
    )

    monkeypatch.setattr(
        scanner,
        "parse_artifacts",
        lambda *_args, **_kwargs: (items, snapshot, {"path": snapshot.path}),
    )
    monkeypatch.setattr(scanner, "write_manifests", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        scanner.sys,
        "argv",
        ["archive_ihacpa_sources.py", "--list-only"],
    )

    scanner.main()

    assert json.loads(capsys.readouterr().out) == _load_json("dry_run_summary.json")


def test_gap_records_for_box_and_inaccessible_artifacts_are_explicit():
    records = _load_json("gap_records.json")

    assert [record["gap"]["gap_id"] for record in records] == [
        "2021-22-sas-box-html-share",
        "2022-23-sas-inaccessible",
    ]

    for record in records:
        assert record["gap"]["reason"].strip()
        assert record["gap"]["expected_resolution"].strip()
        status = provenance.normalize_acquisition_status(
            record["artifact_url"],
            final_url=record["final_url"],
            content_type=record["content_type"],
            downloaded=record["downloaded"],
            failed=record["failed"],
        )
        assert status.value == record["expected_acquisition_status"]


def test_unchanged_source_detection_stays_metadata_only_when_checksum_is_stable():
    record = _load_json("unchanged_source.json")
    previous = record["previous"]
    current = record["current"]

    assert _source_signature(previous) == _source_signature(current)
    assert previous["retrieved_at"] != current["retrieved_at"]
    assert record["changed"] is False


def test_add_year_draft_manifest_stays_source_only_and_keeps_gaps_open():
    manifest = reference_manifest.parse_reference_manifest(
        _load_yaml("draft_manifest_2027.yaml"),
        canonical_path="reference-data/2027/manifest.yaml",
    )

    assert manifest.pricing_year == "2027"
    assert manifest.financial_year == "2027-28"
    assert manifest.current_pricing_year is False
    assert manifest.validation_status == "source-only"
    assert manifest.validation.parity_claim is False
    assert manifest.validation.source_only is True
    assert any(
        "no parity validation" in note.lower() for note in manifest.validation.notes
    )
    assert {gap.gap_id for gap in manifest.gaps} == {
        "2027-sas-box-share",
        "2027-price-weights-not-extracted",
    }
    assert {gap.status for gap in manifest.gaps} == {"open", "tracked"}
    assert manifest.unresolved_gaps()


def test_source_scanner_module_discovers_sources_without_network_access():
    result = scan_sources_dry_run(
        html_documents=(FIXTURE_DIR / "nwau_scanner_listing.html",),
        source_page_url="https://www.ihacpa.gov.au/",
        pricing_year="2027",
    )

    assert result.manifest.pricing_year == "2027"
    assert result.manifest.validation_status == "gap-explicit"
    assert len(result.manifest.discoveries) == 5
    assert any(item.host.endswith("box.com") for item in result.manifest.discoveries)
    assert {gap.kind for gap in result.manifest.gaps} == {"license_unclear"}
    assert "discovery-only output" in result.manifest.notes[0]


def test_sources_cli_scan_and_add_year_emit_review_only_json():
    runner = CliRunner()
    fixture = FIXTURE_DIR / "nwau_scanner_listing.html"

    scan_result = runner.invoke(
        cast(Any, cli),
        [
            "sources",
            "scan",
            "--html-file",
            str(fixture),
            "--source-page-url",
            "https://www.ihacpa.gov.au/",
            "--year",
            "2027",
            "--json",
        ],
    )
    assert scan_result.exit_code == 0
    scan_payload = json.loads(scan_result.output)
    assert scan_payload["pricing_year"] == "2027"
    assert scan_payload["dry_run"] is True
    assert scan_payload["validation_status"] == "gap-explicit"

    add_year_result = runner.invoke(
        cast(Any, cli),
        [
            "sources",
            "add-year",
            "2027",
            "--html-file",
            str(fixture),
            "--source-page-url",
            "https://www.ihacpa.gov.au/",
            "--json",
        ],
    )
    assert add_year_result.exit_code == 0
    add_year_payload = json.loads(add_year_result.output)
    assert add_year_payload["pricing_year"] == "2027"
    assert add_year_payload["dry_run"] is True
    assert add_year_payload["validation_status"] == "gap-explicit"


def test_source_scanner_contract_uses_installed_cli_entrypoint():
    contract = _load_contract("contracts/source-scanner/source-scanner.contract.json")
    dry_run = _load_contract("contracts/source-scanner/examples/dry-run.scan.json")
    add_year = _load_contract(
        "contracts/source-scanner/examples/add-year.draft-manifest.json"
    )

    assert contract["tool"]["name"] == "funding-calculator"
    assert contract["outputs"]["draft_manifest_format"] == "yaml"
    assert dry_run["command"].startswith("funding-calculator sources scan")
    assert dry_run["outputs"]["draft_manifest_path"].endswith("manifest.yaml")
    assert add_year["command"] == "funding-calculator sources add-year 2027"
    assert add_year["manifest_path"].endswith("manifest.yaml")


def test_source_scanner_track_is_marked_complete_and_conservative():
    metadata = _load_contract(
        "conductor/tracks/ihacpa_source_scanner_20260512/metadata.json"
    )
    registry = Path("conductor/tracks.md").read_text(encoding="utf-8")
    spec = Path(
        "conductor/tracks/ihacpa_source_scanner_20260512/spec.md"
    ).read_text(encoding="utf-8")

    assert metadata["status"] == "complete"
    assert metadata["current_state"] in {"prototype", "complete-with-gaps"}
    assert metadata["publication_status"] == "not-ready"
    assert "- [x] **Track: IHACPA Source Scanner**" in registry
    assert "funding-calculator sources scan" in spec
    assert "does not claim calculator parity" in spec


def test_source_scanner_text_urls_and_explicit_urls_cover_source_categories():
    manifest = scan_sources(
        text_documents=(
            "Technical specification https://example.invalid/nwau-2026-specification.pdf\n"
            "Price weights https://example.invalid/price-weights-2026.xlsx\n"
            "Calculator https://example.invalid/calculator-2026.zip\n"
            "SAS package https://example.invalid/ra2026-sas-package\n"
            ,
        ),
        urls=("https://box.com/shared-folder",),
        source_page_url="https://www.ihacpa.gov.au/",
        pricing_year="2026",
        scan_id="unit-scan",
    )

    categories = {item.source_category for item in manifest.discoveries}
    artifact_kinds = {item.artifact_kind for item in manifest.discoveries}

    assert "discovery" in categories
    assert {"documentation", "excel", "support", "sas"} <= artifact_kinds
    assert any(item.review_required for item in manifest.discoveries)
    assert any(gap.kind == "license_unclear" for gap in manifest.gaps)
    assert manifest.unresolved_gaps() == manifest.gaps
    assert "unit-scan" in render_dry_run(manifest)
    assert json.loads(manifest_to_json(manifest))["scan_id"] == "unit-scan"


def test_source_scanner_records_missing_and_filename_scope_gaps():
    missing = scan_sources(source_page_url="https://example.invalid/source")
    assert missing.validation_status == "source-discovered"
    assert missing.discoveries == ()
    assert missing.gaps[0].kind == "source_missing"
    assert "none" in render_dry_run(missing)

    filename_gap = scan_sources(urls=("https://example.invalid",), pricing_year="2026")
    assert filename_gap.discoveries[0].filename == ""
    assert filename_gap.discoveries[0].year_label == "2026"
    assert any(gap.kind == "scope_unknown" for gap in filename_gap.gaps)

    resolved_gap = SourceGapRecord(
        gap_id="gap-resolved",
        kind="review_required",
        scope="unit",
        reason="reviewed",
        expected_resolution="none",
        status="resolved",
        notes=("closed",),
    )
    assert resolved_gap.to_dict()["status"] == "resolved"


def test_source_scanner_html_headings_and_duplicate_merging_use_best_label():
    html = """
    <h2>2026-27 Acute calculator resources</h2>
    <a href="/downloads/calculator.xlsx">short</a>
    <a href="/downloads/calculator.xlsx">A much longer calculator label</a>
    <a href="/downloads/no-year.xlsx">Workbook</a>
    <a>No href</a>
    """
    manifest = scan_sources(
        html_documents=(html,),
        source_page_url="https://example.invalid/base/",
        pricing_year="2026",
    )

    labels = {item.source_url: item.label for item in manifest.discoveries}
    assert labels["https://example.invalid/downloads/calculator.xlsx"].endswith(
        "A much longer calculator label"
    )
    assert any("2026-27 Acute calculator resources" in label for label in labels.values())
    assert all(item.source_kind == "html-link" for item in manifest.discoveries)

    document = SourceDocument(
        kind="urls",
        name="explicit",
        content="https://example.invalid/a.pdf",
        source_url="https://example.invalid/source",
    )
    assert document.to_dict()["kind"] == "urls"


def test_source_scanner_file_inputs_result_dict_and_resolved_gap_filter(tmp_path):
    html_path = tmp_path / "listing.html"
    text_path = tmp_path / "listing.txt"
    html_path.write_text(
        "<a href='/no-year.pdf'>No heading and no year</a>"
        "<h2>2026 Reports</h2><a href='/annual-report.html'>Annual report</a>",
        encoding="utf-8",
    )
    text_path.write_text(
        "Classification resource https://example.invalid/classification-resource-2026.html",
        encoding="utf-8",
    )

    result = scan_sources_dry_run(
        html_documents=(html_path,),
        text_documents=(text_path,),
        source_page_url="https://example.invalid/base/",
        pricing_year="2026",
        scan_id="file-input-scan",
    )
    payload = result.to_dict()

    assert payload["manifest"]["scan_id"] == "file-input-scan"
    assert "IHACPA source scanner dry-run" in payload["dry_run_output"]
    assert any(
        item.source_category in {"classification-resource", "report"}
        for item in result.manifest.discoveries
    )

    resolved_gap = SourceGapRecord(
        gap_id="gap-resolved",
        kind="review_required",
        scope="unit",
        reason="reviewed",
        expected_resolution="none",
        status="resolved",
    )
    manifest = SourceDraftManifest(
        schema_version="1",
        generated_at="2026-06-12T00:00:00+00:00",
        scan_id="resolved-gap",
        source_page_url=None,
        pricing_year=None,
        validation_status="gap-explicit",
        dry_run=True,
        documents=(),
        discoveries=(),
        gaps=(resolved_gap,),
    )
    assert manifest.unresolved_gaps() == ()


def test_source_scanner_private_inference_helpers_cover_edge_categories():
    assert source_scanner._extract_year("https://example.invalid/2026-27/report", "") == (
        "2026-27",
        2026,
    )
    assert source_scanner._extract_year("https://example.invalid/2026-25/report", "") == (
        "2026-25",
        2026,
    )
    assert source_scanner._infer_artifact_kind("https://example.invalid/page.html", "") == (
        provenance.ArtifactKind.DOCUMENTATION.value
    )
    assert source_scanner._infer_source_category(
        "Classification resource",
        "https://example.invalid/resource",
    ) == "classification-resource"
    assert source_scanner._infer_source_category(
        "Annual reports",
        "https://example.invalid/report",
    ) == "report"
    assert source_scanner._discover_text(
        SourceDocument(kind="text", name="empty", content="no links here"),
        base_url=None,
        pricing_year=None,
    ) == []
