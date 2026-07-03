"""Public classification mapping metadata and local-only hook registry.

The registry stays deliberately conservative. It exposes the supported
classification systems, their stream bindings, version matrices, and
placeholder local-only hook references without bundling any proprietary
mapping tables or grouping logic.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final, Literal, cast

from .classification_mapping_registry_data import CLASSIFICATION_MAPPING_ROWS
from .classification_validation import (
    get_classification_name,
    get_classification_requirement,
    get_classification_stream,
    is_classification_licensed,
    normalize_classification_system,
)

__all__ = [
    "CLASSIFICATION_MAPPING_STREAMS",
    "ClassificationLocalHookCompatibilityResult",
    "ClassificationLocalHookReference",
    "ClassificationMappingAssetReference",
    "ClassificationMappingCompatibilityResult",
    "ClassificationMappingRecord",
    "ClassificationMappingRegistryError",
    "build_classification_local_hook_reference",
    "ensure_classification_local_hook_compatibility",
    "ensure_classification_mapping_compatibility",
    "get_classification_mapping_record",
    "list_classification_mapping_records",
    "validate_classification_local_hook_compatibility",
    "validate_classification_mapping_compatibility",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_STREAMS: Final[frozenset[str]] = frozenset(
    {
        "admitted_acute",
        "emergency_department",
        "emergency_service",
        "admitted_non_acute",
        "community_mental_health",
    }
)
_REFERENCE_TYPES: Final[frozenset[str]] = frozenset(
    {"local_command", "local_service", "file_exchange"}
)
_HOOK_STATUSES: Final[frozenset[str]] = frozenset({"placeholder", "resolved"})
_LICENSE_BOUNDARIES: Final[frozenset[str]] = frozenset({"local-only", "restricted"})
_MAPPING_SUPPORT_STATUSES: Final[frozenset[str]] = frozenset(
    {"source_available", "blocked_licensed", "validated", "out_of_scope"}
)


class ClassificationMappingRegistryError(ValueError):
    """Raised when the classification-mapping registry is inconsistent."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ClassificationMappingRegistryError(f"{field} must be a string")
    if not value:
        raise ClassificationMappingRegistryError(f"{field} must not be blank")
    if value.strip() != value:
        raise ClassificationMappingRegistryError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise ClassificationMappingRegistryError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_str_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise ClassificationMappingRegistryError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise ClassificationMappingRegistryError(
                f"{field} must not contain duplicates"
            )
        seen.add(text)
        normalized.append(text)
    if not normalized:
        raise ClassificationMappingRegistryError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_optional_text(value: Any, *, field: str) -> str | None:
    if value is None:
        return None
    return _normalize_non_blank(value, field=field)


def _normalize_stream(stream: str) -> str:
    normalized = _normalize_non_blank(stream, field="stream")
    if normalized not in _STREAMS:
        raise ClassificationMappingRegistryError(
            f"stream must be one of {sorted(_STREAMS)}"
        )
    return normalized


def _build_asset_reference(
    row: dict[str, object],
) -> ClassificationMappingAssetReference:
    return ClassificationMappingAssetReference(
        kind=cast(
            Literal[
                "public-metadata",
                "user-supplied-licensed-file",
                "derived-validation-fixture",
            ],
            row["kind"],
        ),
        source_refs=cast(tuple[str, ...], row["source_refs"]),
        local_path_hint=cast(str | None, row["local_path_hint"]),
        restricted=bool(row["restricted"]),
        notes=cast(tuple[str, ...], row["notes"]),
    )


def _build_hook_reference(
    row: dict[str, object],
    *,
    system: str,
    stream: str,
    pricing_year: str,
    source_refs: tuple[str, ...],
) -> ClassificationLocalHookReference:
    return ClassificationLocalHookReference(
        hook_id=str(row["hook_id"]),
        system=system,
        pricing_year=pricing_year,
        stream=stream,
        reference_type=cast(
            Literal["local_command", "local_service", "file_exchange"],
            row["reference_type"],
        ),
        status=cast(Literal["placeholder", "resolved"], row["status"]),
        license_boundary=cast(
            Literal["local-only", "restricted"], row["license_boundary"]
        ),
        command=cast(str | None, row["command"]),
        reference_uri=cast(str | None, row["reference_uri"]),
        local_path_hint=cast(str | None, row["local_path_hint"]),
        source_refs=cast(tuple[str, ...], row.get("source_refs", source_refs)),
        notes=cast(tuple[str, ...], row["notes"]),
    )


def _build_record(row: dict[str, object]) -> ClassificationMappingRecord:
    system = cast(str, row["system"])
    display_name = cast(str, row["display_name"])
    stream = cast(str, row["stream"])
    licensed = cast(bool, row["licensed"])
    restriction = cast(str | None, row["restriction"])
    support_status = cast(
        Literal["source_available", "blocked_licensed", "validated", "out_of_scope"],
        row["support_status"],
    )
    required_fields = cast(tuple[str, ...], row["required_fields"])
    source_refs = cast(tuple[str, ...], row["source_refs"])
    versions = cast(tuple[tuple[str, str | None], ...], row["versions"])
    public_asset = _build_asset_reference(cast(dict[str, object], row["public_asset"]))
    local_hooks = tuple(
        _build_hook_reference(
            hook,
            system=system,
            stream=stream,
            pricing_year="2026",
            source_refs=source_refs,
        )
        for hook in cast(tuple[dict[str, object], ...], row["local_hooks"])
    )
    notes = cast(tuple[str, ...], row["notes"])
    return ClassificationMappingRecord(
        system=system,
        display_name=display_name,
        stream=stream,
        licensed=licensed,
        restriction=restriction,
        support_status=support_status,
        required_fields=required_fields,
        source_refs=source_refs,
        versions=versions,
        public_asset=public_asset,
        local_hooks=local_hooks,
        notes=notes,
    )


@dataclass(frozen=True, slots=True)
class ClassificationMappingAssetReference:
    """Public, restricted, or derived provenance for a classification record."""

    kind: Literal[
        "public-metadata",
        "user-supplied-licensed-file",
        "derived-validation-fixture",
    ]
    source_refs: tuple[str, ...]
    local_path_hint: str | None
    restricted: bool
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.kind not in {
            "public-metadata",
            "user-supplied-licensed-file",
            "derived-validation-fixture",
        }:
            raise ClassificationMappingRegistryError(
                f"unsupported asset kind {self.kind!r}"
            )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        if self.local_path_hint is not None:
            object.__setattr__(
                self,
                "local_path_hint",
                _normalize_non_blank(self.local_path_hint, field="local_path_hint"),
            )
        object.__setattr__(
            self, "notes", _normalize_str_tuple(self.notes, field="notes")
        )
        if self.kind == "public-metadata":
            if self.restricted:
                raise ClassificationMappingRegistryError(
                    "public-metadata assets must not be restricted"
                )
            if self.local_path_hint is not None:
                raise ClassificationMappingRegistryError(
                    "public-metadata assets must not declare a local_path_hint"
                )
        elif self.kind == "user-supplied-licensed-file":
            if not self.restricted:
                raise ClassificationMappingRegistryError(
                    "user-supplied-licensed-file assets must be restricted"
                )
            if self.local_path_hint is None:
                raise ClassificationMappingRegistryError(
                    "user-supplied-licensed-file assets require a local_path_hint"
                )
        elif self.restricted:
            raise ClassificationMappingRegistryError(
                "derived-validation-fixture assets must not be restricted"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "source_refs": list(self.source_refs),
            "local_path_hint": self.local_path_hint,
            "restricted": self.restricted,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ClassificationLocalHookReference:
    """Local-only mapping hook placeholder for a supported classification."""

    hook_id: str
    system: str
    pricing_year: str
    stream: str
    reference_type: Literal["local_command", "local_service", "file_exchange"]
    status: Literal["placeholder", "resolved"]
    license_boundary: Literal["local-only", "restricted"]
    command: str | None
    reference_uri: str | None
    local_path_hint: str | None
    source_refs: tuple[str, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "hook_id", _normalize_non_blank(self.hook_id, field="hook_id")
        )
        object.__setattr__(self, "system", normalize_classification_system(self.system))
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        object.__setattr__(self, "stream", _normalize_stream(self.stream))
        if self.reference_type not in _REFERENCE_TYPES:
            raise ClassificationMappingRegistryError(
                f"unsupported reference_type {self.reference_type!r}"
            )
        if self.status not in _HOOK_STATUSES:
            raise ClassificationMappingRegistryError(
                f"unsupported status {self.status!r}"
            )
        if self.license_boundary not in _LICENSE_BOUNDARIES:
            raise ClassificationMappingRegistryError(
                f"unsupported license_boundary {self.license_boundary!r}"
            )
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
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        object.__setattr__(
            self, "notes", _normalize_str_tuple(self.notes, field="notes")
        )
        if self.license_boundary != "local-only":
            raise ClassificationMappingRegistryError(
                "local hooks must use the local-only license boundary"
            )

    def to_dict(self) -> dict[str, object]:
        return {
            "hook_id": self.hook_id,
            "system": self.system,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "reference_type": self.reference_type,
            "status": self.status,
            "license_boundary": self.license_boundary,
            "command": self.command,
            "reference_uri": self.reference_uri,
            "local_path_hint": self.local_path_hint,
            "source_refs": list(self.source_refs),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ClassificationMappingRecord:
    """Metadata-only classification registry row for one supported system."""

    system: str
    display_name: str
    stream: str
    licensed: bool
    restriction: str | None
    support_status: Literal[
        "source_available", "blocked_licensed", "validated", "out_of_scope"
    ]
    required_fields: tuple[str, ...]
    source_refs: tuple[str, ...]
    versions: tuple[tuple[str, str | None], ...]
    public_asset: ClassificationMappingAssetReference
    local_hooks: tuple[ClassificationLocalHookReference, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "system", normalize_classification_system(self.system))
        object.__setattr__(
            self,
            "display_name",
            _normalize_non_blank(self.display_name, field="display_name"),
        )
        object.__setattr__(self, "stream", _normalize_stream(self.stream))
        if self.support_status not in _MAPPING_SUPPORT_STATUSES:
            raise ClassificationMappingRegistryError(
                f"unsupported support_status {self.support_status!r}"
            )
        object.__setattr__(
            self,
            "required_fields",
            _normalize_str_tuple(self.required_fields, field="required_fields"),
        )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        if not self.versions:
            raise ClassificationMappingRegistryError("versions must not be empty")
        normalized_versions: list[tuple[str, str | None]] = []
        seen: set[str] = set()
        for year, version in self.versions:
            normalized_year = _normalize_year(year)
            if normalized_year in seen:
                raise ClassificationMappingRegistryError(
                    "versions must not contain duplicate years"
                )
            seen.add(normalized_year)
            normalized_versions.append(
                (
                    normalized_year,
                    _normalize_optional_text(version, field="expected_version"),
                )
            )
        object.__setattr__(self, "versions", tuple(normalized_versions))
        object.__setattr__(self, "public_asset", self.public_asset)
        object.__setattr__(self, "local_hooks", tuple(self.local_hooks))
        object.__setattr__(
            self, "notes", _normalize_str_tuple(self.notes, field="notes")
        )

        if (
            self.required_fields
            != get_classification_requirement(self.system, "2026").required_fields
        ):
            # The requirement validator also guards the canonical required fields.
            # We only use 2026 here because the required fields are system-wide in
            # the current registry and should not drift.
            raise ClassificationMappingRegistryError(
                "required_fields for "
                f"{self.system!r} are inconsistent with the shared "
                "classification validator"
            )

        expected_display_name = get_classification_name(self.system)
        if self.display_name != expected_display_name:
            raise ClassificationMappingRegistryError(
                f"display_name {self.display_name!r} does not match {self.system!r}"
            )
        if self.licensed != is_classification_licensed(self.system):
            raise ClassificationMappingRegistryError(
                f"licensed flag for {self.system!r} is inconsistent"
            )
        if self.stream != get_classification_stream(self.system):
            raise ClassificationMappingRegistryError(
                f"stream for {self.system!r} is inconsistent"
            )
        if self.public_asset.kind != "public-metadata":
            raise ClassificationMappingRegistryError(
                "public_asset must be public metadata"
            )
        if self.system == "ar_drg" and not self.local_hooks:
            raise ClassificationMappingRegistryError(
                "AR-DRG must expose local hook placeholders"
            )
        if self.system != "ar_drg" and self.local_hooks:
            raise ClassificationMappingRegistryError(
                f"{self.system!r} must not expose local-only hook placeholders"
            )

    def version_for_year(self, year: str) -> str | None:
        normalized_year = _normalize_year(year)
        for candidate_year, version in self.versions:
            if candidate_year == normalized_year:
                return version
        return None

    def supported_years(self) -> tuple[str, ...]:
        return tuple(year for year, version in self.versions if version is not None)

    def to_dict(self) -> dict[str, object]:
        return {
            "system": self.system,
            "display_name": self.display_name,
            "stream": self.stream,
            "licensed": self.licensed,
            "restriction": self.restriction,
            "support_status": self.support_status,
            "required_fields": list(self.required_fields),
            "source_refs": list(self.source_refs),
            "versions": [
                {"year": year, "expected_version": version}
                for year, version in self.versions
            ],
            "supported_years": list(self.supported_years()),
            "public_asset": self.public_asset.to_dict(),
            "local_hooks": [hook.to_dict() for hook in self.local_hooks],
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ClassificationMappingCompatibilityResult:
    """Outcome from a classification mapping compatibility check."""

    stream: str
    system: str
    pricing_year: str
    declared_version: str | None
    expected_version: str | None
    support_status: str
    compatible: bool
    reason: str | None
    record: ClassificationMappingRecord | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "stream": self.stream,
            "system": self.system,
            "pricing_year": self.pricing_year,
            "declared_version": self.declared_version,
            "expected_version": self.expected_version,
            "support_status": self.support_status,
            "compatible": self.compatible,
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ClassificationLocalHookCompatibilityResult:
    """Outcome from a local-only mapping hook compatibility check."""

    hook_id: str
    stream: str
    system: str
    pricing_year: str
    compatible: bool
    reason: str | None
    record: ClassificationMappingRecord | None = None
    hook: ClassificationLocalHookReference | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "hook_id": self.hook_id,
            "stream": self.stream,
            "system": self.system,
            "pricing_year": self.pricing_year,
            "compatible": self.compatible,
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
            "hook": None if self.hook is None else self.hook.to_dict(),
        }


_RECORDS: Final[tuple[ClassificationMappingRecord, ...]] = tuple(
    _build_record(row) for row in CLASSIFICATION_MAPPING_ROWS
)

_RECORD_BY_SYSTEM: Final[dict[str, ClassificationMappingRecord]] = {
    record.system: record for record in _RECORDS
}

CLASSIFICATION_MAPPING_STREAMS: Final[dict[str, str]] = {
    record.system: record.stream for record in _RECORDS
}


def list_classification_mapping_records() -> tuple[ClassificationMappingRecord, ...]:
    """Return all known classification mapping registry records."""
    return _RECORDS


def get_classification_mapping_record(
    system: str,
    year: str | None = None,
) -> ClassificationMappingRecord | None:
    """Return the registry record for a classification system."""
    canonical_system = normalize_classification_system(system)
    record = _RECORD_BY_SYSTEM.get(canonical_system)
    if record is None:
        return None
    if year is None:
        return record
    normalized_year = _normalize_year(year)
    if record.version_for_year(normalized_year) is None:
        return None
    return record


def validate_classification_mapping_compatibility(
    stream: str,
    system: str,
    year: str,
    *,
    version: str | None,
) -> ClassificationMappingCompatibilityResult:
    """Check whether a classification stream/system/year/version set is valid."""
    normalized_stream = _normalize_stream(stream)
    canonical_system = normalize_classification_system(system)
    normalized_year = _normalize_year(year)
    record = _RECORD_BY_SYSTEM.get(canonical_system)
    declared_version = (
        None
        if version is None
        else _normalize_non_blank(version, field="classification_version")
    )
    if record is None:
        return ClassificationMappingCompatibilityResult(
            stream=normalized_stream,
            system=canonical_system,
            pricing_year=normalized_year,
            declared_version=declared_version,
            expected_version=None,
            support_status="out_of_scope",
            compatible=False,
            reason=(
                f"{canonical_system} is not available for stream {normalized_stream}"
            ),
            record=None,
        )
    expected_stream = record.stream
    expected_version = record.version_for_year(normalized_year)
    if normalized_stream != expected_stream:
        return ClassificationMappingCompatibilityResult(
            stream=normalized_stream,
            system=canonical_system,
            pricing_year=normalized_year,
            declared_version=declared_version,
            expected_version=expected_version,
            support_status=record.support_status,
            compatible=False,
            reason=(
                f"{record.display_name} is not available for stream {normalized_stream}"
            ),
            record=record,
        )
    if expected_version is None:
        return ClassificationMappingCompatibilityResult(
            stream=normalized_stream,
            system=canonical_system,
            pricing_year=normalized_year,
            declared_version=declared_version,
            expected_version=None,
            support_status=record.support_status,
            compatible=False,
            reason=(
                f"{record.display_name} is not available for pricing year "
                f"{normalized_year}"
            ),
            record=record,
        )
    compatible = declared_version == expected_version
    reason = None
    if declared_version is None:
        reason = (
            f"{record.display_name} {normalized_year} requires version "
            f"{expected_version}"
        )
    elif declared_version != expected_version:
        reason = (
            f"{record.display_name} {normalized_year} expects {expected_version}, "
            f"got {declared_version}"
        )
    return ClassificationMappingCompatibilityResult(
        stream=normalized_stream,
        system=canonical_system,
        pricing_year=normalized_year,
        declared_version=declared_version,
        expected_version=expected_version,
        support_status=record.support_status,
        compatible=compatible,
        reason=reason,
        record=record,
    )


def ensure_classification_mapping_compatibility(
    stream: str,
    system: str,
    year: str,
    *,
    version: str | None,
) -> ClassificationMappingCompatibilityResult:
    """Raise when a classification stream/system/year/version set is invalid."""
    result = validate_classification_mapping_compatibility(
        stream,
        system,
        year,
        version=version,
    )
    if not result.compatible:
        raise ClassificationMappingRegistryError(
            result.reason or "classification mapping is incompatible"
        )
    return result


def build_classification_local_hook_reference(
    *,
    hook_id: str,
    system: str,
    stream: str,
    pricing_year: str,
    reference_type: Literal["local_command", "local_service", "file_exchange"],
    status: Literal["placeholder", "resolved"] = "placeholder",
    license_boundary: Literal["local-only", "restricted"] = "local-only",
    command: str | None = None,
    reference_uri: str | None = None,
    local_path_hint: str | None = None,
    source_refs: tuple[str, ...] = (),
    notes: tuple[str, ...] = (),
) -> ClassificationLocalHookReference:
    """Build a local-only mapping hook placeholder."""
    canonical_system = normalize_classification_system(system)
    normalized_stream = _normalize_stream(stream)
    normalized_year = _normalize_year(pricing_year)
    return ClassificationLocalHookReference(
        hook_id=hook_id,
        system=canonical_system,
        pricing_year=normalized_year,
        stream=normalized_stream,
        reference_type=reference_type,
        status=status,
        license_boundary=license_boundary,
        command=command,
        reference_uri=reference_uri,
        local_path_hint=local_path_hint,
        source_refs=source_refs,
        notes=notes,
    )


def validate_classification_local_hook_compatibility(
    hook: ClassificationLocalHookReference,
) -> ClassificationLocalHookCompatibilityResult:
    """Check whether a local-only mapping hook is structurally valid."""
    record = get_classification_mapping_record(
        hook.system,
        hook.pricing_year,
    )
    if record is None:
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason=(
                f"{hook.system} {hook.pricing_year} does not have a public "
                "registry record"
            ),
            record=None,
            hook=hook,
        )
    if hook.stream != record.stream:
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason=(f"{record.display_name} is not available for stream {hook.stream}"),
            record=record,
            hook=hook,
        )
    if not hook.local_path_hint and not hook.command and not hook.reference_uri:
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason="local hook placeholders must describe licensed content locally",
            record=record,
            hook=hook,
        )
    if hook.reference_type == "local_command" and hook.command is None:
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason="local_command hooks require a command string",
            record=record,
            hook=hook,
        )
    if hook.reference_type == "local_service" and hook.reference_uri is None:
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason="local_service hooks require a reference_uri",
            record=record,
            hook=hook,
        )
    if hook.reference_type == "file_exchange" and hook.local_path_hint is None:
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason="file_exchange hooks require a local_path_hint",
            record=record,
            hook=hook,
        )
    if hook.license_boundary != "local-only":
        return ClassificationLocalHookCompatibilityResult(
            hook_id=hook.hook_id,
            stream=hook.stream,
            system=hook.system,
            pricing_year=hook.pricing_year,
            compatible=False,
            reason="local hooks must stay local-only",
            record=record,
            hook=hook,
        )
    return ClassificationLocalHookCompatibilityResult(
        hook_id=hook.hook_id,
        stream=hook.stream,
        system=hook.system,
        pricing_year=hook.pricing_year,
        compatible=True,
        reason=None,
        record=record,
        hook=hook,
    )


def ensure_classification_local_hook_compatibility(
    hook: ClassificationLocalHookReference,
) -> ClassificationLocalHookCompatibilityResult:
    """Raise when a local-only mapping hook is structurally invalid."""
    result = validate_classification_local_hook_compatibility(hook)
    if not result.compatible:
        raise ClassificationMappingRegistryError(
            result.reason or "local mapping hook is incompatible"
        )
    return result
