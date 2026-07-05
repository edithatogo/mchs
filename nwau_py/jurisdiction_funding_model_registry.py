"""Jurisdiction funding-model registry with explicit source-status rows."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Final, TypedDict, cast

from .jurisdiction_price_sources import (
    JURISDICTIONS,
    get_jurisdiction_price_source,
)
from .nsw_funding_model import get_nsw_state_price
from .price_registry import get_state_price

__all__ = [
    "JurisdictionFundingModelError",
    "JurisdictionFundingModelRecord",
    "JurisdictionFundingModelRegistry",
    "JurisdictionFundingModelStatus",
    "JurisdictionFundingModelValuation",
    "calculate_parallel_jurisdiction_valuations",
    "get_jurisdiction_funding_model_record",
    "list_jurisdiction_funding_model_records",
]


class JurisdictionFundingModelError(ValueError):
    """Raised when a jurisdiction funding-model row is missing or unsupported."""


class JurisdictionFundingModelStatus(Enum):
    """Support status for a jurisdiction funding-model row."""

    PUBLIC = "public"
    LOCAL_ONLY = "local_only"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class JurisdictionFundingModelRecord:
    """Registry row for one jurisdiction and financial year."""

    jurisdiction: str
    financial_year: str
    source_term: str
    source_unit: str
    mapped_unit: str
    price_per_hwau: int | float | None
    source_url: str
    retrieved_on: date
    checksum: str
    licence_status: str
    redistribution_status: str
    stream_applicability: tuple[str, ...]
    adjustment_notes: str
    excluded_activity: str
    support_status: JurisdictionFundingModelStatus
    provenance_notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable representation of the registry row."""
        return {
            "jurisdiction": self.jurisdiction,
            "financial_year": self.financial_year,
            "source_term": self.source_term,
            "source_unit": self.source_unit,
            "mapped_unit": self.mapped_unit,
            "price_per_hwau": self.price_per_hwau,
            "source_url": self.source_url,
            "retrieved_on": self.retrieved_on.isoformat(),
            "checksum": self.checksum,
            "licence_status": self.licence_status,
            "redistribution_status": self.redistribution_status,
            "stream_applicability": list(self.stream_applicability),
            "adjustment_notes": self.adjustment_notes,
            "excluded_activity": self.excluded_activity,
            "support_status": self.support_status.value,
            "provenance_notes": list(self.provenance_notes),
        }


@dataclass(frozen=True, slots=True)
class JurisdictionFundingModelValuation:
    """Parallel valuation result for one jurisdiction row."""

    jurisdiction: str
    financial_year: str
    nwau_units: float
    support_status: JurisdictionFundingModelStatus
    price_per_hwau: float | None
    funding: float | None
    source_term: str
    source_url: str
    provenance_notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable representation of the valuation."""
        return {
            "jurisdiction": self.jurisdiction,
            "financial_year": self.financial_year,
            "nwau_units": self.nwau_units,
            "support_status": self.support_status.value,
            "price_per_hwau": self.price_per_hwau,
            "funding": self.funding,
            "source_term": self.source_term,
            "source_url": self.source_url,
            "provenance_notes": list(self.provenance_notes),
        }


_RETRIEVED_ON: Final[date] = date(2026, 7, 5)


class _FundingRowData(TypedDict):
    source_term: str
    source_unit: str
    mapped_unit: str
    price_per_hwau: int | float | None
    licence_status: str
    redistribution_status: str
    stream_applicability: tuple[str, ...]
    adjustment_notes: str
    excluded_activity: str
    support_status: JurisdictionFundingModelStatus
    provenance_notes: tuple[str, ...]


def _checksum(parts: Iterable[object]) -> str:
    payload = "|".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build_row(
    jurisdiction: str,
    financial_year: str = "2025",
) -> JurisdictionFundingModelRecord:
    source = get_jurisdiction_price_source(jurisdiction, financial_year)
    row = _ROW_DATA[jurisdiction]
    checksum = _checksum(
        (
            jurisdiction,
            financial_year,
            row["source_term"],
            row["source_unit"],
            row["mapped_unit"],
            row["price_per_hwau"],
            source.source_url_or_path,
            row["licence_status"],
            row["redistribution_status"],
            row["support_status"].value,
        )
    )
    return JurisdictionFundingModelRecord(
        jurisdiction=jurisdiction,
        financial_year=financial_year,
        source_term=row["source_term"],
        source_unit=row["source_unit"],
        mapped_unit=row["mapped_unit"],
        price_per_hwau=row["price_per_hwau"],
        source_url=source.source_url_or_path,
        retrieved_on=_RETRIEVED_ON,
        checksum=checksum,
        licence_status=row["licence_status"],
        redistribution_status=row["redistribution_status"],
        stream_applicability=row["stream_applicability"],
        adjustment_notes=row["adjustment_notes"],
        excluded_activity=row["excluded_activity"],
        support_status=row["support_status"],
        provenance_notes=row["provenance_notes"],
    )


_ROW_DATA: Final[dict[str, _FundingRowData]] = {
    "NSW": cast(
        _FundingRowData,
        {
            "source_term": "State Price per NWAU",
            "source_unit": "NWAU24",
            "mapped_unit": "HWAU",
            "price_per_hwau": get_nsw_state_price("2025").state_price_per_hwau,
            "licence_status": "public-web-pdf",
            "redistribution_status": "public_source_fixture",
            "stream_applicability": ("acute", "emergency", "subacute", "non_admitted"),
            "adjustment_notes": (
                "NSW State Price fixture is sourced from public "
                "budget-supplement notes and preserves LHD/SHN scope and DNR "
                "costing context."
            ),
            "excluded_activity": (
                "Excluded or block-funded activity remains governed by the public "
                "service-agreement notes."
            ),
            "support_status": JurisdictionFundingModelStatus.PUBLIC,
            "provenance_notes": (
                "NSW State Price per NWAU24 is published in the 2024-25 "
                "explanatory notes and preserves DNR clinical costing context.",
                "The row preserves State Efficient Price and DNR provenance.",
            ),
        },
    ),
    "VIC": cast(
        _FundingRowData,
        {
            "source_term": "NWAU",
            "source_unit": "NWAU",
            "mapped_unit": "HWAU",
            "price_per_hwau": get_state_price("VIC", "2025").price_per_hwau,
            "licence_status": "synthetic-test-fixture",
            "redistribution_status": "local_only_fixture",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "Victorian state price fixture is local-only and does not claim an "
                "official redistribution right."
            ),
            "excluded_activity": (
                "Residual block and special streams are represented as source metadata "
                "only."
            ),
            "support_status": JurisdictionFundingModelStatus.LOCAL_ONLY,
            "provenance_notes": (
                "Local-only state-price fixture exercises Victorian "
                "funding-model coverage.",
                "No official Victorian price payload is redistributed here.",
            ),
        },
    ),
    "QLD": cast(
        _FundingRowData,
        {
            "source_term": "QWAU",
            "source_unit": "QWAU",
            "mapped_unit": "HWAU",
            "price_per_hwau": get_state_price("QLD", "2025").price_per_hwau,
            "licence_status": "synthetic-test-fixture",
            "redistribution_status": "local_only_fixture",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "Queensland local-only state price fixture preserves the QWAU naming "
                "and does not imply official redistribution."
            ),
            "excluded_activity": (
                "Purchasing and funding-model exceptions remain source metadata only."
            ),
            "support_status": JurisdictionFundingModelStatus.LOCAL_ONLY,
            "provenance_notes": (
                "Local-only fixture is used for Queensland valuation selection tests.",
                "Queensland price terminology remains separate from HWAU abstraction.",
            ),
        },
    ),
    "WA": cast(
        _FundingRowData,
        {
            "source_term": "WAU",
            "source_unit": "WAU",
            "mapped_unit": "HWAU",
            "price_per_hwau": None,
            "licence_status": "public-metadata",
            "redistribution_status": "metadata_only",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "WA funding-model metadata is present, but no redistributable price "
                "fixture is committed."
            ),
            "excluded_activity": (
                "State-specific adjustment rows remain source metadata only."
            ),
            "support_status": JurisdictionFundingModelStatus.PUBLIC,
            "provenance_notes": (
                "Public WA ABF metadata is retained without committed price values.",
                "Numeric extraction is intentionally blocked pending separate "
                "sourcing.",
            ),
        },
    ),
    "SA": cast(
        _FundingRowData,
        {
            "source_term": "State Efficient Price",
            "source_unit": "NWAU",
            "mapped_unit": "HWAU",
            "price_per_hwau": None,
            "licence_status": "public-metadata",
            "redistribution_status": "metadata_only",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "SA funding-model metadata is public, but extracted price rows are "
                "not committed here."
            ),
            "excluded_activity": (
                "Block-funded components remain source metadata only."
            ),
            "support_status": JurisdictionFundingModelStatus.PUBLIC,
            "provenance_notes": (
                "Public SA source metadata is retained without numeric price payloads.",
                "The registry intentionally fails closed for extracted SA pricing.",
            ),
        },
    ),
    "TAS": cast(
        _FundingRowData,
        {
            "source_term": "NWAU",
            "source_unit": "NWAU",
            "mapped_unit": "HWAU",
            "price_per_hwau": None,
            "licence_status": "restricted-or-unclear",
            "redistribution_status": "blocked",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "Tasmanian price extraction remains blocked until a redistributable "
                "source is supplied."
            ),
            "excluded_activity": (
                "Block grants and supplementary lines are not inferred."
            ),
            "support_status": JurisdictionFundingModelStatus.BLOCKED,
            "provenance_notes": (
                "No redistributable Tasmanian price fixture is committed.",
                "The row exists to keep blocked-source handling explicit.",
            ),
        },
    ),
    "ACT": cast(
        _FundingRowData,
        {
            "source_term": "ACT applicable price",
            "source_unit": "ABF service-funding unit",
            "mapped_unit": "HWAU",
            "price_per_hwau": None,
            "licence_status": "public-metadata",
            "redistribution_status": "metadata_only",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "ACT model metadata is present but the registry does not claim an "
                "extracted price schedule."
            ),
            "excluded_activity": (
                "Transition and supplementary grant notes remain external."
            ),
            "support_status": JurisdictionFundingModelStatus.PUBLIC,
            "provenance_notes": (
                "ACT service-agreement metadata is retained without extracted prices.",
                "Local validation is still required for any funded ACT schedule.",
            ),
        },
    ),
    "NT": cast(
        _FundingRowData,
        {
            "source_term": "WAU",
            "source_unit": "WAU",
            "mapped_unit": "HWAU",
            "price_per_hwau": None,
            "licence_status": "restricted-or-unclear",
            "redistribution_status": "blocked",
            "stream_applicability": ("acute", "subacute", "emergency", "non_admitted"),
            "adjustment_notes": (
                "Northern Territory pricing remains blocked until a redistributable "
                "source fixture is available."
            ),
            "excluded_activity": (
                "Remote and territory-specific funding is not inferred."
            ),
            "support_status": JurisdictionFundingModelStatus.BLOCKED,
            "provenance_notes": (
                "No redistributable NT price fixture is committed.",
                "This blocked row is explicit so downstream logic fails closed.",
            ),
        },
    ),
}


class JurisdictionFundingModelRegistry:
    """Registry for jurisdiction funding-model rows."""

    def __init__(self, records: Iterable[JurisdictionFundingModelRecord]) -> None:
        self._records: tuple[JurisdictionFundingModelRecord, ...] = tuple(records)
        self._by_key: dict[tuple[str, str], JurisdictionFundingModelRecord] = {
            (record.jurisdiction, record.financial_year): record
            for record in self._records
        }

    @classmethod
    def default(cls) -> JurisdictionFundingModelRegistry:
        """Build the default public-safe jurisdiction registry."""
        return cls(_build_row(jurisdiction) for jurisdiction in JURISDICTIONS)

    def list_available_years(self) -> list[str]:
        """Return registered financial years."""
        return sorted({record.financial_year for record in self._records})

    def list_available_jurisdictions(
        self, financial_year: str | None = None
    ) -> list[str]:
        """Return jurisdictions with rows, optionally filtered by year."""
        return sorted(
            {
                record.jurisdiction
                for record in self._records
                if financial_year is None or record.financial_year == financial_year
            }
        )

    def get_record(
        self,
        jurisdiction: str,
        financial_year: str,
    ) -> JurisdictionFundingModelRecord | None:
        """Return a registry row if one exists."""
        return self._by_key.get((jurisdiction, financial_year))

    def require_record(
        self,
        jurisdiction: str,
        financial_year: str,
    ) -> JurisdictionFundingModelRecord:
        """Return a registry row or fail closed."""
        record = self.get_record(jurisdiction, financial_year)
        if record is None:
            raise JurisdictionFundingModelError(
                "No jurisdiction funding model row is registered for "
                f"jurisdiction={jurisdiction!r}, financial_year={financial_year!r}"
            )
        return record

    def list_support_statuses(
        self,
        financial_year: str | None = None,
    ) -> dict[str, JurisdictionFundingModelStatus]:
        """Return source-status coverage by jurisdiction."""
        return {
            record.jurisdiction: record.support_status
            for record in self._records
            if financial_year is None or record.financial_year == financial_year
        }

    def select_parallel_valuations(
        self,
        nwau_units: float,
        financial_year: str = "2025",
    ) -> list[JurisdictionFundingModelValuation]:
        """Return parallel valuation outputs for rows with known prices."""
        valuations: list[JurisdictionFundingModelValuation] = []
        for record in self._records:
            if record.financial_year != financial_year:
                continue
            funding = (
                float(nwau_units) * float(record.price_per_hwau)
                if record.price_per_hwau is not None
                else None
            )
            valuations.append(
                JurisdictionFundingModelValuation(
                    jurisdiction=record.jurisdiction,
                    financial_year=record.financial_year,
                    nwau_units=float(nwau_units),
                    support_status=record.support_status,
                    price_per_hwau=(
                        float(record.price_per_hwau)
                        if record.price_per_hwau is not None
                        else None
                    ),
                    funding=funding,
                    source_term=record.source_term,
                    source_url=record.source_url,
                    provenance_notes=record.provenance_notes,
                )
            )
        return valuations


def list_jurisdiction_funding_model_records(
    financial_year: str | None = None,
) -> list[JurisdictionFundingModelRecord]:
    """Return built-in jurisdiction funding-model rows."""
    registry = JurisdictionFundingModelRegistry.default()
    return [
        record
        for record in registry._records
        if financial_year is None or record.financial_year == financial_year
    ]


def get_jurisdiction_funding_model_record(
    jurisdiction: str,
    financial_year: str,
) -> JurisdictionFundingModelRecord:
    """Return a built-in jurisdiction funding-model row."""
    return JurisdictionFundingModelRegistry.default().require_record(
        jurisdiction,
        financial_year,
    )


def calculate_parallel_jurisdiction_valuations(
    nwau_units: float,
    financial_year: str = "2025",
) -> list[JurisdictionFundingModelValuation]:
    """Return parallel valuation outputs for all registered jurisdiction rows."""
    return JurisdictionFundingModelRegistry.default().select_parallel_valuations(
        nwau_units,
        financial_year,
    )
