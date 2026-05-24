"""Metadata-only emergency code mapping pipeline helpers.

The helpers in this module describe versioned emergency mapping bundles without
inventing any code crosswalks or row-level transformations. They keep the
surface deliberately conservative:

- bundle records are versioned and provenance-aware;
- outputs are checked against the emergency transition registry;
- source and output fields stay explicit for auditability; and
- local-only external references remain local path hints, not fetch targets.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal
from urllib.parse import urlsplit

from .emergency_transition_registry import (
    EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS,
    EMERGENCY_CLASSIFICATION_SOURCE_REFS,
    EMERGENCY_STREAMS,
    EmergencyClassificationCompatibilityResult,
    get_emergency_classification_name,
    get_emergency_classification_record,
    get_expected_emergency_classification_version,
    normalize_emergency_classification_system,
    validate_emergency_classification_compatibility,
)

__all__ = [
    "EMERGENCY_CODE_MAPPING_BUNDLE_SCHEMA_VERSION",
    "EMERGENCY_CODE_MAPPING_BUNDLE_VERSION_MATRIX",
    "EMERGENCY_CODE_MAPPING_VALIDATION_STATUSES",
    "EmergencyCodeMappingAssetReference",
    "EmergencyCodeMappingBundleCompatibilityResult",
    "EmergencyCodeMappingBundleRecord",
    "EmergencyCodeMappingDryRunSummary",
    "EmergencyCodeMappingPipelineError",
    "build_emergency_code_mapping_asset_reference",
    "build_emergency_code_mapping_bundle_record",
    "ensure_emergency_code_mapping_bundle_compatibility",
    "get_emergency_code_mapping_bundle_record",
    "list_emergency_code_mapping_bundle_records",
    "summarize_emergency_code_mapping_dry_run",
    "validate_emergency_code_mapping_bundle_compatibility",
]

EMERGENCY_CODE_MAPPING_BUNDLE_SCHEMA_VERSION = "1.0"
EMERGENCY_CODE_MAPPING_VALIDATION_STATUSES: Final[tuple[str, ...]] = (
    "source-only",
    "schema-complete",
    "gap-explicit",
    "partially-validated",
    "validated",
    "deprecated",
)

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")
_BUNDLE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_ASSET_KINDS: Final[tuple[str, ...]] = (
    "public-metadata",
    "local-only-external-reference",
    "derived-validation-fixture",
)


class EmergencyCodeMappingPipelineError(ValueError):
    """Raised when an emergency mapping bundle is inconsistent."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise EmergencyCodeMappingPipelineError(f"{field} must be a string")
    if not value:
        raise EmergencyCodeMappingPipelineError(f"{field} must not be blank")
    if value.strip() != value:
        raise EmergencyCodeMappingPipelineError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise EmergencyCodeMappingPipelineError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str, *, field: str) -> str:
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise EmergencyCodeMappingPipelineError(
            f"{field} must be a deterministic version label"
        )
    return normalized


def _normalize_tuple(
    value: Any,
    *,
    field: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise EmergencyCodeMappingPipelineError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise EmergencyCodeMappingPipelineError(
                f"{field} must not contain duplicates"
            )
        seen.add(text)
        normalized.append(text)
    if not normalized and not allow_empty:
        raise EmergencyCodeMappingPipelineError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_source_ref(value: Any, *, field: str) -> str:
    text = _normalize_non_blank(value, field=field)
    parsed = urlsplit(text)
    if parsed.scheme:
        if not parsed.netloc:
            raise EmergencyCodeMappingPipelineError(
                f"{field} must be an absolute URL or relative path"
            )
        return text
    candidate = Path(text)
    if candidate.is_absolute():
        raise EmergencyCodeMappingPipelineError(
            f"{field} must be an absolute URL or relative path"
        )
    if any(part == ".." for part in candidate.parts):
        raise EmergencyCodeMappingPipelineError(
            f"{field} must not contain parent traversal"
        )
    if not text or text == ".":
        raise EmergencyCodeMappingPipelineError(f"{field} must not be blank")
    return text


def _normalize_relative_path(path: str | Path, *, field: str) -> str:
    candidate = path if isinstance(path, Path) else Path(path)
    raw = candidate.as_posix()
    if not raw or raw == ".":
        raise EmergencyCodeMappingPipelineError(f"{field} must not be blank")
    if candidate.is_absolute():
        raise EmergencyCodeMappingPipelineError(f"{field} must be a relative path")
    if any(part == ".." for part in candidate.parts):
        raise EmergencyCodeMappingPipelineError(
            f"{field} must not contain parent traversal"
        )
    return raw


def _normalize_source_refs(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Iterable):
        raise EmergencyCodeMappingPipelineError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_source_ref(item, field=field)
        if text in seen:
            raise EmergencyCodeMappingPipelineError(
                f"{field} must not contain duplicates"
            )
        seen.add(text)
        normalized.append(text)
    if not normalized:
        raise EmergencyCodeMappingPipelineError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_provenance(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise EmergencyCodeMappingPipelineError(f"{field} must be a mapping")
    return dict(value)


def _normalize_source_page_url(value: Any) -> str:
    text = _normalize_non_blank(value, field="source_page_url")
    parsed = urlsplit(text)
    if not parsed.scheme or not parsed.netloc:
        raise EmergencyCodeMappingPipelineError(
            "source_page_url must be an absolute URL"
        )
    return text


def _compute_checksum(payload: Mapping[str, Any]) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class EmergencyCodeMappingAssetReference:
    """Metadata-only reference for an emergency mapping bundle asset."""

    asset_id: str
    kind: Literal[
        "public-metadata",
        "local-only-external-reference",
        "derived-validation-fixture",
    ]
    source_refs: tuple[str, ...]
    local_path_hint: str | None
    restricted: bool
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "asset_id", _normalize_non_blank(self.asset_id, field="asset_id")
        )
        if not _BUNDLE_ID_RE.fullmatch(self.asset_id):
            raise EmergencyCodeMappingPipelineError(
                "asset_id must be lowercase snake_case and deterministic"
            )
        if self.kind not in _ASSET_KINDS:
            raise EmergencyCodeMappingPipelineError(
                f"unsupported asset kind {self.kind!r}"
            )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_source_refs(self.source_refs, field="source_refs"),
        )
        if self.local_path_hint is not None:
            object.__setattr__(
                self,
                "local_path_hint",
                _normalize_relative_path(self.local_path_hint, field="local_path_hint"),
            )
        object.__setattr__(
            self,
            "notes",
            _normalize_tuple(self.notes, field="notes", allow_empty=True),
        )
        if self.kind == "public-metadata":
            if self.local_path_hint is not None:
                raise EmergencyCodeMappingPipelineError(
                    "public-metadata assets must not declare a local_path_hint"
                )
            if self.restricted:
                raise EmergencyCodeMappingPipelineError(
                    "public-metadata assets must not be restricted"
                )
        elif self.kind == "local-only-external-reference":
            if self.local_path_hint is None:
                raise EmergencyCodeMappingPipelineError(
                    "local-only-external-reference assets require a local_path_hint"
                )
            if not self.restricted:
                raise EmergencyCodeMappingPipelineError(
                    "local-only-external-reference assets must be restricted"
                )
            if any(urlsplit(ref).scheme for ref in self.source_refs):
                raise EmergencyCodeMappingPipelineError(
                    "local-only-external-reference assets must use local source_refs"
                )
        elif self.local_path_hint is None:
            raise EmergencyCodeMappingPipelineError(
                "derived-validation-fixture assets require a local_path_hint"
            )

    @property
    def license_boundary(self) -> Literal["metadata-only", "local-only"]:
        return "local-only" if self.restricted else "metadata-only"

    def to_dict(self) -> dict[str, object]:
        return {
            "asset_id": self.asset_id,
            "kind": self.kind,
            "source_refs": list(self.source_refs),
            "local_path_hint": self.local_path_hint,
            "restricted": self.restricted,
            "license_boundary": self.license_boundary,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class EmergencyCodeMappingBundleRecord:
    """Strict, metadata-only manifest for an emergency mapping bundle."""

    bundle_id: str
    pricing_year: str
    stream: str
    target_system: str
    display_name: str
    bundle_version: str
    source_fields: tuple[str, ...]
    output_fields: tuple[str, ...]
    source_page_url: str
    assets: tuple[EmergencyCodeMappingAssetReference, ...]
    validation_status: str
    provenance: dict[str, Any]
    checksum: str
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "bundle_id", _normalize_non_blank(self.bundle_id, field="bundle_id")
        )
        if not _BUNDLE_ID_RE.fullmatch(self.bundle_id):
            raise EmergencyCodeMappingPipelineError(
                "bundle_id must be lowercase snake_case and deterministic"
            )
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        object.__setattr__(
            self,
            "stream",
            _normalize_non_blank(self.stream, field="stream"),
        )
        if self.stream not in EMERGENCY_STREAMS:
            raise EmergencyCodeMappingPipelineError(
                "stream must be one of the emergency transition registry streams"
            )
        object.__setattr__(
            self,
            "target_system",
            normalize_emergency_classification_system(self.target_system),
        )
        object.__setattr__(
            self,
            "display_name",
            _normalize_non_blank(self.display_name, field="display_name"),
        )
        object.__setattr__(
            self,
            "bundle_version",
            _normalize_version(self.bundle_version, field="bundle_version"),
        )
        object.__setattr__(
            self,
            "source_fields",
            _normalize_tuple(self.source_fields, field="source_fields"),
        )
        object.__setattr__(
            self,
            "output_fields",
            _normalize_tuple(self.output_fields, field="output_fields"),
        )
        object.__setattr__(
            self,
            "source_page_url",
            _normalize_source_page_url(self.source_page_url),
        )
        object.__setattr__(self, "assets", tuple(self.assets))
        object.__setattr__(
            self,
            "validation_status",
            _normalize_non_blank(self.validation_status, field="validation_status"),
        )
        if self.validation_status not in EMERGENCY_CODE_MAPPING_VALIDATION_STATUSES:
            raise EmergencyCodeMappingPipelineError(
                f"unsupported validation_status {self.validation_status!r}"
            )
        object.__setattr__(
            self,
            "provenance",
            _normalize_provenance(self.provenance, field="provenance"),
        )
        object.__setattr__(
            self,
            "notes",
            _normalize_tuple(self.notes, field="notes", allow_empty=True),
        )
        if not self.assets:
            raise EmergencyCodeMappingPipelineError("assets must not be empty")
        asset_ids = [asset.asset_id for asset in self.assets]
        if len(set(asset_ids)) != len(asset_ids):
            raise EmergencyCodeMappingPipelineError(
                "assets must not contain duplicate asset_id values"
            )

        record = get_emergency_classification_record(self.target_system)
        if self.display_name != record.display_name:
            raise EmergencyCodeMappingPipelineError(
                f"display_name for {self.target_system!r} must be "
                f"{record.display_name!r}"
            )
        expected_version = get_expected_emergency_classification_version(
            self.target_system,
            self.pricing_year,
        )
        if expected_version is None:
            raise EmergencyCodeMappingPipelineError(
                f"{self.target_system!r} is not available for pricing year "
                f"{self.pricing_year!r}"
            )
        if self.bundle_version != expected_version:
            raise EmergencyCodeMappingPipelineError(
                f"bundle_version for {self.target_system!r} in {self.pricing_year!r} "
                f"must be {expected_version!r}"
            )
        required_fields = EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS[self.target_system]
        if not set(required_fields).issubset(self.output_fields):
            raise EmergencyCodeMappingPipelineError(
                f"output_fields for {self.target_system!r} in {self.pricing_year!r} "
                f"must include {required_fields!r}"
            )
        if not set(self.source_fields).issubset(self.output_fields):
            raise EmergencyCodeMappingPipelineError(
                "source_fields must be preserved in output_fields for auditability"
            )
        if any(field in required_fields for field in self.source_fields):
            raise EmergencyCodeMappingPipelineError(
                "source_fields must not claim the target classification output"
            )
        other_required_fields = {
            field
            for system, fields in EMERGENCY_CLASSIFICATION_REQUIRED_FIELDS.items()
            if system != self.target_system
            for field in fields
        }
        if any(field in other_required_fields for field in self.source_fields):
            raise EmergencyCodeMappingPipelineError(
                "source_fields must not claim another emergency classification output"
            )
        if self.stream not in record.stream_compatibility:
            raise EmergencyCodeMappingPipelineError(
                f"{self.target_system!r} is not compatible with stream {self.stream!r}"
            )

        if not self.checksum:
            payload = self._checksum_payload()
            object.__setattr__(self, "checksum", _compute_checksum(payload))
        else:
            object.__setattr__(
                self,
                "checksum",
                _normalize_version(self.checksum, field="checksum").lower(),
            )
        if len(self.checksum) != 64 or any(
            char not in "0123456789abcdef" for char in self.checksum
        ):
            raise EmergencyCodeMappingPipelineError(
                "checksum must be a lowercase sha256 hex digest"
            )

    @property
    def license_boundary(self) -> Literal["metadata-only", "local-only"]:
        return (
            "local-only"
            if any(asset.license_boundary == "local-only" for asset in self.assets)
            else "metadata-only"
        )

    def _checksum_payload(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "target_system": self.target_system,
            "display_name": self.display_name,
            "bundle_version": self.bundle_version,
            "source_fields": list(self.source_fields),
            "output_fields": list(self.output_fields),
            "source_page_url": self.source_page_url,
            "assets": [asset.to_dict() for asset in self.assets],
            "validation_status": self.validation_status,
            "provenance": self.provenance,
            "notes": list(self.notes),
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "bundle_id": self.bundle_id,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "target_system": self.target_system,
            "display_name": self.display_name,
            "bundle_version": self.bundle_version,
            "source_fields": list(self.source_fields),
            "output_fields": list(self.output_fields),
            "source_page_url": self.source_page_url,
            "assets": [asset.to_dict() for asset in self.assets],
            "validation_status": self.validation_status,
            "license_boundary": self.license_boundary,
            "provenance": dict(self.provenance),
            "checksum": self.checksum,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class EmergencyCodeMappingBundleCompatibilityResult:
    """Outcome from a fail-closed emergency mapping bundle compatibility check."""

    bundle_id: str
    target_system: str
    display_name: str
    pricing_year: str
    stream: str
    declared_version: str
    expected_version: str | None
    acceptance_state: str
    compatibility_state: Literal[
        "valid",
        "transition",
        "shadow-priced",
        "missing",
        "incompatible",
    ]
    compatible: bool
    source_fields: tuple[str, ...]
    output_fields: tuple[str, ...]
    source_page_url: str
    source_refs: tuple[str, ...]
    reason: str | None
    record: EmergencyCodeMappingBundleRecord | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "bundle_id": self.bundle_id,
            "target_system": self.target_system,
            "display_name": self.display_name,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "declared_version": self.declared_version,
            "expected_version": self.expected_version,
            "acceptance_state": self.acceptance_state,
            "compatibility_state": self.compatibility_state,
            "compatible": self.compatible,
            "source_fields": list(self.source_fields),
            "output_fields": list(self.output_fields),
            "source_page_url": self.source_page_url,
            "source_refs": list(self.source_refs),
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class EmergencyCodeMappingDryRunSummary:
    """Dry-run summary for metadata-only emergency mapping review."""

    bundle_id: str
    pricing_year: str
    stream: str
    target_system: str
    observed_fields: tuple[str, ...]
    unknown_fields: tuple[str, ...]
    unmapped_fields: tuple[str, ...]
    deprecated_fields: tuple[str, ...]
    invalid_fields: tuple[str, ...]
    compatibility: EmergencyCodeMappingBundleCompatibilityResult

    def to_dict(self) -> dict[str, object]:
        return {
            "bundle_id": self.bundle_id,
            "pricing_year": self.pricing_year,
            "stream": self.stream,
            "target_system": self.target_system,
            "observed_fields": list(self.observed_fields),
            "unknown_fields": list(self.unknown_fields),
            "unmapped_fields": list(self.unmapped_fields),
            "deprecated_fields": list(self.deprecated_fields),
            "invalid_fields": list(self.invalid_fields),
            "compatibility": self.compatibility.to_dict(),
        }


def build_emergency_code_mapping_asset_reference(
    *,
    asset_id: str,
    kind: Literal[
        "public-metadata",
        "local-only-external-reference",
        "derived-validation-fixture",
    ],
    source_refs: Iterable[str],
    local_path_hint: str | Path | None,
    restricted: bool,
    notes: Iterable[str] = (),
) -> EmergencyCodeMappingAssetReference:
    """Build a strict metadata-only asset reference for an emergency mapping bundle."""
    return EmergencyCodeMappingAssetReference(
        asset_id=asset_id,
        kind=kind,
        source_refs=tuple(source_refs),
        local_path_hint=None if local_path_hint is None else str(local_path_hint),
        restricted=restricted,
        notes=tuple(notes),
    )


def build_emergency_code_mapping_bundle_record(
    *,
    bundle_id: str,
    pricing_year: str,
    stream: str,
    system: str | None = None,
    target_system: str | None = None,
    display_name: str | None = None,
    bundle_version: str | None = None,
    source_fields: Iterable[str],
    output_fields: Iterable[str],
    source_page_url: str | None = None,
    assets: Iterable[EmergencyCodeMappingAssetReference],
    validation_status: str = "schema-complete",
    provenance: Mapping[str, Any] | None = None,
    checksum: str = "",
    notes: Iterable[str] = (),
) -> EmergencyCodeMappingBundleRecord:
    """Build a strict emergency mapping bundle record from typed inputs."""
    if system is None and target_system is None:
        raise EmergencyCodeMappingPipelineError("system or target_system is required")
    if system is not None and target_system is not None:
        canonical_system = normalize_emergency_classification_system(system)
        if canonical_system != normalize_emergency_classification_system(target_system):
            raise EmergencyCodeMappingPipelineError(
                "system and target_system must refer to the same emergency "
                "classification"
            )
    else:
        selected_system = system if system is not None else target_system
        if selected_system is None:
            raise EmergencyCodeMappingPipelineError(
                "system or target_system is required"
            )
        canonical_system = normalize_emergency_classification_system(selected_system)
    normalized_year = _normalize_year(pricing_year)
    resolved_display_name = (
        display_name
        if display_name is not None
        else get_emergency_classification_name(canonical_system)
    )
    resolved_source_page_url = (
        source_page_url
        if source_page_url is not None
        else EMERGENCY_CLASSIFICATION_SOURCE_REFS[canonical_system][0]
    )
    normalized_version = (
        _normalize_version(bundle_version, field="bundle_version")
        if bundle_version is not None
        else get_expected_emergency_classification_version(
            canonical_system,
            normalized_year,
        )
    )
    if normalized_version is None:
        raise EmergencyCodeMappingPipelineError(
            f"{canonical_system!r} is not available for pricing year "
            f"{normalized_year!r}"
        )
    return EmergencyCodeMappingBundleRecord(
        bundle_id=bundle_id,
        pricing_year=normalized_year,
        stream=stream,
        target_system=canonical_system,
        display_name=resolved_display_name,
        bundle_version=normalized_version,
        source_fields=tuple(source_fields),
        output_fields=tuple(output_fields),
        source_page_url=resolved_source_page_url,
        assets=tuple(assets),
        validation_status=validation_status,
        provenance={} if provenance is None else dict(provenance),
        checksum=checksum,
        notes=tuple(notes),
    )


_EMERGENCY_CODE_MAPPING_BUNDLE_RECORDS: Final[
    tuple[EmergencyCodeMappingBundleRecord, ...]
] = (
    build_emergency_code_mapping_bundle_record(
        bundle_id="emergency_code_mapping_udg_2025",
        pricing_year="2025",
        stream="emergency_department",
        target_system="udg",
        display_name="UDG",
        source_fields=("COMPENSABLE_STATUS", "DVA_STATUS"),
        output_fields=("UDG", "COMPENSABLE_STATUS", "DVA_STATUS"),
        source_page_url=EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"][0],
        assets=(
            build_emergency_code_mapping_asset_reference(
                asset_id="udg_2025_public_metadata",
                kind="public-metadata",
                source_refs=(
                    EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"][0],
                    "conductor/tracks/emergency_code_mapping_pipeline_20260512/spec.md",
                    "nwau_py/emergency_transition_registry.py",
                ),
                local_path_hint=None,
                restricted=False,
                notes=(
                    "Metadata-only reference for the 2025 UDG-era mapping bundle.",
                    "The bundle records source and output fields without a crosswalk.",
                ),
            ),
            build_emergency_code_mapping_asset_reference(
                asset_id="udg_2025_local_reference",
                kind="local-only-external-reference",
                source_refs=(
                    "reference-data/2025/emergency/udg/mapping-bundle.yaml",
                    "reference-data/2025/emergency/udg/manifest.yaml",
                ),
                local_path_hint="archive/ihacpa/raw/2025/emergency/udg/mapping-bundle.yaml",
                restricted=True,
                notes=(
                    "Local-only mapping reference placeholder; no bundle payload "
                    "is committed.",
                    "This reference stays local and is not a fetch target.",
                ),
            ),
            build_emergency_code_mapping_asset_reference(
                asset_id="udg_2025_validation_fixture",
                kind="derived-validation-fixture",
                source_refs=(
                    "tests/fixtures/derived/emergency_code_mapping/2025/udg/manifest.json",
                    "conductor/tracks/emergency_code_mapping_pipeline_20260512/spec.md",
                ),
                local_path_hint="tests/fixtures/derived/emergency_code_mapping/2025/udg/manifest.json",
                restricted=False,
                notes=("Derived validation fixture for dry-run bundle review.",),
            ),
        ),
        validation_status="validated",
        provenance={
            "source_type": "official-and-local-metadata",
            "source_page_url": EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"][0],
            "source_refs": [
                EMERGENCY_CLASSIFICATION_SOURCE_REFS["udg"][0],
                "conductor/tracks/emergency_code_mapping_pipeline_20260512/spec.md",
            ],
            "checksum_algorithm": "sha256",
            "notes": [
                "Metadata-only bundle reference; no crosswalk is embedded.",
                "The bundle preserves source fields and mapped output fields "
                "for auditability.",
            ],
        },
        notes=(
            "UDG-era metadata bundle reference with local-only external mapping hints.",
            "No invented UDG-to-AECC crosswalk is stored here.",
        ),
    ),
    build_emergency_code_mapping_bundle_record(
        bundle_id="emergency_code_mapping_aecc_2026",
        pricing_year="2026",
        stream="emergency_department",
        target_system="aecc",
        display_name="AECC",
        source_fields=("COMPENSABLE_STATUS", "DVA_STATUS"),
        output_fields=("AECC", "COMPENSABLE_STATUS", "DVA_STATUS"),
        source_page_url=EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"][0],
        assets=(
            build_emergency_code_mapping_asset_reference(
                asset_id="aecc_2026_public_metadata",
                kind="public-metadata",
                source_refs=(
                    EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"][0],
                    "conductor/tracks/emergency_code_mapping_pipeline_20260512/spec.md",
                    "nwau_py/emergency_transition_registry.py",
                ),
                local_path_hint=None,
                restricted=False,
                notes=(
                    "Metadata-only reference for the 2026 AECC-era mapping bundle.",
                    "The bundle records source and output fields without a crosswalk.",
                ),
            ),
            build_emergency_code_mapping_asset_reference(
                asset_id="aecc_2026_local_reference",
                kind="local-only-external-reference",
                source_refs=(
                    "reference-data/2026/emergency/aecc/mapping-bundle.yaml",
                    "reference-data/2026/emergency/aecc/manifest.yaml",
                ),
                local_path_hint="archive/ihacpa/raw/2026/emergency/aecc/mapping-bundle.yaml",
                restricted=True,
                notes=(
                    "Local-only mapping reference placeholder; no bundle payload "
                    "is committed.",
                    "This reference stays local and is not a fetch target.",
                ),
            ),
            build_emergency_code_mapping_asset_reference(
                asset_id="aecc_2026_validation_fixture",
                kind="derived-validation-fixture",
                source_refs=(
                    "tests/fixtures/derived/emergency_code_mapping/2026/aecc/manifest.json",
                    "conductor/tracks/emergency_code_mapping_pipeline_20260512/spec.md",
                ),
                local_path_hint="tests/fixtures/derived/emergency_code_mapping/2026/aecc/manifest.json",
                restricted=False,
                notes=("Derived validation fixture for dry-run bundle review.",),
            ),
        ),
        validation_status="validated",
        provenance={
            "source_type": "official-and-local-metadata",
            "source_page_url": EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"][0],
            "source_refs": [
                EMERGENCY_CLASSIFICATION_SOURCE_REFS["aecc"][0],
                "conductor/tracks/emergency_code_mapping_pipeline_20260512/spec.md",
            ],
            "checksum_algorithm": "sha256",
            "notes": [
                "Metadata-only bundle reference; no crosswalk is embedded.",
                "The bundle preserves source fields and mapped output fields "
                "for auditability.",
            ],
        },
        notes=(
            "AECC-era metadata bundle reference with local-only external mapping "
            "hints.",
            "No invented AECC-to-UDG crosswalk is stored here.",
        ),
    ),
)

_EMERGENCY_CODE_MAPPING_BUNDLE_BY_KEY: Final[
    dict[tuple[str, str], EmergencyCodeMappingBundleRecord]
] = {
    (record.target_system, record.pricing_year): record
    for record in _EMERGENCY_CODE_MAPPING_BUNDLE_RECORDS
}

EMERGENCY_CODE_MAPPING_BUNDLE_VERSION_MATRIX: Final[dict[str, dict[str, str]]] = {
    system: {
        record.pricing_year: record.bundle_version
        for record in sorted(
            (
                record
                for record in _EMERGENCY_CODE_MAPPING_BUNDLE_RECORDS
                if record.target_system == system
            ),
            key=lambda record: record.pricing_year,
        )
    }
    for system in sorted(
        {record.target_system for record in _EMERGENCY_CODE_MAPPING_BUNDLE_RECORDS}
    )
}


def list_emergency_code_mapping_bundle_records(
    *,
    system: str | None = None,
    target_system: str | None = None,
    pricing_year: str | None = None,
) -> tuple[EmergencyCodeMappingBundleRecord, ...]:
    """Return registered emergency mapping bundle records, optionally filtered."""
    records = _EMERGENCY_CODE_MAPPING_BUNDLE_RECORDS
    if system is not None and target_system is not None:
        canonical_system = normalize_emergency_classification_system(system)
        if canonical_system != normalize_emergency_classification_system(target_system):
            raise EmergencyCodeMappingPipelineError(
                "system and target_system must refer to the same emergency "
                "classification"
            )
    elif system is not None:
        canonical_system = normalize_emergency_classification_system(system)
    elif target_system is not None:
        canonical_system = normalize_emergency_classification_system(target_system)
    else:
        canonical_system = ""
    if canonical_system:
        records = tuple(
            record for record in records if record.target_system == canonical_system
        )
    if pricing_year is not None:
        normalized_year = _normalize_year(pricing_year)
        records = tuple(
            record for record in records if record.pricing_year == normalized_year
        )
    return records


def get_emergency_code_mapping_bundle_record(
    system: str,
    pricing_year: str,
) -> EmergencyCodeMappingBundleRecord | None:
    """Return a registered emergency mapping bundle record, if one exists."""
    canonical_system = normalize_emergency_classification_system(system)
    normalized_year = _normalize_year(pricing_year)
    return _EMERGENCY_CODE_MAPPING_BUNDLE_BY_KEY.get(
        (canonical_system, normalized_year)
    )


def validate_emergency_code_mapping_bundle_compatibility(
    record: EmergencyCodeMappingBundleRecord,
) -> EmergencyCodeMappingBundleCompatibilityResult:
    """Check whether a mapping bundle record stays within registry scope."""
    registry_result: EmergencyClassificationCompatibilityResult = (
        validate_emergency_classification_compatibility(
            record.target_system,
            record.pricing_year,
            record.bundle_version,
            stream=record.stream,
        )
    )
    if not registry_result.compatible:
        return EmergencyCodeMappingBundleCompatibilityResult(
            bundle_id=record.bundle_id,
            target_system=record.target_system,
            display_name=record.display_name,
            pricing_year=record.pricing_year,
            stream=record.stream,
            declared_version=record.bundle_version,
            expected_version=registry_result.expected_version,
            acceptance_state=registry_result.acceptance_state,
            compatibility_state=registry_result.compatibility_state,
            compatible=False,
            source_fields=record.source_fields,
            output_fields=record.output_fields,
            source_page_url=record.source_page_url,
            source_refs=tuple(
                ref for asset in record.assets for ref in asset.source_refs
            ),
            reason=registry_result.reason,
            record=record,
        )

    return EmergencyCodeMappingBundleCompatibilityResult(
        bundle_id=record.bundle_id,
        target_system=record.target_system,
        display_name=record.display_name,
        pricing_year=record.pricing_year,
        stream=record.stream,
        declared_version=record.bundle_version,
        expected_version=registry_result.expected_version,
        acceptance_state=registry_result.acceptance_state,
        compatibility_state=registry_result.compatibility_state,
        compatible=True,
        source_fields=record.source_fields,
        output_fields=record.output_fields,
        source_page_url=record.source_page_url,
        source_refs=tuple(ref for asset in record.assets for ref in asset.source_refs),
        reason=None,
        record=record,
    )


def ensure_emergency_code_mapping_bundle_compatibility(
    record: EmergencyCodeMappingBundleRecord,
) -> EmergencyCodeMappingBundleCompatibilityResult:
    """Raise when a mapping bundle record falls outside its declared safe scope."""
    result = validate_emergency_code_mapping_bundle_compatibility(record)
    if not result.compatible:
        raise EmergencyCodeMappingPipelineError(
            result.reason or "emergency code mapping bundle is incompatible"
        )
    return result


def summarize_emergency_code_mapping_dry_run(
    record: EmergencyCodeMappingBundleRecord,
    *,
    observed_fields: Iterable[str] = (),
) -> EmergencyCodeMappingDryRunSummary:
    """Summarize a dry-run review for a metadata-only mapping bundle.

    Unknown fields are observed fields not declared by the bundle. Unmapped
    fields are declared source fields that are not preserved in the output
    surface. Deprecated fields may be declared in provenance metadata under the
    ``deprecated_fields`` key.
    """
    observed = _normalize_tuple(
        observed_fields,
        field="observed_fields",
        allow_empty=True,
    )
    declared_surface = set(record.source_fields) | set(record.output_fields)
    unknown = tuple(field for field in observed if field not in declared_surface)
    unmapped = tuple(
        field for field in record.source_fields if field not in record.output_fields
    )
    deprecated_raw = record.provenance.get("deprecated_fields", ())
    deprecated = _normalize_tuple(
        deprecated_raw,
        field="provenance.deprecated_fields",
        allow_empty=True,
    )
    invalid = tuple(
        field
        for field in observed
        if not _BUNDLE_ID_RE.fullmatch(field.replace("-", "_").lower())
        and field not in declared_surface
    )
    return EmergencyCodeMappingDryRunSummary(
        bundle_id=record.bundle_id,
        pricing_year=record.pricing_year,
        stream=record.stream,
        target_system=record.target_system,
        observed_fields=observed,
        unknown_fields=unknown,
        unmapped_fields=unmapped,
        deprecated_fields=deprecated,
        invalid_fields=invalid,
        compatibility=validate_emergency_code_mapping_bundle_compatibility(record),
    )
