from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from nwau_py.ar_drg_mapping_registry import (
    ARDRGMappingRegistryError,
    ensure_ar_drg_mapping_compatibility,
    get_ar_drg_mapping_record,
    get_expected_coding_set_versions,
    list_ar_drg_mapping_records,
    validate_ar_drg_mapping_compatibility,
    validate_ar_drg_version_binding,
)
from nwau_py.calculators.acute import build_acute_contract

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "ar_drg_icd_mapping_registry_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = ROOT / "contracts" / "ar-drg-icd-mapping-registry"
DOCS = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "ar-drg-icd-achi-acs-mapping-registry.mdx"
)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_ar_drg_mapping_track_docs_and_contract_are_complete() -> None:
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
        CONTRACT / "ar-drg-icd-mapping-registry.contract.json",
        CONTRACT / "ar-drg-icd-mapping-registry.schema.json",
        CONTRACT / "examples" / "versioned-mapping-registry.json",
        CONTRACT / "examples" / "license-boundary.json",
        CONTRACT / "examples" / "external-grouper-reference.json",
        DOCS,
    ]:
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    tracks = TRACKS.read_text(encoding="utf-8")
    docs = DOCS.read_text(encoding="utf-8")
    contract = _read_json(CONTRACT / "ar-drg-icd-mapping-registry.contract.json")

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "not-ready"
    assert "nwau_py.ar_drg_mapping_registry" in metadata["primary_contract"]
    assert "- [x] **Track: AR-DRG ICD/ACHI/ACS Mapping Registry**" in tracks
    assert "licensed grouping" in docs.lower()
    assert "does not reimplement" in docs.lower()
    assert contract["tool"]["name"] == "nwau_py.ar_drg_mapping_registry"
    assert contract["privacy"]["contains_phi"] is False


def test_ar_drg_mapping_registry_records_are_metadata_only() -> None:
    records = list_ar_drg_mapping_records()
    assert [record.pricing_year for record in records] == ["2025", "2026"]

    record = get_ar_drg_mapping_record("2026")
    assert record is not None
    assert record.ar_drg_version == "v12.0"
    assert record.icd_10_am_version == "12th edition"
    assert record.achi_version == "12th edition"
    assert record.acs_version == "12th edition"

    assets = {asset.kind: asset for asset in record.assets}
    assert set(assets) == {
        "public-metadata",
        "user-supplied-licensed-file",
        "derived-validation-fixture",
    }
    assert assets["public-metadata"].restricted is False
    assert assets["public-metadata"].local_path_hint is None
    assert assets["user-supplied-licensed-file"].restricted is True
    assert assets["user-supplied-licensed-file"].local_path_hint is not None
    assert "licensed/ar_drg" in assets["user-supplied-licensed-file"].local_path_hint
    assert all("grouping logic" not in note.lower() for note in record.notes)


def test_ar_drg_mapping_registry_accepts_and_rejects_version_sets() -> None:
    assert get_expected_coding_set_versions("2026") == {
        "ar_drg": "v12.0",
        "icd_10_am": "12th edition",
        "achi": "12th edition",
        "acs": "12th edition",
    }

    compatible = validate_ar_drg_mapping_compatibility(
        "2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )
    assert compatible.compatible is True
    assert compatible.record is not None

    incompatible = validate_ar_drg_mapping_compatibility(
        "2026",
        ar_drg_version="v11.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )
    assert incompatible.compatible is False
    assert "expected 'v12.0'" in (incompatible.reason or "")

    missing = validate_ar_drg_version_binding("2014", "v7.0")
    assert missing.compatible is True
    assert missing.record is None

    with pytest.raises(ARDRGMappingRegistryError, match=re.escape("expected 'v12.0'")):
        ensure_ar_drg_mapping_compatibility(
            "2026",
            ar_drg_version="v11.0",
            icd_10_am_version="12th edition",
            achi_version="12th edition",
            acs_version="12th edition",
        )


def test_ar_drg_mapping_registry_rejects_invalid_years_and_missing_versions() -> None:
    with pytest.raises(ARDRGMappingRegistryError, match="four-digit"):
        get_ar_drg_mapping_record("2026-27")

    result = validate_ar_drg_mapping_compatibility(
        "2026",
        ar_drg_version=None,
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )
    assert result.compatible is False
    assert "ar_drg=None" in (result.reason or "")


def test_acute_contract_links_to_ar_drg_mapping_record() -> None:
    contract = build_acute_contract(year="2026")

    assert contract.mapping_record is not None
    assert contract.mapping_record.pricing_year == "2026"
    assert contract.mapping_record.ar_drg_version == "v12.0"


def test_ar_drg_mapping_contract_examples_are_metadata_only() -> None:
    example = _read_json(CONTRACT / "examples" / "versioned-mapping-registry.json")
    boundary = _read_json(CONTRACT / "examples" / "license-boundary.json")
    external = _read_json(CONTRACT / "examples" / "external-grouper-reference.json")

    assert example["registry_id"] == "ar_drg_icd_mapping_registry_20260512"
    assert "licensed icd-10-am table rows" in json.dumps(boundary).lower()
    assert "local-only" in json.dumps(external).lower()
    external_reference = external["reference"]
    assert isinstance(external_reference, dict)
    assert external_reference["implementation_evidence"] is False
    assert "placeholder-only" in str(external_reference["evidence_status"])
    versioned_external = example["records"][3]["reference"]
    assert isinstance(versioned_external, dict)
    assert versioned_external["implementation_evidence"] is False
    assert "patient data" in json.dumps(example["records"][2]["boundary"]).lower()
    assert example["records"][2]["boundary"]["contains_phi"] is False
