"""Conservative AR-DRG grouper integration helpers.

This module intentionally does not implement proprietary grouping logic.
It only provides:

- metadata for user-supplied local external grouper references;
- provenance containers for precomputed or externally derived AR-DRG values;
- compatibility validation against the repository's version registry.

The goal is to support admitted-acute workflows without embedding licensed
grouping tables or a bundled grouper implementation.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Final, Literal

from .ar_drg_mapping_registry import (
    ARDRGMappingCompatibilityResult,
    ARDRGMappingRecord,
    ARDRGMappingRegistryError,
    get_ar_drg_mapping_record,
    get_expected_coding_set_versions,
)

__all__ = [
    "ARDRGGroupRecord",
    "ARDRGGrouperError",
    "ARDRGGrouperProvenance",
    "ARDRGGrouperReference",
    "ARDRGGrouperVersionWindow",
    "build_ar_drg_external_reference",
    "build_ar_drg_group_record_from_reference",
    "build_ar_drg_precomputed_group_record",
    "build_ar_drg_provenance",
    "ensure_ar_drg_grouper_compatibility",
    "hash_ar_drg_grouping_payload",
    "validate_ar_drg_grouper_compatibility",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REFERENCE_TYPES: Final[frozenset[str]] = frozenset(
    {"local_command", "local_service", "file_exchange"}
)
_ACCESS_MODES: Final[frozenset[str]] = frozenset({"user_supplied", "local_only"})
_REFERENCE_STATUSES: Final[frozenset[str]] = frozenset({"resolved", "unresolved"})
_LICENSE_BOUNDARIES: Final[frozenset[str]] = frozenset(
    {"local-only", "restricted", "metadata-only"}
)
_SOURCE_MODES: Final[frozenset[str]] = frozenset({"precomputed", "external-reference"})
_EXPECTED_SYSTEMS: Final[tuple[str, ...]] = (
    "ar_drg",
    "icd_10_am",
    "achi",
    "acs",
)


class ARDRGGrouperError(ARDRGMappingRegistryError):
    """Raised when grouper metadata is incomplete or incompatible."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ARDRGGrouperError(f"{field} must be a string")
    if not value:
        raise ARDRGGrouperError(f"{field} must not be blank")
    if value.strip() != value:
        raise ARDRGGrouperError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise ARDRGGrouperError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str, *, field: str) -> str:
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise ARDRGGrouperError(f"{field} must be a deterministic version label")
    return normalized


def _normalize_optional_version(version: str | None, *, field: str) -> str | None:
    if version is None:
        return None
    return _normalize_version(version, field=field)


def _normalize_str_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise ARDRGGrouperError(f"{field} must be a tuple or list of non-empty strings")
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise ARDRGGrouperError(f"{field} must not contain duplicates")
        seen.add(text)
        normalized.append(text)
    return tuple(normalized)


def _normalize_iso_datetime(value: str) -> str:
    normalized = _normalize_non_blank(value, field="generated_at")
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:  # pragma: no cover - defensive
        raise ARDRGGrouperError("generated_at must be an ISO-8601 timestamp") from exc
    return normalized


def _normalize_sha256(value: str) -> str:
    normalized = _normalize_non_blank(value, field="input_sha256").lower()
    if not _SHA256_RE.fullmatch(normalized):
        raise ARDRGGrouperError(
            "input_sha256 must be a lowercase 64-character sha256 hex digest"
        )
    return normalized


def _utc_now_isoformat() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def hash_ar_drg_grouping_payload(payload: Any) -> str:
    """Return a stable sha256 hash for a JSON-serialisable payload."""
    digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()
    return digest


@dataclass(frozen=True, slots=True)
class ARDRGGrouperVersionWindow:
    """Supported pricing-year and classification-version binding."""

    pricing_year: str
    ar_drg_version: str
    icd_10_am_version: str
    achi_version: str
    acs_version: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        object.__setattr__(
            self,
            "ar_drg_version",
            _normalize_version(self.ar_drg_version, field="ar_drg_version"),
        )
        object.__setattr__(
            self,
            "icd_10_am_version",
            _normalize_version(self.icd_10_am_version, field="icd_10_am_version"),
        )
        object.__setattr__(
            self,
            "achi_version",
            _normalize_version(self.achi_version, field="achi_version"),
        )
        object.__setattr__(
            self,
            "acs_version",
            _normalize_version(self.acs_version, field="acs_version"),
        )

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serialisable version binding."""
        return {
            "pricing_year": self.pricing_year,
            "ar_drg_version": self.ar_drg_version,
            "icd_10_am_version": self.icd_10_am_version,
            "achi_version": self.achi_version,
            "acs_version": self.acs_version,
        }


def _coerce_version_window(
    value: ARDRGGrouperVersionWindow | Mapping[str, Any],
) -> ARDRGGrouperVersionWindow:
    if isinstance(value, ARDRGGrouperVersionWindow):
        return value
    if not isinstance(value, Mapping):
        raise ARDRGGrouperError(
            "supported_versions must contain version window records or mappings"
        )
    return ARDRGGrouperVersionWindow(
        pricing_year=str(value["pricing_year"]),
        ar_drg_version=str(value["ar_drg_version"]),
        icd_10_am_version=str(value["icd_10_am_version"]),
        achi_version=str(value["achi_version"]),
        acs_version=str(value["acs_version"]),
    )


@dataclass(frozen=True, slots=True)
class ARDRGGrouperReference:
    """Local placeholder for a user-supplied external grouper reference."""

    reference_id: str
    reference_type: Literal["local_command", "local_service", "file_exchange"]
    access_mode: Literal["user_supplied", "local_only"]
    license_boundary: Literal["local-only", "restricted", "metadata-only"]
    status: Literal["resolved", "unresolved"]
    command: str | None
    reference_uri: str | None
    local_path_hint: str | None
    supported_versions: tuple[ARDRGGrouperVersionWindow, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reference_id",
            _normalize_non_blank(self.reference_id, field="reference_id"),
        )
        if self.reference_type not in _REFERENCE_TYPES:
            raise ARDRGGrouperError(
                f"unsupported reference_type {self.reference_type!r}"
            )
        if self.access_mode not in _ACCESS_MODES:
            raise ARDRGGrouperError(f"unsupported access_mode {self.access_mode!r}")
        if self.license_boundary not in _LICENSE_BOUNDARIES:
            raise ARDRGGrouperError(
                f"unsupported license_boundary {self.license_boundary!r}"
            )
        if self.status not in _REFERENCE_STATUSES:
            raise ARDRGGrouperError(f"unsupported status {self.status!r}")
        if self.command is not None:
            object.__setattr__(
                self, "command", _normalize_non_blank(self.command, field="command")
            )
        if self.reference_uri is not None:
            object.__setattr__(
                self,
                "reference_uri",
                _normalize_non_blank(self.reference_uri, field="reference_uri"),
            )
        if self.local_path_hint is not None:
            object.__setattr__(
                self,
                "local_path_hint",
                _normalize_non_blank(self.local_path_hint, field="local_path_hint"),
            )

        windows = tuple(
            _coerce_version_window(item) for item in self.supported_versions
        )
        if not windows:
            raise ARDRGGrouperError("supported_versions must not be empty")
        year_index: set[str] = set()
        for window in windows:
            if window.pricing_year in year_index:
                raise ARDRGGrouperError(
                    "supported_versions must not contain duplicate pricing_year values"
                )
            year_index.add(window.pricing_year)
        object.__setattr__(self, "supported_versions", windows)
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes"),
        )

        if self.reference_type == "local_command":
            if self.command is None:
                raise ARDRGGrouperError(
                    "local_command references require a command string"
                )
        elif self.reference_type == "local_service":
            if self.reference_uri is None:
                raise ARDRGGrouperError(
                    "local_service references require a reference_uri"
                )
        elif (
            self.reference_type == "file_exchange"
            and self.local_path_hint is None
            and self.reference_uri is None
        ):
            raise ARDRGGrouperError(
                "file_exchange references require a local_path_hint or reference_uri"
            )

    def supported_years(self) -> tuple[str, ...]:
        """Return the pricing years declared by this reference."""
        return tuple(window.pricing_year for window in self.supported_versions)

    def version_window_for_year(self, year: str) -> ARDRGGrouperVersionWindow | None:
        """Return the declared version window for a pricing year, if present."""
        normalized_year = _normalize_year(year)
        for window in self.supported_versions:
            if window.pricing_year == normalized_year:
                return window
        return None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable external reference manifest."""
        return {
            "reference_id": self.reference_id,
            "reference_type": self.reference_type,
            "access_mode": self.access_mode,
            "license_boundary": self.license_boundary,
            "status": self.status,
            "command": self.command,
            "reference_uri": self.reference_uri,
            "local_path_hint": self.local_path_hint,
            "supported_versions": [
                window.to_dict() for window in self.supported_versions
            ],
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ARDRGGrouperProvenance:
    """Audit trail for a precomputed or externally derived AR-DRG record."""

    pricing_year: str
    source_mode: Literal["precomputed", "external-reference"]
    ar_drg_version: str
    icd_10_am_version: str
    achi_version: str
    acs_version: str
    grouper_version: str | None
    input_sha256: str
    generated_at: str
    external_reference_id: str | None
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        if self.source_mode not in _SOURCE_MODES:
            raise ARDRGGrouperError(f"unsupported source_mode {self.source_mode!r}")
        object.__setattr__(
            self,
            "ar_drg_version",
            _normalize_version(self.ar_drg_version, field="ar_drg_version"),
        )
        object.__setattr__(
            self,
            "icd_10_am_version",
            _normalize_version(self.icd_10_am_version, field="icd_10_am_version"),
        )
        object.__setattr__(
            self,
            "achi_version",
            _normalize_version(self.achi_version, field="achi_version"),
        )
        object.__setattr__(
            self,
            "acs_version",
            _normalize_version(self.acs_version, field="acs_version"),
        )
        if self.grouper_version is not None:
            object.__setattr__(
                self,
                "grouper_version",
                _normalize_version(self.grouper_version, field="grouper_version"),
            )
        object.__setattr__(self, "input_sha256", _normalize_sha256(self.input_sha256))
        object.__setattr__(
            self, "generated_at", _normalize_iso_datetime(self.generated_at)
        )
        if self.external_reference_id is not None:
            object.__setattr__(
                self,
                "external_reference_id",
                _normalize_non_blank(
                    self.external_reference_id, field="external_reference_id"
                ),
            )
        if self.notes:
            object.__setattr__(
                self, "notes", _normalize_str_tuple(self.notes, field="notes")
            )
        else:
            object.__setattr__(self, "notes", tuple())

        if self.source_mode == "external-reference":
            if self.grouper_version is None:
                raise ARDRGGrouperError(
                    "external-reference provenance requires grouper_version"
                )
            if self.external_reference_id is None:
                raise ARDRGGrouperError(
                    "external-reference provenance requires external_reference_id"
                )
        elif self.external_reference_id is not None:
            raise ARDRGGrouperError(
                "precomputed provenance must not declare external_reference_id"
            )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable provenance record."""
        return {
            "pricing_year": self.pricing_year,
            "source_mode": self.source_mode,
            "ar_drg_version": self.ar_drg_version,
            "icd_10_am_version": self.icd_10_am_version,
            "achi_version": self.achi_version,
            "acs_version": self.acs_version,
            "grouper_version": self.grouper_version,
            "input_sha256": self.input_sha256,
            "generated_at": self.generated_at,
            "external_reference_id": self.external_reference_id,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ARDRGGroupRecord:
    """Single AR-DRG output row with conservative provenance metadata."""

    drg: str
    provenance: ARDRGGrouperProvenance
    episode_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "drg", _normalize_non_blank(self.drg, field="drg"))
        if self.episode_id is not None:
            object.__setattr__(
                self,
                "episode_id",
                _normalize_non_blank(self.episode_id, field="episode_id"),
            )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable grouped record."""
        return {
            "drg": self.drg,
            "episode_id": self.episode_id,
            "provenance": self.provenance.to_dict(),
        }


def _expected_versions(year: str) -> dict[str, str | None]:
    normalized_year = _normalize_year(year)
    return get_expected_coding_set_versions(normalized_year)


def _selected_versions_from_reference(
    reference: ARDRGGrouperReference, year: str
) -> dict[str, str | None] | None:
    window = reference.version_window_for_year(year)
    if window is None:
        return None
    return {
        "ar_drg": window.ar_drg_version,
        "icd_10_am": window.icd_10_am_version,
        "achi": window.achi_version,
        "acs": window.acs_version,
    }


def _normalize_declared_versions(
    *,
    ar_drg_version: str | None,
    icd_10_am_version: str | None,
    achi_version: str | None,
    acs_version: str | None,
) -> dict[str, str | None]:
    return {
        "ar_drg": _normalize_optional_version(ar_drg_version, field="ar_drg_version"),
        "icd_10_am": _normalize_optional_version(
            icd_10_am_version, field="icd_10_am_version"
        ),
        "achi": _normalize_optional_version(achi_version, field="achi_version"),
        "acs": _normalize_optional_version(acs_version, field="acs_version"),
    }


def _compatibility_result(
    *,
    year: str,
    declared_versions: dict[str, str | None],
    expected_versions: dict[str, str | None],
    record: ARDRGMappingRecord | None,
    reason: str | None,
) -> ARDRGMappingCompatibilityResult:
    compatible = reason is None
    return ARDRGMappingCompatibilityResult(
        pricing_year=_normalize_year(year),
        declared_versions=declared_versions,
        expected_versions=expected_versions,
        compatible=compatible,
        reason=reason,
        record=record,
    )


def validate_ar_drg_grouper_compatibility(
    year: str,
    *,
    ar_drg_version: str | None = None,
    icd_10_am_version: str | None = None,
    achi_version: str | None = None,
    acs_version: str | None = None,
    reference: ARDRGGrouperReference | None = None,
) -> ARDRGMappingCompatibilityResult:
    """Validate a precomputed or external-reference AR-DRG version set.

    The function is intentionally conservative. It only checks version
    alignment and registry provenance. It does not execute a grouper.
    """
    normalized_year = _normalize_year(year)
    expected_versions = _expected_versions(normalized_year)
    record = get_ar_drg_mapping_record(normalized_year)

    if reference is not None:
        reference_versions = _selected_versions_from_reference(
            reference, normalized_year
        )
        if reference_versions is None:
            return _compatibility_result(
                year=normalized_year,
                declared_versions={
                    "ar_drg": None,
                    "icd_10_am": None,
                    "achi": None,
                    "acs": None,
                },
                expected_versions=expected_versions,
                record=record,
                reason=(
                    f"external grouper reference {reference.reference_id!r} does not "
                    "declare a supported version window for pricing year "
                    f"{normalized_year}"
                ),
            )
        explicit_versions = _normalize_declared_versions(
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )
        explicit_values = [
            value for value in explicit_versions.values() if value is not None
        ]
        if explicit_values and any(
            explicit_versions[system] != reference_versions[system]
            for system in _EXPECTED_SYSTEMS
            if explicit_versions[system] is not None
        ):
            return _compatibility_result(
                year=normalized_year,
                declared_versions=explicit_versions,
                expected_versions=expected_versions,
                record=record,
                reason=(
                    "explicit versions must match the selected external reference "
                    f"window for pricing year {normalized_year}"
                ),
            )
        declared_versions = reference_versions
    else:
        declared_versions = _normalize_declared_versions(
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )
        missing = [
            system for system, value in declared_versions.items() if value is None
        ]
        if missing:
            return _compatibility_result(
                year=normalized_year,
                declared_versions=declared_versions,
                expected_versions=expected_versions,
                record=record,
                reason=("missing declared version(s): " + ", ".join(sorted(missing))),
            )

    mismatches = [
        f"{system}={declared_versions[system]!r} "
        f"(expected {expected_versions[system]!r})"
        for system in _EXPECTED_SYSTEMS
        if declared_versions[system] != expected_versions[system]
    ]
    if mismatches:
        return _compatibility_result(
            year=normalized_year,
            declared_versions=declared_versions,
            expected_versions=expected_versions,
            record=record,
            reason="AR-DRG grouping version set is incompatible: "
            + ", ".join(mismatches),
        )

    if record is not None:
        return record.validate_full_set(
            ar_drg_version=declared_versions["ar_drg"],
            icd_10_am_version=declared_versions["icd_10_am"],
            achi_version=declared_versions["achi"],
            acs_version=declared_versions["acs"],
        )

    return _compatibility_result(
        year=normalized_year,
        declared_versions=declared_versions,
        expected_versions=expected_versions,
        record=None,
        reason=None,
    )


def ensure_ar_drg_grouper_compatibility(
    year: str,
    *,
    ar_drg_version: str | None = None,
    icd_10_am_version: str | None = None,
    achi_version: str | None = None,
    acs_version: str | None = None,
    reference: ARDRGGrouperReference | None = None,
) -> ARDRGMappingCompatibilityResult:
    """Raise when an AR-DRG grouper version set is incompatible."""
    result = validate_ar_drg_grouper_compatibility(
        year,
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
        reference=reference,
    )
    if not result.compatible:
        raise ARDRGGrouperError(result.reason or "AR-DRG grouper metadata is invalid")
    return result


def build_ar_drg_external_reference(
    *,
    reference_id: str,
    reference_type: Literal["local_command", "local_service", "file_exchange"],
    access_mode: Literal["user_supplied", "local_only"] = "user_supplied",
    license_boundary: Literal[
        "local-only",
        "restricted",
        "metadata-only",
    ] = "local-only",
    status: Literal["resolved", "unresolved"] = "unresolved",
    command: str | None = None,
    reference_uri: str | None = None,
    local_path_hint: str | None = None,
    supported_versions: Iterable[ARDRGGrouperVersionWindow | Mapping[str, Any]],
    notes: Iterable[str] = (),
) -> ARDRGGrouperReference:
    """Build a conservative local external grouper reference manifest."""
    windows = tuple(_coerce_version_window(item) for item in supported_versions)
    return ARDRGGrouperReference(
        reference_id=reference_id,
        reference_type=reference_type,
        access_mode=access_mode,
        license_boundary=license_boundary,
        status=status,
        command=command,
        reference_uri=reference_uri,
        local_path_hint=local_path_hint,
        supported_versions=windows,
        notes=tuple(notes),
    )


def build_ar_drg_provenance(
    *,
    year: str,
    ar_drg_version: str,
    icd_10_am_version: str,
    achi_version: str,
    acs_version: str,
    input_sha256: str,
    source_mode: Literal["precomputed", "external-reference"] = "precomputed",
    grouper_version: str | None = None,
    external_reference_id: str | None = None,
    generated_at: str | None = None,
    notes: Iterable[str] = (),
    reference: ARDRGGrouperReference | None = None,
) -> ARDRGGrouperProvenance:
    """Build provenance after validating a year/version binding.

    ``reference`` is optional and only used to anchor validation when the
    provenance is derived from a local external grouper reference.
    """
    if reference is not None:
        ensure_ar_drg_grouper_compatibility(
            year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
            reference=reference,
        )
    else:
        ensure_ar_drg_grouper_compatibility(
            year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )

    return ARDRGGrouperProvenance(
        pricing_year=year,
        source_mode=source_mode,
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
        grouper_version=grouper_version,
        input_sha256=input_sha256,
        generated_at=generated_at or _utc_now_isoformat(),
        external_reference_id=external_reference_id,
        notes=tuple(notes),
    )


def build_ar_drg_precomputed_group_record(
    drg: str,
    *,
    year: str,
    ar_drg_version: str,
    icd_10_am_version: str,
    achi_version: str,
    acs_version: str,
    input_sha256: str,
    episode_id: str | None = None,
    grouper_version: str | None = None,
    generated_at: str | None = None,
    notes: Iterable[str] = (),
) -> ARDRGGroupRecord:
    """Build a grouped record when AR-DRG values are already precomputed."""
    provenance = build_ar_drg_provenance(
        year=year,
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
        input_sha256=input_sha256,
        source_mode="precomputed",
        grouper_version=grouper_version,
        generated_at=generated_at,
        notes=notes,
    )
    return ARDRGGroupRecord(drg=drg, episode_id=episode_id, provenance=provenance)


def build_ar_drg_group_record_from_reference(
    drg: str,
    *,
    year: str,
    reference: ARDRGGrouperReference,
    input_sha256: str,
    grouper_version: str,
    episode_id: str | None = None,
    generated_at: str | None = None,
    notes: Iterable[str] = (),
) -> ARDRGGroupRecord:
    """Build a grouped record derived from a local external grouper reference."""
    result = validate_ar_drg_grouper_compatibility(year, reference=reference)
    if not result.compatible:
        raise ARDRGGrouperError(
            result.reason or "external grouper reference is invalid"
        )
    provenance = build_ar_drg_provenance(
        year=year,
        ar_drg_version=str(result.declared_versions["ar_drg"]),
        icd_10_am_version=str(result.declared_versions["icd_10_am"]),
        achi_version=str(result.declared_versions["achi"]),
        acs_version=str(result.declared_versions["acs"]),
        input_sha256=input_sha256,
        source_mode="external-reference",
        grouper_version=grouper_version,
        external_reference_id=reference.reference_id,
        generated_at=generated_at,
        notes=notes,
        reference=reference,
    )
    return ARDRGGroupRecord(drg=drg, episode_id=episode_id, provenance=provenance)
