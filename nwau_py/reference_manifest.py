"""Strict loaders for IHACPA reference-data manifests."""

from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlsplit

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

__all__ = [
    "SUPPORTED_MANIFEST_SCHEMA_VERSION",
    "SUPPORTED_VALIDATION_STATUSES",
    "ReferenceArtifact",
    "ReferenceCodingSet",
    "ReferenceDataManifest",
    "ReferenceGap",
    "ReferenceManifestError",
    "ReferenceValidation",
    "load_reference_manifest",
    "parse_reference_manifest",
]

SUPPORTED_MANIFEST_SCHEMA_VERSION = "1.0"
SUPPORTED_VALIDATION_STATUSES = (
    "source-discovered",
    "source-only",
    "schema-complete",
    "gap-explicit",
    "partially-validated",
    "validated",
    "deprecated",
)
PINNED_EXAMPLE_YEARS = ("2025", "2026")


class ReferenceManifestError(ValueError):
    """Raised when a reference-data manifest fails strict validation."""


def _non_blank(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    if value.strip() != value or not value:
        raise ValueError(f"{field_name} must be a non-empty trimmed string")
    return value


def _url(value: Any, field_name: str) -> str:
    url = _non_blank(value, field_name)
    parsed = urlsplit(url)
    if not parsed.scheme or not (parsed.netloc or parsed.path):
        raise ValueError(f"{field_name} must be an absolute URL")
    return url


def _sha256(value: Any) -> str:
    digest = _non_blank(value, "sha256")
    if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
        raise ValueError("sha256 must be a lowercase 64-character hex digest")
    return digest


def _iso_date(value: Any, field_name: str) -> date:
    if isinstance(value, date) and not isinstance(value, bool):
        return value
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO-8601 date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO-8601 date") from exc


def _as_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return value


def _format_validation_error(exc: ValidationError) -> str:
    lines = []
    for error in sorted(exc.errors(), key=lambda item: tuple(map(str, item["loc"]))):
        location = ".".join(str(part) for part in error["loc"])
        lines.append(f"- {location}: {error['msg']}")
    return "reference manifest validation failed:\n" + "\n".join(lines)


class StrictModel(BaseModel):
    """Shared strict pydantic configuration for manifest models."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class ReferenceSourceRegister(StrictModel):
    """Top-level IHACPA source-page register."""

    resource_page_url: str
    resource_page_published_on: date
    resource_page_last_updated_on: date | None = None
    technical_spec_url: str | None = None
    technical_spec_published_on: date | None = None
    price_weights_reference: dict[str, Any] = Field(default_factory=dict)
    adjustments_reference: dict[str, Any] = Field(default_factory=dict)

    @field_validator("resource_page_url", "technical_spec_url")
    @classmethod
    def _validate_urls(cls, value: Any, info: Any) -> str | None:
        if value is None:
            return None
        return _url(value, info.field_name)

    @field_validator(
        "resource_page_published_on",
        "resource_page_last_updated_on",
        "technical_spec_published_on",
        mode="before",
    )
    @classmethod
    def _validate_dates(cls, value: Any, info: Any) -> date | None:
        if value is None:
            return None
        return _iso_date(value, info.field_name)


class ReferenceArtifact(StrictModel):
    """Source artifact with provenance and digest."""

    artifact_id: str
    kind: str
    service_stream: str
    title: str
    url: str
    local_path: str
    published_on: date
    retrieved_on: date
    publication_date_basis: str
    sha256: str
    bytes: int
    license: str
    provenance: str

    @field_validator(
        "artifact_id",
        "kind",
        "service_stream",
        "title",
        "local_path",
        "publication_date_basis",
        "license",
        "provenance",
    )
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("url")
    @classmethod
    def _validate_url(cls, value: Any) -> str:
        return _url(value, "url")

    @field_validator("published_on", "retrieved_on", mode="before")
    @classmethod
    def _validate_dates(cls, value: Any, info: Any) -> date:
        return _iso_date(value, info.field_name)

    @field_validator("sha256")
    @classmethod
    def _validate_sha256(cls, value: Any) -> str:
        return _sha256(value)

    @field_validator("bytes")
    @classmethod
    def _validate_bytes(cls, value: Any) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("bytes must be a positive integer")
        return value


class ReferenceCodingSet(StrictModel):
    """Versioned coding-set reference."""

    name: str
    version: str
    status: str
    source_url: str
    note: str
    official_page_version: str | None = None

    @field_validator("name", "version", "status", "note", "official_page_version")
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str | None:
        if value is None:
            return None
        return _non_blank(value, info.field_name)

    @field_validator("source_url")
    @classmethod
    def _validate_source_url(cls, value: Any) -> str:
        return _url(value, "source_url")


class ReferenceValidation(StrictModel):
    """Validation status for a pricing-year manifest."""

    status: Literal[
        "source-discovered",
        "source-only",
        "schema-complete",
        "gap-explicit",
        "partially-validated",
        "validated",
        "deprecated",
    ]
    parity_claim: bool
    source_only: bool
    notes: tuple[str, ...]

    @field_validator("notes", mode="before")
    @classmethod
    def _validate_notes(cls, value: Any) -> tuple[str, ...]:
        items = _as_list(value, "validation.notes")
        if not all(isinstance(item, str) and item for item in items):
            raise ValueError("validation.notes must contain non-empty strings")
        return tuple(item for item in items if isinstance(item, str))


class ReferenceGap(StrictModel):
    """Explicit missing-artifact or unresolved-scope record."""

    gap_id: str
    kind: Literal[
        "source_missing",
        "publication_pending",
        "checksum_unavailable",
        "value_unpublished",
        "license_unclear",
        "scope_unknown",
        "validation_blocked",
    ]
    scope: str
    reason: str
    expected_resolution: str
    introduced_at: date
    status: Literal["open", "tracked", "resolved"]

    @field_validator("gap_id", "scope", "reason", "expected_resolution")
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("introduced_at", mode="before")
    @classmethod
    def _validate_introduced_at(cls, value: Any) -> date:
        return _iso_date(value, "introduced_at")


class ReferenceDataManifest(StrictModel):
    """Strict machine-readable manifest for one IHACPA pricing year."""

    schema_version: str
    bundle_id: str
    pricing_year: str
    financial_year: str
    calculator: str
    current_pricing_year: bool
    validation_status: Literal[
        "source-discovered",
        "source-only",
        "schema-complete",
        "gap-explicit",
        "partially-validated",
        "validated",
        "deprecated",
    ]
    source_register: ReferenceSourceRegister
    source_artifacts: tuple[ReferenceArtifact, ...]
    constants: dict[str, Any]
    coding_sets: tuple[ReferenceCodingSet, ...]
    validation: ReferenceValidation
    gaps: tuple[ReferenceGap, ...]
    canonical_path: Path

    @field_validator("schema_version")
    @classmethod
    def _validate_schema_version(cls, value: Any) -> str:
        schema_version = _non_blank(value, "schema_version")
        if schema_version != SUPPORTED_MANIFEST_SCHEMA_VERSION:
            raise ValueError(
                "unsupported schema_version "
                f"{schema_version!r}; expected {SUPPORTED_MANIFEST_SCHEMA_VERSION!r}"
            )
        return schema_version

    @field_validator("bundle_id", "pricing_year", "financial_year", "calculator")
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("source_artifacts", "coding_sets", "gaps", mode="before")
    @classmethod
    def _validate_lists(cls, value: Any, info: Any) -> tuple[Any, ...]:
        return tuple(_as_list(value, info.field_name))

    @field_validator("canonical_path", mode="before")
    @classmethod
    def _validate_path(cls, value: Any) -> Path:
        if isinstance(value, Path):
            return value
        if not isinstance(value, str) or not value:
            raise ValueError("canonical_path must be a non-empty path")
        return Path(value)

    @field_validator("source_artifacts")
    @classmethod
    def _validate_artifact_ids(
        cls, value: tuple[ReferenceArtifact, ...]
    ) -> tuple[ReferenceArtifact, ...]:
        if not value:
            raise ValueError("source_artifacts must not be empty")
        duplicates = [
            name
            for name, count in Counter(item.artifact_id for item in value).items()
            if count > 1
        ]
        if duplicates:
            raise ValueError(
                "source_artifacts contains duplicate artifact_id values: "
                + ", ".join(sorted(duplicates))
            )
        return value

    @field_validator("gaps")
    @classmethod
    def _validate_gap_ids(
        cls, value: tuple[ReferenceGap, ...]
    ) -> tuple[ReferenceGap, ...]:
        duplicates = [
            name
            for name, count in Counter(item.gap_id for item in value).items()
            if count > 1
        ]
        if duplicates:
            raise ValueError(
                "gaps contains duplicate gap_id values: "
                + ", ".join(sorted(duplicates))
            )
        return value

    def unresolved_gaps(self) -> tuple[ReferenceGap, ...]:
        """Return gaps that still block stronger validation claims."""
        return tuple(gap for gap in self.gaps if gap.status != "resolved")


def parse_reference_manifest(
    payload: Any,
    *,
    canonical_path: str | Path,
) -> ReferenceDataManifest:
    """Validate a raw manifest payload and attach its canonical path."""
    if not isinstance(payload, dict):
        raise ReferenceManifestError("reference manifest must be a mapping")
    data = dict(payload)
    data["canonical_path"] = Path(canonical_path)

    try:
        manifest = ReferenceDataManifest.model_validate(data)
    except ValidationError as exc:
        raise ReferenceManifestError(_format_validation_error(exc)) from exc

    expected_path = Path("reference-data") / manifest.pricing_year / "manifest.yaml"
    actual_path = manifest.canonical_path
    if actual_path.is_absolute() and "reference-data" in actual_path.parts:
        start = actual_path.parts.index("reference-data")
        actual_path = Path(*actual_path.parts[start:])
    if actual_path.as_posix() != expected_path.as_posix():
        raise ReferenceManifestError(
            "reference manifest validation failed:\n"
            f"- canonical_path: expected {expected_path.as_posix()!r}, "
            f"got {manifest.canonical_path.as_posix()!r}"
        )
    if manifest.validation_status != manifest.validation.status:
        raise ReferenceManifestError(
            "reference manifest validation failed:\n"
            "- validation.status: must match top-level validation_status"
        )
    if manifest.validation_status == "validated" and manifest.unresolved_gaps():
        raise ReferenceManifestError(
            "reference manifest validation failed:\n"
            "- gaps: validated manifests must not contain unresolved gaps"
        )
    return manifest


def load_reference_manifest(manifest_path: str | Path) -> ReferenceDataManifest:
    """Load and strictly validate a YAML reference-data manifest from disk."""
    path = Path(manifest_path)
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ReferenceManifestError(
            f"failed to parse YAML reference manifest at {path}: {exc}"
        ) from exc
    return parse_reference_manifest(payload, canonical_path=path)
