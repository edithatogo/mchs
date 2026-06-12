from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

import nwau_py
from nwau_py import emergency_grouper
from nwau_py.emergency_grouper import (
    EmergencyGrouperError,
    EmergencyGrouperOutputRecord,
    EmergencyGrouperVersionWindow,
    build_emergency_external_reference,
    build_emergency_output_record_from_reference,
    build_emergency_precomputed_output_record,
    build_emergency_provenance,
    ensure_emergency_grouper_compatibility,
    validate_emergency_grouper_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "emergency_grouper_integration_20260512"
CONTRACT = ROOT / "contracts" / "emergency-grouper-integration"
SHA = "0" * 64


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _reference() -> emergency_grouper.EmergencyGrouperReference:
    return build_emergency_external_reference(
        reference_id="local_aecc_service",
        reference_type="local_service",
        status="resolved",
        reference_uri="http://localhost:8765/aecc",
        supported_versions=(
            {
                "system": "aecc",
                "pricing_year": "2026",
                "emergency_classification_version": "v1.1",
                "stream_compatibility": ("emergency_department",),
                "source_refs": (
                    "contracts/emergency-grouper-integration/examples/"
                    "external-local-grouper-service-reference.json",
                ),
            },
        ),
        notes=("local-only service reference",),
    )


def test_track_and_contract_target_the_emergency_grouper_surface() -> None:
    metadata = _read_json(TRACK / "metadata.json")
    contract = _read_json(CONTRACT / "emergency-grouper-integration.contract.json")
    spec = (TRACK / "spec.md").read_text(encoding="utf-8")

    assert metadata["track_id"] == "emergency_grouper_integration_20260512"
    assert metadata["current_state"] in {
        "roadmap-only",
        "implemented-metadata-integration",
        "complete-with-gaps",
    }
    primary_contract = metadata["primary_contract"]
    assert isinstance(primary_contract, str)
    assert "nwau_py.emergency_grouper" in primary_contract
    assert _as_mapping(contract["tool"])["name"] == "nwau_py.emergency_grouper"
    assert _as_mapping(contract["privacy"])["contains_phi"] is False
    assert "precomputed UDG/AECC outputs" in spec
    assert "external command integration" in spec
    assert "service integration" in spec
    assert "file-exchange integration" in spec
    assert "Never silently convert between UDG and AECC" in spec


def test_emergency_grouper_placeholders_are_not_implementation_evidence() -> None:
    reference = _read_json(
        CONTRACT / "examples" / "external-local-grouper-service-reference.json"
    )
    precomputed = _read_json(CONTRACT / "examples" / "precomputed-output-manifest.json")

    assert reference["access_mode"] == "local-only"
    assert reference.get("implementation_evidence", False) is False
    assert "placeholder-only" in str(
        reference.get("evidence_status", "placeholder-only")
    )
    assert precomputed["output_status"] == "synthetic"
    assert precomputed.get("implementation_evidence", False) is False
    assert "synthetic" in str(precomputed.get("evidence_status", "synthetic"))
    assert _as_mapping(precomputed["provenance"])["classification_basis"] in {
        "precomputed_official_classification",
        "synthetic_precomputed_placeholder",
    }


def test_precomputed_outputs_validate_strictly_and_record_provenance() -> None:
    record = build_emergency_precomputed_output_record(
        "AECC-01",
        system="aecc",
        year="2026",
        stream="emergency_department",
        emergency_classification_version="v1.1",
        input_sha256=SHA,
        episode_id="synthetic-episode-1",
        mapping_bundle_id="emergency_code_mapping_aecc_2026",
        mapping_bundle_version="v1.1",
    )

    assert record.classification_code == "AECC-01"
    assert record.episode_id == "synthetic-episode-1"
    assert record.provenance.system == "aecc"
    assert record.provenance.source_mode == "precomputed"
    assert record.provenance.mapping_stage == "pre-mapping"
    assert record.provenance.input_sha256 == SHA

    compatibility = validate_emergency_grouper_compatibility(
        "aecc",
        "2026",
        "v1.1",
        stream="emergency_department",
    )
    assert compatibility.compatible is True
    assert compatibility.compatibility_state == "valid"


def test_external_reference_outputs_validate_local_only_reference_scope() -> None:
    reference = _reference()

    compatibility = ensure_emergency_grouper_compatibility(
        "aecc",
        "2026",
        None,
        stream="emergency_department",
        source_mode="external-reference",
        reference=reference,
    )
    assert compatibility.compatible is True
    assert compatibility.reference_id == "local_aecc_service"
    assert compatibility.declared_version == "v1.1"

    record = build_emergency_output_record_from_reference(
        "AECC-99",
        system="aecc",
        year="2026",
        stream="emergency_department",
        reference=reference,
        input_sha256=SHA,
        tool_id="local-aecc-service",
        tool_version="1.0",
        mapping_bundle_id="emergency_code_mapping_aecc_2026",
        mapping_bundle_version="v1.1",
    )
    assert record.provenance.source_mode == "external-reference"
    assert record.provenance.external_reference_id == "local_aecc_service"
    assert record.provenance.tool_id == "local-aecc-service"
    assert record.provenance.mapping_stage == "post-mapping"


def test_invalid_year_reference_and_remote_service_fail_closed() -> None:
    reference = _reference()

    result = validate_emergency_grouper_compatibility(
        "aecc",
        "2025",
        None,
        stream="emergency_department",
        source_mode="external-reference",
        reference=reference,
    )
    assert result.compatible is False
    assert "does not support" in (result.reason or "")

    with pytest.raises(EmergencyGrouperError, match="local host"):
        build_emergency_external_reference(
            reference_id="remote_service",
            reference_type="local_service",
            status="resolved",
            reference_uri="https://example.com/aecc",
            supported_versions=reference.supported_versions,
        )

    with pytest.raises(EmergencyGrouperError, match="requires a local reference"):
        ensure_emergency_grouper_compatibility(
            "aecc",
            "2026",
            None,
            stream="emergency_department",
            source_mode="external-reference",
            reference=None,
        )


def test_trusted_precomputed_mode_is_explicit_and_noop_only() -> None:
    result = validate_emergency_grouper_compatibility(
        "aecc",
        "2026",
        None,
        stream="emergency_department",
        trust_precomputed=True,
    )
    assert result.compatible is True
    assert result.validation_mode == "trusted-precomputed"
    assert result.compatibility_state == "trusted-precomputed"
    assert result.reason is None


def test_public_exports_include_emergency_grouper_surface() -> None:
    expected = {
        "EMERGENCY_GROUPER_COMPATIBILITY_STATES",
        "EMERGENCY_GROUPER_MAPPING_STAGES",
        "EMERGENCY_GROUPER_REFERENCE_TYPES",
        "EMERGENCY_GROUPER_SOURCE_MODES",
        "EMERGENCY_GROUPER_VERSION_MATRIX",
        "EmergencyGrouperCompatibilityResult",
        "EmergencyGrouperError",
        "EmergencyGrouperOutputRecord",
        "EmergencyGrouperProvenance",
        "EmergencyGrouperReference",
        "EmergencyGrouperVersionWindow",
        "build_emergency_external_reference",
        "build_emergency_output_record_from_reference",
        "build_emergency_precomputed_output_record",
        "build_emergency_provenance",
        "emergency_grouper",
        "ensure_emergency_grouper_compatibility",
        "validate_emergency_grouper_compatibility",
    }
    assert expected.issubset(set(nwau_py.__all__))
    module_exports = set(emergency_grouper.__all__) | {"emergency_grouper"}
    assert expected.issubset(module_exports)

    for name in expected:
        assert getattr(nwau_py, name) is not None


def test_emergency_grouper_reference_and_window_validation_edges() -> None:
    window = EmergencyGrouperVersionWindow(
        system="AECC",
        pricing_year="2026",
        emergency_classification_version="v1.1",
        stream_compatibility=("emergency_department",),
        source_refs=("contracts/emergency-grouper-integration/spec.md",),
    )
    assert window.to_dict()["system"] == "aecc"

    with pytest.raises(EmergencyGrouperError, match="lowercase snake_case"):
        build_emergency_external_reference(
            reference_id="BadReference",
            reference_type="local_command",
            command="run-aecc",
            supported_versions=(window,),
        )
    with pytest.raises(EmergencyGrouperError, match="require a command"):
        build_emergency_external_reference(
            reference_id="missing_command",
            reference_type="local_command",
            supported_versions=(window,),
        )
    with pytest.raises(EmergencyGrouperError, match="require a reference_uri"):
        build_emergency_external_reference(
            reference_id="missing_uri",
            reference_type="local_service",
            supported_versions=(window,),
        )
    with pytest.raises(EmergencyGrouperError, match="local_path_hint or reference_uri"):
        build_emergency_external_reference(
            reference_id="missing_file",
            reference_type="file_exchange",
            supported_versions=(window,),
        )
    with pytest.raises(EmergencyGrouperError, match="local host"):
        build_emergency_external_reference(
            reference_id="remote_http",
            reference_type="local_service",
            reference_uri="https://example.invalid/aecc",
            supported_versions=(window,),
        )
    with pytest.raises(EmergencyGrouperError, match="duplicate system/year"):
        build_emergency_external_reference(
            reference_id="duplicate_window",
            reference_type="local_command",
            command="run-aecc",
            supported_versions=(window, window),
        )


def test_emergency_grouper_external_reference_fail_closed_edges() -> None:
    unresolved = build_emergency_external_reference(
        reference_id="unresolved_aecc_service",
        reference_type="local_service",
        status="unresolved",
        reference_uri="http://127.0.0.1:8765/aecc",
        supported_versions=_reference().supported_versions,
    )
    stream_limited = build_emergency_external_reference(
        reference_id="stream_limited_aecc_service",
        reference_type="local_service",
        status="resolved",
        reference_uri="file://localhost/tmp/aecc",
        supported_versions=(
            {
                "system": "aecc",
                "pricing_year": "2026",
                "emergency_classification_version": "v1.1",
                "stream_compatibility": ("emergency_department",),
                "source_refs": ("contracts/emergency-grouper-integration/spec.md",),
            },
        ),
    )

    unresolved_result = validate_emergency_grouper_compatibility(
        "aecc",
        "2026",
        None,
        stream="emergency_department",
        source_mode="external-reference",
        reference=unresolved,
    )
    stream_result = validate_emergency_grouper_compatibility(
        "aecc",
        "2026",
        None,
        stream="emergency_service",
        source_mode="external-reference",
        reference=stream_limited,
    )
    version_result = validate_emergency_grouper_compatibility(
        "aecc",
        "2026",
        "v1.0",
        stream="emergency_department",
        source_mode="external-reference",
        reference=stream_limited,
    )
    invalid_stream = validate_emergency_grouper_compatibility(
        "aecc",
        "2026",
        "v1.1",
        stream="ward",
    )

    assert unresolved_result.compatible is False
    assert "not resolved" in (unresolved_result.reason or "")
    assert stream_result.compatible is False
    assert "not compatible with stream" in (stream_result.reason or "")
    assert version_result.compatible is False
    assert "explicit version must match" in (version_result.reason or "")
    assert invalid_stream.compatible is False
    assert invalid_stream.compatibility_state == "incompatible"


def test_emergency_grouper_provenance_and_output_records_fail_closed() -> None:
    with pytest.raises(EmergencyGrouperError, match="sha256"):
        build_emergency_provenance(
            system="aecc",
            year="2026",
            stream="emergency_department",
            emergency_classification_version="v1.1",
            input_sha256="not-a-sha",
        )
    with pytest.raises(EmergencyGrouperError, match="tool_id, tool_version"):
        build_emergency_provenance(
            system="aecc",
            year="2026",
            stream="emergency_department",
            emergency_classification_version="v1.1",
            input_sha256=SHA,
            source_mode="external-reference",
        )
    with pytest.raises(EmergencyGrouperError, match="must not declare"):
        build_emergency_provenance(
            system="aecc",
            year="2026",
            stream="emergency_department",
            emergency_classification_version="v1.1",
            input_sha256=SHA,
            external_reference_id="local_aecc_service",
        )
    with pytest.raises(EmergencyGrouperError, match="table_version"):
        build_emergency_provenance(
            system="aecc",
            year="2026",
            stream="emergency_department",
            emergency_classification_version="v1.1",
            input_sha256=SHA,
            table_version="v1.0",
        )
    with pytest.raises(EmergencyGrouperError, match="mapping_stage"):
        build_emergency_provenance(
            system="aecc",
            year="2026",
            stream="emergency_department",
            emergency_classification_version="v1.1",
            input_sha256=SHA,
            mapping_stage="converted",  # type: ignore[arg-type]
        )
    with pytest.raises(EmergencyGrouperError, match="provenance"):
        EmergencyGrouperOutputRecord(
            classification_code="AECC-01",
            provenance=object(),  # type: ignore[arg-type]
        )


def test_emergency_grouper_private_normalizers_fail_closed() -> None:
    with pytest.raises(EmergencyGrouperError, match="field must be a string"):
        emergency_grouper._normalize_non_blank(1, field="field")
    with pytest.raises(EmergencyGrouperError, match="must not be blank"):
        emergency_grouper._normalize_non_blank("", field="field")
    with pytest.raises(EmergencyGrouperError, match="leading or trailing"):
        emergency_grouper._normalize_non_blank(" value ", field="field")
    with pytest.raises(EmergencyGrouperError, match="supported four-digit"):
        emergency_grouper._normalize_year("2027")
    with pytest.raises(EmergencyGrouperError, match="deterministic version"):
        emergency_grouper._normalize_version("v1!", field="version")
    with pytest.raises(EmergencyGrouperError, match="tuple or list"):
        emergency_grouper._normalize_str_tuple("abc", field="items")
    with pytest.raises(EmergencyGrouperError, match="duplicates"):
        emergency_grouper._normalize_str_tuple(("a", "a"), field="items")
    with pytest.raises(EmergencyGrouperError, match="must not be empty"):
        emergency_grouper._normalize_str_tuple((), field="items")
    with pytest.raises(EmergencyGrouperError, match="unsupported streams"):
        emergency_grouper._normalize_streams(("ward",))
    with pytest.raises(EmergencyGrouperError, match="one of"):
        emergency_grouper._normalize_local_reference_uri(
            "ftp://localhost/aecc",
            field="reference_uri",
        )
    with pytest.raises(EmergencyGrouperError, match="parent traversal"):
        emergency_grouper._normalize_local_reference_uri(
            "../aecc",
            field="reference_uri",
        )

    checksum = emergency_grouper._compute_checksum({"b": 2, "a": 1})
    assert len(checksum) == 64
