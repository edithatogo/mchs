"""Public-safe source index for Australian jurisdiction price-model discovery."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Final

__all__ = [
    "JURISDICTIONS",
    "JurisdictionPriceSourceIndex",
    "JurisdictionPriceSourceRecord",
    "JurisdictionPriceSourceStatus",
    "SourceIndexError",
    "get_jurisdiction_price_source",
    "list_jurisdiction_price_sources",
    "validate_price_source_coverage",
]


class SourceIndexError(ValueError):
    """Raised when jurisdiction source-index coverage is missing or invalid."""


class JurisdictionPriceSourceStatus(Enum):
    """Redistribution and extraction status for a jurisdiction price source."""

    PUBLIC_METADATA = "public_metadata"
    LOCAL_ONLY = "local_only"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class JurisdictionPriceSourceRecord:
    """Source metadata for one jurisdiction price-model discovery row."""

    jurisdiction: str
    financial_year: str
    source_title: str
    source_url_or_path: str
    retrieved_on: date
    checksum: str
    licence_status: str
    redistribution_status: str
    source_unit: str
    mapped_unit: str
    price_term: str
    stream_applicability: tuple[str, ...]
    adjustment_notes: str
    support_status: JurisdictionPriceSourceStatus
    extraction_notes: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable representation of the source row."""
        return {
            "jurisdiction": self.jurisdiction,
            "financial_year": self.financial_year,
            "source_title": self.source_title,
            "source_url_or_path": self.source_url_or_path,
            "retrieved_on": self.retrieved_on.isoformat(),
            "checksum": self.checksum,
            "licence_status": self.licence_status,
            "redistribution_status": self.redistribution_status,
            "source_unit": self.source_unit,
            "mapped_unit": self.mapped_unit,
            "price_term": self.price_term,
            "stream_applicability": list(self.stream_applicability),
            "adjustment_notes": self.adjustment_notes,
            "support_status": self.support_status.value,
            "extraction_notes": self.extraction_notes,
        }


JURISDICTIONS: Final[tuple[str, ...]] = (
    "NSW",
    "VIC",
    "QLD",
    "WA",
    "SA",
    "TAS",
    "ACT",
    "NT",
)

_RETRIEVED_ON: Final[date] = date(2026, 7, 5)


def _checksum(parts: Iterable[object]) -> str:
    payload = "|".join(str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _record(
    *,
    jurisdiction: str,
    financial_year: str,
    source_title: str,
    source_url_or_path: str,
    licence_status: str,
    redistribution_status: str,
    source_unit: str,
    mapped_unit: str,
    price_term: str,
    stream_applicability: Sequence[str],
    adjustment_notes: str,
    support_status: JurisdictionPriceSourceStatus,
    extraction_notes: str,
) -> JurisdictionPriceSourceRecord:
    checksum = _checksum(
        (
            jurisdiction,
            financial_year,
            source_title,
            source_url_or_path,
            licence_status,
            redistribution_status,
            source_unit,
            mapped_unit,
            price_term,
            ",".join(stream_applicability),
            support_status.value,
        )
    )
    return JurisdictionPriceSourceRecord(
        jurisdiction=jurisdiction,
        financial_year=financial_year,
        source_title=source_title,
        source_url_or_path=source_url_or_path,
        retrieved_on=_RETRIEVED_ON,
        checksum=checksum,
        licence_status=licence_status,
        redistribution_status=redistribution_status,
        source_unit=source_unit,
        mapped_unit=mapped_unit,
        price_term=price_term,
        stream_applicability=tuple(stream_applicability),
        adjustment_notes=adjustment_notes,
        support_status=support_status,
        extraction_notes=extraction_notes,
    )


_SOURCE_ROWS: Final[tuple[JurisdictionPriceSourceRecord, ...]] = (
    _record(
        jurisdiction="NSW",
        financial_year="2025",
        source_title="NSW activity based funding source discovery row",
        source_url_or_path="https://www.health.nsw.gov.au/",
        licence_status="public metadata; official price extraction not redistributed",
        redistribution_status="metadata_only",
        source_unit="NWAU or NSW service-agreement activity unit, source dependent",
        mapped_unit="HWAU after source-specific validation",
        price_term="state price or service-agreement price, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes=(
            "Requires NSW source-specific validation before values are extracted."
        ),
        support_status=JurisdictionPriceSourceStatus.BLOCKED,
        extraction_notes=(
            "No redistributable NSW price value is committed. A public-safe source "
            "row exists so downstream extraction must fail closed until a sourced "
            "document and licence decision are registered."
        ),
    ),
    _record(
        jurisdiction="VIC",
        financial_year="2025",
        source_title="Victoria National Funding Model implementation resources",
        source_url_or_path=(
            "https://www.health.vic.gov.au/data-reporting/"
            "national-funding-model-implementation-resources"
        ),
        licence_status="public web metadata",
        redistribution_status="metadata_only",
        source_unit="NWAU",
        mapped_unit="HWAU",
        price_term="Victorian funding-model price term, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes=(
            "Victoria states the National Funding Model uses NWAU across major streams."
        ),
        support_status=JurisdictionPriceSourceStatus.PUBLIC_METADATA,
        extraction_notes=(
            "Metadata can be redistributed; numeric price extraction remains gated."
        ),
    ),
    _record(
        jurisdiction="QLD",
        financial_year="2025",
        source_title=(
            "Queensland public hospital services purchasing and funding models"
        ),
        source_url_or_path=(
            "https://www.health.qld.gov.au/system-governance/health-system/"
            "managing/funding-model"
        ),
        licence_status="public web metadata",
        redistribution_status="metadata_only",
        source_unit="QWAU",
        mapped_unit="HWAU after Queensland-specific mapping validation",
        price_term=(
            "Queensland Efficient Price or HHS service-agreement price, not extracted"
        ),
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes=(
            "QWAU-specific terms must not be treated as national NWAU without "
            "mapping evidence."
        ),
        support_status=JurisdictionPriceSourceStatus.PUBLIC_METADATA,
        extraction_notes=(
            "Metadata can be redistributed; numeric price extraction remains gated."
        ),
    ),
    _record(
        jurisdiction="WA",
        financial_year="2025",
        source_title="WA Health activity based funding",
        source_url_or_path="https://www.health.wa.gov.au/Our-performance/Activity-based-funding",
        licence_status="public web metadata",
        redistribution_status="metadata_only",
        source_unit="ABF activity unit, source dependent",
        mapped_unit="HWAU after WA-specific validation",
        price_term="WA ABF price term, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes=(
            "WA public page confirms ABF context but does not provide a reusable "
            "price schedule."
        ),
        support_status=JurisdictionPriceSourceStatus.PUBLIC_METADATA,
        extraction_notes=(
            "Metadata can be redistributed; numeric price extraction remains gated."
        ),
    ),
    _record(
        jurisdiction="SA",
        financial_year="2025",
        source_title="SA Health public hospital funding allocation technical bulletins",
        source_url_or_path=(
            "https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/"
            "sa+health+internet/resources/funding+allocation+technical+bulletins+"
            "for+south+australian+public+hospitals+2024-25"
        ),
        licence_status="public web metadata",
        redistribution_status="metadata_only",
        source_unit="state-funded activity unit, source dependent",
        mapped_unit="HWAU after SA-specific validation",
        price_term="SA allocation or activity price term, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes=(
            "Technical bulletin source must be reviewed before values are extracted."
        ),
        support_status=JurisdictionPriceSourceStatus.PUBLIC_METADATA,
        extraction_notes=(
            "Metadata can be redistributed; numeric price extraction remains gated."
        ),
    ),
    _record(
        jurisdiction="TAS",
        financial_year="2025",
        source_title="Tasmanian Health Service funding and service-plan discovery row",
        source_url_or_path="https://www.health.tas.gov.au/",
        licence_status="public metadata; official price extraction not redistributed",
        redistribution_status="metadata_only",
        source_unit="NWAU or Tasmanian service-plan activity unit, source dependent",
        mapped_unit="HWAU after Tasmanian-specific validation",
        price_term="Tasmanian service-plan price term, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes="Requires source-specific review before values are extracted.",
        support_status=JurisdictionPriceSourceStatus.BLOCKED,
        extraction_notes=(
            "No redistributable Tasmanian price value or authoritative schedule "
            "is committed."
        ),
    ),
    _record(
        jurisdiction="ACT",
        financial_year="2025",
        source_title="ACT activity based funding service agreement",
        source_url_or_path="https://www.act.gov.au/open/activity-based-funding-service-agreement",
        licence_status="public web metadata",
        redistribution_status="metadata_only",
        source_unit="ABF service funding agreement unit, source dependent",
        mapped_unit="HWAU after ACT-specific validation",
        price_term="ACT service funding agreement price term, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes=(
            "ACT commissioning terms must be validated before calculator use."
        ),
        support_status=JurisdictionPriceSourceStatus.PUBLIC_METADATA,
        extraction_notes=(
            "Metadata can be redistributed; numeric price extraction remains gated."
        ),
    ),
    _record(
        jurisdiction="NT",
        financial_year="2025",
        source_title="Northern Territory activity based funding discovery row",
        source_url_or_path="https://health.nt.gov.au/",
        licence_status="public metadata; official price extraction not redistributed",
        redistribution_status="metadata_only",
        source_unit="price-volume or activity based funding unit, source dependent",
        mapped_unit="HWAU after NT-specific validation",
        price_term="NT price-volume or funding-model term, not extracted",
        stream_applicability=("acute", "subacute", "emergency", "non_admitted"),
        adjustment_notes="No current redistributable NT price schedule is registered.",
        support_status=JurisdictionPriceSourceStatus.BLOCKED,
        extraction_notes=(
            "No redistributable NT price value or authoritative schedule is committed."
        ),
    ),
)


class JurisdictionPriceSourceIndex:
    """Lookup and validation API for jurisdiction price source metadata."""

    def __init__(self, rows: Iterable[JurisdictionPriceSourceRecord]) -> None:
        self._rows: tuple[JurisdictionPriceSourceRecord, ...] = tuple(rows)
        self._by_key: dict[tuple[str, str], JurisdictionPriceSourceRecord] = {
            (row.jurisdiction, row.financial_year): row for row in self._rows
        }

    @classmethod
    def default(cls) -> JurisdictionPriceSourceIndex:
        """Return the built-in public-safe source index."""
        return cls(_SOURCE_ROWS)

    def list_sources(
        self,
        *,
        financial_year: str | None = None,
        status: JurisdictionPriceSourceStatus | None = None,
    ) -> list[JurisdictionPriceSourceRecord]:
        """List source rows, optionally filtered by year and support status."""
        return [
            row
            for row in self._rows
            if (financial_year is None or row.financial_year == financial_year)
            and (status is None or row.support_status is status)
        ]

    def get_source(
        self,
        jurisdiction: str,
        financial_year: str,
    ) -> JurisdictionPriceSourceRecord | None:
        """Return the source row for a jurisdiction/year pair, if registered."""
        return self._by_key.get((jurisdiction, financial_year))

    def require_source(
        self,
        jurisdiction: str,
        financial_year: str,
    ) -> JurisdictionPriceSourceRecord:
        """Return a source row or fail closed if one has not been registered."""
        row = self.get_source(jurisdiction, financial_year)
        if row is None:
            raise SourceIndexError(
                "No jurisdiction price source registered for "
                f"jurisdiction={jurisdiction!r}, financial_year={financial_year!r}"
            )
        return row

    def validate_coverage(
        self,
        *,
        financial_year: str,
        jurisdictions: Sequence[str] = JURISDICTIONS,
    ) -> None:
        """Fail closed unless every required jurisdiction has a source row."""
        missing = [
            jurisdiction
            for jurisdiction in jurisdictions
            if self.get_source(jurisdiction, financial_year) is None
        ]
        if missing:
            raise SourceIndexError(
                "Missing jurisdiction price source rows for "
                f"{financial_year}: {', '.join(missing)}"
            )


def list_jurisdiction_price_sources(
    *,
    financial_year: str | None = None,
    status: JurisdictionPriceSourceStatus | None = None,
) -> list[JurisdictionPriceSourceRecord]:
    """List built-in jurisdiction price source rows."""
    return JurisdictionPriceSourceIndex.default().list_sources(
        financial_year=financial_year,
        status=status,
    )


def get_jurisdiction_price_source(
    jurisdiction: str,
    financial_year: str,
) -> JurisdictionPriceSourceRecord:
    """Return a built-in jurisdiction price source row or fail closed."""
    return JurisdictionPriceSourceIndex.default().require_source(
        jurisdiction,
        financial_year,
    )


def validate_price_source_coverage(financial_year: str) -> None:
    """Validate built-in source coverage for every Australian jurisdiction."""
    JurisdictionPriceSourceIndex.default().validate_coverage(
        financial_year=financial_year,
    )
