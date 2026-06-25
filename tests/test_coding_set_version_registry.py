from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast

import pytest
import yaml
from click.testing import CliRunner

from nwau_py.cli.main import cli
from nwau_py.coding_set_registry import (
    CodingSetRegistryError,
    ensure_coding_set_compatibility,
    get_coding_set_family,
    get_coding_set_version,
    get_expected_coding_set_version,
    get_supported_coding_set_years,
    is_coding_set_licensed,
    is_coding_set_restricted,
    list_coding_set_families,
    validate_coding_set_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "coding_set_version_registry_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
REFERENCE_DATA_2025 = ROOT / "reference-data" / "2025" / "manifest.yaml"
REFERENCE_DATA_2026 = ROOT / "reference-data" / "2026" / "manifest.yaml"
CONTRACT = ROOT / "contracts" / "coding-set-registry"
DOCS = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "coding-set-version-registry.mdx"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _read_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def test_coding_set_registry_track_docs_and_contract_are_complete():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        TRACK / "review.md",
        CONTRACT / "coding-set-registry.contract.json",
        CONTRACT / "coding-set-registry.schema.json",
        CONTRACT / "examples" / "registry-entries.json",
        DOCS,
    ]:
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    registry = _read_text(TRACKS)
    docs = _read_text(DOCS)

    assert metadata["track_id"] == "coding_set_version_registry_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "not-ready"
    assert "nwau_py.coding_set_registry" in metadata["primary_contract"]
    assert "- [x] **Track: Coding-Set Version Registry**" in registry
    assert "restricted licensed products" in docs
    assert "user-managed boundary" in docs


def test_coding_set_registry_covers_required_families_and_license_boundaries():
    families = {family.display_name: family for family in list_coding_set_families()}

    assert set(families) >= {
        "AR-DRG",
        "AECC",
        "UDG",
        "Tier 2",
        "AMHCC",
        "ICD-10-AM",
        "ACHI",
        "ACS",
        "AN-SNAP",
    }
    assert is_coding_set_licensed("AR-DRG") is True
    assert is_coding_set_restricted("ICD-10-AM") is True
    assert is_coding_set_licensed("AECC") is False
    assert is_coding_set_restricted("AECC") is False
    assert "2026" in get_supported_coding_set_years("Tier 2")


@pytest.mark.parametrize(
    ("system", "year", "version"),
    [
        ("ar_drg", "2026", "v12.0"),
        ("tier_2", "2026", "v10.0"),
        ("aecc", "2026", "v1.1"),
        ("udg", "2026", "UDG_v1.3"),
        ("amhcc", "2026", "v1"),
        ("icd_10_am", "2026", "12th edition"),
        ("achi", "2026", "12th edition"),
        ("acs", "2026", "12th edition"),
        ("an_snap", "2026", "v5"),
    ],
)
def test_coding_set_registry_accepts_compatible_versions(system, year, version):
    result = validate_coding_set_compatibility(system, year, version)

    assert result.compatible is True
    assert result.expected_version == version
    assert get_expected_coding_set_version(system, year) == version
    assert get_coding_set_version(system, year) == version


def test_coding_set_registry_rejects_incompatible_missing_and_restricted_cases():
    mismatch = validate_coding_set_compatibility("AR-DRG", "2026", "v11.0")
    assert mismatch.compatible is False
    assert "expects v12.0" in (mismatch.reason or "")

    missing = validate_coding_set_compatibility("AECC", "2019", "v1.1")
    assert missing.compatible is False
    assert missing.expected_version is None
    assert "not mapped" in (missing.reason or "")

    undeclared = validate_coding_set_compatibility("Tier 2", "2026", None)
    assert undeclared.compatible is False
    assert "requires version v10.0" in (undeclared.reason or "")

    restricted = validate_coding_set_compatibility(
        "ICD-10-AM",
        "2026",
        "12th edition",
    )
    assert restricted.compatible is True
    assert restricted.licensed is True
    assert restricted.restriction

    with pytest.raises(CodingSetRegistryError, match=re.escape("expects v12.0")):
        ensure_coding_set_compatibility("AR-DRG", "2026", "v11.0")


def test_coding_set_registry_links_pricing_year_manifests_to_expected_versions():
    for manifest_path in [REFERENCE_DATA_2025, REFERENCE_DATA_2026]:
        manifest = _read_yaml(manifest_path)
        pricing_year = str(manifest["pricing_year"])
        coding_sets = manifest["coding_sets"]
        assert isinstance(coding_sets, list)

        for entry in coding_sets:
            assert isinstance(entry, dict)
            name = str(entry["name"])
            version = str(entry["version"])
            family = get_coding_set_family(name)
            expected = get_coding_set_version(family.system, pricing_year)
            assert expected == version


def test_coding_set_registry_cli_lists_and_validates_metadata_only_records():
    runner = CliRunner()

    list_result = runner.invoke(
        cast(Any, cli),
        ["coding-set", "registry", "list", "--year", "2026"],
    )
    assert list_result.exit_code == 0, list_result.output
    listing = json.loads(list_result.output)
    assert any(item["display_name"] == "AR-DRG" for item in listing["families"])
    assert all(item["metadata_only"] is True for item in listing["families"])

    pass_result = runner.invoke(
        cast(Any, cli),
        [
            "coding-set",
            "registry",
            "validate-compatibility",
            "--entry",
            "AR-DRG",
            "--year",
            "2026",
            "--version",
            "v12.0",
        ],
    )
    assert pass_result.exit_code == 0, pass_result.output
    assert json.loads(pass_result.output)["compatible"] is True

    fail_result = runner.invoke(
        cast(Any, cli),
        [
            "coding-set",
            "registry",
            "validate-compatibility",
            "--entry",
            "AR-DRG",
            "--year",
            "2026",
            "--version",
            "v11.0",
        ],
    )
    assert fail_result.exit_code == 1
    assert json.loads(fail_result.output)["compatible"] is False


def test_coding_set_registry_contract_examples_are_metadata_only():
    contract = _read_json(CONTRACT / "coding-set-registry.contract.json")
    entries = _read_json(CONTRACT / "examples" / "registry-entries.json")

    assert contract["tool"]["name"] == "funding-calculator"
    assert entries["privacy"]["classification"] == "synthetic"
    assert entries["summary"]["licensed_table_payloads"] == 0
    assert all(
        entry["table_payload_kind"] == "metadata_only"
        for entry in entries["registry_entries"]
    )
