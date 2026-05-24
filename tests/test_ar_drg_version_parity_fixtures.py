from __future__ import annotations

import pytest

from nwau_py.ar_drg_grouper import ARDRGGrouperVersionWindow
from nwau_py.ar_drg_version_parity_fixtures import (
    ARDRGParityFixtureError,
    build_ar_drg_parity_fixture_reference,
    get_ar_drg_parity_fixture_record,
    list_ar_drg_parity_fixture_records,
    register_ar_drg_local_licensed_parity_fixture_reference,
    register_ar_drg_synthetic_parity_fixture,
    validate_ar_drg_parity_fixture_scope,
)


def _window_2026() -> ARDRGGrouperVersionWindow:
    return ARDRGGrouperVersionWindow(
        pricing_year="2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )


def test_registry_exposes_safe_synthetic_and_local_only_references() -> None:
    records = list_ar_drg_parity_fixture_records()

    assert {record.pricing_year for record in records} == {"2025", "2026"}
    assert {record.fixture_kind for record in records} == {
        "synthetic",
        "local-licensed-reference",
    }
    assert all("outputs" not in record.to_dict() for record in records)


def test_registry_lookups_are_exact_and_metadata_only() -> None:
    record = get_ar_drg_parity_fixture_record("ar_drg_version_parity_synthetic_2026")

    assert record is not None
    assert record.fixture_kind == "synthetic"
    assert record.license_boundary == "metadata-only"
    assert record.restricted is False
    assert record.grouper_version is None


def test_registration_helpers_validate_version_scope_and_local_boundaries() -> None:
    synthetic = register_ar_drg_synthetic_parity_fixture(
        fixture_id="ar_drg_version_parity_synthetic_custom_2026",
        version_window=_window_2026(),
        source_refs=(
            "conductor/tracks/ar_drg_version_parity_fixtures_20260512/spec.md",
            "reference-data/2026/manifest.yaml",
        ),
        local_path_hint="tests/fixtures/derived/ar_drg_version_parity/2026/custom.json",
        notes=("synthetic parity pack",),
    )
    licensed = register_ar_drg_local_licensed_parity_fixture_reference(
        fixture_id="ar_drg_version_parity_local_custom_2026",
        version_window=_window_2026(),
        source_refs=(
            "conductor/tracks/ar_drg_version_parity_fixtures_20260512/spec.md",
            "https://www.ihacpa.gov.au/resources/ar-drg-version-120",
        ),
        local_path_hint="archive/ihacpa/raw/2026/licensed/ar_drg/parity/custom.json",
        grouper_version="v12.0-local",
        notes=("local licensed parity reference",),
    )

    synthetic_result = validate_ar_drg_parity_fixture_scope(synthetic)
    licensed_result = validate_ar_drg_parity_fixture_scope(licensed)

    assert synthetic_result.compatible is True
    assert licensed_result.compatible is True
    assert synthetic.version_scope()["grouper_version"] is None
    assert licensed.version_scope()["grouper_version"] == "v12.0-local"


def test_invalid_cross_version_scope_fails_closed() -> None:
    bad_record = build_ar_drg_parity_fixture_reference(
        fixture_id="ar_drg_version_parity_synthetic_bad_2026",
        fixture_kind="synthetic",
        workflow_mode="precomputed",
        version_window={
            "pricing_year": "2026",
            "ar_drg_version": "v11.0",
            "icd_10_am_version": "12th edition",
            "achi_version": "12th edition",
            "acs_version": "12th edition",
        },
        source_refs=("reference-data/2026/manifest.yaml",),
        local_path_hint="tests/fixtures/derived/ar_drg_version_parity/2026/bad.json",
        notes=("bad cross-version pack",),
    )

    result = validate_ar_drg_parity_fixture_scope(bad_record)

    assert result.compatible is False
    assert "expected 'v12.0'" in (result.reason or "")


def test_local_licensed_registration_requires_external_reference_mode() -> None:
    with pytest.raises(ARDRGParityFixtureError, match="external-reference"):
        build_ar_drg_parity_fixture_reference(
            fixture_id="ar_drg_version_parity_local_bad",
            fixture_kind="local-licensed-reference",
            workflow_mode="precomputed",
            version_window=_window_2026(),
            source_refs=("reference-data/2026/manifest.yaml",),
            local_path_hint="archive/ihacpa/raw/2026/licensed/ar_drg/parity/bad.json",
            grouper_version="v12.0-local",
        )
