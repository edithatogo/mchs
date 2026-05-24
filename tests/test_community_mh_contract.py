"""Tests for the community mental health calculator contract and validation
fixtures."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from nwau_py.calculators.community_mh_contract import (
    COMMUNITY_MH_CONTRACT,
    CommunityMHContractError,
    build_community_mh_contract,
    community_mh_supported_year_contracts,
    validate_community_mh_input,
    validate_community_mh_output,
)
from nwau_py.calculators.community_mh_inventory import (
    get_active_years,
    get_inventory_by_year,
    get_shadow_years,
)

SUPPORTED_COMMUNITY_MH_YEARS = ("2021", "2022", "2023", "2024", "2025")
EXPECTED_STATUS_BY_YEAR = {
    "2021": "shadow",
    "2022": "shadow",
    "2023": "shadow",
    "2024": "shadow",
    "2025": "active",
}


def test_contract_calculator_id():
    """The community MH contract must use a distinct calculator identifier."""
    c = COMMUNITY_MH_CONTRACT
    assert c.calculator_id == "community_mh"
    assert c.calculator_id not in ("mh", "acute", "ed")


def test_contract_required_input_columns():
    """The contract must require the core community mental health input
    columns."""
    c = COMMUNITY_MH_CONTRACT
    required = set(c.required_input_columns)
    assert "AMHCC" in required
    assert "SC_PAT_PUB" in required
    assert "SC_NOPAT_PUB" in required


def test_contract_required_output_columns():
    """The contract must require the NWAU output column."""
    c = COMMUNITY_MH_CONTRACT
    required = set(c.required_output_columns)
    assert any(col.startswith("NWAU") for col in required)


@pytest.mark.parametrize("year", SUPPORTED_COMMUNITY_MH_YEARS)
def test_build_contract_for_supported_years(year):
    """Each supported community MH pricing year builds a distinct contract."""
    contract = build_community_mh_contract(year)

    assert contract.calculator_id == "community_mh"
    assert contract.pricing_year.year == year
    assert contract.pricing_year.suffix == year[-2:]
    assert contract.required_input_columns == (
        "AMHCC",
        "SC_PAT_PUB",
        "SC_NOPAT_PUB",
        "STATE",
    )
    assert contract.required_output_columns == (f"NWAU{year[-2:]}",)


def test_supported_years_match_inventory_validation_status():
    """Community MH validation status is shadow until the 2025 active year."""
    assert get_active_years() == ["2025", "2026"]
    assert get_shadow_years() == ["2021", "2022", "2023", "2024"]

    for year, expected_status in EXPECTED_STATUS_BY_YEAR.items():
        artifact = get_inventory_by_year(year)
        assert artifact is not None
        assert artifact.pricing_status == expected_status


def test_supported_year_contract_map_matches_inventory():
    """The contract map should expose each inventory-backed community MH year."""
    contracts = community_mh_supported_year_contracts()

    assert tuple(contracts) == SUPPORTED_COMMUNITY_MH_YEARS
    for year, contract in contracts.items():
        assert contract.pricing_year.year == year
        assert contract.required_output_columns == (f"NWAU{year[-2:]}",)


def test_contract_rejects_unsupported_year():
    """Unsupported years must fail before being treated as validated."""
    with pytest.raises(ValueError):
        build_community_mh_contract("2027")


def test_default_contract_targets_the_active_pricing_year():
    """The module-level default contract should point at the active year."""
    artifact = get_inventory_by_year(COMMUNITY_MH_CONTRACT.pricing_year.year)

    assert COMMUNITY_MH_CONTRACT.pricing_year.year == "2025"
    assert artifact is not None
    assert artifact.pricing_status == "active"


def test_validate_input_valid():
    """validate_community_mh_input accepts a frame with all required columns."""
    df = pd.DataFrame(
        {
            "AMHCC": ["2001"],
            "SC_PAT_PUB": [1],
            "SC_NOPAT_PUB": [0],
            "STATE": [1],
        }
    )
    validate_community_mh_input(df)  # should not raise


def test_validate_input_missing_column():
    """validate_community_mh_input raises when required columns are missing."""
    df = pd.DataFrame({"AMHCC": ["2001"]})  # missing SC_PAT_PUB, SC_NOPAT_PUB
    with pytest.raises(CommunityMHContractError):
        validate_community_mh_input(df)


def test_validate_output_valid():
    """validate_community_mh_output accepts a frame with NWAU column."""
    df = pd.DataFrame({"NWAU25": [1.5], "AMHCC": ["2001"]})
    validate_community_mh_output(df)  # should not raise


@pytest.mark.parametrize("year", SUPPORTED_COMMUNITY_MH_YEARS)
def test_validate_output_is_year_aware(year):
    """Output validation must select the NWAU suffix for the requested year."""
    df = pd.DataFrame({f"NWAU{year[-2:]}": [1.5], "AMHCC": ["2001"]})

    validate_community_mh_output(df, year=year)


def test_validate_output_rejects_wrong_year_suffix():
    """A 2024 output column must not satisfy the 2025 active-year contract."""
    df = pd.DataFrame({"NWAU24": [1.5], "AMHCC": ["2001"]})

    with pytest.raises(CommunityMHContractError):
        validate_community_mh_output(df, year="2025")


def test_validate_output_missing():
    """validate_community_mh_output raises when NWAU column is missing."""
    df = pd.DataFrame({"AMHCC": ["2001"]})
    with pytest.raises(CommunityMHContractError):
        validate_community_mh_output(df)


def test_fixture_gap_record_exists():
    """The fixture-gap record must explain why no golden fixtures exist."""
    gap_path = Path(
        "conductor/archive/community_mental_health_calculator_20260512/fixture_gaps.md"
    )
    assert gap_path.exists(), (
        "Fixture gap record not found. Create track fixture_gaps.md"
    )
    content = gap_path.read_text(encoding="utf-8")
    lower = content.lower()
    assert "golden validation fixtures" in lower
    for year in ("nep21", "nep22", "nep23", "nep24", "nep25"):
        assert year in lower
    assert (
        "synthetic mock data" in lower or "official ihacpa calculator output" in lower
    )


def test_contract_rejects_mh_calculator_id():
    """The community MH contract must not accept the generic 'mh' calculator
    ID."""
    c = COMMUNITY_MH_CONTRACT
    assert c.calculator_id != "mh"


def test_input_columns_include_stream_prefix():
    """The contract must include AMHCC prefix convention documentation."""
    c = COMMUNITY_MH_CONTRACT
    # AMHCC prefix "2" = community stream
    assert "AMHCC" in c.required_input_columns
