"""Registry helpers for AR-DRG, ICD-10-AM, ACHI, and ACS mapping provenance."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final, Literal, cast

from .ar_drg_mapping_registry_data import AR_DRG_MAPPING_REGISTRY_ROWS
from .coding_set_registry import get_expected_coding_set_version

__all__ = [
    "ARDRG_MAPPING_SYSTEMS",
    "ARDRGMappingAssetReference",
    "ARDRGMappingCompatibilityResult",
    "ARDRGMappingRecord",
    "ARDRGMappingRegistryError",
    "ensure_ar_drg_mapping_compatibility",
    "get_ar_drg_mapping_record",
    "get_expected_ar_drg_version",
    "get_expected_coding_set_versions",
    "list_ar_drg_mapping_records",
    "validate_ar_drg_mapping_compatibility",
    "validate_ar_drg_version_binding",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")
_ASSET_KINDS: Final[frozenset[str]] = frozenset(
    {
        "public-metadata",
        "user-supplied-licensed-file",
        "derived-validation-fixture",
    }
)
_EXPECTED_SYSTEMS: Final[tuple[str, ...]] = (
    "ar_drg",
    "icd_10_am",
    "achi",
    "acs",
)

ARDRG_MAPPING_SYSTEMS: Final[dict[str, str]] = {
    "ar_drg": "AR-DRG",
    "icd_10_am": "ICD-10-AM",
    "achi": "ACHI",
    "acs": "ACS",
}


class ARDRGMappingRegistryError(ValueError):
    """Raised when the mapping registry metadata is inconsistent."""


def _expected_coding_set_versions(year: str) -> dict[str, str | None]:
    return {
        system: get_expected_coding_set_version(system, year)
        for system in _EXPECTED_SYSTEMS
    }


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ARDRGMappingRegistryError(f"{field} must be a string")
    if not value:
        raise ARDRGMappingRegistryError(f"{field} must not be blank")
    if value.strip() != value:
        raise ARDRGMappingRegistryError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise ARDRGMappingRegistryError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_version(version: str, *, field: str) -> str:
    normalized = _normalize_non_blank(version, field=field)
    if not _VERSION_RE.fullmatch(normalized):
        raise ARDRGMappingRegistryError(
            f"{field} must be a deterministic version label"
        )
    return normalized


def _normalize_str_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, (list, tuple)):
        raise ARDRGMappingRegistryError(
            f"{field} must be a tuple or list of non-empty strings"
        )
    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        text = _normalize_non_blank(item, field=field)
        if text in seen:
            raise ARDRGMappingRegistryError(f"{field} must not contain duplicates")
        seen.add(text)
        normalized.append(text)
    if not normalized:
        raise ARDRGMappingRegistryError(f"{field} must not be empty")
    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ARDRGMappingAssetReference:
    """Public, restricted, or derived provenance for a registry record."""

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
        if self.kind not in _ASSET_KINDS:
            raise ARDRGMappingRegistryError(f"unsupported asset kind {self.kind!r}")
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
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes"),
        )
        if self.kind == "public-metadata":
            if self.local_path_hint is not None:
                raise ARDRGMappingRegistryError(
                    "public-metadata assets must not declare a local_path_hint"
                )
            if self.restricted:
                raise ARDRGMappingRegistryError(
                    "public-metadata assets must not be restricted"
                )
        elif self.kind == "user-supplied-licensed-file":
            if self.local_path_hint is None:
                raise ARDRGMappingRegistryError(
                    "user-supplied-licensed-file assets require a local_path_hint"
                )
            if not self.restricted:
                raise ARDRGMappingRegistryError(
                    "user-supplied-licensed-file assets must be restricted"
                )
        elif self.kind == "derived-validation-fixture":
            if self.local_path_hint is None:
                raise ARDRGMappingRegistryError(
                    "derived-validation-fixture assets require a local_path_hint"
                )
            if self.restricted:
                raise ARDRGMappingRegistryError(
                    "derived-validation-fixture assets must not be restricted"
                )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable asset reference."""
        return {
            "kind": self.kind,
            "source_refs": list(self.source_refs),
            "local_path_hint": self.local_path_hint,
            "restricted": self.restricted,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ARDRGMappingCompatibilityResult:
    """Outcome from an AR-DRG mapping compatibility check."""

    pricing_year: str
    declared_versions: dict[str, str | None]
    expected_versions: dict[str, str | None]
    compatible: bool
    reason: str | None
    record: ARDRGMappingRecord | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable compatibility result."""
        return {
            "pricing_year": self.pricing_year,
            "declared_versions": dict(self.declared_versions),
            "expected_versions": dict(self.expected_versions),
            "compatible": self.compatible,
            "reason": self.reason,
            "record": None if self.record is None else self.record.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class ARDRGMappingRecord:
    """Immutable provenance record for a pricing-year mapping bundle."""

    pricing_year: str
    financial_year: str
    effective_years: tuple[str, ...]
    ar_drg_version: str
    icd_10_am_version: str | None
    achi_version: str | None
    acs_version: str | None
    assets: tuple[ARDRGMappingAssetReference, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        normalized_year = _normalize_year(self.pricing_year)
        object.__setattr__(self, "pricing_year", normalized_year)
        object.__setattr__(
            self,
            "financial_year",
            _normalize_non_blank(self.financial_year, field="financial_year"),
        )
        normalized_effective_years = _normalize_str_tuple(
            self.effective_years, field="effective_years"
        )
        if normalized_year not in normalized_effective_years:
            raise ARDRGMappingRegistryError(
                "effective_years must include the record's pricing_year"
            )
        object.__setattr__(self, "effective_years", normalized_effective_years)
        object.__setattr__(
            self,
            "ar_drg_version",
            _normalize_version(self.ar_drg_version, field="ar_drg_version"),
        )
        for field_name in ("icd_10_am_version", "achi_version", "acs_version"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(
                    self,
                    field_name,
                    _normalize_version(value, field=field_name),
                )
        normalized_assets = tuple(self.assets)
        if not normalized_assets:
            raise ARDRGMappingRegistryError("assets must not be empty")
        object.__setattr__(self, "assets", normalized_assets)
        object.__setattr__(
            self,
            "notes",
            _normalize_str_tuple(self.notes, field="notes"),
        )

        kinds = {asset.kind for asset in self.assets}
        required_kinds = frozenset(
            {
                "public-metadata",
                "user-supplied-licensed-file",
                "derived-validation-fixture",
            }
        )
        if not required_kinds.issubset(kinds):
            missing = sorted(required_kinds - kinds)
            raise ARDRGMappingRegistryError(
                "assets must include public metadata, a user-supplied licensed file, "
                "and a derived validation fixture; missing: " + ", ".join(missing)
            )

        expected = _expected_coding_set_versions(self.pricing_year)
        mismatches: list[str] = []
        for system, expected_version in expected.items():
            declared_version = getattr(self, f"{system}_version")
            if declared_version != expected_version:
                mismatches.append(
                    f"{system}={declared_version!r} (expected {expected_version!r})"
                )
        if mismatches:
            raise ARDRGMappingRegistryError(
                "record does not match the current coding-set registry: "
                + ", ".join(mismatches)
            )

    def expected_coding_set_versions(self) -> dict[str, str | None]:
        """Return the expected coding-set versions for this pricing year."""
        return {
            "ar_drg": self.ar_drg_version,
            "icd_10_am": self.icd_10_am_version,
            "achi": self.achi_version,
            "acs": self.acs_version,
        }

    def version_binding(self) -> tuple[str, str | None]:
        """Return the AR-DRG version binding for this record."""
        return self.pricing_year, self.ar_drg_version

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable registry record."""
        return {
            "pricing_year": self.pricing_year,
            "financial_year": self.financial_year,
            "effective_years": list(self.effective_years),
            "ar_drg_version": self.ar_drg_version,
            "icd_10_am_version": self.icd_10_am_version,
            "achi_version": self.achi_version,
            "acs_version": self.acs_version,
            "assets": [asset.to_dict() for asset in self.assets],
            "notes": list(self.notes),
        }

    def validate_ar_drg_version(
        self,
        version: str | None,
    ) -> ARDRGMappingCompatibilityResult:
        """Check whether an AR-DRG version matches this record."""
        declared = None
        if version is not None:
            declared = _normalize_version(version, field="ar_drg_version")
        compatible = declared == self.ar_drg_version
        reason = None
        if declared is None:
            reason = (
                f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} {self.pricing_year} "
                f"requires version {self.ar_drg_version}"
            )
        elif not compatible:
            reason = (
                f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} {self.pricing_year} expects "
                f"{self.ar_drg_version}, got {declared}"
            )
        return ARDRGMappingCompatibilityResult(
            pricing_year=self.pricing_year,
            declared_versions={"ar_drg": declared},
            expected_versions={"ar_drg": self.ar_drg_version},
            compatible=compatible,
            reason=reason,
            record=self,
        )

    def validate_full_set(
        self,
        *,
        ar_drg_version: str | None,
        icd_10_am_version: str | None,
        achi_version: str | None,
        acs_version: str | None,
    ) -> ARDRGMappingCompatibilityResult:
        """Check whether a full ICD/ACHI/ACS/AR-DRG version set matches this record."""
        declared_versions = _declared_versions(
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )
        expected_versions = self.expected_coding_set_versions()
        mismatches = [
            f"{system}={declared_versions[system]!r} "
            f"(expected {expected_versions[system]!r})"
            for system in _EXPECTED_SYSTEMS
            if declared_versions[system] != expected_versions[system]
        ]
        compatible = not mismatches
        reason = None
        if mismatches:
            reason = (
                f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} {self.pricing_year} "
                "mapping set is incompatible: "
                f"{', '.join(mismatches)}"
            )
        return ARDRGMappingCompatibilityResult(
            pricing_year=self.pricing_year,
            declared_versions=declared_versions,
            expected_versions=expected_versions,
            compatible=compatible,
            reason=reason,
            record=self,
        )


_AR_DRG_MAPPING_RECORDS: Final[tuple[ARDRGMappingRecord, ...]] = tuple(
    ARDRGMappingRecord(
        pricing_year=str(row["pricing_year"]),
        financial_year=str(row["financial_year"]),
        effective_years=cast(tuple[str, ...], row["effective_years"]),
        ar_drg_version=str(row["ar_drg_version"]),
        icd_10_am_version=cast(str | None, row["icd_10_am_version"]),
        achi_version=cast(str | None, row["achi_version"]),
        acs_version=cast(str | None, row["acs_version"]),
        assets=tuple(
            ARDRGMappingAssetReference(
                kind=cast(
                    Literal[
                        "public-metadata",
                        "user-supplied-licensed-file",
                        "derived-validation-fixture",
                    ],
                    asset["kind"],
                ),
                source_refs=cast(tuple[str, ...], asset["source_refs"]),
                local_path_hint=cast(str | None, asset["local_path_hint"]),
                restricted=bool(asset["restricted"]),
                notes=cast(tuple[str, ...], asset["notes"]),
            )
            for asset in cast(tuple[dict[str, object], ...], row["assets"])
        ),
        notes=cast(tuple[str, ...], row["notes"]),
    )
    for row in AR_DRG_MAPPING_REGISTRY_ROWS
)

_RECORD_BY_YEAR: Final[dict[str, ARDRGMappingRecord]] = {
    record.pricing_year: record for record in _AR_DRG_MAPPING_RECORDS
}


def _declared_versions(
    *,
    ar_drg_version: str | None,
    icd_10_am_version: str | None,
    achi_version: str | None,
    acs_version: str | None,
) -> dict[str, str | None]:
    return {
        "ar_drg": None
        if ar_drg_version is None
        else _normalize_version(ar_drg_version, field="ar_drg_version"),
        "icd_10_am": None
        if icd_10_am_version is None
        else _normalize_version(icd_10_am_version, field="icd_10_am_version"),
        "achi": None
        if achi_version is None
        else _normalize_version(achi_version, field="achi_version"),
        "acs": None
        if acs_version is None
        else _normalize_version(acs_version, field="acs_version"),
    }


def list_ar_drg_mapping_records() -> tuple[ARDRGMappingRecord, ...]:
    """Return all known AR-DRG mapping registry records."""
    return _AR_DRG_MAPPING_RECORDS


def get_ar_drg_mapping_record(year: str) -> ARDRGMappingRecord | None:
    """Return the provenance record for a pricing year, if one exists."""
    normalized_year = _normalize_year(year)
    return _RECORD_BY_YEAR.get(normalized_year)


def get_expected_ar_drg_version(year: str) -> str | None:
    """Return the expected AR-DRG version for a pricing year."""
    normalized_year = _normalize_year(year)
    return get_expected_coding_set_version("ar_drg", normalized_year)


def get_expected_coding_set_versions(year: str) -> dict[str, str | None]:
    """Return the expected coding-set versions for a pricing year."""
    normalized_year = _normalize_year(year)
    return _expected_coding_set_versions(normalized_year)


def validate_ar_drg_version_binding(
    year: str,
    version: str | None,
) -> ARDRGMappingCompatibilityResult:
    """Check whether an AR-DRG version matches the expected pricing-year binding."""
    normalized_year = _normalize_year(year)
    expected_version = get_expected_ar_drg_version(normalized_year)
    declared = None
    if version is not None:
        declared = _normalize_version(version, field="ar_drg_version")
    compatible = expected_version is not None and declared == expected_version
    reason = None
    if expected_version is None:
        reason = (
            f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} is not mapped for pricing year "
            f"{normalized_year}"
        )
    elif declared is None:
        reason = (
            f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} {normalized_year} requires version "
            f"{expected_version}"
        )
    elif declared != expected_version:
        reason = (
            f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} {normalized_year} expects "
            f"{expected_version}, got {declared}"
        )
    return ARDRGMappingCompatibilityResult(
        pricing_year=normalized_year,
        declared_versions={"ar_drg": declared},
        expected_versions={"ar_drg": expected_version},
        compatible=compatible,
        reason=reason,
        record=get_ar_drg_mapping_record(normalized_year),
    )


def validate_ar_drg_mapping_compatibility(
    year: str,
    *,
    ar_drg_version: str | None,
    icd_10_am_version: str | None,
    achi_version: str | None,
    acs_version: str | None,
) -> ARDRGMappingCompatibilityResult:
    """Check whether a full mapping/version set matches the registry record."""
    normalized_year = _normalize_year(year)
    record = get_ar_drg_mapping_record(normalized_year)
    if record is None:
        return ARDRGMappingCompatibilityResult(
            pricing_year=normalized_year,
            declared_versions=_declared_versions(
                ar_drg_version=ar_drg_version,
                icd_10_am_version=icd_10_am_version,
                achi_version=achi_version,
                acs_version=acs_version,
            ),
            expected_versions=get_expected_coding_set_versions(normalized_year),
            compatible=False,
            reason=(
                f"{ARDRG_MAPPING_SYSTEMS['ar_drg']} {normalized_year} does not have a "
                "provenance registry record"
            ),
            record=None,
        )
    return record.validate_full_set(
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
    )


def ensure_ar_drg_mapping_compatibility(
    year: str,
    *,
    ar_drg_version: str | None,
    icd_10_am_version: str | None,
    achi_version: str | None,
    acs_version: str | None,
) -> ARDRGMappingCompatibilityResult:
    """Raise when a declared AR-DRG mapping/version set is incompatible."""
    result = validate_ar_drg_mapping_compatibility(
        year,
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
    )
    if not result.compatible:
        raise ARDRGMappingRegistryError(result.reason or "mapping set is incompatible")
    return result
