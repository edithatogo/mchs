"""Conservative workflow helpers for licensed classification products.

This module is intentionally metadata-only. It provides:

- strict manifest records for local-only ICD-10-AM, ACHI, ACS, and AR-DRG
  asset references;
- path validation that rejects absolute or traversal-prone local hints;
- allowlisted metadata for machine-readable manifests; and
- commit-safe exclusion checks for restricted assets that must stay out of Git.

It does not bundle licensed tables, code rows, or grouper binaries.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal, cast
from urllib.parse import urlsplit

from .coding_set_registry import (
    get_expected_coding_set_version,
    normalize_coding_set_system,
)
from .licensed_product_workflow_data import LICENSED_PRODUCT_WORKFLOW_ROWS

__all__ = [
    "ALLOWED_LICENSED_PRODUCT_METADATA_KEYS",
    "COMMIT_SAFE_LICENSED_ROOTS",
    "LICENSED_PRODUCT_SYSTEMS",
    "LOCAL_ONLY_LICENSED_ROOTS",
    "LicensedProductAssetReference",
    "LicensedProductCompatibilityResult",
    "LicensedProductManifestRecord",
    "LicensedProductWorkflowError",
    "build_licensed_product_asset_reference",
    "build_licensed_product_manifest_record",
    "diagnose_missing_licensed_assets",
    "ensure_commit_safe_exclusion",
    "ensure_licensed_product_compatibility",
    "get_licensed_product_manifest_record",
    "is_commit_safe_excluded_path",
    "is_local_only_licensed_path",
    "list_licensed_product_manifest_records",
    "resolve_licensed_product_env_path",
    "validate_licensed_product_compatibility",
]

LICENSED_PRODUCT_SYSTEMS: Final[tuple[str, ...]] = (
    "ar_drg",
    "icd_10_am",
    "achi",
    "acs",
)
LOCAL_ONLY_LICENSED_ROOTS: Final[tuple[Path, ...]] = (
    Path("archive/ihacpa/raw"),
    Path("licensed"),
)
COMMIT_SAFE_LICENSED_ROOTS: Final[tuple[Path, ...]] = (Path("archive/ihacpa/raw"),)
ALLOWED_LICENSED_PRODUCT_METADATA_KEYS: Final[frozenset[str]] = frozenset(
    {
        "asset_role",
        "display_name",
        "expected_version",
        "financial_year",
        "license_boundary",
        "manifest_role",
        "pricing_year",
        "product_family",
        "source_page_url",
        "source_refs",
        "system",
        "version",
    }
)
_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")
_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:[\\/]")


class LicensedProductWorkflowError(ValueError):
    """Raised when a licensed-product manifest or path is invalid."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise LicensedProductWorkflowError(f"{field} must be a string")
    if not value:
        raise LicensedProductWorkflowError(f"{field} must not be blank")
    if value.strip() != value:
        raise LicensedProductWorkflowError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise LicensedProductWorkflowError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str | None, *, field: str) -> str | None:
    if version is None:
        return None
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise LicensedProductWorkflowError(
            f"{field} must be a deterministic version label"
        )
    return normalized


def _normalize_str_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise LicensedProductWorkflowError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise LicensedProductWorkflowError(f"{field} must not contain duplicates")
        seen.add(text)
        normalized.append(text)
    if not normalized:
        raise LicensedProductWorkflowError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_relative_path(path: str | Path, *, field: str) -> str:
    candidate = path if isinstance(path, Path) else Path(path)
    if candidate == Path(""):
        raise LicensedProductWorkflowError(f"{field} must not be blank")
    raw = candidate.as_posix()
    if _WINDOWS_DRIVE_RE.match(raw) or candidate.is_absolute():
        raise LicensedProductWorkflowError(f"{field} must be a relative path")
    if any(part == ".." for part in candidate.parts):
        raise LicensedProductWorkflowError(f"{field} must not contain parent traversal")
    normalized = candidate.as_posix()
    if not normalized or normalized == ".":
        raise LicensedProductWorkflowError(f"{field} must not be blank")
    return normalized


def _is_descendant(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def is_local_only_licensed_path(path: str | Path) -> bool:
    """Return ``True`` when a path points into local-only licensed storage."""
    normalized = Path(_normalize_relative_path(path, field="path"))
    return any(_is_descendant(normalized, root) for root in LOCAL_ONLY_LICENSED_ROOTS)


def is_commit_safe_excluded_path(path: str | Path) -> bool:
    """Return ``True`` when a path is inside a Git-ignored licensed root."""
    normalized = Path(_normalize_relative_path(path, field="path"))
    return any(_is_descendant(normalized, root) for root in COMMIT_SAFE_LICENSED_ROOTS)


def ensure_commit_safe_exclusion(path: str | Path) -> str:
    """Raise when a restricted path is not inside a commit-safe exclusion root."""
    normalized = _normalize_relative_path(path, field="path")
    if not is_commit_safe_excluded_path(normalized):
        raise LicensedProductWorkflowError(
            "restricted licensed assets must live under commit-safe ignored storage "
            "(expected a path under archive/ihacpa/raw/)"
        )
    return normalized


def resolve_licensed_product_env_path(
    env_var: str,
    *,
    environ: Mapping[str, str] | None = None,
    subpath: str | Path | None = None,
) -> str:
    """Resolve an environment-backed licensed asset reference safely.

    The resolved value is still a local-only path hint. The returned path is
    normalized and validated, but the function does not read the asset.
    """
    name = _normalize_non_blank(env_var, field="env_var")
    env = os.environ if environ is None else environ
    value = env.get(name)
    if value is None or not value:
        raise LicensedProductWorkflowError(
            f"required licensed asset environment variable {name!r} is not set"
        )
    base = Path(_normalize_relative_path(value, field=f"env.{name}"))
    resolved = (
        base
        if subpath is None
        else base
        / _normalize_relative_path(
            subpath,
            field="subpath",
        )
    )
    normalized = _normalize_relative_path(resolved, field=f"env.{name}")
    if not is_local_only_licensed_path(normalized):
        raise LicensedProductWorkflowError(
            f"environment variable {name!r} must resolve to local-only licensed storage"
        )
    return normalized


def _normalize_metadata_value(value: Any, *, field: str) -> Any:
    if isinstance(value, str):
        return _normalize_non_blank(value, field=field)
    if isinstance(value, (bool, int)) or value is None:
        return value
    if isinstance(value, (list, tuple)):
        return _normalize_str_tuple(value, field=field)
    raise LicensedProductWorkflowError(
        f"{field} values must be strings, booleans, integers, null, or lists of strings"
    )


def _normalize_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, Mapping):
        raise LicensedProductWorkflowError("metadata must be a mapping")
    unexpected = sorted(set(metadata) - set(ALLOWED_LICENSED_PRODUCT_METADATA_KEYS))
    if unexpected:
        raise LicensedProductWorkflowError(
            "metadata contains unsupported keys: " + ", ".join(unexpected)
        )
    return {
        key: _normalize_metadata_value(value, field=f"metadata.{key}")
        for key, value in metadata.items()
    }


def _normalize_source_url(value: str) -> str:
    normalized = _normalize_non_blank(value, field="source_page_url")
    parsed = urlsplit(normalized)
    if not parsed.scheme or not (parsed.netloc or parsed.path):
        raise LicensedProductWorkflowError("source_page_url must be an absolute URL")
    return normalized


@dataclass(frozen=True, slots=True)
class LicensedProductAssetReference:
    """Metadata-only reference for a licensed or public asset placeholder."""

    asset_id: str
    kind: Literal[
        "public-metadata",
        "user-supplied-licensed-file",
        "derived-validation-fixture",
    ]
    source_refs: tuple[str, ...]
    local_path_hint: str | None
    restricted: bool
    metadata: dict[str, Any]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "asset_id", _normalize_non_blank(self.asset_id, field="asset_id")
        )
        if self.kind not in {
            "public-metadata",
            "user-supplied-licensed-file",
            "derived-validation-fixture",
        }:
            raise LicensedProductWorkflowError(f"unsupported asset kind {self.kind!r}")
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        if self.local_path_hint is not None:
            object.__setattr__(
                self,
                "local_path_hint",
                _normalize_relative_path(self.local_path_hint, field="local_path_hint"),
            )
        object.__setattr__(self, "metadata", _normalize_metadata(self.metadata))
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes"),
        )

        if self.kind == "public-metadata":
            if self.local_path_hint is not None:
                raise LicensedProductWorkflowError(
                    "public-metadata assets must not declare a local_path_hint"
                )
            if self.restricted:
                raise LicensedProductWorkflowError(
                    "public-metadata assets must not be restricted"
                )
        elif self.kind == "user-supplied-licensed-file":
            if self.local_path_hint is None:
                raise LicensedProductWorkflowError(
                    "user-supplied-licensed-file assets require a local_path_hint"
                )
            if not self.restricted:
                raise LicensedProductWorkflowError(
                    "user-supplied-licensed-file assets must be restricted"
                )
            ensure_commit_safe_exclusion(self.local_path_hint)
        elif self.restricted:
            raise LicensedProductWorkflowError(
                "derived-validation-fixture assets must not be restricted"
            )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable asset reference."""
        return {
            "asset_id": self.asset_id,
            "kind": self.kind,
            "source_refs": list(self.source_refs),
            "local_path_hint": self.local_path_hint,
            "restricted": self.restricted,
            "metadata": dict(self.metadata),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class LicensedProductManifestRecord:
    """Strict, metadata-only manifest for a licensed product family."""

    pricing_year: str
    financial_year: str
    system: str
    display_name: str
    expected_version: str | None
    source_page_url: str
    assets: tuple[LicensedProductAssetReference, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "system", normalize_coding_set_system(self.system))
        object.__setattr__(self, "pricing_year", _normalize_year(self.pricing_year))
        object.__setattr__(
            self,
            "financial_year",
            _normalize_non_blank(self.financial_year, field="financial_year"),
        )
        object.__setattr__(
            self,
            "display_name",
            _normalize_non_blank(self.display_name, field="display_name"),
        )
        object.__setattr__(
            self,
            "expected_version",
            _normalize_version(self.expected_version, field="expected_version"),
        )
        object.__setattr__(
            self,
            "source_page_url",
            _normalize_source_url(self.source_page_url),
        )
        object.__setattr__(self, "assets", tuple(self.assets))
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes"),
        )

        if not self.assets:
            raise LicensedProductWorkflowError("assets must not be empty")

        asset_ids = [asset.asset_id for asset in self.assets]
        if len(set(asset_ids)) != len(asset_ids):
            raise LicensedProductWorkflowError(
                "assets must not contain duplicate asset_id values"
            )

        expected_version = get_expected_coding_set_version(
            self.system,
            self.pricing_year,
        )
        if self.expected_version != expected_version:
            raise LicensedProductWorkflowError(
                f"expected_version for {self.system!r} in {self.pricing_year!r} "
                f"must be {expected_version!r}"
            )

    def asset_for_id(self, asset_id: str) -> LicensedProductAssetReference | None:
        """Return the matching asset reference when present."""
        normalized_asset_id = _normalize_non_blank(asset_id, field="asset_id")
        for asset in self.assets:
            if asset.asset_id == normalized_asset_id:
                return asset
        return None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable manifest record."""
        return {
            "pricing_year": self.pricing_year,
            "financial_year": self.financial_year,
            "system": self.system,
            "display_name": self.display_name,
            "expected_version": self.expected_version,
            "source_page_url": self.source_page_url,
            "assets": [asset.to_dict() for asset in self.assets],
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class LicensedProductCompatibilityResult:
    """Outcome from a licensed-product compatibility check."""

    pricing_year: str
    system: str
    display_name: str
    declared_version: str | None
    expected_version: str | None
    compatible: bool
    reason: str | None
    record: LicensedProductManifestRecord | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serialisable compatibility result."""
        return {
            "pricing_year": self.pricing_year,
            "system": self.system,
            "display_name": self.display_name,
            "declared_version": self.declared_version,
            "expected_version": self.expected_version,
            "compatible": self.compatible,
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
        }


def _build_asset_reference(row: Mapping[str, Any]) -> LicensedProductAssetReference:
    return LicensedProductAssetReference(
        asset_id=str(row["asset_id"]),
        kind=cast(
            Literal[
                "public-metadata",
                "user-supplied-licensed-file",
                "derived-validation-fixture",
            ],
            row["kind"],
        ),
        source_refs=tuple(cast(tuple[str, ...], row["source_refs"])),
        local_path_hint=cast(str | None, row["local_path_hint"]),
        restricted=bool(row["restricted"]),
        metadata=dict(cast(Mapping[str, Any], row["metadata"])),
        notes=tuple(cast(tuple[str, ...], row["notes"])),
    )


def build_licensed_product_asset_reference(
    *,
    asset_id: str,
    kind: Literal[
        "public-metadata",
        "user-supplied-licensed-file",
        "derived-validation-fixture",
    ],
    source_refs: Iterable[str],
    local_path_hint: str | Path | None,
    restricted: bool,
    metadata: Mapping[str, Any],
    notes: Iterable[str] = (),
) -> LicensedProductAssetReference:
    """Build a strict asset reference for a licensed-product manifest."""
    return LicensedProductAssetReference(
        asset_id=asset_id,
        kind=kind,
        source_refs=tuple(source_refs),
        local_path_hint=None if local_path_hint is None else str(local_path_hint),
        restricted=restricted,
        metadata=dict(metadata),
        notes=tuple(notes),
    )


def _build_manifest_record(row: Mapping[str, Any]) -> LicensedProductManifestRecord:
    assets = tuple(
        _build_asset_reference(asset)
        for asset in cast(Iterable[Mapping[str, Any]], row["assets"])
    )
    return LicensedProductManifestRecord(
        pricing_year=str(row["pricing_year"]),
        financial_year=str(row["financial_year"]),
        system=str(row["system"]),
        display_name=str(row["display_name"]),
        expected_version=cast(str | None, row["expected_version"]),
        source_page_url=str(row["source_page_url"]),
        assets=assets,
        notes=tuple(cast(tuple[str, ...], row["notes"])),
    )


def build_licensed_product_manifest_record(
    *,
    pricing_year: str,
    financial_year: str,
    system: str,
    display_name: str,
    expected_version: str | None = None,
    source_page_url: str,
    assets: Iterable[LicensedProductAssetReference],
    notes: Iterable[str] = (),
) -> LicensedProductManifestRecord:
    """Build a strict manifest record from typed inputs."""
    canonical_system = normalize_coding_set_system(system)
    normalized_year = _normalize_year(pricing_year)
    normalized_expected_version = (
        _normalize_version(expected_version, field="expected_version")
        if expected_version is not None
        else get_expected_coding_set_version(canonical_system, normalized_year)
    )
    return LicensedProductManifestRecord(
        pricing_year=normalized_year,
        financial_year=financial_year,
        system=canonical_system,
        display_name=display_name,
        expected_version=normalized_expected_version,
        source_page_url=source_page_url,
        assets=tuple(assets),
        notes=tuple(notes),
    )


_MANIFEST_RECORDS: Final[tuple[LicensedProductManifestRecord, ...]] = tuple(
    _build_manifest_record(row) for row in LICENSED_PRODUCT_WORKFLOW_ROWS
)


def list_licensed_product_manifest_records(
    year: str | None = None,
) -> tuple[LicensedProductManifestRecord, ...]:
    """Return all licensed-product manifest records, optionally filtered by year."""
    if year is None:
        return _MANIFEST_RECORDS
    normalized_year = _normalize_year(year)
    return tuple(
        record for record in _MANIFEST_RECORDS if record.pricing_year == normalized_year
    )


def get_licensed_product_manifest_record(
    system: str,
    year: str,
) -> LicensedProductManifestRecord | None:
    """Return the manifest record for a system/year pair, if present."""
    canonical_system = normalize_coding_set_system(system)
    normalized_year = _normalize_year(year)
    for record in _MANIFEST_RECORDS:
        if record.system == canonical_system and record.pricing_year == normalized_year:
            return record
    return None


def diagnose_missing_licensed_assets(
    system: str,
    year: str,
    *,
    existing_paths: Iterable[str | Path] = (),
) -> tuple[dict[str, object], ...]:
    """Return safe diagnostics for missing restricted local assets.

    Diagnostics identify the missing asset category and local path hint. They
    never inspect or expose restricted file contents.
    """
    record = get_licensed_product_manifest_record(system, year)
    if record is None:
        canonical_system = normalize_coding_set_system(system)
        return (
            {
                "system": canonical_system,
                "pricing_year": _normalize_year(year),
                "asset_id": "manifest-record",
                "missing_category": "licensed-product-manifest",
                "local_path_hint": None,
                "safe_message": (
                    f"{canonical_system} {year} is missing a metadata-only "
                    "licensed-product manifest record"
                ),
            },
        )

    normalized_existing = {
        _normalize_relative_path(path, field="existing_paths")
        for path in existing_paths
    }
    diagnostics: list[dict[str, object]] = []
    for asset in record.assets:
        if not asset.restricted:
            continue
        hint = asset.local_path_hint
        if hint is None or hint not in normalized_existing:
            diagnostics.append(
                {
                    "system": record.system,
                    "pricing_year": record.pricing_year,
                    "asset_id": asset.asset_id,
                    "missing_category": asset.metadata.get(
                        "asset_role",
                        "licensed-local-asset",
                    ),
                    "local_path_hint": hint,
                    "safe_message": (
                        f"{record.system} {record.pricing_year} is missing "
                        f"local licensed asset category {asset.asset_id!r}"
                    ),
                }
            )
    return tuple(diagnostics)


def _expected_version_for(system: str, year: str) -> str | None:
    canonical_system = normalize_coding_set_system(system)
    normalized_year = _normalize_year(year)
    return get_expected_coding_set_version(canonical_system, normalized_year)


def _compatible_result(
    *,
    year: str,
    system: str,
    declared_version: str | None,
    expected_version: str | None,
    record: LicensedProductManifestRecord | None,
    reason: str | None,
) -> LicensedProductCompatibilityResult:
    canonical_system = normalize_coding_set_system(system)
    return LicensedProductCompatibilityResult(
        pricing_year=_normalize_year(year),
        system=canonical_system,
        display_name=record.display_name if record is not None else canonical_system,
        declared_version=declared_version,
        expected_version=expected_version,
        compatible=reason is None,
        reason=reason,
        record=record,
    )


def validate_licensed_product_compatibility(
    system: str,
    year: str,
    *,
    declared_version: str | None = None,
    source_page_url: str | None = None,
    local_path_hint: str | Path | None = None,
) -> LicensedProductCompatibilityResult:
    """Validate a licensed-product record without exposing restricted content."""
    canonical_system = normalize_coding_set_system(system)
    normalized_year = _normalize_year(year)
    expected_version = _expected_version_for(canonical_system, normalized_year)
    record = get_licensed_product_manifest_record(canonical_system, normalized_year)

    if expected_version is None:
        return _compatible_result(
            year=normalized_year,
            system=canonical_system,
            declared_version=declared_version,
            expected_version=None,
            record=record,
            reason=(
                f"{canonical_system} is not mapped for pricing year {normalized_year}"
            ),
        )

    normalized_declared: str | None
    if declared_version is not None:
        normalized_declared = _normalize_version(
            declared_version,
            field="declared_version",
        )
        if normalized_declared != expected_version:
            return _compatible_result(
                year=normalized_year,
                system=canonical_system,
                declared_version=normalized_declared,
                expected_version=expected_version,
                record=record,
                reason=(
                    f"{canonical_system} {normalized_year} expects "
                    f"{expected_version!r}, "
                    f"got {normalized_declared!r}"
                ),
            )
    else:
        normalized_declared = None

    if source_page_url is not None:
        normalized_source_page_url = _normalize_source_url(source_page_url)
        if record is not None and normalized_source_page_url != record.source_page_url:
            return _compatible_result(
                year=normalized_year,
                system=canonical_system,
                declared_version=normalized_declared,
                expected_version=expected_version,
                record=record,
                reason=(
                    f"source_page_url for {canonical_system} {normalized_year} "
                    "does not match the recorded manifest boundary"
                ),
            )

    if local_path_hint is not None:
        normalized_local_path = _normalize_relative_path(
            local_path_hint, field="local_path_hint"
        )
        if not is_local_only_licensed_path(normalized_local_path):
            return _compatible_result(
                year=normalized_year,
                system=canonical_system,
                declared_version=normalized_declared,
                expected_version=expected_version,
                record=record,
                reason=(
                    f"local_path_hint for {canonical_system} {normalized_year} must "
                    "point at local-only licensed storage"
                ),
            )

    if record is not None:
        for asset in record.assets:
            if asset.restricted and not is_commit_safe_excluded_path(
                asset.local_path_hint or ""
            ):
                return _compatible_result(
                    year=normalized_year,
                    system=canonical_system,
                    declared_version=normalized_declared,
                    expected_version=expected_version,
                    record=record,
                    reason=(
                        f"asset {asset.asset_id!r} for {canonical_system} "
                        f"{normalized_year} is not commit-safe"
                    ),
                )

    return _compatible_result(
        year=normalized_year,
        system=canonical_system,
        declared_version=normalized_declared,
        expected_version=expected_version,
        record=record,
        reason=None,
    )


def ensure_licensed_product_compatibility(
    system: str,
    year: str,
    *,
    declared_version: str | None = None,
    source_page_url: str | None = None,
    local_path_hint: str | Path | None = None,
) -> LicensedProductCompatibilityResult:
    """Raise when a licensed-product manifest is incompatible."""
    result = validate_licensed_product_compatibility(
        system,
        year,
        declared_version=declared_version,
        source_page_url=source_page_url,
        local_path_hint=local_path_hint,
    )
    if not result.compatible:
        raise LicensedProductWorkflowError(
            result.reason or "licensed-product manifest is invalid"
        )
    return result
