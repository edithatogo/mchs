"""Metadata-only emergency grouper integration helpers.

This module defines the safe boundary for emergency UDG/AECC outputs when the
classification has already been produced or when the user supplies a local
command, service, or file-exchange reference. It does not implement any
grouper logic or mapping crosswalks.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final, Literal
from urllib.parse import urlsplit

from .emergency_transition_registry import (
    EMERGENCY_STREAMS,
    EmergencyClassificationRegistryError,
    get_emergency_classification_name,
    get_emergency_classification_record,
    get_emergency_classification_status,
    get_expected_emergency_classification_version,
    list_emergency_classification_records,
    normalize_emergency_classification_system,
    validate_emergency_classification_compatibility,
)

__all__ = [
    "EMERGENCY_GROUPER_COMPATIBILITY_STATES",
    "EMERGENCY_GROUPER_MAPPING_STAGES",
    "EMERGENCY_GROUPER_REFERENCE_TYPES",
    "EMERGENCY_GROUPER_SOURCE_MODES",
    "EMERGENCY_GROUPER_VERSION_MATRIX",
    "EmergencyGrouperCompatibilityResult",
    "EmergencyGrouperError",
    "EmergencyGrouperOutputRecord",
    "EmergencyGrouperProvenance",
    "EmergencyGrouperReference",
    "EmergencyGrouperVersionWindow",
    "build_emergency_external_reference",
    "build_emergency_output_record_from_reference",
    "build_emergency_precomputed_output_record",
    "build_emergency_provenance",
    "ensure_emergency_grouper_compatibility",
    "validate_emergency_grouper_compatibility",
]

EMERGENCY_GROUPER_REFERENCE_TYPES: Final[tuple[str, ...]] = (
    "local_command",
    "local_service",
    "file_exchange",
)
EMERGENCY_GROUPER_SOURCE_MODES: Final[tuple[str, ...]] = (
    "precomputed",
    "external-reference",
)
EMERGENCY_GROUPER_MAPPING_STAGES: Final[tuple[str, ...]] = (
    "unknown",
    "pre-mapping",
    "post-mapping",
)
EMERGENCY_GROUPER_COMPATIBILITY_STATES: Final[tuple[str, ...]] = (
    "valid",
    "transition",
    "shadow-priced",
    "missing",
    "incompatible",
    "trusted-precomputed",
)
_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_REFERENCE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_LOCAL_HOSTS: Final[frozenset[str]] = frozenset({"localhost", "127.0.0.1", "::1"})
_SUPPORTED_SCHEMES: Final[frozenset[str]] = frozenset({"http", "https", "file"})


class EmergencyGrouperError(EmergencyClassificationRegistryError):
    """Raised when the emergency grouper integration metadata is invalid."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise EmergencyGrouperError(f"{field} must be a string")
    if not value:
        raise EmergencyGrouperError(f"{field} must not be blank")
    if value.strip() != value:
        raise EmergencyGrouperError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise EmergencyGrouperError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str, *, field: str) -> str:
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise EmergencyGrouperError(f"{field} must be a deterministic version label")
    return normalized


def _normalize_str_tuple(
    value: Any,
    *,
    field: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise EmergencyGrouperError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise EmergencyGrouperError(f"{field} must not contain duplicates")
        seen.add(text)
        normalized.append(text)
    if not normalized and not allow_empty:
        raise EmergencyGrouperError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_streams(streams: Any) -> tuple[str, ...]:
    normalized = _normalize_str_tuple(streams, field="stream_compatibility")
    unknown = tuple(stream for stream in normalized if stream not in EMERGENCY_STREAMS)
    if unknown:
        raise EmergencyGrouperError(
            "stream_compatibility contains unsupported streams: " + ", ".join(unknown)
        )
    return normalized


def _normalize_iso_datetime(value: Any) -> str:
    normalized = _normalize_non_blank(value, field="generated_at")
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:  # pragma: no cover - defensive
        raise EmergencyGrouperError(
            "generated_at must be an ISO-8601 timestamp"
        ) from exc
    return normalized


def _normalize_sha256(value: Any) -> str:
    normalized = _normalize_non_blank(value, field="input_sha256").lower()
    if not _SHA256_RE.fullmatch(normalized):
        raise EmergencyGrouperError(
            "input_sha256 must be a lowercase 64-character sha256 hex digest"
        )
    return normalized


def _normalize_relative_path(path: str | Path, *, field: str) -> str:
    candidate = path if isinstance(path, Path) else Path(path)
    raw = candidate.as_posix()
    if not raw or raw == ".":
        raise EmergencyGrouperError(f"{field} must not be blank")
    if candidate.is_absolute():
        raise EmergencyGrouperError(f"{field} must be a relative path")
    if any(part == ".." for part in candidate.parts):
        raise EmergencyGrouperError(f"{field} must not contain parent traversal")
    return raw


def _normalize_local_reference_uri(value: Any, *, field: str) -> str:
    text = _normalize_non_blank(value, field=field)
    parsed = urlsplit(text)
    if not parsed.scheme:
        return _normalize_relative_path(text, field=field)
    if parsed.scheme not in _SUPPORTED_SCHEMES:
        raise EmergencyGrouperError(
            f"{field} must use one of {sorted(_SUPPORTED_SCHEMES)} or a relative path"
        )
    if parsed.scheme in {"http", "https"}:
        host = parsed.hostname
        if host not in _LOCAL_HOSTS:
            raise EmergencyGrouperError(
                f"{field} must point to a local host when using http(s)"
            )
    return text


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _compute_checksum(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


EMERGENCY_GROUPER_VERSION_MATRIX: Final[dict[str, dict[str, str | None]]] = {
    record.system: {item.year: item.version for item in record.versions}
    for record in list_emergency_classification_records()
}


@dataclass(frozen=True, slots=True)
class EmergencyGrouperVersionWindow:
    """Supported pricing-year and emergency-classification version binding."""

    system: str
    pricing_year: str
    emergency_classification_version: str
    stream_compatibility: tuple[str, ...]
    source_refs: tuple[str, ...]
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "system",
            normalize_emergency_classification_system(self.system),
        )
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        object.__setattr__(
            self,
            "emergency_classification_version",
            _normalize_version(
                self.emergency_classification_version,
                field="emergency_classification_version",
            ),
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

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "pricing_year": self.pricing_year,
            "emergency_classification_version": self.emergency_classification_version,
            "stream_compatibility": list(self.stream_compatibility),
            "source_refs": list(self.source_refs),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class EmergencyGrouperReference:
    """Local reference manifest for an emergency grouper or mapping service."""

    reference_id: str
    reference_type: Literal["local_command", "local_service", "file_exchange"]
    access_mode: Literal["user_supplied", "local_only"]
    license_boundary: Literal["local-only", "restricted", "metadata-only"]
    status: Literal["resolved", "unresolved"]
    command: str | None
    reference_uri: str | None
    local_path_hint: str | None
    supported_versions: tuple[EmergencyGrouperVersionWindow, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "reference_id",
            _normalize_non_blank(self.reference_id, field="reference_id"),
        )
        if not _REFERENCE_ID_RE.fullmatch(self.reference_id):
            raise EmergencyGrouperError(
                "reference_id must be lowercase snake_case and deterministic"
            )
        if self.reference_type not in EMERGENCY_GROUPER_REFERENCE_TYPES:
            raise EmergencyGrouperError(
                f"unsupported reference_type {self.reference_type!r}"
            )
        if self.access_mode not in {"user_supplied", "local_only"}:
            raise EmergencyGrouperError(f"unsupported access_mode {self.access_mode!r}")
        if self.license_boundary not in {"local-only", "restricted", "metadata-only"}:
            raise EmergencyGrouperError(
                f"unsupported license_boundary {self.license_boundary!r}"
            )
        if self.status not in {"resolved", "unresolved"}:
            raise EmergencyGrouperError(f"unsupported status {self.status!r}")
        if self.command is not None:
            object.__setattr__(
                self, "command", _normalize_non_blank(self.command, field="command")
            )
        if self.reference_uri is not None:
            object.__setattr__(
                self,
                "reference_uri",
                _normalize_local_reference_uri(
                    self.reference_uri, field="reference_uri"
                ),
            )
        if self.local_path_hint is not None:
            object.__setattr__(
                self,
                "local_path_hint",
                _normalize_relative_path(self.local_path_hint, field="local_path_hint"),
            )

        windows = tuple(
            _coerce_version_window(item) for item in self.supported_versions
        )
        if not windows:
            raise EmergencyGrouperError("supported_versions must not be empty")
        year_index: set[tuple[str, str]] = set()
        for window in windows:
            key = (window.system, window.pricing_year)
            if key in year_index:
                raise EmergencyGrouperError(
                    "supported_versions must not contain duplicate system/year values"
                )
            year_index.add(key)
        object.__setattr__(self, "supported_versions", windows)
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes", allow_empty=True),
        )

        if self.reference_type == "local_command":
            if self.command is None:
                raise EmergencyGrouperError(
                    "local_command references require a command string"
                )
        elif self.reference_type == "local_service":
            if self.reference_uri is None:
                raise EmergencyGrouperError(
                    "local_service references require a reference_uri"
                )
        elif (
            self.reference_type == "file_exchange"
            and self.local_path_hint is None
            and self.reference_uri is None
        ):
            raise EmergencyGrouperError(
                "file_exchange references require a local_path_hint or reference_uri"
            )

    def version_window_for_year(
        self, system: str, year: str
    ) -> EmergencyGrouperVersionWindow | None:
        normalized_system = normalize_emergency_classification_system(system)
        normalized_year = _normalize_year(year)
        for window in self.supported_versions:
            if (
                window.system == normalized_system
                and window.pricing_year == normalized_year
            ):
                return window
        return None

    def to_dict(self) -> dict[str, object]:
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
class EmergencyGrouperProvenance:
    """Audit trail for a precomputed or externally derived emergency output."""

    system: str
    pricing_year: str
    stream: str
    emergency_classification_version: str
    source_mode: Literal["precomputed", "external-reference"]
    tool_id: str | None
    tool_version: str | None
    table_version: str
    input_sha256: str
    generated_at: str
    mapping_stage: Literal["unknown", "pre-mapping", "post-mapping"]
    mapping_bundle_id: str | None
    mapping_bundle_version: str | None
    external_reference_id: str | None
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "system",
            normalize_emergency_classification_system(self.system),
        )
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        object.__setattr__(
            self,
            "stream",
            _normalize_non_blank(self.stream, field="stream"),
        )
        if self.stream not in EMERGENCY_STREAMS:
            raise EmergencyGrouperError(
                "stream must be one of the emergency transition registry streams"
            )
        object.__setattr__(
            self,
            "emergency_classification_version",
            _normalize_version(
                self.emergency_classification_version,
                field="emergency_classification_version",
            ),
        )
        if self.source_mode not in EMERGENCY_GROUPER_SOURCE_MODES:
            raise EmergencyGrouperError(f"unsupported source_mode {self.source_mode!r}")
        if self.tool_id is not None:
            object.__setattr__(
                self, "tool_id", _normalize_non_blank(self.tool_id, field="tool_id")
            )
        if self.tool_version is not None:
            object.__setattr__(
                self,
                "tool_version",
                _normalize_version(self.tool_version, field="tool_version"),
            )
        object.__setattr__(
            self,
            "table_version",
            _normalize_version(self.table_version, field="table_version"),
        )
        object.__setattr__(self, "input_sha256", _normalize_sha256(self.input_sha256))
        object.__setattr__(
            self,
            "generated_at",
            _normalize_iso_datetime(self.generated_at),
        )
        if self.mapping_stage not in EMERGENCY_GROUPER_MAPPING_STAGES:
            raise EmergencyGrouperError(
                f"unsupported mapping_stage {self.mapping_stage!r}"
            )
        if self.mapping_bundle_id is not None:
            object.__setattr__(
                self,
                "mapping_bundle_id",
                _normalize_non_blank(self.mapping_bundle_id, field="mapping_bundle_id"),
            )
        if self.mapping_bundle_version is not None:
            object.__setattr__(
                self,
                "mapping_bundle_version",
                _normalize_version(
                    self.mapping_bundle_version, field="mapping_bundle_version"
                ),
            )
        if self.external_reference_id is not None:
            object.__setattr__(
                self,
                "external_reference_id",
                _normalize_non_blank(
                    self.external_reference_id, field="external_reference_id"
                ),
            )
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes", allow_empty=True),
        )
        if self.source_mode == "external-reference":
            if self.tool_id is None or self.tool_version is None:
                raise EmergencyGrouperError(
                    "external-reference provenance requires tool_id and tool_version"
                )
            if self.external_reference_id is None:
                raise EmergencyGrouperError(
                    "external-reference provenance requires external_reference_id"
                )
        elif self.external_reference_id is not None:
            raise EmergencyGrouperError(
                "precomputed provenance must not declare external_reference_id"
            )
        if self.table_version != self.emergency_classification_version:
            raise EmergencyGrouperError(
                "table_version must match emergency_classification_version"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "emergency_classification_version": self.emergency_classification_version,
            "source_mode": self.source_mode,
            "tool_id": self.tool_id,
            "tool_version": self.tool_version,
            "table_version": self.table_version,
            "input_sha256": self.input_sha256,
            "generated_at": self.generated_at,
            "mapping_stage": self.mapping_stage,
            "mapping_bundle_id": self.mapping_bundle_id,
            "mapping_bundle_version": self.mapping_bundle_version,
            "external_reference_id": self.external_reference_id,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class EmergencyGrouperOutputRecord:
    """Single emergency output row with conservative provenance metadata."""

    classification_code: str
    provenance: EmergencyGrouperProvenance
    episode_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "classification_code",
            _normalize_non_blank(self.classification_code, field="classification_code"),
        )
        if not isinstance(self.provenance, EmergencyGrouperProvenance):
            raise EmergencyGrouperError(
                "provenance must be an EmergencyGrouperProvenance"
            )
        if self.episode_id is not None:
            object.__setattr__(
                self,
                "episode_id",
                _normalize_non_blank(self.episode_id, field="episode_id"),
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "classification_code": self.classification_code,
            "episode_id": self.episode_id,
            "provenance": self.provenance.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class EmergencyGrouperCompatibilityResult:
    """Outcome from a fail-closed emergency grouper compatibility check."""

    system: str
    display_name: str
    pricing_year: str
    stream: str | None
    declared_version: str | None
    expected_version: str | None
    acceptance_state: Literal["valid", "transition", "shadow-priced", "unavailable"]
    compatibility_state: Literal[
        "valid",
        "transition",
        "shadow-priced",
        "missing",
        "incompatible",
        "trusted-precomputed",
    ]
    compatible: bool
    source_mode: Literal["precomputed", "external-reference"]
    validation_mode: Literal["strict", "trusted-precomputed"]
    reference_id: str | None
    reference_type: str | None
    source_refs: tuple[str, ...]
    reason: str | None
    record: EmergencyGrouperOutputRecord | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "display_name": self.display_name,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "declared_version": self.declared_version,
            "expected_version": self.expected_version,
            "acceptance_state": self.acceptance_state,
            "compatibility_state": self.compatibility_state,
            "compatible": self.compatible,
            "source_mode": self.source_mode,
            "validation_mode": self.validation_mode,
            "reference_id": self.reference_id,
            "reference_type": self.reference_type,
            "source_refs": list(self.source_refs),
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
        }


def _coerce_version_window(
    value: EmergencyGrouperVersionWindow | dict[str, Any],
) -> EmergencyGrouperVersionWindow:
    if isinstance(value, EmergencyGrouperVersionWindow):
        return value
    if not isinstance(value, dict):
        raise EmergencyGrouperError(
            "supported_versions must contain version window records or mappings"
        )
    return EmergencyGrouperVersionWindow(
        system=str(value["system"]),
        pricing_year=str(value["pricing_year"]),
        emergency_classification_version=str(value["emergency_classification_version"]),
        stream_compatibility=tuple(value["stream_compatibility"]),
        source_refs=tuple(value["source_refs"]),
        notes=tuple(value.get("notes", ())),
    )


def _result(
    *,
    system: str,
    year: str,
    stream: str | None,
    declared_version: str | None,
    expected_version: str | None,
    acceptance_state: Literal["valid", "transition", "shadow-priced", "unavailable"],
    compatibility_state: Literal[
        "valid",
        "transition",
        "shadow-priced",
        "missing",
        "incompatible",
        "trusted-precomputed",
    ],
    compatible: bool,
    source_mode: Literal["precomputed", "external-reference"],
    validation_mode: Literal["strict", "trusted-precomputed"],
    reference: EmergencyGrouperReference | None,
    reason: str | None,
    record: EmergencyGrouperOutputRecord | None = None,
) -> EmergencyGrouperCompatibilityResult:
    display_name = get_emergency_classification_name(system)
    source_refs = (
        tuple(
            dict.fromkeys(
                ref
                for window in reference.supported_versions
                for ref in window.source_refs
            )
        )
        if reference is not None
        else get_emergency_classification_record(system).source_refs
    )
    return EmergencyGrouperCompatibilityResult(
        system=normalize_emergency_classification_system(system),
        display_name=display_name,
        pricing_year=_normalize_year(year),
        stream=stream,
        declared_version=declared_version,
        expected_version=expected_version,
        acceptance_state=acceptance_state,
        compatibility_state=compatibility_state,
        compatible=compatible,
        source_mode=source_mode,
        validation_mode=validation_mode,
        reference_id=None if reference is None else reference.reference_id,
        reference_type=None if reference is None else reference.reference_type,
        source_refs=source_refs,
        reason=reason,
        record=record,
    )


def validate_emergency_grouper_compatibility(
    system: str,
    year: str,
    classification_version: str | None,
    *,
    stream: str | None = None,
    source_mode: Literal["precomputed", "external-reference"] = "precomputed",
    reference: EmergencyGrouperReference | None = None,
    trust_precomputed: bool = False,
) -> EmergencyGrouperCompatibilityResult:
    """Validate a precomputed or external-reference emergency version set."""
    canonical_system = normalize_emergency_classification_system(system)
    normalized_year = _normalize_year(year)
    record = get_emergency_classification_record(canonical_system)
    acceptance_state = get_emergency_classification_status(
        canonical_system, normalized_year
    )
    expected_version = get_expected_emergency_classification_version(
        canonical_system, normalized_year
    )
    validation_mode: Literal["strict", "trusted-precomputed"] = (
        "trusted-precomputed"
        if source_mode == "precomputed" and trust_precomputed
        else "strict"
    )

    normalized_stream: str | None
    if stream is not None:
        normalized_stream = _normalize_non_blank(stream, field="stream")
        if normalized_stream not in EMERGENCY_STREAMS:
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=reference,
                reason=(
                    "stream must be one of the emergency transition registry streams"
                ),
            )
    else:
        normalized_stream = None

    if source_mode == "external-reference":
        if reference is None:
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=None,
                reason="external-reference mode requires a local reference manifest",
            )
        if reference.status != "resolved":
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=reference,
                reason=(
                    f"external reference {reference.reference_id!r} is not resolved"
                ),
            )
        window = reference.version_window_for_year(canonical_system, normalized_year)
        if window is None:
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=reference,
                reason=(
                    f"reference {reference.reference_id!r} does not support "
                    f"{canonical_system!r} for pricing year {normalized_year!r}"
                ),
            )
        if (
            normalized_stream is not None
            and normalized_stream not in window.stream_compatibility
        ):
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=reference,
                reason=(
                    f"reference {reference.reference_id!r} is not compatible with "
                    f"stream {normalized_stream!r}"
                ),
            )
        if (
            classification_version is not None
            and classification_version != window.emergency_classification_version
        ):
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=reference,
                reason=(
                    "explicit version must match the selected external reference "
                    f"window for pricing year {normalized_year}"
                ),
            )
        declared_version = window.emergency_classification_version
        compatibility = validate_emergency_classification_compatibility(
            canonical_system,
            normalized_year,
            declared_version,
            stream=normalized_stream,
        )
        if not compatibility.compatible:
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=declared_version,
                expected_version=compatibility.expected_version,
                acceptance_state=compatibility.acceptance_state,
                compatibility_state=compatibility.compatibility_state,
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=reference,
                reason=compatibility.reason,
            )
        return _result(
            system=canonical_system,
            year=normalized_year,
            stream=normalized_stream,
            declared_version=declared_version,
            expected_version=compatibility.expected_version,
            acceptance_state=compatibility.acceptance_state,
            compatibility_state=compatibility.compatibility_state,
            compatible=True,
            source_mode=source_mode,
            validation_mode=validation_mode,
            reference=reference,
            reason=None,
        )

    if trust_precomputed:
        if (
            normalized_stream is not None
            and normalized_stream not in record.stream_compatibility
        ):
            return _result(
                system=canonical_system,
                year=normalized_year,
                stream=normalized_stream,
                declared_version=classification_version,
                expected_version=expected_version,
                acceptance_state=acceptance_state,
                compatibility_state="incompatible",
                compatible=False,
                source_mode=source_mode,
                validation_mode=validation_mode,
                reference=None,
                reason=(
                    f"{record.display_name} is not compatible with stream "
                    f"{normalized_stream!r}"
                ),
            )
        return _result(
            system=canonical_system,
            year=normalized_year,
            stream=normalized_stream,
            declared_version=classification_version,
            expected_version=expected_version,
            acceptance_state=acceptance_state,
            compatibility_state="trusted-precomputed",
            compatible=True,
            source_mode=source_mode,
            validation_mode=validation_mode,
            reference=None,
            reason=None,
        )

    compatibility = validate_emergency_classification_compatibility(
        canonical_system,
        normalized_year,
        classification_version,
        stream=normalized_stream,
    )
    return _result(
        system=canonical_system,
        year=normalized_year,
        stream=normalized_stream,
        declared_version=compatibility.declared_version,
        expected_version=compatibility.expected_version,
        acceptance_state=compatibility.acceptance_state,
        compatibility_state=compatibility.compatibility_state,
        compatible=compatibility.compatible,
        source_mode=source_mode,
        validation_mode=validation_mode,
        reference=None,
        reason=compatibility.reason,
    )


def ensure_emergency_grouper_compatibility(
    system: str,
    year: str,
    classification_version: str | None,
    *,
    stream: str | None = None,
    source_mode: Literal["precomputed", "external-reference"] = "precomputed",
    reference: EmergencyGrouperReference | None = None,
    trust_precomputed: bool = False,
) -> EmergencyGrouperCompatibilityResult:
    """Raise when an emergency grouper version set is incompatible."""
    result = validate_emergency_grouper_compatibility(
        system,
        year,
        classification_version,
        stream=stream,
        source_mode=source_mode,
        reference=reference,
        trust_precomputed=trust_precomputed,
    )
    if not result.compatible:
        raise EmergencyGrouperError(
            result.reason or "emergency grouper metadata is invalid"
        )
    return result


def build_emergency_external_reference(
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
    local_path_hint: str | Path | None = None,
    supported_versions: Iterable[EmergencyGrouperVersionWindow | dict[str, Any]],
    notes: Iterable[str] = (),
) -> EmergencyGrouperReference:
    """Build a conservative local emergency grouper reference manifest."""
    windows = tuple(_coerce_version_window(item) for item in supported_versions)
    return EmergencyGrouperReference(
        reference_id=reference_id,
        reference_type=reference_type,
        access_mode=access_mode,
        license_boundary=license_boundary,
        status=status,
        command=command,
        reference_uri=reference_uri,
        local_path_hint=None if local_path_hint is None else str(local_path_hint),
        supported_versions=windows,
        notes=tuple(notes),
    )


def build_emergency_provenance(
    *,
    system: str,
    year: str,
    stream: str,
    emergency_classification_version: str,
    input_sha256: str,
    source_mode: Literal["precomputed", "external-reference"] = "precomputed",
    tool_id: str | None = None,
    tool_version: str | None = None,
    table_version: str | None = None,
    generated_at: str | None = None,
    mapping_stage: Literal["unknown", "pre-mapping", "post-mapping"] = "unknown",
    mapping_bundle_id: str | None = None,
    mapping_bundle_version: str | None = None,
    external_reference_id: str | None = None,
    notes: Iterable[str] = (),
) -> EmergencyGrouperProvenance:
    """Build emergency provenance after validating the declared metadata."""
    canonical_system = normalize_emergency_classification_system(system)
    normalized_year = _normalize_year(year)
    normalized_version = _normalize_version(
        emergency_classification_version,
        field="emergency_classification_version",
    )
    if table_version is None:
        resolved_table_version = normalized_version
    else:
        resolved_table_version = _normalize_version(
            table_version,
            field="table_version",
        )
    if resolved_table_version != normalized_version:
        raise EmergencyGrouperError(
            "table_version must match emergency_classification_version"
        )
    if source_mode == "external-reference":
        if tool_id is None or tool_version is None or external_reference_id is None:
            raise EmergencyGrouperError(
                "external-reference provenance requires tool_id, tool_version, "
                "and external_reference_id"
            )
    elif external_reference_id is not None:
        raise EmergencyGrouperError(
            "precomputed provenance must not declare external_reference_id"
        )
    if mapping_stage not in EMERGENCY_GROUPER_MAPPING_STAGES:
        raise EmergencyGrouperError(f"unsupported mapping_stage {mapping_stage!r}")
    return EmergencyGrouperProvenance(
        system=canonical_system,
        pricing_year=normalized_year,
        stream=stream,
        emergency_classification_version=normalized_version,
        source_mode=source_mode,
        tool_id=tool_id,
        tool_version=tool_version,
        table_version=resolved_table_version,
        input_sha256=input_sha256,
        generated_at=generated_at or datetime.now(timezone.utc).isoformat(),
        mapping_stage=mapping_stage,
        mapping_bundle_id=mapping_bundle_id,
        mapping_bundle_version=mapping_bundle_version,
        external_reference_id=external_reference_id,
        notes=tuple(notes),
    )


def build_emergency_precomputed_output_record(
    classification_code: str,
    *,
    system: str,
    year: str,
    stream: str,
    emergency_classification_version: str,
    input_sha256: str,
    episode_id: str | None = None,
    tool_id: str | None = None,
    tool_version: str | None = None,
    table_version: str | None = None,
    generated_at: str | None = None,
    mapping_stage: Literal["unknown", "pre-mapping", "post-mapping"] = "pre-mapping",
    mapping_bundle_id: str | None = None,
    mapping_bundle_version: str | None = None,
    notes: Iterable[str] = (),
    trust_precomputed: bool = False,
) -> EmergencyGrouperOutputRecord:
    """Build a grouped record when the emergency classification is precomputed."""
    ensure_emergency_grouper_compatibility(
        system,
        year,
        emergency_classification_version,
        stream=stream,
        source_mode="precomputed",
        trust_precomputed=trust_precomputed,
    )
    provenance = build_emergency_provenance(
        system=system,
        year=year,
        stream=stream,
        emergency_classification_version=emergency_classification_version,
        input_sha256=input_sha256,
        source_mode="precomputed",
        tool_id=tool_id,
        tool_version=tool_version,
        table_version=table_version,
        generated_at=generated_at,
        mapping_stage=mapping_stage,
        mapping_bundle_id=mapping_bundle_id,
        mapping_bundle_version=mapping_bundle_version,
        notes=notes,
    )
    return EmergencyGrouperOutputRecord(
        classification_code=classification_code,
        episode_id=episode_id,
        provenance=provenance,
    )


def build_emergency_output_record_from_reference(
    classification_code: str,
    *,
    system: str,
    year: str,
    stream: str,
    reference: EmergencyGrouperReference,
    input_sha256: str,
    emergency_classification_version: str | None = None,
    tool_id: str,
    tool_version: str,
    table_version: str | None = None,
    episode_id: str | None = None,
    generated_at: str | None = None,
    mapping_stage: Literal["unknown", "pre-mapping", "post-mapping"] = "post-mapping",
    mapping_bundle_id: str | None = None,
    mapping_bundle_version: str | None = None,
    notes: Iterable[str] = (),
) -> EmergencyGrouperOutputRecord:
    """Build a grouped record derived from a local external emergency reference."""
    result = ensure_emergency_grouper_compatibility(
        system,
        year,
        emergency_classification_version,
        stream=stream,
        source_mode="external-reference",
        reference=reference,
    )
    resolved_version = (
        emergency_classification_version
        if emergency_classification_version is not None
        else result.declared_version
    )
    provenance = build_emergency_provenance(
        system=system,
        year=year,
        stream=stream,
        emergency_classification_version=str(resolved_version),
        input_sha256=input_sha256,
        source_mode="external-reference",
        tool_id=tool_id,
        tool_version=tool_version,
        table_version=table_version
        if table_version is not None
        else str(resolved_version),
        generated_at=generated_at,
        mapping_stage=mapping_stage,
        mapping_bundle_id=mapping_bundle_id,
        mapping_bundle_version=mapping_bundle_version,
        external_reference_id=reference.reference_id,
        notes=notes,
    )
    return EmergencyGrouperOutputRecord(
        classification_code=classification_code,
        episode_id=episode_id,
        provenance=provenance,
    )
