"""Strict emergency UDG/AECC transition registry.

The helpers in this module model the boundary between Urgency Disposition
Groups (UDG) and the Australian Emergency Care Classification (AECC) without
inventing any crosswalk, fallback mapping, or equivalence class.

The registry is intentionally conservative:

- it records year-by-year version applicability;
- it separates shadow-priced and transition-period handling from active use;
- it keeps provenance attached to the registry rows; and
- it fails closed when a system/year/version combination is not valid.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Final, Literal

__all__ = [
    "EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS",
    "EMERGENCY_CLASSIFICATION_SOURCE_REFS",
    "EMERGENCY_CLASSIFICATION_SYSTEMS",
    "EMERGENCY_CLASSIFICATION_VERSION_MATRIX",
    "EMERGENCY_STREAMS",
    "EMERGENCY_TRANSITION_PERIODS",
    "EmergencyClassificationCompatibilityResult",
    "EmergencyClassificationRecord",
    "EmergencyClassificationRegistryError",
    "EmergencyClassificationVersion",
    "EmergencyTransitionPeriod",
    "ensure_emergency_classification_compatibility",
    "get_emergency_classification_name",
    "get_emergency_classification_record",
    "get_emergency_classification_status",
    "get_emergency_classification_version",
    "get_emergency_supported_years",
    "get_emergency_transition_period",
    "get_emergency_transition_years",
    "get_expected_emergency_classification_version",
    "list_emergency_classification_records",
    "list_emergency_transition_periods",
    "normalize_emergency_classification_system",
    "validate_aecc_input",
    "validate_emergency_classification_compatibility",
    "validate_emergency_input",
    "validate_udg_input",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")

EMERGENCY_STREAMS: Final[tuple[str, ...]] = (
    "emergency_department",
    "emergency_service",
)

EMERGENCY_CLASSIFICATION_SYSTEMS: Final[dict[str, str]] = {
    "aecc": "AECC",
    "udg": "UDG",
}

EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS: Final[dict[str, tuple[str, ...]]] = {
    "aecc": ("AECC",),
    "udg": ("UDG",),
}

EMERGENCY_CLASSIFICATION_SOURCE_REFS: Final[dict[str, tuple[str, ...]]] = {
    "aecc": (
        "https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc",
        "https://www.ihacpa.gov.au/health-care/classification/emergency-care",
    ),
    "udg": (
        "https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg",
        "https://www.ihacpa.gov.au/health-care/classification/emergency-care",
    ),
}


class EmergencyClassificationRegistryError(ValueError):
    """Raised when the emergency transition registry is inconsistent."""


AcceptanceState = Literal["valid", "transition", "shadow-priced", "unavailable"]


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise EmergencyClassificationRegistryError(f"{field} must be a string")
    if not value:
        raise EmergencyClassificationRegistryError(f"{field} must not be blank")
    if value.strip() != value:
        raise EmergencyClassificationRegistryError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise EmergencyClassificationRegistryError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str, *, field: str) -> str:
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise EmergencyClassificationRegistryError(
            f"{field} must be a deterministic version label"
        )
    return normalized


def _normalize_str_tuple(
    value: Any,
    *,
    field: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise EmergencyClassificationRegistryError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise EmergencyClassificationRegistryError(
                f"{field} must not contain duplicates"
            )
        seen.add(text)
        normalized.append(text)
    if not normalized and not allow_empty:
        raise EmergencyClassificationRegistryError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_streams(streams: Any) -> tuple[str, ...]:
    normalized = _normalize_str_tuple(streams, field="stream_compatibility")
    unknown = tuple(stream for stream in normalized if stream not in EMERGENCY_STREAMS)
    if unknown:
        raise EmergencyClassificationRegistryError(
            "stream_compatibility contains unsupported streams: " + ", ".join(unknown)
        )
    return normalized


def normalize_emergency_classification_system(system: str) -> str:
    """Return the canonical system identifier for an emergency classification."""
    normalized = _normalize_non_blank(system, field="classification_system")
    canonical = EMERGENCY_CLASSIFICATION_SYSTEMS.get(normalized.lower())
    if canonical is None:
        raise EmergencyClassificationRegistryError(
            "classification_system must be one of "
            f"{sorted(EMERGENCY_CLASSIFICATION_SYSTEMS)} or their display names"
        )
    return normalized.lower()


@dataclass(frozen=True, slots=True)
class EmergencyClassificationVersion:
    """Version metadata for a pricing year."""

    year: str
    version: str | None
    acceptance_state: AcceptanceState
    source_fields: tuple[str, ...]
    stream_compatibility: tuple[str, ...]
    source_refs: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "year", _normalize_year(self.year))
        if self.version is not None:
            object.__setattr__(
                self,
                "version",
                _normalize_version(self.version, field="version"),
            )
        if self.acceptance_state not in {
            "valid",
            "transition",
            "shadow-priced",
            "unavailable",
        }:
            raise EmergencyClassificationRegistryError(
                f"unsupported acceptance_state {self.acceptance_state!r}"
            )
        object.__setattr__(
            self,
            "source_fields",
            _normalize_str_tuple(self.source_fields, field="source_fields"),
        )
        object.__setattr__(
            self,
            "stream_compatibility",
            _normalize_streams(self.stream_compatibility),
        )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes", allow_empty=True),
        )
        if self.acceptance_state == "unavailable" and self.version is not None:
            raise EmergencyClassificationRegistryError(
                "unavailable versions must not declare a version label"
            )
        if self.acceptance_state != "unavailable" and self.version is None:
            raise EmergencyClassificationRegistryError(
                "available versions require a version label"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "year": self.year,
            "version": self.version,
            "acceptance_state": self.acceptance_state,
            "source_fields": list(self.source_fields),
            "stream_compatibility": list(self.stream_compatibility),
            "source_refs": list(self.source_refs),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class EmergencyTransitionPeriod:
    """Conservative transition window for a pricing-year span."""

    system: str
    start_year: str
    end_year: str
    acceptance_state: AcceptanceState
    source_refs: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "system",
            normalize_emergency_classification_system(self.system),
        )
        start_year = _normalize_year(self.start_year)
        end_year = _normalize_year(self.end_year)
        if start_year > end_year:
            raise EmergencyClassificationRegistryError(
                "start_year must not be later than end_year"
            )
        object.__setattr__(self, "start_year", start_year)
        object.__setattr__(self, "end_year", end_year)
        if self.acceptance_state not in {
            "valid",
            "transition",
            "shadow-priced",
            "unavailable",
        }:
            raise EmergencyClassificationRegistryError(
                f"unsupported acceptance_state {self.acceptance_state!r}"
            )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes", allow_empty=True),
        )

    def covers(self, year: str) -> bool:
        normalized_year = _normalize_year(year)
        return self.start_year <= normalized_year <= self.end_year

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "acceptance_state": self.acceptance_state,
            "source_refs": list(self.source_refs),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class EmergencyClassificationRecord:
    """Immutable registry entry for a single emergency classification family."""

    system: str
    display_name: str
    aliases: tuple[str, ...]
    required_fields: tuple[str, ...]
    stream_compatibility: tuple[str, ...]
    source_refs: tuple[str, ...]
    notes: tuple[str, ...]
    versions: tuple[EmergencyClassificationVersion, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "system",
            normalize_emergency_classification_system(self.system),
        )
        object.__setattr__(
            self,
            "display_name",
            _normalize_non_blank(self.display_name, field="display_name"),
        )
        object.__setattr__(
            self,
            "aliases",
            _normalize_str_tuple(self.aliases, field="aliases"),
        )
        object.__setattr__(
            self,
            "required_fields",
            _normalize_str_tuple(self.required_fields, field="required_fields"),
        )
        object.__setattr__(
            self,
            "stream_compatibility",
            _normalize_streams(self.stream_compatibility),
        )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes", allow_empty=True),
        )
        normalized_versions = tuple(self.versions)
        if not normalized_versions:
            raise EmergencyClassificationRegistryError("versions must not be empty")
        object.__setattr__(self, "versions", normalized_versions)
        years = {item.year for item in normalized_versions}
        if len(years) != len(normalized_versions):
            raise EmergencyClassificationRegistryError(
                "versions must not contain duplicate pricing years"
            )

    def version_for_year(self, year: str) -> EmergencyClassificationVersion | None:
        normalized_year = _normalize_year(year)
        for item in self.versions:
            if item.year == normalized_year:
                return item
        return None

    def expected_version_for_year(self, year: str) -> str | None:
        record = self.version_for_year(year)
        return None if record is None else record.version

    def acceptance_state_for_year(self, year: str) -> AcceptanceState:
        record = self.version_for_year(year)
        return "unavailable" if record is None else record.acceptance_state

    def supported_years(self) -> tuple[str, ...]:
        return tuple(
            item.year
            for item in self.versions
            if item.acceptance_state != "unavailable"
        )

    def transition_years(self) -> tuple[str, ...]:
        ordered = sorted(self.versions, key=lambda item: item.year)
        transition_years: list[str] = []
        previous_state: AcceptanceState | None = None
        previous_version: str | None = None
        for item in ordered:
            if previous_state is None:
                previous_state = item.acceptance_state
                previous_version = item.version
                continue
            if (
                item.acceptance_state != previous_state
                or item.version != previous_version
            ):
                transition_years.append(item.year)
            previous_state = item.acceptance_state
            previous_version = item.version
        return tuple(transition_years)

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "display_name": self.display_name,
            "aliases": list(self.aliases),
            "required_fields": list(self.required_fields),
            "stream_compatibility": list(self.stream_compatibility),
            "source_refs": list(self.source_refs),
            "notes": list(self.notes),
            "versions": [version.to_dict() for version in self.versions],
            "supported_years": list(self.supported_years()),
            "transition_years": list(self.transition_years()),
        }


@dataclass(frozen=True, slots=True)
class EmergencyClassificationCompatibilityResult:
    """Outcome from a fail-closed emergency classification compatibility check."""

    system: str
    display_name: str
    pricing_year: str
    declared_version: str | None
    expected_version: str | None
    acceptance_state: AcceptanceState
    compatibility_state: Literal[
        "valid",
        "transition",
        "shadow-priced",
        "missing",
        "incompatible",
    ]
    compatible: bool
    stream: str | None
    stream_compatibility: tuple[str, ...]
    required_fields: tuple[str, ...]
    observed_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    source_refs: tuple[str, ...]
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "display_name": self.display_name,
            "pricing_year": self.pricing_year,
            "declared_version": self.declared_version,
            "expected_version": self.expected_version,
            "acceptance_state": self.acceptance_state,
            "compatibility_state": self.compatibility_state,
            "compatible": self.compatible,
            "stream": self.stream,
            "stream_compatibility": list(self.stream_compatibility),
            "required_fields": list(self.required_fields),
            "observed_fields": list(self.observed_fields),
            "missing_fields": list(self.missing_fields),
            "source_refs": list(self.source_refs),
            "reason": self.reason,
        }


_EMERGENCY_CLASSIFICATION_RECORDS: Final[tuple[EmergencyClassificationRecord, ...]] = (
    EmergencyClassificationRecord(
        system="udg",
        display_name="UDG",
        aliases=("udg",),
        required_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["udg"],
        stream_compatibility=EMERGENCY_STREAMS,
        source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"],
        notes=(
            "UDG remains recorded for transition-period compatibility.",
            "The registry does not define any UDG-to-AECC crosswalk.",
        ),
        versions=(
            *(
                EmergencyClassificationVersion(
                    year=year,
                    version="URG_v1.4",
                    acceptance_state="valid",
                    source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["udg"],
                    stream_compatibility=EMERGENCY_STREAMS,
                    source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"],
                    notes=("Legacy UDG pricing year.",),
                )
                for year in ("2013", "2014", "2015", "2016", "2017", "2018", "2019")
            ),
            EmergencyClassificationVersion(
                year="2020",
                version="URG_v1.4",
                acceptance_state="transition",
                source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["udg"],
                stream_compatibility=EMERGENCY_STREAMS,
                source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"],
                notes=(
                    "Transition year before AECC shadow pricing becomes available.",
                ),
            ),
            *(
                EmergencyClassificationVersion(
                    year=year,
                    version="UDG_v1.3",
                    acceptance_state="transition",
                    source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["udg"],
                    stream_compatibility=EMERGENCY_STREAMS,
                    source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"],
                    notes=("Legacy UDG remains accepted in the transition window.",),
                )
                for year in ("2021", "2022", "2023", "2024", "2025", "2026")
            ),
        ),
    ),
    EmergencyClassificationRecord(
        system="aecc",
        display_name="AECC",
        aliases=("aecc",),
        required_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["aecc"],
        stream_compatibility=EMERGENCY_STREAMS,
        source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
        notes=(
            "AECC is the current emergency-care classification surface in this "
            "registry.",
            "Shadow-priced entries are recorded explicitly and are not translated.",
        ),
        versions=(
            *(
                EmergencyClassificationVersion(
                    year=year,
                    version=None,
                    acceptance_state="unavailable",
                    source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["aecc"],
                    stream_compatibility=EMERGENCY_STREAMS,
                    source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
                    notes=("AECC is not available in this pricing year.",),
                )
                for year in ("2013", "2014", "2015", "2016", "2017", "2018", "2019")
            ),
            EmergencyClassificationVersion(
                year="2020",
                version="v1.0_shadow",
                acceptance_state="shadow-priced",
                source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["aecc"],
                stream_compatibility=EMERGENCY_STREAMS,
                source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
                notes=("AECC v1.0 is shadow-priced in this transition year.",),
            ),
            EmergencyClassificationVersion(
                year="2021",
                version="v1.0",
                acceptance_state="valid",
                source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["aecc"],
                stream_compatibility=EMERGENCY_STREAMS,
                source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
                notes=("AECC enters active use from the 2021 pricing year.",),
            ),
            *(
                EmergencyClassificationVersion(
                    year=year,
                    version="v1.1",
                    acceptance_state="valid",
                    source_fields=EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS["aecc"],
                    stream_compatibility=EMERGENCY_STREAMS,
                    source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
                    notes=("AECC v1.1 remains the active version.",),
                )
                for year in ("2022", "2023", "2024", "2025", "2026")
            ),
        ),
    ),
)

_EMERGENCY_CLASSIFICATION_BY_SYSTEM: Final[dict[str, EmergencyClassificationRecord]] = {
    record.system: record for record in _EMERGENCY_CLASSIFICATION_RECORDS
}

EMERGENCY_CLASSIFICATION_VERSION_MATRIX: Final[dict[str, dict[str, str | None]]] = {
    record.system: {item.year: item.version for item in record.versions}
    for record in _EMERGENCY_CLASSIFICATION_RECORDS
}

EMERGENCY_TRANSITION_PERIODS: Final[tuple[EmergencyTransitionPeriod, ...]] = (
    EmergencyTransitionPeriod(
        system="udg",
        start_year="2013",
        end_year="2019",
        acceptance_state="valid",
        source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"],
        notes=("Legacy UDG years before the AECC transition window.",),
    ),
    EmergencyTransitionPeriod(
        system="udg",
        start_year="2020",
        end_year="2026",
        acceptance_state="transition",
        source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"],
        notes=("UDG remains accepted through the transition window.",),
    ),
    EmergencyTransitionPeriod(
        system="aecc",
        start_year="2020",
        end_year="2020",
        acceptance_state="shadow-priced",
        source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
        notes=("AECC is shadow-priced in the first transition year.",),
    ),
    EmergencyTransitionPeriod(
        system="aecc",
        start_year="2021",
        end_year="2026",
        acceptance_state="valid",
        source_refs=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"],
        notes=("AECC is active from the 2021 pricing year onward.",),
    ),
)


def list_emergency_classification_records() -> tuple[
    EmergencyClassificationRecord, ...
]:
    """Return all known emergency classification records."""
    return _EMERGENCY_CLASSIFICATION_RECORDS


def get_emergency_classification_record(system: str) -> EmergencyClassificationRecord:
    """Return the registry entry for an emergency classification family."""
    canonical = normalize_emergency_classification_system(system)
    return _EMERGENCY_CLASSIFICATION_BY_SYSTEM[canonical]


def get_emergency_classification_name(system: str) -> str:
    """Return the display name for an emergency classification family."""
    return get_emergency_classification_record(system).display_name


def get_emergency_supported_years(system: str) -> tuple[str, ...]:
    """Return the years where the emergency classification is available."""
    return get_emergency_classification_record(system).supported_years()


def get_emergency_transition_years(system: str) -> tuple[str, ...]:
    """Return the years where the emergency registry changes acceptance state."""
    return get_emergency_classification_record(system).transition_years()


def get_expected_emergency_classification_version(system: str, year: str) -> str | None:
    """Return the expected version for a system/year pair."""
    return get_emergency_classification_record(system).expected_version_for_year(year)


def get_emergency_classification_version(system: str, year: str) -> str | None:
    """Alias for ``get_expected_emergency_classification_version``."""
    return get_expected_emergency_classification_version(system, year)


def get_emergency_classification_status(system: str, year: str) -> AcceptanceState:
    """Return the acceptance state for a system/year pair."""
    return get_emergency_classification_record(system).acceptance_state_for_year(year)


def list_emergency_transition_periods(
    system: str | None = None,
) -> tuple[EmergencyTransitionPeriod, ...]:
    """Return the registry transition periods, optionally filtered by system."""
    if system is None:
        return EMERGENCY_TRANSITION_PERIODS
    canonical = normalize_emergency_classification_system(system)
    return tuple(
        period for period in EMERGENCY_TRANSITION_PERIODS if period.system == canonical
    )


def get_emergency_transition_period(
    system: str,
    year: str,
) -> EmergencyTransitionPeriod | None:
    """Return the transition period covering a pricing year, if any."""
    normalized_year = _normalize_year(year)
    for period in list_emergency_transition_periods(system):
        if period.covers(normalized_year):
            return period
    return None


def _validate_required_fields(
    observed_fields: Any,
    required_fields: tuple[str, ...],
) -> tuple[str, ...]:
    if isinstance(observed_fields, (str, bytes)) or not isinstance(
        observed_fields, Iterable
    ):
        raise EmergencyClassificationRegistryError(
            "observed_fields must be an iterable of emergency field names"
        )
    normalized_observed = _normalize_str_tuple(
        observed_fields, field="observed_fields", allow_empty=True
    )
    observed_set = set(normalized_observed)
    missing = tuple(field for field in required_fields if field not in observed_set)
    return missing


def _result(
    *,
    record: EmergencyClassificationRecord,
    year: str,
    declared_version: str | None,
    missing_fields: tuple[str, ...] = (),
    stream: str | None = None,
    reason: str | None = None,
) -> EmergencyClassificationCompatibilityResult:
    period = get_emergency_transition_period(record.system, year)
    acceptance_state = "unavailable" if period is None else period.acceptance_state
    compatible = reason is None and not missing_fields and declared_version is not None
    return EmergencyClassificationCompatibilityResult(
        system=record.system,
        display_name=record.display_name,
        pricing_year=_normalize_year(year),
        declared_version=declared_version,
        expected_version=record.expected_version_for_year(year),
        acceptance_state=acceptance_state,
        compatibility_state="incompatible",
        compatible=compatible,
        stream=stream,
        stream_compatibility=record.stream_compatibility,
        required_fields=record.required_fields,
        observed_fields=(),
        missing_fields=missing_fields,
        source_refs=record.source_refs,
        reason=reason,
    )


def validate_emergency_classification_compatibility(
    system: str,
    year: str,
    version: str | None,
    *,
    stream: str | None = None,
) -> EmergencyClassificationCompatibilityResult:
    """Check whether a declared version matches the registry expectation."""
    record = get_emergency_classification_record(system)
    normalized_year = _normalize_year(year)
    expected_version = record.expected_version_for_year(normalized_year)
    declared_version: str | None = None
    if version is not None:
        declared_version = _normalize_version(
            version, field="emergency_classification_version"
        )

    period = get_emergency_transition_period(record.system, normalized_year)
    acceptance_state = "unavailable" if period is None else period.acceptance_state

    if stream is not None:
        normalized_stream = _normalize_non_blank(stream, field="stream")
        if normalized_stream not in record.stream_compatibility:
            return EmergencyClassificationCompatibilityResult(
                system=record.system,
                display_name=record.display_name,
                pricing_year=normalized_year,
                declared_version=declared_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                stream=normalized_stream,
                stream_compatibility=record.stream_compatibility,
                required_fields=record.required_fields,
                observed_fields=(),
                missing_fields=(),
                source_refs=record.source_refs,
                reason=(
                    f"{record.display_name} is not compatible with stream "
                    f"{normalized_stream!r}"
                ),
            )
    else:
        normalized_stream = None

    if expected_version is None:
        reason = (
            f"{record.display_name} is not available for pricing year {normalized_year}"
        )
        return EmergencyClassificationCompatibilityResult(
            system=record.system,
            display_name=record.display_name,
            pricing_year=normalized_year,
            declared_version=declared_version,
            expected_version=None,
            acceptance_state=acceptance_state,
            compatibility_state="incompatible",
            compatible=False,
            stream=normalized_stream,
            stream_compatibility=record.stream_compatibility,
            required_fields=record.required_fields,
            observed_fields=(),
            missing_fields=(),
            source_refs=record.source_refs,
            reason=reason,
        )

    if declared_version is None:
        if expected_version is None:
            reason = (
                f"{record.display_name} is not available for pricing year "
                f"{normalized_year} and no emergency_classification_version was "
                "supplied"
            )
        else:
            reason = (
                f"{record.display_name} {normalized_year} requires an explicit "
                f"emergency_classification_version of {expected_version}"
            )
        return EmergencyClassificationCompatibilityResult(
            system=record.system,
            display_name=record.display_name,
            pricing_year=normalized_year,
            declared_version=None,
            expected_version=expected_version,
            acceptance_state=acceptance_state,
            compatibility_state="missing",
            compatible=False,
            stream=normalized_stream,
            stream_compatibility=record.stream_compatibility,
            required_fields=record.required_fields,
            observed_fields=(),
            missing_fields=(),
            source_refs=record.source_refs,
            reason=reason,
        )

    if declared_version != expected_version:
        reason = (
            f"{record.display_name} {normalized_year} expects {expected_version}, "
            f"got {declared_version}"
        )
        return EmergencyClassificationCompatibilityResult(
            system=record.system,
            display_name=record.display_name,
            pricing_year=normalized_year,
            declared_version=declared_version,
            expected_version=expected_version,
            acceptance_state=acceptance_state,
            compatibility_state="incompatible",
            compatible=False,
            stream=normalized_stream,
            stream_compatibility=record.stream_compatibility,
            required_fields=record.required_fields,
            observed_fields=(),
            missing_fields=(),
            source_refs=record.source_refs,
            reason=reason,
        )

    compatibility_state: Literal["valid", "transition", "shadow-priced"]
    if acceptance_state == "unavailable":
        raise EmergencyClassificationRegistryError(
            "compatible emergency classification cannot be unavailable"
        )
    else:
        compatibility_state = acceptance_state

    return EmergencyClassificationCompatibilityResult(
        system=record.system,
        display_name=record.display_name,
        pricing_year=normalized_year,
        declared_version=declared_version,
        expected_version=expected_version,
        acceptance_state=acceptance_state,
        compatibility_state=compatibility_state,
        compatible=True,
        stream=normalized_stream,
        stream_compatibility=record.stream_compatibility,
        required_fields=record.required_fields,
        observed_fields=(),
        missing_fields=(),
        source_refs=record.source_refs,
        reason=None,
    )


def validate_emergency_input(
    system: str,
    year: str,
    observed_fields: Any,
    *,
    version: str | None,
    stream: str | None = None,
) -> EmergencyClassificationCompatibilityResult:
    """Validate required emergency fields and declared version compatibility."""
    record = get_emergency_classification_record(system)
    normalized_year = _normalize_year(year)
    missing_fields = _validate_required_fields(observed_fields, record.required_fields)
    compatibility = validate_emergency_classification_compatibility(
        record.system,
        normalized_year,
        version,
        stream=stream,
    )
    if missing_fields:
        reason = "missing required emergency classification fields: " + ", ".join(
            missing_fields
        )
        return EmergencyClassificationCompatibilityResult(
            system=compatibility.system,
            display_name=compatibility.display_name,
            pricing_year=compatibility.pricing_year,
            declared_version=compatibility.declared_version,
            expected_version=compatibility.expected_version,
            acceptance_state=compatibility.acceptance_state,
            compatibility_state="missing",
            compatible=False,
            stream=compatibility.stream,
            stream_compatibility=compatibility.stream_compatibility,
            required_fields=compatibility.required_fields,
            observed_fields=(
                _normalize_str_tuple(
                    observed_fields, field="observed_fields", allow_empty=True
                )
                if not isinstance(observed_fields, (str, bytes))
                else ()
            ),
            missing_fields=missing_fields,
            source_refs=compatibility.source_refs,
            reason=reason,
        )

    return EmergencyClassificationCompatibilityResult(
        system=compatibility.system,
        display_name=compatibility.display_name,
        pricing_year=compatibility.pricing_year,
        declared_version=compatibility.declared_version,
        expected_version=compatibility.expected_version,
        acceptance_state=compatibility.acceptance_state,
        compatibility_state=compatibility.compatibility_state,
        compatible=compatibility.compatible,
        stream=compatibility.stream,
        stream_compatibility=compatibility.stream_compatibility,
        required_fields=compatibility.required_fields,
        observed_fields=(
            _normalize_str_tuple(
                observed_fields, field="observed_fields", allow_empty=True
            )
            if not isinstance(observed_fields, (str, bytes))
            else ()
        ),
        missing_fields=compatibility.missing_fields,
        source_refs=compatibility.source_refs,
        reason=compatibility.reason,
    )


def validate_aecc_input(
    observed_fields: Any,
    *,
    year: str,
    version: str | None,
    stream: str | None = None,
) -> EmergencyClassificationCompatibilityResult:
    """Validate an AECC emergency classification input surface."""
    return validate_emergency_input(
        "aecc",
        year,
        observed_fields,
        version=version,
        stream=stream,
    )


def validate_udg_input(
    observed_fields: Any,
    *,
    year: str,
    version: str | None,
    stream: str | None = None,
) -> EmergencyClassificationCompatibilityResult:
    """Validate a UDG emergency classification input surface."""
    return validate_emergency_input(
        "udg",
        year,
        observed_fields,
        version=version,
        stream=stream,
    )


def ensure_emergency_classification_compatibility(
    system: str,
    year: str,
    version: str | None,
    *,
    stream: str | None = None,
) -> EmergencyClassificationCompatibilityResult:
    """Raise when a declared emergency classification version is incompatible."""
    result = validate_emergency_classification_compatibility(
        system,
        year,
        version,
        stream=stream,
    )
    if not result.compatible:
        raise EmergencyClassificationRegistryError(
            result.reason or "emergency classification is incompatible"
        )
    return result
