"""NSW-specific funding model registry with public-source fixtures."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Final, TypedDict

from .price_registry import get_national_price

__all__ = [
    "NSWFundingModelError",
    "NSWFundingModelRecord",
    "NSWFundingModelRegistry",
    "NSWFundingModelStatus",
    "apply_parallel_nsw_valuation",
    "get_nsw_state_price",
]


class NSWFundingModelError(ValueError):
    """Raised when NSW funding-model coverage is unavailable."""


class NSWFundingModelStatus(Enum):
    """Support status for a NSW funding-model row."""

    PUBLIC = "public"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class NSWFundingModelRecord:
    """Immutable NSW funding-model record for one financial year."""

    financial_year: str
    source_term: str
    state_price_per_hwau: int | float | None
    source_url: str
    retrieved_on: date
    checksum: str
    licence_status: str
    district_network_scope: tuple[str, ...]
    adjustment_notes: str
    excluded_activity: str
    support_status: NSWFundingModelStatus
    provenance_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable representation of the NSW row."""
        return {
            "financial_year": self.financial_year,
            "source_term": self.source_term,
            "state_price_per_hwau": self.state_price_per_hwau,
            "source_url": self.source_url,
            "retrieved_on": self.retrieved_on.isoformat(),
            "checksum": self.checksum,
            "licence_status": self.licence_status,
            "district_network_scope": list(self.district_network_scope),
            "adjustment_notes": self.adjustment_notes,
            "excluded_activity": self.excluded_activity,
            "support_status": self.support_status.value,
            "provenance_notes": list(self.provenance_notes),
        }


_RETRIEVED_ON: Final[date] = date(2026, 7, 5)


class _NSWRecordData(TypedDict):
    source_term: str
    state_price_per_hwau: int | float
    source_url: str
    licence_status: str
    district_network_scope: tuple[str, ...]
    adjustment_notes: str
    excluded_activity: str
    support_status: NSWFundingModelStatus
    provenance_notes: tuple[str, ...]


_RECORDS: Final[dict[str, _NSWRecordData]] = {
    "2025": {
        "source_term": "NWAU24",
        "state_price_per_hwau": 5675,
        "source_url": (
            "https://www.seslhd.health.nsw.gov.au/sites/default/files/groups/"
            "Executive_Services/Service_Agreement/2024-25%20Explanatory%20Notes%20"
            "for%20Section%204%20Budget%20-%20attachment%20to%20NSW%20Ministry~ern%"
            "20Sydney%20Local%20Health%20District%20for%20the%20period%201%20July%"
            "2024%20to%2030%20June%202025.pdf"
        ),
        "licence_status": "public-web-pdf",
        "district_network_scope": (
            "Local Health District",
            "Specialty Health Network",
        ),
        "adjustment_notes": (
            "NSW State Efficient Price informed by DNR clinical costing and "
            "applied through LHD/SHN service-agreement budget schedules."
        ),
        "excluded_activity": (
            "Excluded or block-funded activity remains governed by the service "
            "agreement notes and is not treated as the state price."
        ),
        "support_status": NSWFundingModelStatus.PUBLIC,
        "provenance_notes": (
            "The 2024-25 explanatory notes state the NSW State Efficient Price as "
            "5675 per NWAU24 and cite DNR clinical costing support.",
            "The budget schedule keeps LHD/SHN service-agreement scope and notes "
            "separate from the price row.",
        ),
    },
    "2026": {
        "source_term": "NWAU25",
        "state_price_per_hwau": 6081,
        "source_url": "https://www.health.nsw.gov.au/Performance/Documents/service-agreement-generic.pdf",
        "licence_status": "public-web-pdf",
        "district_network_scope": (
            "Local Health District",
            "Specialty Health Network",
        ),
        "adjustment_notes": (
            "NSW State Price for growth activity is published in the 2025-26 "
            "funding and performance supplement."
        ),
        "excluded_activity": (
            "Networked arrangements, transfers, and excluded activity continue to "
            "follow the service-agreement notes."
        ),
        "support_status": NSWFundingModelStatus.PUBLIC,
        "provenance_notes": (
            "The 2025-26 funding supplement states the NSW State Price as 6081 "
            "per NWAU25.",
            "This fixture is a public source record, not a redistributable service "
            "agreement corpus.",
        ),
    },
}


def _checksum(parts: Iterable[object]) -> str:
    payload = "|".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_record(financial_year: str) -> NSWFundingModelRecord:
    payload = _RECORDS.get(financial_year)
    if payload is None:
        raise NSWFundingModelError(
            "No NSW funding model source fixture is registered for "
            f"year={financial_year!r}"
        )
    return NSWFundingModelRecord(
        financial_year=financial_year,
        source_term=str(payload["source_term"]),
        state_price_per_hwau=payload["state_price_per_hwau"],
        source_url=str(payload["source_url"]),
        retrieved_on=_RETRIEVED_ON,
        checksum=_checksum(
            (
                financial_year,
                payload["source_term"],
                payload["state_price_per_hwau"],
                payload["source_url"],
                payload["licence_status"],
                payload["support_status"].value,
            )
        ),
        licence_status=str(payload["licence_status"]),
        district_network_scope=tuple(payload["district_network_scope"]),
        adjustment_notes=str(payload["adjustment_notes"]),
        excluded_activity=str(payload["excluded_activity"]),
        support_status=payload["support_status"],
        provenance_notes=tuple(payload["provenance_notes"]),
    )


class NSWFundingModelRegistry:
    """Registry of public-source NSW funding-model fixtures."""

    def __init__(self, records: Sequence[NSWFundingModelRecord]) -> None:
        self._records: tuple[NSWFundingModelRecord, ...] = tuple(records)
        self._by_year: dict[str, NSWFundingModelRecord] = {
            record.financial_year: record for record in self._records
        }

    @classmethod
    def default(cls) -> NSWFundingModelRegistry:
        """Return the built-in public-source NSW registry."""
        return cls([_build_record(year) for year in ("2025", "2026")])

    def list_available_years(self) -> list[str]:
        """Return all years with a registered NSW source fixture."""
        return sorted(self._by_year)

    def get_record(self, financial_year: str) -> NSWFundingModelRecord | None:
        """Return the source fixture for a year, if registered."""
        return self._by_year.get(financial_year)

    def require_record(self, financial_year: str) -> NSWFundingModelRecord:
        """Return a source fixture or fail closed when one is missing."""
        record = self.get_record(financial_year)
        if record is None:
            raise NSWFundingModelError(
                "No NSW funding model source fixture is registered for "
                f"year={financial_year!r}"
            )
        return record

    def require_state_price(self, financial_year: str) -> NSWFundingModelRecord:
        """Return the NSW state-price record or fail closed when unavailable."""
        record = self.require_record(financial_year)
        if record.state_price_per_hwau is None:
            raise NSWFundingModelError(
                f"NSW state price is unavailable for year={financial_year!r}"
            )
        return record


def get_nsw_state_price(financial_year: str) -> NSWFundingModelRecord:
    """Return the built-in NSW state-price fixture."""
    return NSWFundingModelRegistry.default().require_state_price(financial_year)


def apply_parallel_nsw_valuation(
    nwau_units: float,
    *,
    financial_year: str,
) -> dict[str, object]:
    """Return parallel NSW and national valuation outputs for a given HWAU count."""
    nsw_record = get_nsw_state_price(financial_year)
    national_record = get_national_price(financial_year)
    nsw_price = float(nsw_record.state_price_per_hwau or 0)
    national_price = float(national_record.price_per_hwau or 0)
    return {
        "financial_year": financial_year,
        "nwau_units": float(nwau_units),
        "state_source_term": nsw_record.source_term,
        "state_source_status": nsw_record.support_status.value,
        "nsw_state_price_per_hwau": nsw_price,
        "nsw_funding": float(nwau_units) * nsw_price,
        "national_source_term": "NEP",
        "national_source_status": national_record.support_status.value,
        "national_price_per_hwau": national_price,
        "national_funding": float(nwau_units) * national_price,
    }
