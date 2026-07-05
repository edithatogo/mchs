"""Registry for national, state, local, and discounted HWAU/NWAU price schedules."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Final, cast

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

_PRICE_REGISTRY_RETRIEVAL_DATE: Final[date] = date(2026, 7, 5)


def _checksum(parts: Iterable[object]) -> str:
    payload = "|".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _period_for_year(year: str) -> tuple[str, str]:
    start_year = int(year) - 1
    end_year = int(year)
    return (f"{start_year}-07-01", f"{end_year}-06-30")


def _record(
    *,
    jurisdiction: str,
    year: str,
    price_per_hwau: int | float | None,
    source_url: str,
    licence: str,
    schedule_type: PriceScheduleType,
    support_status: PriceSourceStatus,
    discount_rule: PriceDiscountRule | None = None,
    provenance_notes: Sequence[str] = (),
) -> PriceScheduleRecord:
    return PriceScheduleRecord(
        jurisdiction=jurisdiction,
        year=year,
        price_per_hwau=price_per_hwau,
        currency="AUD",
        effective_period=_period_for_year(year),
        source_url=source_url,
        retrieval_date=_PRICE_REGISTRY_RETRIEVAL_DATE,
        checksum=_checksum(
            (
                jurisdiction,
                year,
                price_per_hwau,
                source_url,
                licence,
                schedule_type.value,
                support_status.value,
            )
        ),
        licence=licence,
        schedule_type=schedule_type,
        discount_rule=discount_rule,
        support_status=support_status,
        provenance_notes=tuple(provenance_notes),
    )


def _national_records() -> list[PriceScheduleRecord]:
    records: list[PriceScheduleRecord] = []
    for year in get_supported_pricing_years():
        price = get_nep(year)
        if price is None:
            continue
        records.append(
            _record(
                jurisdiction="National",
                year=year,
                price_per_hwau=price,
                source_url=(
                    "https://www.ihacpa.gov.au/resources/"
                    f"national-efficient-price-determination-{year}"
                ),
                licence="public",
                schedule_type=PriceScheduleType.NATIONAL,
                support_status=PriceSourceStatus.PUBLIC,
                provenance_notes=(
                    "IHACPA NEP headline value from shared pricing constants.",
                    "National source terminology is NEP per NWAU; mapped to HWAU.",
                ),
            )
        )
    return records


def _state_records() -> list[PriceScheduleRecord]:
    records: list[PriceScheduleRecord] = []
    for jurisdiction, prices_by_year in _STATE_PRICES.items():
        for year, price in prices_by_year.items():
            records.append(
                _record(
                    jurisdiction=jurisdiction,
                    year=year,
                    price_per_hwau=price,
                    source_url=f"local://synthetic/state-prices/{jurisdiction}/{year}",
                    licence="synthetic-test-fixture",
                    schedule_type=PriceScheduleType.STATE,
                    support_status=PriceSourceStatus.LOCAL_ONLY,
                    provenance_notes=(
                        "Synthetic local-only fixture; not an official sourced price.",
                        "Used to exercise state price registry behavior.",
                    ),
                )
            )
    return records


def _local_records() -> list[PriceScheduleRecord]:
    records: list[PriceScheduleRecord] = []
    for jurisdiction, prices_by_year in _LOCAL_PRICES.items():
        for year, price in prices_by_year.items():
            records.append(
                _record(
                    jurisdiction=jurisdiction,
                    year=year,
                    price_per_hwau=price,
                    source_url=f"local://synthetic/local-prices/{jurisdiction}/{year}",
                    licence="synthetic-test-fixture",
                    schedule_type=PriceScheduleType.LOCAL,
                    support_status=PriceSourceStatus.LOCAL_ONLY,
                    provenance_notes=(
                        "Synthetic local-only fixture; not an official sourced price.",
                        "Used to exercise local price registry behavior.",
                    ),
                )
            )
    return records


def _discounted_records() -> list[PriceScheduleRecord]:
    records: list[PriceScheduleRecord] = []
    for jurisdiction, (rule_type, payload) in _DISCOUNTED_RULES.items():
        base_jurisdiction = jurisdiction.split("_", 1)[0]
        for year in sorted(_STATE_PRICES.get(base_jurisdiction, {})):
            base_price = _STATE_PRICES[base_jurisdiction][year]
            value = float(cast(int | float, payload["value"]))
            if rule_type == "multiplier":
                price: int | float = round(base_price * value)
            elif rule_type == "fixed_price":
                price = int(value)
            elif rule_type == "percentage_discount":
                price = round(base_price * value)
            else:
                raise PriceRegistryError(f"Unsupported discount rule {rule_type!r}")
            rule = PriceDiscountRule(
                rule_type=rule_type,
                value=value,
                description=str(payload["description"]),
            )
            records.append(
                _record(
                    jurisdiction=jurisdiction,
                    year=year,
                    price_per_hwau=price,
                    source_url=f"local://synthetic/discount-rules/{jurisdiction}/{year}",
                    licence="synthetic-test-fixture",
                    schedule_type=PriceScheduleType.DISCOUNTED,
                    discount_rule=rule,
                    support_status=PriceSourceStatus.LOCAL_ONLY,
                    provenance_notes=(
                        "Synthetic discount fixture; not an official sourced price.",
                        f"Derived from synthetic {base_jurisdiction} state price.",
                    ),
                )
            )
    return records


def _blocked_records() -> list[PriceScheduleRecord]:
    return [
        _record(
            jurisdiction="WA_blocked_local_source",
            year="2025",
            price_per_hwau=None,
            source_url="restricted://wa/local-price-source",
            licence="restricted-local-source",
            schedule_type=PriceScheduleType.LOCAL,
            support_status=PriceSourceStatus.BLOCKED,
            provenance_notes=(
                "Placeholder for a restricted local source.",
                "No price is redistributed; consumers must supply licensed data.",
            ),
        )
    ]


class PriceRegistry:
    """Runtime registry for public and local-only price schedule records."""

    def __init__(self, records: Iterable[PriceScheduleRecord]) -> None:
        self._records: tuple[PriceScheduleRecord, ...] = tuple(records)
        self._by_key: dict[tuple[str, str], PriceScheduleRecord] = {
            (record.jurisdiction, record.year): record for record in self._records
        }

    @classmethod
    def default(cls) -> PriceRegistry:
        """Build the default public-safe registry."""
        return cls(
            [
                *_national_records(),
                *_state_records(),
                *_local_records(),
                *_discounted_records(),
                *_blocked_records(),
            ]
        )

    def list_available_years(self) -> list[str]:
        """Return years with at least one registered schedule."""
        return sorted({record.year for record in self._records})

    def list_available_jurisdictions(self, year: str | None = None) -> list[str]:
        """Return jurisdictions with registered schedules, optionally by year."""
        return sorted(
            {
                record.jurisdiction
                for record in self._records
                if year is None or record.year == year
            }
        )

    def get_price(self, jurisdiction: str, year: str) -> PriceScheduleRecord | None:
        """Return a price schedule if registered, including blocked records."""
        return self._by_key.get((jurisdiction, year))

    def require_price(self, jurisdiction: str, year: str) -> PriceScheduleRecord:
        """Return a price schedule or fail closed when one is unavailable."""
        record = self.get_price(jurisdiction, year)
        if record is None:
            raise PriceRegistryError(
                f"No price schedule available; schedule is not available for "
                f"jurisdiction={jurisdiction!r}, "
                f"year={year!r}"
            )
        return record

    def require_typed_price(
        self,
        jurisdiction: str,
        year: str,
        schedule_type: PriceScheduleType,
    ) -> PriceScheduleRecord:
        """Return a schedule of the expected type with a redistributable price."""
        record = self.require_price(jurisdiction, year)
        if record.schedule_type is not schedule_type:
            raise PriceRegistryError(
                f"Price schedule for {jurisdiction!r} in {year!r} is "
                f"{record.schedule_type.value!r}, not {schedule_type.value!r}"
            )
        if record.price_per_hwau is None:
            raise PriceRegistryError(
                f"Price schedule for {jurisdiction!r} in {year!r} is not available "
                f"because source status is {record.support_status.value!r}"
            )
        return record


def _default_registry() -> PriceRegistry:
    return PriceRegistry.default()


def list_available_years() -> list[str]:
    """Return years with at least one registered price schedule."""
    return _default_registry().list_available_years()


def list_available_jurisdictions(year: str | None = None) -> list[str]:
    """Return jurisdictions with registered price schedules."""
    return _default_registry().list_available_jurisdictions(year)


def get_national_price(year: str) -> PriceScheduleRecord:
    """Return the national efficient price schedule for a year."""
    return _default_registry().require_typed_price(
        "National",
        year,
        PriceScheduleType.NATIONAL,
    )


def get_state_price(jurisdiction: str, year: str) -> PriceScheduleRecord:
    """Return a state or jurisdiction price schedule."""
    return _default_registry().require_typed_price(
        jurisdiction,
        year,
        PriceScheduleType.STATE,
    )


def get_local_price(jurisdiction: str, year: str) -> PriceScheduleRecord:
    """Return a local price schedule."""
    return _default_registry().require_typed_price(
        jurisdiction,
        year,
        PriceScheduleType.LOCAL,
    )


def get_discounted_price(jurisdiction: str, year: str) -> PriceScheduleRecord:
    """Return a discounted price schedule."""
    return _default_registry().require_typed_price(
        jurisdiction,
        year,
        PriceScheduleType.DISCOUNTED,
    )
