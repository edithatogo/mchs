from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

import pytest
import yaml
from click.testing import CliRunner

from nwau_py.reference_manifest import ReferenceManifestError, parse_reference_manifest
from nwau_py.pricing_year_validation import (
    format_pricing_year_validation_report,
    validate_pricing_year,
)

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
        pytest.skip(f"CLI import failed: {_CLI_ERR}")
    if "validate-year" not in _cli.commands:
        pytest.skip("validate-year CLI is not available in this revision")

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


def test_pricing_year_validation_rejects_bad_year_labels() -> None:
    with pytest.raises(ValueError, match="leading or trailing"):
        validate_pricing_year(" 2025")
    with pytest.raises(ValueError, match="four-digit"):
        validate_pricing_year("25")


def test_pricing_year_validation_reports_missing_local_evidence(tmp_path: Path) -> None:
    report = validate_pricing_year("2027", repo_root=tmp_path)
    payload = report.to_dict()
    rendered = format_pricing_year_validation_report(report)

    assert report.passed is False
    assert payload["pricing_year"] == "2027"
    assert payload["validation_status"] == "missing"
    assert payload["fixture_evidence"] == []
    assert any("missing reference-data manifest" in error for error in report.errors)
    assert any("missing fixture evidence" in error for error in report.errors)
    assert "reference-data unresolved gaps: none" in rendered
    assert "fixture evidence packs: none" in rendered
    assert "local validation gate: failed" in rendered
    assert "support claim: not asserted" in rendered


def test_pricing_year_validation_surfaces_fixture_year_mismatches(
    tmp_path: Path,
) -> None:
    fixture_root = tmp_path / "tests" / "fixtures" / "golden"
    fixture_root.mkdir(parents=True)
    shutil.copytree(
        ROOT / "tests" / "fixtures" / "golden" / "acute_2025",
        fixture_root / "acute_2027",
    )

    report = validate_pricing_year("2027", repo_root=tmp_path)

    assert report.passed is False
    assert any("declares pricing_year '2025'" in error for error in report.errors)
    assert any("missing fixture evidence" in error for error in report.errors)


def test_pricing_year_validation_records_valid_fixture_evidence_without_support_claim(
    tmp_path: Path,
) -> None:
    fixture_root = tmp_path / "tests" / "fixtures" / "golden"
    fixture_root.mkdir(parents=True)
    shutil.copytree(
        ROOT / "tests" / "fixtures" / "golden" / "acute_2025",
        fixture_root / "acute_2025",
    )

    report = validate_pricing_year("2025", repo_root=tmp_path)
    payload = report.to_dict()
    rendered = format_pricing_year_validation_report(report)

    assert report.passed is False
    assert payload["fixture_evidence"][0]["pack_type"] == "golden"
    assert payload["fixture_evidence"][0]["fixture_id"] == "acute_2025"
    assert payload["support_claim"] == "not asserted"
    assert any("fixture evidence:" in warning for warning in report.warnings)
    assert "fixture evidence packs: golden:acute_2025" in rendered


def test_pricing_year_validation_track_metadata_and_registry_are_explicit():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    index = _read_text(TRACK / "index.md")
    registry = _read_text(TRACKS)

    assert metadata["track_id"] == "pricing_year_validation_gates_20260512"
    assert metadata["status"] == "complete"
    assert metadata["track_class"] == "validator"
    assert metadata["current_state"] == "implemented-with-explicit-validation-gaps"
    assert metadata["publication_status"] == "not-ready"
    assert "funding-calculator validate-year <year>" in metadata["primary_contract"]

    assert "pricing_year_validation_gates_20260512" in index
    assert "Specification" in index
    assert "Implementation Plan" in index
    assert "Pricing-Year Validation Gates" in registry
    assert "prevent pricing years from being marked supported or validated" in registry
    assert "[./tracks/pricing_year_validation_gates_20260512/]" in registry
    assert "- [x] **Track: Pricing-Year Validation Gates**" in registry
