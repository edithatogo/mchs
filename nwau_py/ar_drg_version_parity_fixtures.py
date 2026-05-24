"""Metadata helpers for safe AR-DRG version parity fixtures.

The helpers in this module stay conservative by design:

- they register synthetic fixture metadata and local-only licensed references;
- they validate version scope against the repository's AR-DRG registries;
- they keep fixture payloads and grouped outputs out of the helper layer.

Nothing here embeds proprietary grouping outputs or licensed AR-DRG tables.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Literal, cast

from .ar_drg_grouper import (
    ARDRGGrouperVersionWindow,
    validate_ar_drg_grouper_compatibility,
)
from .ar_drg_version_parity_fixtures_data import AR_DRG_VERSION_PARITY_FIXTURE_ROWS
from .licensed_product_workflow import validate_licensed_product_compatibility

__all__ = [
    "ARDRGParityFixtureCompatibilityResult",
    "ARDRGParityFixtureError",
    "ARDRGParityFixtureRecord",
    "build_ar_drg_parity_fixture_reference",
    "ensure_ar_drg_parity_fixture_scope",
    "get_ar_drg_parity_fixture_record",
    "list_ar_drg_parity_fixture_records",
    "register_ar_drg_local_licensed_parity_fixture_reference",
    "register_ar_drg_synthetic_parity_fixture",
    "validate_ar_drg_parity_fixture_scope",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")
_FIXTURE_KINDS: Final[frozenset[str]] = frozenset(
    {"synthetic", "local-licensed-reference"}
)
_WORKFLOW_MODES: Final[frozenset[str]] = frozenset(
    {"precomputed", "external-reference"}
)
_LICENSE_BOUNDARIES: Final[dict[str, str]] = {
    "synthetic": "metadata-only",
    "local-licensed-reference": "local-only",
}
_FIXTURE_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class ARDRGParityFixtureError(ValueError):
    """Raised when a parity-fixture reference is incomplete or incompatible."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ARDRGParityFixtureError(f"{field} must be a string")
    if not value:
        raise ARDRGParityFixtureError(f"{field} must not be blank")
    if value.strip() != value:
        raise ARDRGParityFixtureError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise ARDRGParityFixtureError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str, *, field: str) -> str:
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise ARDRGParityFixtureError(f"{field} must be a deterministic version label")
    return normalized


def _normalize_str_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise ARDRGParityFixtureError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise ARDRGParityFixtureError(f"{field} must not contain duplicates")
        seen.add(text)
        normalized.append(text)
    if not normalized:
        raise ARDRGParityFixtureError(f"{field} must not be empty")
    return tuple(normalized)


def _normalize_relative_path(path: str | Path, *, field: str) -> str:
    candidate = path if isinstance(path, Path) else Path(path)
    raw = candidate.as_posix()
    if not raw or raw == ".":
        raise ARDRGParityFixtureError(f"{field} must not be blank")
    if candidate.is_absolute():
        raise ARDRGParityFixtureError(f"{field} must be a relative path")
    if any(part == ".." for part in candidate.parts):
        raise ARDRGParityFixtureError(f"{field} must not contain parent traversal")
    return raw


def _coerce_version_window(
    value: ARDRGGrouperVersionWindow | Mapping[str, Any],
) -> ARDRGGrouperVersionWindow:
    if isinstance(value, ARDRGGrouperVersionWindow):
        return value
    if not isinstance(value, Mapping):
        raise ARDRGParityFixtureError(
            "version_window must be a version window record or mapping"
        )
    return ARDRGGrouperVersionWindow(
        pricing_year=str(value["pricing_year"]),
        ar_drg_version=str(value["ar_drg_version"]),
        icd_10_am_version=str(value["icd_10_am_version"]),
        achi_version=str(value["achi_version"]),
        acs_version=str(value["acs_version"]),
    )


@dataclass(frozen=True, slots=True)
class ARDRGParityFixtureRecord:
    """Conservative metadata for a safe AR-DRG parity fixture reference."""

    fixture_id: str
    fixture_kind: Literal["synthetic", "local-licensed-reference"]
    workflow_mode: Literal["precomputed", "external-reference"]
    version_window: ARDRGGrouperVersionWindow
    grouper_version: str | None
    source_refs: tuple[str, ...]
    local_path_hint: str
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "fixture_id",
            _normalize_non_blank(self.fixture_id, field="fixture_id"),
        )
        if not _FIXTURE_ID_RE.fullmatch(self.fixture_id):
            raise ARDRGParityFixtureError(
                "fixture_id must be lowercase snake_case and deterministic"
            )
        if self.fixture_kind not in _FIXTURE_KINDS:
            raise ARDRGParityFixtureError(
                f"unsupported fixture_kind {self.fixture_kind!r}"
            )
        if self.workflow_mode not in _WORKFLOW_MODES:
            raise ARDRGParityFixtureError(
                f"unsupported workflow_mode {self.workflow_mode!r}"
            )
        if self.fixture_kind == "synthetic" and self.workflow_mode != "precomputed":
            raise ARDRGParityFixtureError(
                "synthetic parity fixtures must use precomputed workflow mode"
            )
        if (
            self.fixture_kind == "local-licensed-reference"
            and self.workflow_mode != "external-reference"
        ):
            raise ARDRGParityFixtureError(
                "local-licensed parity fixture references must use "
                "external-reference workflow mode"
            )
        object.__setattr__(
            self,
            "version_window",
            _coerce_version_window(self.version_window),
        )
        if self.grouper_version is not None:
            object.__setattr__(
                self,
                "grouper_version",
                _normalize_version(self.grouper_version, field="grouper_version"),
            )
        object.__setattr__(
            self,
            "source_refs",
            _normalize_str_tuple(self.source_refs, field="source_refs"),
        )
        object.__setattr__(
            self,
            "local_path_hint",
            _normalize_relative_path(self.local_path_hint, field="local_path_hint"),
        )
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes"),
        )
        if self.workflow_mode == "external-reference" and self.grouper_version is None:
            raise ARDRGParityFixtureError(
                "external-reference parity fixtures require grouper_version"
            )

    @property
    def pricing_year(self) -> str:
        return self.version_window.pricing_year

    @property
    def license_boundary(self) -> Literal["metadata-only", "local-only"]:
        return cast(
            Literal["metadata-only", "local-only"],
            _LICENSE_BOUNDARIES[self.fixture_kind],
        )

    @property
    def restricted(self) -> bool:
        return self.fixture_kind == "local-licensed-reference"

    def version_scope(self) -> dict[str, str | None]:
        """Return the declared AR-DRG and coding-set version scope."""
        scope: dict[str, str | None] = dict(self.version_window.to_dict())
        scope["grouper_version"] = self.grouper_version
        return scope

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable parity-fixture record."""
        return {
            "fixture_id": self.fixture_id,
            "fixture_kind": self.fixture_kind,
            "workflow_mode": self.workflow_mode,
            "license_boundary": self.license_boundary,
            "restricted": self.restricted,
            "version_window": self.version_window.to_dict(),
            "grouper_version": self.grouper_version,
            "source_refs": list(self.source_refs),
            "local_path_hint": self.local_path_hint,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ARDRGParityFixtureCompatibilityResult:
    """Outcome from a parity-fixture version scope validation."""

    fixture_id: str
    pricing_year: str
    fixture_kind: Literal["synthetic", "local-licensed-reference"]
    workflow_mode: Literal["precomputed", "external-reference"]
    declared_versions: dict[str, str | None]
    expected_versions: dict[str, str | None]
    grouper_version: str | None
    compatible: bool
    reason: str | None
    record: ARDRGParityFixtureRecord | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable compatibility result."""
        return {
            "fixture_id": self.fixture_id,
            "pricing_year": self.pricing_year,
            "fixture_kind": self.fixture_kind,
            "workflow_mode": self.workflow_mode,
            "declared_versions": dict(self.declared_versions),
            "expected_versions": dict(self.expected_versions),
            "grouper_version": self.grouper_version,
            "compatible": self.compatible,
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
        }


def build_ar_drg_parity_fixture_reference(
    *,
    fixture_id: str,
    fixture_kind: Literal["synthetic", "local-licensed-reference"],
    workflow_mode: Literal["precomputed", "external-reference"],
    version_window: ARDRGGrouperVersionWindow | Mapping[str, Any],
    source_refs: Iterable[str],
    local_path_hint: str | Path,
    notes: Iterable[str] = (),
    grouper_version: str | None = None,
) -> ARDRGParityFixtureRecord:
    """Build a conservative parity-fixture reference without validating scope."""
    return ARDRGParityFixtureRecord(
        fixture_id=fixture_id,
        fixture_kind=fixture_kind,
        workflow_mode=workflow_mode,
        version_window=_coerce_version_window(version_window),
        grouper_version=grouper_version,
        source_refs=tuple(source_refs),
        local_path_hint=_normalize_relative_path(
            local_path_hint, field="local_path_hint"
        ),
        notes=tuple(notes),
    )


def register_ar_drg_synthetic_parity_fixture(
    *,
    fixture_id: str,
    version_window: ARDRGGrouperVersionWindow | Mapping[str, Any],
    source_refs: Iterable[str],
    local_path_hint: str | Path,
    notes: Iterable[str] = (),
) -> ARDRGParityFixtureRecord:
    """Register a synthetic parity fixture after validating its scope."""
    record = build_ar_drg_parity_fixture_reference(
        fixture_id=fixture_id,
        fixture_kind="synthetic",
        workflow_mode="precomputed",
        version_window=version_window,
        source_refs=source_refs,
        local_path_hint=local_path_hint,
        notes=notes,
    )
    ensure_ar_drg_parity_fixture_scope(record)
    return record


def register_ar_drg_local_licensed_parity_fixture_reference(
    *,
    fixture_id: str,
    version_window: ARDRGGrouperVersionWindow | Mapping[str, Any],
    source_refs: Iterable[str],
    local_path_hint: str | Path,
    grouper_version: str,
    notes: Iterable[str] = (),
) -> ARDRGParityFixtureRecord:
    """Register a local-only licensed parity fixture reference."""
    record = build_ar_drg_parity_fixture_reference(
        fixture_id=fixture_id,
        fixture_kind="local-licensed-reference",
        workflow_mode="external-reference",
        version_window=version_window,
        source_refs=source_refs,
        local_path_hint=local_path_hint,
        notes=notes,
        grouper_version=grouper_version,
    )
    ensure_ar_drg_parity_fixture_scope(record)
    return record


def _build_registry() -> tuple[ARDRGParityFixtureRecord, ...]:
    records: list[ARDRGParityFixtureRecord] = []
    for row in AR_DRG_VERSION_PARITY_FIXTURE_ROWS:
        record = build_ar_drg_parity_fixture_reference(
            fixture_id=str(row["fixture_id"]),
            fixture_kind=cast(
                Literal["synthetic", "local-licensed-reference"],
                row["fixture_kind"],
            ),
            workflow_mode=cast(
                Literal["precomputed", "external-reference"],
                row["workflow_mode"],
            ),
            version_window=cast(Mapping[str, Any], row["version_window"]),
            source_refs=tuple(cast(tuple[str, ...], row["source_refs"])),
            local_path_hint=str(row["local_path_hint"]),
            notes=tuple(cast(tuple[str, ...], row["notes"])),
            grouper_version=(
                None
                if row.get("grouper_version") is None
                else str(row["grouper_version"])
            ),
        )
        records.append(record)
    return tuple(records)


_AR_DRG_PARITY_FIXTURE_RECORDS: Final[tuple[ARDRGParityFixtureRecord, ...]] = (
    _build_registry()
)
_AR_DRG_PARITY_FIXTURE_BY_ID: Final[dict[str, ARDRGParityFixtureRecord]] = {
    record.fixture_id: record for record in _AR_DRG_PARITY_FIXTURE_RECORDS
}


def list_ar_drg_parity_fixture_records(
    *,
    pricing_year: str | None = None,
    fixture_kind: str | None = None,
) -> tuple[ARDRGParityFixtureRecord, ...]:
    """Return the registered parity-fixture references, optionally filtered."""
    records = _AR_DRG_PARITY_FIXTURE_RECORDS
    if pricing_year is not None:
        normalized_year = _normalize_year(pricing_year)
        records = tuple(
            record for record in records if record.pricing_year == normalized_year
        )
    if fixture_kind is not None:
        normalized_kind = _normalize_non_blank(fixture_kind, field="fixture_kind")
        if normalized_kind not in _FIXTURE_KINDS:
            raise ARDRGParityFixtureError(
                f"unsupported fixture_kind {normalized_kind!r}"
            )
        records = tuple(
            record for record in records if record.fixture_kind == normalized_kind
        )
    return records


def get_ar_drg_parity_fixture_record(
    fixture_id: str,
) -> ARDRGParityFixtureRecord | None:
    """Return a registered parity fixture by identifier, if one exists."""
    normalized_id = _normalize_non_blank(fixture_id, field="fixture_id")
    if not _FIXTURE_ID_RE.fullmatch(normalized_id):
        raise ARDRGParityFixtureError(
            "fixture_id must be lowercase snake_case and deterministic"
        )
    return _AR_DRG_PARITY_FIXTURE_BY_ID.get(normalized_id)


def validate_ar_drg_parity_fixture_scope(
    record: ARDRGParityFixtureRecord,
) -> ARDRGParityFixtureCompatibilityResult:
    """Check whether a parity fixture stays within its declared version scope."""
    version_window = record.version_window
    grouping_result = validate_ar_drg_grouper_compatibility(
        version_window.pricing_year,
        ar_drg_version=version_window.ar_drg_version,
        icd_10_am_version=version_window.icd_10_am_version,
        achi_version=version_window.achi_version,
        acs_version=version_window.acs_version,
    )
    if not grouping_result.compatible:
        return ARDRGParityFixtureCompatibilityResult(
            fixture_id=record.fixture_id,
            pricing_year=record.pricing_year,
            fixture_kind=record.fixture_kind,
            workflow_mode=record.workflow_mode,
            declared_versions=dict(grouping_result.declared_versions),
            expected_versions=dict(grouping_result.expected_versions),
            grouper_version=record.grouper_version,
            compatible=False,
            reason=grouping_result.reason,
            record=record,
        )

    reason: str | None = None
    if record.fixture_kind == "local-licensed-reference":
        licensed_result = validate_licensed_product_compatibility(
            "AR-DRG",
            record.pricing_year,
            declared_version=version_window.ar_drg_version,
            local_path_hint=record.local_path_hint,
        )
        if not licensed_result.compatible:
            reason = licensed_result.reason

    if (
        reason is None
        and record.workflow_mode == "external-reference"
        and record.grouper_version is None
    ):
        reason = "external-reference parity fixtures require grouper_version"

    compatible = reason is None
    return ARDRGParityFixtureCompatibilityResult(
        fixture_id=record.fixture_id,
        pricing_year=record.pricing_year,
        fixture_kind=record.fixture_kind,
        workflow_mode=record.workflow_mode,
        declared_versions=dict(grouping_result.declared_versions),
        expected_versions=dict(grouping_result.expected_versions),
        grouper_version=record.grouper_version,
        compatible=compatible,
        reason=reason,
        record=record,
    )


def ensure_ar_drg_parity_fixture_scope(
    record: ARDRGParityFixtureRecord,
) -> ARDRGParityFixtureCompatibilityResult:
    """Raise when a parity fixture falls outside its declared safe scope."""
    result = validate_ar_drg_parity_fixture_scope(record)
    if not result.compatible:
        raise ARDRGParityFixtureError(
            result.reason or "AR-DRG parity fixture scope is incompatible"
        )
    return result
