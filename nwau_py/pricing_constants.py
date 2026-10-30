from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
from typing import Final

__all__ = [
    "NEC26",
    "NEC26_SOURCE",
    "NEC_BY_YEAR",
    "NEP26",
    "NEP26_SOURCE",
    "NEP_BY_YEAR",
    "PRICING_CONSTANTS_SCHEMA_VERSION",
    "NecPricing",
    "PricingConstantSource",
    "get_nec",
    "get_nep",
    "get_supported_pricing_years",
]

PRICING_CONSTANTS_SCHEMA_VERSION: Final[str] = "1.0"


@dataclass(frozen=True, slots=True)
class PricingConstantSource:
    """Conservative source metadata for a published IHACPA pricing constant."""

    resource_url: str
    artifact_url: str
    published_on: date
    last_updated_on: date | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class NecPricing:
    """Fixed-plus-variable NEC headline values for a pricing year."""

    fixed_cost_dollars: int
    variable_cost_per_nwau: int
    in_scope_hospitals: int
    source: PricingConstantSource


def _load_nep_values() -> dict[str, int]:
    payload = json.loads(
        files("nwau_py").joinpath("data/pricing_constants.json").read_text()
    )
    values: dict[str, int] = {}
    for year, record in payload.items():
        value = record["value"]
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"Invalid packaged NEP for {year}")
        values[str(year)] = value
    return values


NEP_BY_YEAR: Final[dict[str, int]] = _load_nep_values()
NEP26: Final[int] = NEP_BY_YEAR["2026"]
NEP26_SOURCE: Final[PricingConstantSource] = PricingConstantSource(
    resource_url="https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27",
    artifact_url="https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_price_determination_2026-27_2.pdf",
    published_on=date(2026, 3, 11),
    last_updated_on=date(2026, 3, 16),
    notes=(
        "NEP26 is set at $7,418 per NWAU(26).",
        "The resource page also links the official PDF and price-weight tables.",
    ),
)

NEC26_SOURCE: Final[PricingConstantSource] = PricingConstantSource(
    resource_url="https://www.ihacpa.gov.au/resources/national-efficient-cost-determination-2026-27",
    artifact_url="https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_cost_determination_2026-27.pdf",
    published_on=date(2026, 3, 11),
    last_updated_on=date(2026, 3, 13),
    notes=(
        "Headline NEC26 values are published as a fixed-plus-variable model.",
        "Fixed cost: $3.127m. Variable cost: $8,003.",
    ),
)

NEC26: Final[NecPricing] = NecPricing(
    fixed_cost_dollars=3_127_000,
    variable_cost_per_nwau=8_003,
    in_scope_hospitals=364,
    source=NEC26_SOURCE,
)

# NEC (National Efficient Cost) by pricing year.
NEC_BY_YEAR: Final[dict[str, NecPricing | None]] = {
    "2025": None,
    "2026": NEC26,
}


def get_nep(year: str) -> int | None:
    """Return the NEP price per NWAU for a pricing year, if available."""
    return NEP_BY_YEAR.get(year)


def get_nec(year: str) -> NecPricing | None:
    """Return the NEC headline components for a pricing year, if available."""
    return NEC_BY_YEAR.get(year)


def get_supported_pricing_years() -> list[str]:
    """Return supported pricing years in ascending order."""
    return sorted(NEP_BY_YEAR)
