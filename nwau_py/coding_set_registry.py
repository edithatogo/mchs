"""Registry helpers for coding-set versions, licensing, and compatibility."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final, cast

from .coding_set_registry_data import CODING_SET_FAMILY_ROWS

__all__ = [
    "CLASSIFICATION_REQUIRED_FIELDS",
    "CLASSIFICATION_SYSTEMS",
    "CLASSIFICATION_VERSION_MATRIX",
    "CodingSetCompatibilityResult",
    "CodingSetFamily",
    "CodingSetPolicy",
    "CodingSetRegistryError",
    "CodingSetVersion",
    "ensure_coding_set_compatibility",
    "get_coding_set_family",
    "get_coding_set_policy",
    "get_coding_set_restriction",
    "get_coding_set_version",
    "get_expected_coding_set_version",
    "get_supported_coding_set_years",
    "is_coding_set_licensed",
    "is_coding_set_restricted",
    "list_coding_set_families",
    "normalize_coding_set_system",
    "validate_coding_set_compatibility",
]

_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_VERSION_RE = re.compile(r"^[A-Za-z0-9_. -]+$")


class CodingSetRegistryError(ValueError):
    """Raised when a coding-set registry lookup is invalid."""


@dataclass(frozen=True, slots=True)
class CodingSetVersion:
    """Year/version pairing for a coding-set family."""

    year: str
    expected_version: str | None

    def to_dict(self) -> dict[str, str | None]:
        """Return a JSON-serializable version row."""
        return {
            "year": self.year,
            "expected_version": self.expected_version,
        }


@dataclass(frozen=True, slots=True)
class CodingSetFamily:
    """Immutable description of a coding-set family."""

    system: str
    display_name: str
    aliases: tuple[str, ...]
    licensed: bool
    restriction: str | None
    notes: tuple[str, ...]
    versions: tuple[CodingSetVersion, ...]

    def version_for_year(self, year: str) -> str | None:
        for item in self.versions:
            if item.year == year:
                return item.expected_version
        return None

    def supported_years(self) -> tuple[str, ...]:
        return tuple(
            item.year for item in self.versions if item.expected_version is not None
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable registry family."""
        return {
            "system": self.system,
            "display_name": self.display_name,
            "aliases": list(self.aliases),
            "licensed": self.licensed,
            "restriction": self.restriction,
            "notes": list(self.notes),
            "versions": [version.to_dict() for version in self.versions],
            "supported_years": list(self.supported_years()),
        }


@dataclass(frozen=True, slots=True)
class CodingSetPolicy:
    """Licensing and restriction metadata for a family."""

    licensed: bool
    restriction: str | None
    notes: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable licensing policy."""
        return {
            "licensed": self.licensed,
            "restriction": self.restriction,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class CodingSetCompatibilityResult:
    """Outcome from a compatibility check."""

    system: str
    display_name: str
    pricing_year: str
    declared_version: str | None
    expected_version: str | None
    licensed: bool
    restriction: str | None
    compatible: bool
    reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable compatibility result."""
        return {
            "system": self.system,
            "display_name": self.display_name,
            "pricing_year": self.pricing_year,
            "declared_version": self.declared_version,
            "expected_version": self.expected_version,
            "licensed": self.licensed,
            "restriction": self.restriction,
            "compatible": self.compatible,
            "reason": self.reason,
        }


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise CodingSetRegistryError(f"{field} must be a string")
    if not value:
        raise CodingSetRegistryError(f"{field} must not be blank")
    if value.strip() != value:
        raise CodingSetRegistryError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise CodingSetRegistryError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_alias(alias: str) -> str:
    return _normalize_non_blank(alias, field="coding_set_system").lower()


def _build_family(row: dict[str, object]) -> CodingSetFamily:
    versions = cast(tuple[tuple[str, str | None], ...], row["versions"])
    return CodingSetFamily(
        system=str(row["system"]),
        display_name=str(row["display_name"]),
        aliases=tuple(str(alias) for alias in cast(tuple[str, ...], row["aliases"])),
        licensed=bool(row["licensed"]),
        restriction=(None if row["restriction"] is None else str(row["restriction"])),
        notes=tuple(str(note) for note in cast(tuple[str, ...], row["notes"])),
        versions=tuple(
            CodingSetVersion(year=str(year), expected_version=version)
            for year, version in versions
        ),
    )


_CODING_SET_FAMILIES: Final[tuple[CodingSetFamily, ...]] = tuple(
    _build_family(row) for row in CODING_SET_FAMILY_ROWS
)

_FAMILY_BY_SYSTEM: Final[dict[str, CodingSetFamily]] = {
    family.system: family for family in _CODING_SET_FAMILIES
}
_ALIASES: Final[dict[str, str]] = {
    _normalize_alias(alias): family.system
    for family in _CODING_SET_FAMILIES
    for alias in (family.system, family.display_name, *family.aliases)
}

CLASSIFICATION_SYSTEMS: Final[dict[str, str]] = {
    system: _FAMILY_BY_SYSTEM[system].display_name
    for system in ("ar_drg", "aecc", "udg", "tier_2", "amhcc")
}

CLASSIFICATION_REQUIRED_FIELDS: Final[dict[str, tuple[str, ...]]] = {
    "ar_drg": ("DRG",),
    "aecc": ("AECC",),
    "udg": ("UDG",),
    "tier_2": ("TIER2_CLINIC",),
    "amhcc": ("AMHCC",),
}

CLASSIFICATION_VERSION_MATRIX: Final[dict[str, dict[str, str | None]]] = {
    system: {item.year: item.expected_version for item in family.versions}
    for system, family in _FAMILY_BY_SYSTEM.items()
    if system in CLASSIFICATION_SYSTEMS
}


def list_coding_set_families() -> tuple[CodingSetFamily, ...]:
    """Return all known coding-set families in registry order."""
    return _CODING_SET_FAMILIES


def normalize_coding_set_system(system: str) -> str:
    """Return the canonical system identifier for a coding-set family."""
    normalized = _normalize_alias(system)
    canonical = _ALIASES.get(normalized)
    if canonical is None:
        raise CodingSetRegistryError(
            "coding_set_system must be one of "
            f"{sorted(family.display_name for family in _CODING_SET_FAMILIES)} "
            "or their alias forms"
        )
    return canonical


def get_coding_set_family(system: str) -> CodingSetFamily:
    """Return the registry entry for a coding-set family."""
    canonical = normalize_coding_set_system(system)
    return _FAMILY_BY_SYSTEM[canonical]


def get_coding_set_policy(system: str) -> CodingSetPolicy:
    """Return the licensing policy for a coding-set family."""
    family = get_coding_set_family(system)
    return CodingSetPolicy(
        licensed=family.licensed,
        restriction=family.restriction,
        notes=family.notes,
    )


def get_coding_set_restriction(system: str) -> str | None:
    """Return the restriction text for a coding-set family."""
    return get_coding_set_policy(system).restriction


def is_coding_set_licensed(system: str) -> bool:
    """Return ``True`` when a coding set is licensed."""
    return get_coding_set_policy(system).licensed


def is_coding_set_restricted(system: str) -> bool:
    """Return ``True`` when a coding set has an explicit restriction note."""
    return get_coding_set_restriction(system) is not None


def get_supported_coding_set_years(system: str) -> tuple[str, ...]:
    """Return the supported years for a coding-set family."""
    return get_coding_set_family(system).supported_years()


def get_expected_coding_set_version(system: str, year: str) -> str | None:
    """Return the expected version for a coding-set system/year pair."""
    canonical = normalize_coding_set_system(system)
    normalized_year = _normalize_year(year)
    return _FAMILY_BY_SYSTEM[canonical].version_for_year(normalized_year)


def get_coding_set_version(system: str, year: str) -> str | None:
    """Alias for ``get_expected_coding_set_version``."""
    return get_expected_coding_set_version(system, year)


def validate_coding_set_compatibility(
    system: str,
    year: str,
    version: str | None,
) -> CodingSetCompatibilityResult:
    """Check whether a declared version matches the registry expectation."""
    family = get_coding_set_family(system)
    normalized_year = _normalize_year(year)
    expected_version = family.version_for_year(normalized_year)
    declared_version: str | None = None
    if version is not None:
        declared_version = _normalize_non_blank(version, field="coding_set_version")
        if not _VERSION_RE.fullmatch(declared_version):
            raise CodingSetRegistryError(
                "coding_set_version must be a deterministic version label"
            )

    if expected_version is None:
        reason = (
            f"{family.display_name} is not mapped for pricing year {normalized_year}"
        )
        return CodingSetCompatibilityResult(
            system=family.system,
            display_name=family.display_name,
            pricing_year=normalized_year,
            declared_version=declared_version,
            expected_version=None,
            licensed=family.licensed,
            restriction=family.restriction,
            compatible=False,
            reason=reason,
        )

    compatible = declared_version == expected_version
    reason = None
    if declared_version is None:
        reason = (
            f"{family.display_name} {normalized_year} requires version "
            f"{expected_version}"
        )
    elif not compatible:
        reason = (
            f"{family.display_name} {normalized_year} expects {expected_version}, "
            f"got {declared_version}"
        )

    return CodingSetCompatibilityResult(
        system=family.system,
        display_name=family.display_name,
        pricing_year=normalized_year,
        declared_version=declared_version,
        expected_version=expected_version,
        licensed=family.licensed,
        restriction=family.restriction,
        compatible=compatible,
        reason=reason,
    )


def ensure_coding_set_compatibility(
    system: str,
    year: str,
    version: str | None,
) -> CodingSetCompatibilityResult:
    """Raise when a declared coding-set version is incompatible."""
    result = validate_coding_set_compatibility(system, year, version)
    if not result.compatible:
        raise CodingSetRegistryError(result.reason or "coding set is incompatible")
    return result
