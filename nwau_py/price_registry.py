"""Registry for national, state, local, and discounted HWAU/NWAU price schedules."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Final, TypedDict

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


class _DiscountRulePayload(TypedDict):
    value: float
    description: str


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

_DISCOUNTED_RULES: Final[dict[str, tuple[str, _DiscountRulePayload]]] = {
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

_SYNTHETIC_RETRIEVAL_DATE: Final[date] = date(2026, 6, 12)
_SYNTHETIC_LICENCE: Final[str] = "synthetic-test-fixture"
_SOURCE_ROOT: Final[str] = "https://example.test/prices"


def _normalise_year(year: str | int) -> str:
    value = str(year)
    if value not in get_supported_pricing_years():
        raise PriceRegistryError(f"unsupported pricing year: {value}")
    return value


def _normalise_jurisdiction(jurisdiction: str) -> str:
    return jurisdiction.strip()


def _effective_period_for_year(year: str) -> tuple[str, str]:
    start = int(year) - 1
    return (f"{start}-07-01", f"{year}-06-30")


def _checksum(*parts: object) -> str:
    payload = "|".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _record(
    *,
    jurisdiction: str,
    year: str,
    price_per_hwau: int | float | None,
    schedule_type: PriceScheduleType,
    support_status: PriceSourceStatus,
    discount_rule: PriceDiscountRule | None = None,
    source_url: str | None = None,
    licence: str = _SYNTHETIC_LICENCE,
    provenance_notes: tuple[str, ...] = (),
) -> PriceScheduleRecord:
    source = source_url or f"{_SOURCE_ROOT}/{jurisdiction.lower()}-{year}"
    return PriceScheduleRecord(
        jurisdiction=jurisdiction,
        year=year,
        price_per_hwau=price_per_hwau,
        currency="AUD",
        effective_period=_effective_period_for_year(year),
        source_url=source,
        retrieval_date=_SYNTHETIC_RETRIEVAL_DATE,
        checksum=_checksum(
            jurisdiction,
            year,
            price_per_hwau,
            schedule_type.value,
            discount_rule.to_dict() if discount_rule else "",
        ),
        licence=licence,
        schedule_type=schedule_type,
        discount_rule=discount_rule,
        support_status=support_status,
        provenance_notes=provenance_notes,
    )


def _state_price(jurisdiction: str, year: str) -> int:
    prices = _STATE_PRICES.get(jurisdiction)
    if prices is None:
        raise PriceRegistryError(f"unknown state price jurisdiction: {jurisdiction}")
    try:
        return prices[year]
    except KeyError as exc:
        raise PriceRegistryError(
            f"state price unavailable for {jurisdiction} in {year}"
        ) from exc


def _local_price(jurisdiction: str, year: str) -> int:
    prices = _LOCAL_PRICES.get(jurisdiction)
    if prices is None:
        raise PriceRegistryError(f"unknown local price jurisdiction: {jurisdiction}")
    try:
        return prices[year]
    except KeyError as exc:
        raise PriceRegistryError(
            f"local price unavailable for {jurisdiction} in {year}"
        ) from exc


def list_available_years() -> list[str]:
    """Return pricing years with a national price in this package."""
    return get_supported_pricing_years()


def list_available_jurisdictions(
    schedule_type: PriceScheduleType | str | None = None,
) -> list[str]:
    """Return available jurisdictions for state, local, or discounted schedules."""
    if isinstance(schedule_type, str):
        schedule_type = PriceScheduleType(schedule_type)
    if schedule_type is PriceScheduleType.STATE:
        return sorted(_STATE_PRICES)
    if schedule_type is PriceScheduleType.LOCAL:
        return sorted(_LOCAL_PRICES)
    if schedule_type is PriceScheduleType.DISCOUNTED:
        return sorted(_DISCOUNTED_RULES)
    if schedule_type is PriceScheduleType.NATIONAL:
        return ["National"]
    return sorted({"National", *_STATE_PRICES, *_LOCAL_PRICES, *_DISCOUNTED_RULES})


def get_national_price(year: str | int) -> PriceScheduleRecord:
    """Return the public national NEP price schedule for a pricing year."""
    pricing_year = _normalise_year(year)
    price = get_nep(pricing_year)
    if price is None:
        raise PriceRegistryError(f"national price unavailable for {pricing_year}")
    return _record(
        jurisdiction="National",
        year=pricing_year,
        price_per_hwau=price,
        schedule_type=PriceScheduleType.NATIONAL,
        support_status=PriceSourceStatus.PUBLIC,
        source_url=f"https://www.ihacpa.gov.au/pricing/nep-{pricing_year}",
        licence="public",
        provenance_notes=("NEP value sourced from packaged pricing constants.",),
    )


def get_state_price(jurisdiction: str, year: str | int) -> PriceScheduleRecord:
    """Return a synthetic state price schedule record."""
    pricing_year = _normalise_year(year)
    state = _normalise_jurisdiction(jurisdiction).upper()
    return _record(
        jurisdiction=state,
        year=pricing_year,
        price_per_hwau=_state_price(state, pricing_year),
        schedule_type=PriceScheduleType.STATE,
        support_status=PriceSourceStatus.LOCAL_ONLY,
        provenance_notes=(
            "Synthetic state price fixture; not an official jurisdictional schedule.",
        ),
    )


def get_local_price(jurisdiction: str, year: str | int) -> PriceScheduleRecord:
    """Return a synthetic local health network price schedule record."""
    pricing_year = _normalise_year(year)
    local = _normalise_jurisdiction(jurisdiction)
    return _record(
        jurisdiction=local,
        year=pricing_year,
        price_per_hwau=_local_price(local, pricing_year),
        schedule_type=PriceScheduleType.LOCAL,
        support_status=PriceSourceStatus.LOCAL_ONLY,
        provenance_notes=(
            "Synthetic local price fixture; no licensed payload bundled.",
        ),
    )


def get_discounted_price(rule_name: str, year: str | int) -> PriceScheduleRecord:
    """Return a synthetic discounted price schedule derived from a base state."""
    pricing_year = _normalise_year(year)
    rule_key = _normalise_jurisdiction(rule_name)
    try:
        rule_type, payload = _DISCOUNTED_RULES[rule_key]
    except KeyError as exc:
        raise PriceRegistryError(f"unknown discount rule: {rule_key}") from exc

    base_state = rule_key.split("_", maxsplit=1)[0].upper()
    base_price = _state_price(base_state, pricing_year)
    value = float(payload["value"])
    if rule_type == "multiplier":
        discounted = round(base_price * value, 2)
    elif rule_type == "fixed_price":
        discounted = value
    elif rule_type == "percentage_discount":
        discounted = round(base_price * value, 2)
    else:  # pragma: no cover - protects future rule additions.
        raise PriceRegistryError(f"unsupported discount rule type: {rule_type}")

    rule = PriceDiscountRule(
        rule_type=rule_type,
        value=value,
        description=str(payload["description"]),
    )
    return _record(
        jurisdiction=rule_key,
        year=pricing_year,
        price_per_hwau=discounted,
        schedule_type=PriceScheduleType.DISCOUNTED,
        support_status=PriceSourceStatus.LOCAL_ONLY,
        discount_rule=rule,
        provenance_notes=(
            f"Synthetic discounted schedule derived from {base_state} fixture price.",
        ),
    )


class PriceRegistry:
    """Facade for price schedule lookups with explicit source-status handling."""

    def list_years(self) -> list[str]:
        return list_available_years()

    def list_jurisdictions(
        self,
        schedule_type: PriceScheduleType | str | None = None,
    ) -> list[str]:
        return list_available_jurisdictions(schedule_type)

    def national(self, year: str | int) -> PriceScheduleRecord:
        return get_national_price(year)

    def state(self, jurisdiction: str, year: str | int) -> PriceScheduleRecord:
        return get_state_price(jurisdiction, year)

    def local(self, jurisdiction: str, year: str | int) -> PriceScheduleRecord:
        return get_local_price(jurisdiction, year)

    def discounted(self, rule_name: str, year: str | int) -> PriceScheduleRecord:
        return get_discounted_price(rule_name, year)
