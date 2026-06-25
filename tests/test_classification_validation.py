from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from nwau_py.classification_validation import (
    ClassificationValidationError,
    get_classification_version,
    get_supported_classification_years,
    get_transition_years,
    is_classification_licensed,
    validate_aecc_input,
    validate_amhcc_input,
    validate_ar_drg_input,
    validate_tier_2_input,
    validate_udg_input,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "classification_input_validation_20260512"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_track_matrix_records_streams_versions_and_license_caveats():
    matrix = _read_text(TRACK / "classification_matrix.md")

    for phrase in [
        "AR-DRG",
        "AECC",
        "UDG",
        "Tier 2",
        "AMHCC",
        "licensed / non-redistributable",
        "Do not treat them as interchangeable",
        "Version 10.0",
    ]:
        assert phrase in matrix


def test_classification_track_archive_metadata_records_scope_and_gaps():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))

    assert metadata["track_id"] == "classification_input_validation_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "nwau_py/classification_validation.py" in metadata["completion_evidence"]
    assert (TRACK / "review.md").exists()


@pytest.mark.parametrize(
    ("validator", "fields", "year", "version"),
    [
        (validate_ar_drg_input, ("DRG",), "2026", "v12.0"),
        (validate_aecc_input, ("AECC",), "2026", "v1.1"),
        (validate_udg_input, ("UDG",), "2026", "UDG_v1.3"),
        (validate_tier_2_input, ("TIER2_CLINIC",), "2026", "v10.0"),
        (validate_amhcc_input, ("AMHCC",), "2026", "v1"),
    ],
)
def test_stream_validators_accept_matching_year_versions(
    validator,
    fields,
    year,
    version,
):
    result = validator(fields, year=year, version=version)

    assert result.is_valid is True
    assert result.pricing_year == year
    assert result.declared_version == version
    assert result.required_fields == fields


def test_ar_drg_validator_reports_missing_required_field():
    with pytest.raises(ClassificationValidationError, match="DRG"):
        validate_ar_drg_input(("LOS",), year="2026", version="v12.0")


def test_ed_classification_versions_are_not_interchangeable():
    with pytest.raises(ClassificationValidationError, match=re.escape("expects v1.1")):
        validate_aecc_input(("AECC",), year="2026", version="UDG_v1.3")

    with pytest.raises(
        ClassificationValidationError,
        match=re.escape("expects UDG_v1.3"),
    ):
        validate_udg_input(("UDG",), year="2026", version="v1.1")


def test_tier_2_is_pricing_year_aware():
    assert get_classification_version("tier_2", "2025") == "v7"
    assert get_classification_version("tier_2", "2026") == "v10.0"

    with pytest.raises(
        ClassificationValidationError,
        match=re.escape("expects v10.0"),
    ):
        validate_tier_2_input(("TIER2_CLINIC",), year="2026", version="v9.1")


def test_classification_metadata_exposes_transitions_and_license_flags():
    assert is_classification_licensed("AR-DRG") is True
    assert is_classification_licensed("AECC") is False
    assert "2026" in get_transition_years("AR-DRG")
    assert "2026" in get_supported_classification_years("Tier 2")


@pytest.mark.parametrize(
    ("label", "validator", "observed_fields", "year", "version", "missing_field"),
    [
        pytest.param(
            "acute",
            validate_ar_drg_input,
            ("LOS", "ICU_HOURS"),
            "2026",
            "v12.0",
            "DRG",
            id="acute-ar-drg",
        ),
        pytest.param(
            "ed-aecc",
            validate_aecc_input,
            ("COMPENSABLE_STATUS", "DVA_STATUS"),
            "2026",
            "v1.1",
            "AECC",
            id="ed-aecc",
        ),
        pytest.param(
            "ed-udg",
            validate_udg_input,
            ("COMPENSABLE_STATUS", "DVA_STATUS"),
            "2026",
            "UDG_v1.3",
            "UDG",
            id="ed-udg",
        ),
        pytest.param(
            "outpatients-tier-2",
            validate_tier_2_input,
            ("STATE", "SERVICE_DATE"),
            "2026",
            "v10.0",
            "TIER2_CLINIC",
            id="outpatients-tier-2",
        ),
        pytest.param(
            "mh-community-mh-amhcc",
            validate_amhcc_input,
            ("STATE", "LOS"),
            "2026",
            "v1",
            "AMHCC",
            id="mh-community-mh-amhcc",
        ),
    ],
)
def test_calculator_preflight_rejects_missing_classification_fields_before_formula(
    label,
    validator,
    observed_fields,
    year,
    version,
    missing_field,
):
    formula_reached = False

    def _formula() -> None:
        nonlocal formula_reached
        formula_reached = True

    with pytest.raises(ClassificationValidationError, match=missing_field):
        validator(observed_fields, year=year, version=version)
        _formula()

    assert formula_reached is False, label


@pytest.mark.parametrize(
    ("label", "validator", "observed_fields", "year", "version", "expected_version"),
    [
        pytest.param(
            "acute",
            validate_ar_drg_input,
            ("DRG", "LOS", "ICU_HOURS"),
            "2026",
            "v11.0",
            "v12.0",
            id="acute-ar-drg",
        ),
        pytest.param(
            "ed-aecc",
            validate_aecc_input,
            ("AECC", "COMPENSABLE_STATUS", "DVA_STATUS"),
            "2026",
            "v1.0",
            "v1.1",
            id="ed-aecc",
        ),
        pytest.param(
            "ed-udg",
            validate_udg_input,
            ("UDG", "COMPENSABLE_STATUS", "DVA_STATUS"),
            "2026",
            "v1.1",
            "UDG_v1.3",
            id="ed-udg",
        ),
        pytest.param(
            "outpatients-tier-2",
            validate_tier_2_input,
            ("TIER2_CLINIC", "STATE", "SERVICE_DATE"),
            "2026",
            "v7",
            "v10.0",
            id="outpatients-tier-2",
        ),
        pytest.param(
            "mh-community-mh-amhcc",
            validate_amhcc_input,
            ("AMHCC", "STATE", "LOS"),
            "2026",
            "v2",
            "v1",
            id="mh-community-mh-amhcc",
        ),
    ],
)
def test_calculator_preflight_rejects_version_mismatches_before_formula(
    label,
    validator,
    observed_fields,
    year,
    version,
    expected_version,
):
    formula_reached = False

    def _formula() -> None:
        nonlocal formula_reached
        formula_reached = True

    with pytest.raises(
        ClassificationValidationError,
        match=re.escape(f"expects {expected_version}, got {version}"),
    ):
        validator(observed_fields, year=year, version=version)
        _formula()

    assert formula_reached is False, label
