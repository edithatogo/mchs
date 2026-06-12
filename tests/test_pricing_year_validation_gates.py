from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
import yaml
from click.testing import CliRunner

import nwau_py.pricing_year_validation as pyv
from nwau_py.fixtures import FixtureManifestError
from nwau_py.reference_manifest import ReferenceManifestError, parse_reference_manifest

_cli: Any | None = None
try:
    from nwau_py.cli.main import cli as imported_cli

    _cli = imported_cli
    _CLI_ERR = None
except Exception as exc:  # pragma: no cover - environment dependent
    _CLI_ERR = exc

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "pricing_year_validation_gates_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "pricing_year_validation_gates"
    / "manifest.yaml"
)
CANONICAL_PATH = "reference-data/2027/manifest.yaml"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_fixture() -> dict[str, Any]:
    payload = yaml.safe_load(_read_text(FIXTURE))
    assert isinstance(payload, dict)
    return payload


def test_pricing_year_validation_fixture_records_explicit_missing_evidence():
    manifest = parse_reference_manifest(_load_fixture(), canonical_path=CANONICAL_PATH)

    assert manifest.pricing_year == "2027"
    assert manifest.financial_year == "2027-28"
    assert manifest.validation_status == "source-only"
    assert manifest.validation.parity_claim is False
    assert manifest.validation.source_only is True

    gaps_by_scope = {gap.scope: gap for gap in manifest.gaps}
    assert set(gaps_by_scope) == {
        "source_register.resource_page_url",
        "source_artifacts[0].extraction",
        "fixtures.acute_2027",
    }
    source_gap_reason = gaps_by_scope["source_register.resource_page_url"].reason
    assert "archived" in source_gap_reason.lower()
    assert "extracted" in gaps_by_scope["source_artifacts[0].extraction"].reason.lower()
    assert "fixture pack" in gaps_by_scope["fixtures.acute_2027"].reason.lower()
    assert manifest.unresolved_gaps()


def test_pricing_year_validation_rejects_overclaiming_validated_transition():
    payload = deepcopy(_load_fixture())
    payload["validation_status"] = "validated"
    payload["validation"]["status"] = "validated"
    payload["validation"]["parity_claim"] = True
    payload["validation"]["source_only"] = False

    with pytest.raises(ReferenceManifestError, match="unresolved gaps"):
        parse_reference_manifest(payload, canonical_path=CANONICAL_PATH)


def test_pricing_year_validation_cli_json_is_machine_readable_when_available():
    if _cli is None:
        pytest.fail(f"CLI import failed: {_CLI_ERR}")
    if "validate-year" not in _cli.commands:
        pytest.fail("validate-year CLI is not available in this revision")

    runner = CliRunner()
    result = runner.invoke(
        cast(Any, _cli),
        ["validate-year", "2025", "--json"],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["pricing_year"] == "2025"
    assert payload["passed"] is True
    assert payload["validation_status"] in {
        "source-discovered",
        "source-only",
        "schema-complete",
        "gap-explicit",
        "partially-validated",
        "validated",
        "deprecated",
    }


def test_pricing_year_validation_track_metadata_and_registry_are_explicit():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    index = _read_text(TRACK / "index.md")
    registry = _read_text(TRACKS)

    assert metadata["track_id"] == "pricing_year_validation_gates_20260512"
    assert metadata["status"] == "complete"
    assert metadata["track_class"] == "validator"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "not-ready"
    assert metadata["gap_blockers"]
    assert metadata["completion_policy"].startswith("complete-with-gaps means")
    assert "funding-calculator validate-year <year>" in metadata["primary_contract"]

    assert "pricing_year_validation_gates_20260512" in index
    assert "scaffold" not in index.lower()
    assert "not a publication-ready support claim" in index
    assert "Specification" in index
    assert "Implementation Plan" in index
    assert "Pricing-Year Validation Gates" in registry
    assert "prevent pricing years from being marked supported or validated" in registry
    assert "[./tracks/pricing_year_validation_gates_20260512/]" in registry
    assert "- [x] **Track: Pricing-Year Validation Gates**" in registry


def test_pricing_year_validation_helpers_fail_closed_for_bad_years_and_payloads(
    tmp_path: Path,
) -> None:
    assert pyv._validate_year_label("2025") == "2025"

    for bad_year in [" 2025", "2025 ", "25", "20A5"]:
        with pytest.raises(ValueError):
            pyv._validate_year_label(bad_year)

    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text("{}", encoding="utf-8")
    payload = SimpleNamespace(path="payload.json")
    payload_path = tmp_path / "payload.json"
    payload_path.write_text("{}", encoding="utf-8")

    assert pyv._validated_payload_paths(manifest_path, {"input": payload}) == [
        payload_path
    ]

    with pytest.raises(FixtureManifestError, match="missing declared payload"):
        pyv._validated_payload_paths(
            manifest_path,
            {"missing": SimpleNamespace(path="missing.json")},
        )


def test_pricing_year_validation_report_format_and_discovery_paths(
    tmp_path: Path,
) -> None:
    bundle_manifest = tmp_path / "tests" / "fixtures" / "bundles" / "acute_2025"
    golden_manifest = tmp_path / "tests" / "fixtures" / "golden" / "acute_2025"
    bundle_manifest.mkdir(parents=True)
    golden_manifest.mkdir(parents=True)
    (bundle_manifest / "manifest.json").write_text("{}", encoding="utf-8")
    (golden_manifest / "manifest.json").write_text("{}", encoding="utf-8")

    assert pyv._iter_fixture_manifest_paths(tmp_path, "2025") == [
        ("bundle", bundle_manifest / "manifest.json"),
        ("golden", golden_manifest / "manifest.json"),
    ]

    evidence = pyv.PricingYearFixtureEvidence(
        pack_type="bundle",
        manifest_path=bundle_manifest / "manifest.json",
        fixture_id="acute_2025",
        payload_paths=(bundle_manifest / "payload.json",),
    )
    report = pyv.PricingYearValidationReport(
        year="2025",
        repo_root=tmp_path,
        reference_manifest_path=tmp_path / "reference-data" / "2025" / "manifest.yaml",
        reference_manifest_status="source-only",
        reference_manifest_current_year=False,
        reference_manifest_parity_claim=False,
        reference_manifest_unresolved_gaps=("fixtures.acute_2025",),
        fixture_evidence=(evidence,),
        warnings=("fixture evidence: bundle:acute_2025",),
        errors=("offline gap",),
    )

    payload = report.to_dict()
    rendered = pyv.format_pricing_year_validation_report(report)

    assert payload["passed"] is False
    assert payload["support_claim"] == "not asserted"
    assert payload["fixture_evidence"][0]["fixture_id"] == "acute_2025"
    assert "reference-data unresolved gaps: fixtures.acute_2025" in rendered
    assert "fixture evidence packs: bundle:acute_2025" in rendered
    assert "local validation gate: failed" in rendered


def test_pricing_year_validation_missing_repo_evidence_reports_all_gaps(
    tmp_path: Path,
) -> None:
    report = pyv.validate_pricing_year("2025", repo_root=tmp_path)
    rendered = pyv.format_pricing_year_validation_report(report)

    assert report.passed is False
    assert report.reference_manifest_status == "missing"
    assert any("missing reference-data manifest" in error for error in report.errors)
    assert any("missing fixture evidence" in error for error in report.errors)
    assert "fixture evidence packs: none" in rendered
    assert "support claim: not asserted" in rendered
