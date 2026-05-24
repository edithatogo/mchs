from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

import nwau_py
from nwau_py import emergency_code_mapping_pipeline as pipeline
from nwau_py import emergency_transition_registry
from nwau_py.emergency_code_mapping_pipeline import (
    EmergencyCodeMappingPipelineError,
    build_emergency_code_mapping_asset_reference,
    build_emergency_code_mapping_bundle_record,
    ensure_emergency_code_mapping_bundle_compatibility,
    get_emergency_code_mapping_bundle_record,
    list_emergency_code_mapping_bundle_records,
    summarize_emergency_code_mapping_dry_run,
    validate_emergency_code_mapping_bundle_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "emergency_code_mapping_pipeline_20260512"
CONTRACT = ROOT / "contracts" / "emergency-code-mapping-pipeline"


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def test_track_metadata_spec_and_contract_are_mapping_pipeline_scoped() -> None:
    for path in (
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACK / "plan.md",
        TRACK / "spec.md",
        CONTRACT / "README.md",
        CONTRACT / "emergency-code-mapping-pipeline.contract.json",
        CONTRACT / "emergency-code-mapping-pipeline.schema.json",
        CONTRACT / "examples" / "mapping-bundle-manifest.json",
        CONTRACT / "examples" / "dry-run-mapping-summary.json",
        CONTRACT / "examples" / "diagnostics.json",
        CONTRACT / "examples" / "local-only-external-mapping-placeholder.json",
        CONTRACT / "examples" / "no-proprietary-payload-boundary.json",
    ):
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    contract = _read_json(CONTRACT / "emergency-code-mapping-pipeline.contract.json")
    spec = (TRACK / "spec.md").read_text(encoding="utf-8")

    assert metadata["track_id"] == "emergency_code_mapping_pipeline_20260512"
    assert metadata["current_state"] in {
        "roadmap-only",
        "implemented-metadata-pipeline",
    }
    primary_contract = metadata["primary_contract"]
    assert isinstance(primary_contract, str)
    assert "nwau_py.emergency_code_mapping_pipeline" in primary_contract
    assert _as_mapping(contract["tool"])["name"] == (
        "nwau_py.emergency_code_mapping_pipeline"
    )
    assert _as_mapping(contract["privacy"])["contains_phi"] is False
    assert "Do not invent" in spec
    assert "mapping-bundle schema" in spec


def test_registered_mapping_bundles_cover_udg_and_aecc_eras() -> None:
    records = list_emergency_code_mapping_bundle_records()
    assert [record.bundle_id for record in records] == [
        "emergency_code_mapping_udg_2025",
        "emergency_code_mapping_aecc_2026",
    ]

    udg = get_emergency_code_mapping_bundle_record("udg", "2025")
    aecc = get_emergency_code_mapping_bundle_record("aecc", "2026")
    assert udg is not None
    assert aecc is not None

    assert udg.target_system == "udg"
    assert udg.bundle_version == "UDG_v1.3"
    assert udg.license_boundary == "local-only"
    assert udg.output_fields == ("UDG", "COMPENSABLE_STATUS", "DVA_STATUS")

    assert aecc.target_system == "aecc"
    assert aecc.bundle_version == "v1.1"
    assert aecc.license_boundary == "local-only"
    assert aecc.output_fields == ("AECC", "COMPENSABLE_STATUS", "DVA_STATUS")

    assert pipeline.EMERGENCY_CODE_MAPPING_BUNDLE_VERSION_MATRIX == {
        "aecc": {"2026": "v1.1"},
        "udg": {"2025": "UDG_v1.3"},
    }


def test_mapping_bundle_validation_uses_transition_registry_and_fails_closed() -> None:
    record = get_emergency_code_mapping_bundle_record("aecc", "2026")
    assert record is not None

    compatibility = validate_emergency_code_mapping_bundle_compatibility(record)
    assert compatibility.compatible is True
    assert compatibility.expected_version == "v1.1"
    assert compatibility.compatibility_state == "valid"

    ensured = ensure_emergency_code_mapping_bundle_compatibility(record)
    assert ensured.bundle_id == record.bundle_id

    bad_asset = build_emergency_code_mapping_asset_reference(
        asset_id="bad_local_reference",
        kind="local-only-external-reference",
        source_refs=("reference-data/2020/emergency/aecc/mapping-bundle.yaml",),
        local_path_hint="archive/ihacpa/raw/2020/emergency/aecc/mapping-bundle.yaml",
        restricted=True,
        notes=("local only",),
    )
    with pytest.raises(
        EmergencyCodeMappingPipelineError,
        match=r"must be 'v1\.0_shadow'",
    ):
        build_emergency_code_mapping_bundle_record(
            bundle_id="bad_aecc_2020_mapping",
            pricing_year="2020",
            stream="emergency_department",
            target_system="aecc",
            display_name="AECC",
            bundle_version="v1.1",
            source_fields=("COMPENSABLE_STATUS",),
            output_fields=("AECC", "COMPENSABLE_STATUS"),
            assets=(bad_asset,),
            validation_status="schema-complete",
            provenance={"source_type": "local-only"},
        )


def test_mapping_bundle_rejects_silent_crosswalk_and_preserves_raw_fields() -> None:
    asset = build_emergency_code_mapping_asset_reference(
        asset_id="synthetic_fixture",
        kind="derived-validation-fixture",
        source_refs=("tests/fixtures/derived/emergency/mapping.json",),
        local_path_hint="tests/fixtures/derived/emergency/mapping.json",
        restricted=False,
        notes=("synthetic",),
    )

    with pytest.raises(
        EmergencyCodeMappingPipelineError,
        match="source_fields must not claim another emergency classification output",
    ):
        build_emergency_code_mapping_bundle_record(
            bundle_id="bad_crosswalk_claim",
            pricing_year="2026",
            stream="emergency_department",
            target_system="aecc",
            display_name="AECC",
            source_fields=("UDG",),
            output_fields=("AECC", "UDG"),
            assets=(asset,),
            validation_status="schema-complete",
            provenance={"source_type": "synthetic"},
        )

    with pytest.raises(
        EmergencyCodeMappingPipelineError,
        match="source_fields must be preserved",
    ):
        build_emergency_code_mapping_bundle_record(
            bundle_id="bad_audit_surface",
            pricing_year="2026",
            stream="emergency_department",
            target_system="aecc",
            display_name="AECC",
            source_fields=("TRIAGE_CATEGORY",),
            output_fields=("AECC",),
            assets=(asset,),
            validation_status="schema-complete",
            provenance={"source_type": "synthetic"},
        )


def test_dry_run_reports_unknown_unmapped_deprecated_and_invalid_fields() -> None:
    record = get_emergency_code_mapping_bundle_record("udg", "2025")
    assert record is not None

    summary = summarize_emergency_code_mapping_dry_run(
        record,
        observed_fields=("UDG", "COMPENSABLE_STATUS", "legacy-field", "bad field"),
    )
    assert summary.compatibility.compatible is True
    assert summary.unknown_fields == ("legacy-field", "bad field")
    assert summary.unmapped_fields == ()
    assert summary.invalid_fields == ("bad field",)

    payload = summary.to_dict()
    assert payload["target_system"] == "udg"
    assert _as_mapping(payload["compatibility"])["compatible"] is True


def test_public_exports_include_mapping_pipeline_and_transition_api() -> None:
    expected = {
        "EmergencyCodeMappingAssetReference",
        "EmergencyCodeMappingBundleCompatibilityResult",
        "EmergencyCodeMappingBundleRecord",
        "EmergencyCodeMappingDryRunSummary",
        "EmergencyCodeMappingPipelineError",
        "build_emergency_code_mapping_asset_reference",
        "build_emergency_code_mapping_bundle_record",
        "emergency_code_mapping_pipeline",
        "ensure_emergency_code_mapping_bundle_compatibility",
        "get_emergency_code_mapping_bundle_record",
        "list_emergency_code_mapping_bundle_records",
        "summarize_emergency_code_mapping_dry_run",
        "validate_emergency_code_mapping_bundle_compatibility",
    }
    assert expected.issubset(set(nwau_py.__all__))
    pipeline_exports = set(pipeline.__all__) | {"emergency_code_mapping_pipeline"}
    assert expected.issubset(pipeline_exports)

    assert (
        emergency_transition_registry.get_emergency_classification_status(
            "aecc",
            "2026",
        )
        == "valid"
    )
