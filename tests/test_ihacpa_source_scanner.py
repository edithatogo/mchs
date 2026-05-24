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
from nwau_py.cli.main import cli
from nwau_py.source_scanner import scan_sources_dry_run
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
    spec = Path("conductor/tracks/ihacpa_source_scanner_20260512/spec.md").read_text(
        encoding="utf-8"
    )

    assert metadata["status"] == "complete"
    assert metadata["current_state"] == "prototype"
    assert metadata["publication_status"] == "not-ready"
    assert "- [x] **Track: IHACPA Source Scanner**" in registry
    assert "funding-calculator sources scan" in spec
    assert "does not claim calculator parity" in spec
