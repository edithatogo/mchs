from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

import nwau_py
import nwau_py.calculators as calculators
from nwau_py import (
    ClassificationValidationError,
    ClassificationValidationResult,
    EmergencyClassificationCompatibilityResult,
    get_classification_requirement,
    get_classification_version,
    get_emergency_classification_status,
    get_emergency_transition_period,
    get_supported_classification_years,
    get_supported_pricing_years,
    get_transition_years,
    validate_aecc_input,
    validate_emergency_input,
    validate_udg_input,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = (
    ROOT / "conductor" / "tracks" / "emergency_udg_aecc_transition_registry_20260512"
)

AECC_FIELDS = ("AECC", "COMPENSABLE_STATUS", "DVA_STATUS")
UDG_FIELDS = ("UDG", "COMPENSABLE_STATUS", "DVA_STATUS")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def test_track_metadata_and_spec_record_the_transition_registry_contract():
    metadata = _read_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")

    assert metadata["track_id"] == "emergency_udg_aecc_transition_registry_20260512"
    assert metadata["current_state"] == "implemented-metadata-registry"
    assert metadata["description"] == (
        "Document and validate emergency classification transition registry "
        "semantics for UDG and AECC versions, pricing-year applicability, "
        "stream compatibility, source licensing caveats, and "
        "no-invented-crosswalk boundaries."
    )
    assert "Do not silently translate UDG to AECC" in spec
    assert "Preserve explicit provenance" in spec
    assert "pricing-year" in spec
    assert "stream compatibility" in spec


def test_supported_pricing_years_and_emergency_transition_boundaries():
    assert tuple(get_supported_pricing_years()) == ("2025", "2026")
    assert get_supported_classification_years("udg") == (
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025",
        "2026",
    )
    assert get_supported_classification_years("aecc") == (
        "2020",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025",
        "2026",
    )
    assert get_transition_years("udg") == ("2021",)
    assert get_transition_years("aecc") == ("2020", "2021", "2022")
    assert get_classification_version("aecc", "2020") == "v1.0_shadow"
    assert get_classification_version("aecc", "2021") == "v1.0"
    assert get_classification_version("aecc", "2026") == "v1.1"
    assert get_classification_version("udg", "2026") == "UDG_v1.3"


@pytest.mark.parametrize(
    ("validator", "observed_fields", "year", "version", "expected_message"),
    [
        (
            validate_aecc_input,
            UDG_FIELDS,
            "2026",
            "v1.1",
            "AECC 2026 is missing required fields: AECC",
        ),
        (
            validate_udg_input,
            AECC_FIELDS,
            "2026",
            "UDG_v1.3",
            "UDG 2026 is missing required fields: UDG",
        ),
        (
            validate_aecc_input,
            AECC_FIELDS,
            "2026",
            "UDG_v1.3",
            "AECC 2026 expects v1.1, got UDG_v1.3",
        ),
        (
            validate_udg_input,
            UDG_FIELDS,
            "2026",
            "v1.1",
            "UDG 2026 expects UDG_v1.3, got v1.1",
        ),
    ],
)
def test_aecc_and_udg_validation_fails_closed_on_cross_stream_interchangeability(
    validator,
    observed_fields,
    year,
    version,
    expected_message,
):
    with pytest.raises(
        ClassificationValidationError,
        match=re.escape(expected_message),
    ):
        validator(observed_fields, year=year, version=version)


def test_registry_exposes_licensed_and_provenance_adjacent_metadata():
    aecc_requirement = get_classification_requirement("aecc", "2026")
    udg_requirement = get_classification_requirement("udg", "2026")

    assert aecc_requirement.display_name == "AECC"
    assert aecc_requirement.pricing_year == "2026"
    assert aecc_requirement.expected_version == "v1.1"
    assert aecc_requirement.required_fields == ("AECC",)
    assert aecc_requirement.licensed is False

    assert udg_requirement.display_name == "UDG"
    assert udg_requirement.pricing_year == "2026"
    assert udg_requirement.expected_version == "UDG_v1.3"
    assert udg_requirement.required_fields == ("UDG",)
    assert udg_requirement.licensed is False

    validated = validate_aecc_input(AECC_FIELDS, year="2026", version="v1.1")
    assert isinstance(validated, ClassificationValidationResult)
    assert validated.is_valid is True
    assert validated.licensed is False
    assert validated.expected_version == "v1.1"
    assert validated.required_fields == ("AECC",)
    assert validated.observed_fields == AECC_FIELDS


def test_dedicated_emergency_registry_reports_transition_state_and_stream_scope():
    assert get_emergency_classification_status("aecc", "2020") == "shadow-priced"
    assert get_emergency_classification_status("aecc", "2026") == "valid"
    assert get_emergency_classification_status("udg", "2026") == "transition"

    period = get_emergency_transition_period("aecc", "2020")
    assert period is not None
    assert period.acceptance_state == "shadow-priced"

    result = validate_emergency_input(
        "aecc",
        "2020",
        AECC_FIELDS,
        version="v1.0_shadow",
        stream="emergency_department",
    )
    assert isinstance(result, EmergencyClassificationCompatibilityResult)
    assert result.compatible is True
    assert result.compatibility_state == "shadow-priced"
    assert result.stream == "emergency_department"
    assert "emergency_department" in result.stream_compatibility

    stream_failure = validate_emergency_input(
        "aecc",
        "2020",
        AECC_FIELDS,
        version="v1.0_shadow",
        stream="non_emergency_stream",
    )
    assert stream_failure.compatible is False
    assert stream_failure.compatibility_state == "incompatible"
    assert "not compatible with stream" in (stream_failure.reason or "")


def test_public_api_exports_include_the_emergency_registry_surface():
    expected_top_level_exports = {
        "ClassificationValidationError",
        "ClassificationValidationResult",
        "EmergencyClassificationCompatibilityResult",
        "get_emergency_classification_status",
        "get_emergency_transition_period",
        "get_classification_requirement",
        "get_classification_version",
        "get_supported_classification_years",
        "get_supported_pricing_years",
        "get_transition_years",
        "validate_emergency_input",
        "validate_aecc_input",
        "validate_udg_input",
    }
    expected_calculator_exports = {"EDParams", "calculate_ed"}

    assert expected_top_level_exports.issubset(set(nwau_py.__all__))
    assert expected_calculator_exports.issubset(set(calculators.__all__))

    for name in expected_top_level_exports:
        assert getattr(nwau_py, name) is not None

    for name in expected_calculator_exports:
        assert getattr(calculators, name) is not None
