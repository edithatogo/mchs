"""Registry for national, state, local, and discounted HWAU/NWAU price schedules."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Final

from .pricing_constants import get_nep, get_supported_pricing_years

__all__ = [
    "PriceDiscountRule",
    "PriceRegistry",
    "PriceRegistryError",
    "PriceScheduleRecord",
    "PriceScheduleType",
    "PriceSourceStatus",
    "get_discounted_price",
    "get_local_price",
    "get_national_price",
    "get_state_price",
    "list_available_jurisdictions",
    "list_available_years",
]


class PriceRegistryError(ValueError):
    """Raised when a price-schedule lookup is invalid, unavailable, or not licensed."""


class PriceScheduleType(Enum):
    """Categorisation of a price schedule's jurisdictional scope."""

    NATIONAL = "national"
    STATE = "state"
    LOCAL = "local"
    DISCOUNTED = "discounted"


class PriceSourceStatus(Enum):
    """Licensing and redistribution status of a price schedule source."""

    PUBLIC = "public"
    LOCAL_ONLY = "local_only"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class PriceDiscountRule:
    """A discount or override rule applied to a base price schedule."""

    rule_type: str
    value: float
    description: str

    def to_dict(self) -> dict[str, object]:
        return {
            "rule_type": self.rule_type,
            "value": self.value,
            "description": self.description,
        }


@dataclass(frozen=True, slots=True)
class PriceScheduleRecord:
    """Immutable record of a single price-schedule observation."""

    jurisdiction: str
    year: str
    price_per_hwau: int | float | None
    currency: str
    effective_period: tuple[str, str]
    source_url: str
    retrieval_date: date
    checksum: str
    licence: str
    schedule_type: PriceScheduleType
    discount_rule: PriceDiscountRule | None = None
    support_status: PriceSourceStatus = PriceSourceStatus.UNKNOWN
    provenance_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "jurisdiction": self.jurisdiction,
            "year": self.year,
            "price_per_hwau": self.price_per_hwau,
            "currency": self.currency,
            "effective_period": {
                "start": self.effective_period[0],
                "end": self.effective_period[1],
            },
            "source_url": self.source_url,
            "retrieval_date": self.retrieval_date.isoformat(),
            "checksum": self.checksum,
            "licence": self.licence,
            "schedule_type": self.schedule_type.value,
            "support_status": self.support_status.value,
            "provenance_notes": list(self.provenance_notes),
        }
        if self.discount_rule is not None:
            result["discount_rule"] = self.discount_rule.to_dict()
        return result


# ---------------------------------------------------------------------------
# Synthetic (fictitious) state price schedules for demonstration
# ---------------------------------------------------------------------------

_NSW_PRICES: Final[dict[str, int]] = {
    "2025": 7_300,
    "2026": 7_250,
}

_VIC_PRICES: Final[dict[str, int]] = {
    "2025": 7_600,
    "2026": 7_550,
}

_QLD_PRICES: Final[dict[str, int]] = {
    "2025": 7_200,
    "2026": 7_150,
}

_STATE_PRICES: Final[dict[str, dict[str, int]]] = {
    "NSW": _NSW_PRICES,
    "VIC": _VIC_PRICES,
    "QLD": _QLD_PRICES,
}

# ---------------------------------------------------------------------------
# Synthetic (fictitious) local / discounted price schedules
# ---------------------------------------------------------------------------

_LOCAL_PRICES: Final[dict[str, dict[str, int]]] = {
    "Sydney_LHN": {"2025": 7_100, "2026": 7_050},
    "Melbourne_LHN": {"2025": 7_500, "2026": 7_450},
    "Brisbane_LHN": {"2025": 7_100, "2026": 7_000},
}

_DISCOUNTED_RULES: Final[dict[str, tuple[str, dict[str, object]]]] = {
    "NSW_rural_multiplier": (
        "multiplier",
        {"value": 1.15, "description": "Rural loading multiplier"},
    ),
    "VIC_fixed_discount": (
        "fixed_price",
        {"value": 6_800, "description": "Fixed discounted price for regional VIC"},
    ),
    "QLD_percentage_discount": (
        "percentage_discount",
        {"value": 0.95, "description": "5% discount for high-volume providers"},
    ),
}

