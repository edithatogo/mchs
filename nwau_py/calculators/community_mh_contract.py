"""Community mental health contract boundary helpers.

This module keeps the community mental health stream separate from the admitted
mental health calculator path. It only describes the input/output contract
surface used by adapters and orchestration layers:

- the calculator identifier for community mental health,
- the required input columns for the stream, and
- the year-specific output column naming convention.
"""

from __future__ import annotations

from typing import Any, Final

from nwau_py.classification_validation import (
    ClassificationValidationError,
    get_classification_version,
    validate_amhcc_input,
)
from nwau_py.contracts import (
    CalculatorContract,
    ContractValidationError,
    PricingYear,
    validate_required_input_columns,
    validate_required_output_columns,
)

__all__ = [
    "COMMUNITY_MH_CALCULATOR_ID",
    "COMMUNITY_MH_CONTRACT",
    "COMMUNITY_MH_DEFAULT_YEAR",
    "COMMUNITY_MH_INPUT_COLUMNS",
    "COMMUNITY_MH_OUTPUT_COLUMNS",
    "CommunityMHContractError",
    "build_community_mh_contract",
    "community_mh_output_columns",
    "community_mh_supported_year_contracts",
    "validate_community_mh_input",
    "validate_community_mh_output",
]

COMMUNITY_MH_CALCULATOR_ID: Final[str] = "community_mh"
COMMUNITY_MH_DEFAULT_YEAR: Final[str] = "2025"

COMMUNITY_MH_INPUT_COLUMNS: Final[tuple[str, ...]] = (
    "AMHCC",
    "SC_PAT_PUB",
    "SC_NOPAT_PUB",
    "STATE",
)


class CommunityMHContractError(ContractValidationError):
    """Raised when a community mental health contract constraint is violated."""


def community_mh_output_columns(year: str) -> tuple[str, ...]:
    """Return the required output columns for a community MH pricing year."""
    pricing_year = PricingYear(year=year)
    return (f"NWAU{pricing_year.suffix}",)


COMMUNITY_MH_OUTPUT_COLUMNS: Final[tuple[str, ...]] = community_mh_output_columns(
    COMMUNITY_MH_DEFAULT_YEAR
)


def build_community_mh_contract(year: str) -> CalculatorContract:
    """Build a contract for the community mental health stream.

    Parameters
    ----------
    year:
        Four-digit pricing year (for example, ``"2025"``).

    Returns
    -------
    CalculatorContract
        A frozen Pydantic model describing the community mental health
        calculator boundary.
    """
    pricing_year = PricingYear(year=year)
    return CalculatorContract(
        calculator_id=COMMUNITY_MH_CALCULATOR_ID,
        pricing_year=pricing_year,
        required_input_columns=COMMUNITY_MH_INPUT_COLUMNS,
        required_output_columns=community_mh_output_columns(pricing_year.year),
    )


COMMUNITY_MH_CONTRACT: Final[CalculatorContract] = build_community_mh_contract(
    COMMUNITY_MH_DEFAULT_YEAR
)


def community_mh_supported_year_contracts(
    years: tuple[str, ...] = ("2021", "2022", "2023", "2024", "2025"),
) -> dict[str, CalculatorContract]:
    """Return year-keyed community mental health contracts."""
    return {year: build_community_mh_contract(year) for year in years}


def _contract_for_year(year: str | None) -> CalculatorContract:
    if year is None:
        return COMMUNITY_MH_CONTRACT
    return build_community_mh_contract(year)


def _dataframe_columns(df: Any) -> tuple[str, ...]:
    return tuple(str(column) for column in df.columns)


def validate_community_mh_input(df: Any, *, year: str | None = None) -> None:
    """Validate input columns for the community mental health stream.

    Parameters
    ----------
    df:
        Input DataFrame to validate.
    year:
        Optional pricing year used to select the contract. When omitted, the
        current active default year is used.

    Raises
    ------
    CommunityMHContractError
        If required input columns are missing.
    """
    contract = _contract_for_year(year)
    try:
        validate_required_input_columns(
            _dataframe_columns(df),
            contract.required_input_columns,
        )
        validate_amhcc_input(
            tuple(df.columns),
            year=contract.pricing_year.year,
            version=get_classification_version("amhcc", contract.pricing_year.year),
        )
    except ClassificationValidationError as exc:
        raise CommunityMHContractError(str(exc)) from exc
    except ValueError as exc:
        raise CommunityMHContractError(str(exc)) from exc


def validate_community_mh_output(df: Any, *, year: str | None = None) -> None:
    """Validate output columns from the community mental health stream.

    Parameters
    ----------
    df:
        Output DataFrame to validate.
    year:
        Optional pricing year used to select the required NWAU output column.
        When omitted, the current active default year is used.

    Raises
    ------
    CommunityMHContractError
        If the NWAU output column is missing.
    """
    contract = _contract_for_year(year)
    try:
        validate_required_output_columns(
            _dataframe_columns(df),
            contract.required_output_columns,
        )
    except ValueError as exc:
        raise CommunityMHContractError(str(exc)) from exc
