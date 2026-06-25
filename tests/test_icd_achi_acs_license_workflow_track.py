from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import nwau_py.licensed_product_workflow as lpw
from nwau_py.licensed_product_workflow import (
    LicensedProductAssetReference,
    LicensedProductManifestRecord,
    LicensedProductWorkflowError,
    build_licensed_product_asset_reference,
    build_licensed_product_manifest_record,
    diagnose_missing_licensed_assets,
    ensure_commit_safe_exclusion,
    ensure_licensed_product_compatibility,
    get_licensed_product_manifest_record,
    is_commit_safe_excluded_path,
    is_local_only_licensed_path,
    list_licensed_product_manifest_records,
    resolve_licensed_product_env_path,
    validate_licensed_product_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "icd_achi_acs_license_workflow_20260512"
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

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
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
    asset = manifest["assets"][0]
    assert isinstance(asset, dict)
    assert asset["implementation_evidence"] is False
    assert "placeholder-only" in str(asset["evidence_status"])
    assert boundary["boundary"]["storage_policy"] == "local-only"
    assert guard["diagnostics"]["status"] == "pass"


def test_license_workflow_rejects_path_metadata_and_asset_shape_errors() -> None:
    for path in ["/tmp/licensed", "C:/licensed/icd", "../licensed/icd", "."]:
        with pytest.raises(LicensedProductWorkflowError):
            is_local_only_licensed_path(path)

    with pytest.raises(LicensedProductWorkflowError, match="commit-safe"):
        ensure_commit_safe_exclusion("licensed/icd_10_am")

    with pytest.raises(LicensedProductWorkflowError, match="relative path"):
        resolve_licensed_product_env_path(
            "MCHS_LICENSED_ROOT",
            environ={"MCHS_LICENSED_ROOT": "/tmp/licensed"},
        )

    with pytest.raises(LicensedProductWorkflowError, match="local-only"):
        resolve_licensed_product_env_path(
            "MCHS_LICENSED_ROOT",
            environ={"MCHS_LICENSED_ROOT": "tmp/licensed"},
        )

    with pytest.raises(LicensedProductWorkflowError, match="duplicates"):
        build_licensed_product_asset_reference(
            asset_id="dup-source",
            kind="public-metadata",
            source_refs=("https://example.invalid/a", "https://example.invalid/a"),
            local_path_hint=None,
            restricted=False,
            metadata={"source_refs": ["a"]},
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="local_path_hint"):
        build_licensed_product_asset_reference(
            asset_id="bad-public-path",
            kind="public-metadata",
            source_refs=("https://example.invalid/a",),
            local_path_hint="archive/ihacpa/raw/2026/licensed/icd_10_am",
            restricted=False,
            metadata={"asset_role": "metadata"},
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="require a local_path_hint"):
        build_licensed_product_asset_reference(
            asset_id="missing-path",
            kind="user-supplied-licensed-file",
            source_refs=("https://example.invalid/a",),
            local_path_hint=None,
            restricted=True,
            metadata={"asset_role": "licensed-table-manifest"},
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="must be restricted"):
        build_licensed_product_asset_reference(
            asset_id="not-restricted",
            kind="user-supplied-licensed-file",
            source_refs=("https://example.invalid/a",),
            local_path_hint="archive/ihacpa/raw/2026/licensed/icd_10_am",
            restricted=False,
            metadata={"asset_role": "licensed-table-manifest"},
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="must not be restricted"):
        build_licensed_product_asset_reference(
            asset_id="restricted-derived",
            kind="derived-validation-fixture",
            source_refs=("https://example.invalid/a",),
            local_path_hint=None,
            restricted=True,
            metadata={"asset_role": "fixture"},
            notes=("metadata only",),
        )


def test_license_workflow_manifest_builders_and_compatibility_edges() -> None:
    asset = build_licensed_product_asset_reference(
        asset_id="icd-10-am-public-source",
        kind="public-metadata",
        source_refs=("https://example.invalid/source",),
        local_path_hint=None,
        restricted=False,
        metadata={
            "asset_role": "manifest-boundary",
            "source_refs": ["public catalogue"],
            "pricing_year": "2026",
        },
        notes=("metadata only",),
    )
    record = build_licensed_product_manifest_record(
        pricing_year="2026",
        financial_year="2026-27",
        system="ICD-10-AM",
        display_name="ICD-10-AM test boundary",
        source_page_url="https://example.invalid/source",
        assets=(asset,),
        notes=("metadata only",),
    )

    assert isinstance(asset, LicensedProductAssetReference)
    assert isinstance(record, LicensedProductManifestRecord)
    assert record.expected_version == "12th edition"
    assert record.asset_for_id("icd-10-am-public-source") is asset
    assert record.asset_for_id("missing") is None
    assert record.to_dict()["assets"][0]["metadata"]["pricing_year"] == "2026"

    with pytest.raises(LicensedProductWorkflowError, match="duplicate asset_id"):
        build_licensed_product_manifest_record(
            pricing_year="2026",
            financial_year="2026-27",
            system="ICD-10-AM",
            display_name="ICD-10-AM duplicate boundary",
            source_page_url="https://example.invalid/source",
            assets=(asset, asset),
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="expected_version"):
        build_licensed_product_manifest_record(
            pricing_year="2026",
            financial_year="2026-27",
            system="ICD-10-AM",
            display_name="ICD-10-AM wrong version boundary",
            expected_version="11th edition",
            source_page_url="https://example.invalid/source",
            assets=(asset,),
            notes=("metadata only",),
        )

    with pytest.raises(LicensedProductWorkflowError, match="absolute URL"):
        build_licensed_product_manifest_record(
            pricing_year="2026",
            financial_year="2026-27",
            system="ICD-10-AM",
            display_name="ICD-10-AM source boundary",
            source_page_url="not-a-url",
            assets=(asset,),
            notes=("metadata only",),
        )

    mismatch = validate_licensed_product_compatibility(
        "ICD-10-AM",
        "2026",
        declared_version="12th edition",
        source_page_url="https://example.invalid/wrong",
    )
    assert mismatch.compatible is False
    assert "source_page_url" in (mismatch.reason or "")

    ok = ensure_licensed_product_compatibility(
        "ICD-10-AM",
        "2026",
        declared_version="12th edition",
        source_page_url=(
            get_licensed_product_manifest_record("ICD-10-AM", "2026").source_page_url
        ),
        local_path_hint="archive/ihacpa/raw/2026/licensed/icd_10_am",
    )
    assert ok.compatible is True

    with pytest.raises(LicensedProductWorkflowError, match="expects '12th edition'"):
        ensure_licensed_product_compatibility(
            "ICD-10-AM",
            "2026",
            declared_version="11th edition",
        )

    diagnostics = diagnose_missing_licensed_assets("ICD-10-AM", "2013")
    assert diagnostics[0]["missing_category"] == "licensed-product-manifest"


def test_license_workflow_normalizers_reject_blank_duplicate_and_bad_values() -> None:
    with pytest.raises(LicensedProductWorkflowError, match="asset_id must be a string"):
        LicensedProductAssetReference(
            asset_id=1,  # type: ignore[arg-type]
            kind="public-metadata",
            source_refs=("https://example.invalid/source",),
            local_path_hint=None,
            restricted=False,
            metadata={"asset_role": "metadata"},
            notes=("metadata only",),
        )
    with pytest.raises(
        LicensedProductWorkflowError,
        match="asset_id must not be blank",
    ):
        LicensedProductAssetReference(
            asset_id="",
            kind="public-metadata",
            source_refs=("https://example.invalid/source",),
            local_path_hint=None,
            restricted=False,
            metadata={"asset_role": "metadata"},
            notes=("metadata only",),
        )
    with pytest.raises(
        LicensedProductWorkflowError,
        match="leading or trailing whitespace",
    ):
        LicensedProductAssetReference(
            asset_id=" bad ",
            kind="public-metadata",
            source_refs=("https://example.invalid/source",),
            local_path_hint=None,
            restricted=False,
            metadata={"asset_role": "metadata"},
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match="source_refs must be"):
        LicensedProductAssetReference(
            asset_id="bad-source-type",
            kind="public-metadata",
            source_refs="https://example.invalid/source",  # type: ignore[arg-type]
            local_path_hint=None,
            restricted=False,
            metadata={"asset_role": "metadata"},
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match="unsupported asset kind"):
        LicensedProductAssetReference(
            asset_id="bad-kind",
            kind="unknown",  # type: ignore[arg-type]
            source_refs=("https://example.invalid/source",),
            local_path_hint=None,
            restricted=False,
            metadata={"asset_role": "metadata"},
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match=r"metadata\.source_refs"):
        build_licensed_product_asset_reference(
            asset_id="bad-metadata-list",
            kind="public-metadata",
            source_refs=("https://example.invalid/source",),
            local_path_hint=None,
            restricted=False,
            metadata={"source_refs": ["duplicate", "duplicate"]},
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match=r"metadata\.asset_role"):
        build_licensed_product_asset_reference(
            asset_id="bad-metadata-value",
            kind="public-metadata",
            source_refs=("https://example.invalid/source",),
            local_path_hint=None,
            restricted=False,
            metadata={"asset_role": object()},
            notes=("metadata only",),
        )


def test_license_workflow_manifest_and_validation_error_edges() -> None:
    asset = build_licensed_product_asset_reference(
        asset_id="icd-public-source",
        kind="public-metadata",
        source_refs=("https://example.invalid/source",),
        local_path_hint=None,
        restricted=False,
        metadata={"asset_role": "manifest-boundary"},
        notes=("metadata only",),
    )

    with pytest.raises(LicensedProductWorkflowError, match="supported four-digit"):
        build_licensed_product_manifest_record(
            pricing_year="2027",
            financial_year="2027-28",
            system="ICD-10-AM",
            display_name="ICD-10-AM future boundary",
            source_page_url="https://example.invalid/source",
            assets=(asset,),
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match="deterministic version"):
        build_licensed_product_manifest_record(
            pricing_year="2026",
            financial_year="2026-27",
            system="ICD-10-AM",
            display_name="ICD-10-AM bad version",
            expected_version="12th edition!",
            source_page_url="https://example.invalid/source",
            assets=(asset,),
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match="must not be empty"):
        build_licensed_product_manifest_record(
            pricing_year="2026",
            financial_year="2026-27",
            system="ICD-10-AM",
            display_name="ICD-10-AM no assets",
            source_page_url="https://example.invalid/source",
            assets=(),
            notes=("metadata only",),
        )
    with pytest.raises(LicensedProductWorkflowError, match="must be an absolute URL"):
        validate_licensed_product_compatibility(
            "ICD-10-AM",
            "2026",
            source_page_url="relative/source",
        )

    record = build_licensed_product_manifest_record(
        pricing_year="2026",
        financial_year="2026-27",
        system="ICD-10-AM",
        display_name="ICD-10-AM valid boundary",
        source_page_url="https://example.invalid/source",
        assets=(asset,),
        notes=("metadata only",),
    )
    with pytest.raises(
        LicensedProductWorkflowError,
        match="leading or trailing whitespace",
    ):
        record.asset_for_id(" icd-public-source ")


def test_license_workflow_private_normalizers_cover_scalar_edges() -> None:
    assert lpw._normalize_version(None, field="optional_version") is None
    assert lpw._normalize_metadata_value(True, field="metadata.flag") is True
    assert lpw._normalize_metadata_value(1, field="metadata.count") == 1
    assert lpw._normalize_metadata_value(None, field="metadata.empty") is None
    assert lpw._is_descendant(Path("licensed/icd"), Path("archive/ihacpa/raw")) is False

    with pytest.raises(LicensedProductWorkflowError, match="must not be blank"):
        lpw._normalize_relative_path("", field="path")
    with pytest.raises(LicensedProductWorkflowError, match="absolute URL"):
        lpw._normalize_source_url("https:")
