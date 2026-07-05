from __future__ import annotations

import pytest

from nwau_py import nsw_funding_model


def test_nsw_registry_exposes_public_sourced_years_and_provenance() -> None:
    registry = nsw_funding_model.NSWFundingModelRegistry.default()

    assert registry.list_available_years() == ["2025", "2026"]

    record_2025 = registry.require_record("2025")
    record_2026 = registry.require_record("2026")

    assert record_2025.state_price_per_hwau == 5675
    assert record_2025.source_term == "NWAU24"
    assert record_2025.support_status is nsw_funding_model.NSWFundingModelStatus.PUBLIC
    assert "State Efficient Price" in record_2025.provenance_notes[0]
    assert record_2026.state_price_per_hwau == 6081
    assert record_2026.source_term == "NWAU25"
    assert record_2026.support_status is nsw_funding_model.NSWFundingModelStatus.PUBLIC
    assert record_2026.checksum


def test_nsw_registry_fails_closed_for_missing_years() -> None:
    registry = nsw_funding_model.NSWFundingModelRegistry.default()

    with pytest.raises(nsw_funding_model.NSWFundingModelError, match="No NSW funding"):
        registry.require_record("2024")

    blocked = registry.get_record("2024")
    assert blocked is None
    with pytest.raises(nsw_funding_model.NSWFundingModelError, match="No NSW funding"):
        registry.require_state_price("2024")


def test_nsw_parallel_valuation_uses_nsw_and_national_prices() -> None:
    valuation = nsw_funding_model.apply_parallel_nsw_valuation(
        100.0,
        financial_year="2026",
    )

    assert valuation["nwau_units"] == 100.0
    assert valuation["nsw_state_price_per_hwau"] == 6081
    assert valuation["nsw_funding"] == 608100.0
    assert valuation["national_price_per_hwau"] == 7418
    assert valuation["national_funding"] == 741800.0
    assert valuation["state_source_term"] == "NWAU25"
    assert valuation["state_source_status"] == "public"


def test_nsw_registry_serializes_scope_and_notes() -> None:
    record = nsw_funding_model.get_nsw_state_price("2025")
    payload = record.to_dict()

    assert payload["state_price_per_hwau"] == 5675
    assert payload["district_network_scope"] == [
        "Local Health District",
        "Specialty Health Network",
    ]
    assert payload["support_status"] == "public"
    assert "DNR" in record.provenance_notes[0]
    assert "LHD/SHN" in record.adjustment_notes
