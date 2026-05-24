from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from nwau_py.licensed_product_workflow import (
    LicensedProductWorkflowError,
    build_licensed_product_asset_reference,
    diagnose_missing_licensed_assets,
    ensure_commit_safe_exclusion,
    get_licensed_product_manifest_record,
    is_commit_safe_excluded_path,
    is_local_only_licensed_path,
    list_licensed_product_manifest_records,
    resolve_licensed_product_env_path,
    validate_licensed_product_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "icd_achi_acs_license_workflow_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = ROOT / "contracts" / "icd-achi-acs-license-workflow"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def test_license_workflow_track_docs_and_contract_are_complete() -> None:
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
        TRACKS,
        CONTRACT / "icd-achi-acs-license-workflow.contract.json",
        CONTRACT / "icd-achi-acs-license-workflow.schema.json",
        CONTRACT / "examples" / "local-licensed-asset-manifest.json",
        CONTRACT / "examples" / "commit-guard-diagnostics.json",
        CONTRACT / "examples" / "setup-placeholders.json",
    ]:
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    tracks = _read_text(TRACKS)
    spec = _read_text(TRACK / "spec.md")

    assert metadata["status"] == "complete"
    assert metadata["current_state"] == "implemented-local-only-workflow"
    assert metadata["publication_status"] == "not-ready"
    assert "nwau_py.licensed_product_workflow" in metadata["primary_contract"]
    assert "- [x] **Track: ICD-10-AM/ACHI/ACS Licensed Product Workflow**" in tracks
    assert "environment variables" in spec
    assert "must not commit, mirror, or redistribute" in spec


def test_manifest_records_are_metadata_only_and_commit_safe() -> None:
    records = list_licensed_product_manifest_records("2026")
    systems = {record.system for record in records}

    assert {"ar_drg", "icd_10_am", "achi", "acs"} <= systems
    record = get_licensed_product_manifest_record("ICD-10-AM", "2026")
    assert record is not None
    assert record.expected_version == "12th edition"

    restricted_assets = [asset for asset in record.assets if asset.restricted]
    assert restricted_assets
    assert all(asset.local_path_hint is not None for asset in restricted_assets)
    assert all(
        is_commit_safe_excluded_path(asset.local_path_hint or "")
        for asset in restricted_assets
    )


def test_local_only_and_env_backed_paths_validate_without_reading_assets() -> None:
    assert is_local_only_licensed_path("archive/ihacpa/raw/2026/licensed/icd_10_am")
    assert is_local_only_licensed_path("licensed/icd_10_am")
    assert not is_commit_safe_excluded_path("licensed/icd_10_am")
    assert ensure_commit_safe_exclusion(
        "archive/ihacpa/raw/2026/licensed/icd_10_am"
    ).endswith("icd_10_am")

    resolved = resolve_licensed_product_env_path(
        "MCHS_LICENSED_ROOT",
        environ={"MCHS_LICENSED_ROOT": "archive/ihacpa/raw/2026/licensed"},
        subpath="icd_10_am",
    )
    assert resolved == "archive/ihacpa/raw/2026/licensed/icd_10_am"

    with pytest.raises(LicensedProductWorkflowError, match="not set"):
        resolve_licensed_product_env_path("MISSING_LICENSED_ROOT", environ={})


def test_restricted_payloads_and_unsafe_metadata_are_rejected() -> None:
    with pytest.raises(LicensedProductWorkflowError, match="public-metadata"):
        build_licensed_product_asset_reference(
            asset_id="bad-public",
            kind="public-metadata",
            source_refs=("https://example.invalid/public",),
            local_path_hint=None,
            restricted=True,
            metadata={"asset_role": "manifest-boundary"},
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="unsupported keys"):
        build_licensed_product_asset_reference(
            asset_id="bad-metadata",
            kind="user-supplied-licensed-file",
            source_refs=("https://example.invalid/licensed",),
            local_path_hint="archive/ihacpa/raw/2026/licensed/icd_10_am",
            restricted=True,
            metadata={"code_rows": ["A00"]},
            notes=("unsafe metadata",),
        )


def test_missing_local_asset_diagnostics_are_safe_and_non_disclosing() -> None:
    diagnostics = diagnose_missing_licensed_assets("ICD-10-AM", "2026")

    assert diagnostics
    diagnostic_json = json.dumps(diagnostics).lower()
    assert "licensed-table-manifest" in diagnostic_json
    assert "a00" not in diagnostic_json
    assert "diagnosis" not in diagnostic_json
    assert all("safe_message" in item for item in diagnostics)

    record = get_licensed_product_manifest_record("ICD-10-AM", "2026")
    assert record is not None
    existing = [
        asset.local_path_hint
        for asset in record.assets
        if asset.restricted and asset.local_path_hint is not None
    ]
    assert (
        diagnose_missing_licensed_assets(
            "ICD-10-AM",
            "2026",
            existing_paths=existing,
        )
        == ()
    )


def test_licensed_product_compatibility_fails_closed() -> None:
    ok = validate_licensed_product_compatibility(
        "ICD-10-AM",
        "2026",
        declared_version="12th edition",
        local_path_hint="archive/ihacpa/raw/2026/licensed/icd_10_am",
    )
    assert ok.compatible is True

    mismatch = validate_licensed_product_compatibility(
        "ICD-10-AM",
        "2026",
        declared_version="11th edition",
    )
    assert mismatch.compatible is False
    assert "expects '12th edition'" in (mismatch.reason or "")

    unsafe = validate_licensed_product_compatibility(
        "ICD-10-AM",
        "2026",
        local_path_hint="tmp/icd_10_am",
    )
    assert unsafe.compatible is False
    assert "local-only" in (unsafe.reason or "")

    with pytest.raises(LicensedProductWorkflowError, match="parent traversal"):
        is_local_only_licensed_path("../licensed/icd_10_am")


def test_contract_examples_are_synthetic_and_local_only() -> None:
    manifest = _read_json(CONTRACT / "examples" / "local-licensed-asset-manifest.json")
    boundary = _read_json(CONTRACT / "examples" / "license-boundary.json")
    guard = _read_json(CONTRACT / "examples" / "commit-guard-diagnostics.json")

    assert manifest["privacy"]["contains_phi"] is False
    assert "licensed code rows" not in json.dumps(manifest).lower()
    assert boundary["boundary"]["storage_policy"] == "local-only"
    assert guard["diagnostics"]["status"] == "pass"
