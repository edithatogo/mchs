from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

import nwau_py
from nwau_py import emergency_classification_parity_fixtures as parity
from nwau_py.emergency_classification_parity_fixtures import (
    EmergencyClassificationParityFixtureError,
    build_emergency_classification_parity_fixture_reference,
    ensure_emergency_classification_parity_fixture_scope,
    get_emergency_classification_parity_fixture_record,
    list_emergency_classification_parity_fixture_records,
    register_emergency_local_official_classification_parity_fixture_reference,
    register_emergency_synthetic_classification_parity_fixture,
    validate_emergency_classification_parity_fixture_scope,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = (
    ROOT / "conductor" / "tracks" / "emergency_classification_parity_fixtures_20260512"
)
CONTRACT = ROOT / "contracts" / "emergency-classification-parity-fixtures"


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def test_track_and_contract_define_parity_fixture_boundary() -> None:
    metadata = _read_json(TRACK / "metadata.json")
    contract = _read_json(
        CONTRACT / "emergency-classification-parity-fixtures.contract.json"
    )
    spec = (TRACK / "spec.md").read_text(encoding="utf-8")

    assert metadata["track_id"] == "emergency_classification_parity_fixtures_20260512"
    assert metadata["current_state"] in {
        "roadmap-only",
        "implemented-metadata-fixtures",
    }
    primary_contract = metadata["primary_contract"]
    assert isinstance(primary_contract, str)
    assert "nwau_py.emergency_classification_parity_fixtures" in primary_contract
    assert _as_mapping(contract["tool"])["name"] == (
        "nwau_py.emergency_classification_parity_fixtures"
    )
    assert _as_mapping(contract["privacy"])["contains_phi"] is False
    assert "synthetic fixtures" in spec
    assert "local official fixtures" in spec.lower()
    assert "cross-version fixture reuse" in spec


def test_registered_fixtures_cover_synthetic_and_local_official() -> None:
    records = list_emergency_classification_parity_fixture_records()
    assert [record.fixture_id for record in records] == [
        "emergency_classification_parity_synthetic_2025_udg",
        "emergency_classification_parity_local_official_2025_udg",
        "emergency_classification_parity_synthetic_2026_aecc",
        "emergency_classification_parity_local_official_2026_aecc",
    ]

    synthetic = list_emergency_classification_parity_fixture_records(
        fixture_type="synthetic"
    )
    official = list_emergency_classification_parity_fixture_records(
        fixture_type="local_official"
    )
    assert len(synthetic) == 2
    assert len(official) == 2

    udg = get_emergency_classification_parity_fixture_record(
        "emergency_classification_parity_synthetic_2025_udg"
    )
    aecc = get_emergency_classification_parity_fixture_record(
        "emergency_classification_parity_synthetic_2026_aecc"
    )
    assert udg is not None
    assert aecc is not None
    assert udg.classifier_system == "udg"
    assert udg.nwau_edition == "NWAU25"
    assert aecc.classifier_system == "aecc"
    assert aecc.nwau_edition == "NWAU26"
    assert parity.EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_VERSION_MATRIX == {
        "aecc": {"2026": "v1.1"},
        "udg": {"2025": "UDG_v1.3"},
    }


def test_fixture_scope_validates_registry_mapping_and_grouper() -> None:
    for record in list_emergency_classification_parity_fixture_records():
        result = validate_emergency_classification_parity_fixture_scope(record)
        assert result.compatible is True
        assert result.reason is None
        assert result.expected_versions["classifier_version"] == (
            record.classifier_version
        )
        assert result.expected_versions["mapping_table_version"] == (
            record.mapping_table_version
        )
        assert result.expected_outputs["expected_classification"] == (
            record.expected_classification
        )
        ensure_emergency_classification_parity_fixture_scope(record)


def test_registration_helpers_preserve_synthetic_and_local_boundaries() -> None:
    synthetic = register_emergency_synthetic_classification_parity_fixture(
        fixture_id="custom_synthetic_2026_aecc",
        classifier_family="AECC",
        classifier_version="v1.1",
        mapping_table_version="v1.1",
        pricing_year="2026",
        stream="emergency_department",
        raw_source_fields=("COMPENSABLE_STATUS", "DVA_STATUS"),
        expected_classification="AECC",
        expected_nwau_outputs=("Error_Code", "GWAU26", "NWAU26"),
        source_refs=(
            "conductor/tracks/emergency_classification_parity_fixtures_20260512/"
            "spec.md",
        ),
        local_path_hint="tests/fixtures/derived/emergency_classification_parity/custom.json",
        notes=("synthetic",),
    )
    assert synthetic.fixture_type == "synthetic"
    assert synthetic.assertion_mode == "precomputed"

    local = register_emergency_local_official_classification_parity_fixture_reference(
        fixture_id="custom_local_official_2026_aecc",
        classifier_family="AECC",
        classifier_version="v1.1",
        mapping_table_version="v1.1",
        pricing_year="2026",
        stream="emergency_department",
        raw_source_fields=("COMPENSABLE_STATUS", "DVA_STATUS"),
        expected_classification="AECC",
        expected_nwau_outputs=("Error_Code", "GWAU26", "NWAU26"),
        source_refs=("archive/ihacpa/raw/2026/emergency/aecc/parity/manifest.json",),
        local_path_hint="archive/ihacpa/raw/2026/emergency/aecc/parity/manifest.json",
        notes=("local only",),
    )
    assert local.fixture_type == "local_official"
    assert local.assertion_mode == "derived"


def test_cross_year_version_and_nwau_output_misuse_fail_closed() -> None:
    bad_version = build_emergency_classification_parity_fixture_reference(
        fixture_id="bad_aecc_2026_wrong_version",
        fixture_type="synthetic",
        assertion_mode="precomputed",
        classifier_family="AECC",
        classifier_version="v1.0",
        mapping_table_version="v1.0",
        pricing_year="2026",
        stream="emergency_department",
        raw_source_fields=("COMPENSABLE_STATUS", "DVA_STATUS"),
        expected_classification="AECC",
        expected_nwau_outputs=("Error_Code", "GWAU26", "NWAU26"),
        source_refs=(
            "conductor/tracks/emergency_classification_parity_fixtures_20260512/"
            "spec.md",
        ),
        local_path_hint="tests/fixtures/derived/emergency_classification_parity/bad.json",
        notes=("bad version",),
    )
    result = validate_emergency_classification_parity_fixture_scope(bad_version)
    assert result.compatible is False
    assert result.expected_versions["classifier_version"] == "v1.1"

    with pytest.raises(
        EmergencyClassificationParityFixtureError,
        match="expected_nwau_outputs must include",
    ):
        build_emergency_classification_parity_fixture_reference(
            fixture_id="bad_aecc_2026_outputs",
            fixture_type="synthetic",
            assertion_mode="precomputed",
            classifier_family="AECC",
            classifier_version="v1.1",
            mapping_table_version="v1.1",
            pricing_year="2026",
            stream="emergency_department",
            raw_source_fields=("COMPENSABLE_STATUS", "DVA_STATUS"),
            expected_classification="AECC",
            expected_nwau_outputs=("Error_Code", "GWAU25", "NWAU25"),
            source_refs=(
                "conductor/tracks/emergency_classification_parity_fixtures_20260512/spec.md",
            ),
            local_path_hint=(
                "tests/fixtures/derived/emergency_classification_parity/bad.json"
            ),
            notes=("bad outputs",),
        )


def test_public_exports_include_parity_fixture_surface() -> None:
    expected = {
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ASSERTION_MODES",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_ROWS",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_TYPES",
        "EMERGENCY_CLASSIFICATION_PARITY_FIXTURE_VERSION_MATRIX",
        "EmergencyClassificationParityFixtureCompatibilityResult",
        "EmergencyClassificationParityFixtureError",
        "EmergencyClassificationParityFixtureRecord",
        "build_emergency_classification_parity_fixture_reference",
        "emergency_classification_parity_fixtures",
        "ensure_emergency_classification_parity_fixture_scope",
        "get_emergency_classification_parity_fixture_record",
        "list_emergency_classification_parity_fixture_records",
        "register_emergency_local_official_classification_parity_fixture_reference",
        "register_emergency_synthetic_classification_parity_fixture",
        "validate_emergency_classification_parity_fixture_scope",
    }
    assert expected.issubset(set(nwau_py.__all__))
    module_exports = set(parity.__all__) | {"emergency_classification_parity_fixtures"}
    assert expected.issubset(module_exports)
    for name in expected:
        assert getattr(nwau_py, name) is not None
