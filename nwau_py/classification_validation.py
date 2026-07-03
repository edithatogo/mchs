"""Strict classification-input validation helpers for NWAU calculator feeds.

This module keeps validation separate from calculator execution. It validates
only the classification boundary:

- required classification fields are present;
- pricing-year to classification-version compatibility is deterministic; and
- the validation result is explicit and immutable.

The helpers are intentionally narrow and do not depend on pandas or on any
calculator formula implementation.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any, Final, cast

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from .classification_mapping_registry_data import CLASSIFICATION_MAPPING_ROWS

__all__ = [
    "AECC_REQUIRED_FIELDS",
    "AMHCC_REQUIRED_FIELDS",
    "AR_DRG_REQUIRED_FIELDS",
    "CLASSIFICATION_REQUIRED_FIELDS",
    "CLASSIFICATION_SOURCE_REFS",
    "CLASSIFICATION_STREAMS",
    "CLASSIFICATION_SUPPORT_STATUS",
    "CLASSIFICATION_VERSION_MATRIX",
    "CLASSIFICATION_YEAR_RE",
    "TIER_2_REQUIRED_FIELDS",
    "UDG_REQUIRED_FIELDS",
    "ClassificationRequirement",
    "ClassificationValidationError",
    "ClassificationValidationResult",
    "build_classification_requirement",
    "get_classification_name",
    "get_classification_requirement",
    "get_classification_source_refs",
    "get_classification_stream",
    "get_classification_support_status",
    "get_classification_version",
    "get_expected_classification_version",
    "get_required_classification_fields",
    "get_supported_classification_years",
    "get_transition_years",
    "is_classification_licensed",
    "normalize_classification_system",
    "validate_aecc_input",
    "validate_amhcc_input",
    "validate_ar_drg_input",
    "validate_classification_input",
    "validate_classification_version",
    "validate_required_classification_fields",
    "validate_tier_2_input",
    "validate_udg_input",
]

CLASSIFICATION_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_CLASSIFICATION_VERSION_RE = re.compile(r"^[A-Za-z0-9_.-]+$")

_ROW_BY_SYSTEM: Final[dict[str, dict[str, object]]] = {
    str(row["system"]): row for row in CLASSIFICATION_MAPPING_ROWS
}

_SYSTEM_ALIASES: Final[dict[str, str]] = {
    str(alias).lower(): str(row["system"])
    for row in CLASSIFICATION_MAPPING_ROWS
    for alias in (
        row["system"],
        row["display_name"],
        *cast(tuple[str, ...], row["aliases"]),
    )
}

CLASSIFICATION_SYSTEMS: Final[dict[str, str]] = {
    system: str(row["display_name"]) for system, row in _ROW_BY_SYSTEM.items()
}

LICENSED_CLASSIFICATIONS: Final[frozenset[str]] = frozenset(
    system for system, row in _ROW_BY_SYSTEM.items() if bool(row["licensed"])
)

CLASSIFICATION_REQUIRED_FIELDS: Final[dict[str, tuple[str, ...]]] = {
    system: cast(tuple[str, ...], row["required_fields"])
    for system, row in _ROW_BY_SYSTEM.items()
}

AR_DRG_REQUIRED_FIELDS: Final[tuple[str, ...]] = CLASSIFICATION_REQUIRED_FIELDS[
    "ar_drg"
]
AECC_REQUIRED_FIELDS: Final[tuple[str, ...]] = CLASSIFICATION_REQUIRED_FIELDS["aecc"]
UDG_REQUIRED_FIELDS: Final[tuple[str, ...]] = CLASSIFICATION_REQUIRED_FIELDS["udg"]
TIER_2_REQUIRED_FIELDS: Final[tuple[str, ...]] = CLASSIFICATION_REQUIRED_FIELDS[
    "tier_2"
]
AMHCC_REQUIRED_FIELDS: Final[tuple[str, ...]] = CLASSIFICATION_REQUIRED_FIELDS["amhcc"]

CLASSIFICATION_SOURCE_REFS: Final[dict[str, tuple[str, ...]]] = {
    system: cast(tuple[str, ...], row["source_refs"])
    for system, row in _ROW_BY_SYSTEM.items()
}

CLASSIFICATION_STREAMS: Final[dict[str, str]] = {
    system: str(row["stream"]) for system, row in _ROW_BY_SYSTEM.items()
}

CLASSIFICATION_SUPPORT_STATUS: Final[dict[str, str]] = {
    system: str(row["support_status"]) for system, row in _ROW_BY_SYSTEM.items()
}

CLASSIFICATION_VERSION_MATRIX: Final[dict[str, dict[str, str | None]]] = {
    system: dict(cast(tuple[tuple[str, str | None]], row["versions"]))
    for system, row in _ROW_BY_SYSTEM.items()
}


class ClassificationValidationError(ValueError):
    """Raised when a classification input contract is invalid."""


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ClassificationValidationError(f"{field} must be a string")
    if not value:
        raise ClassificationValidationError(f"{field} must not be blank")
    if value.strip() != value:
        raise ClassificationValidationError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_fields(fields: Iterable[str], *, field: str) -> tuple[str, ...]:
    if isinstance(fields, (str, bytes)):
        raise ClassificationValidationError(
            f"{field} must be an iterable of classification field names"
        )

    normalized: list[str] = []
    seen: set[str] = set()
    for name in fields:
        normalized_name = _normalize_non_blank(name, field=field)
        if normalized_name in seen:
            raise ClassificationValidationError(
                f"{field} must not contain duplicate names"
            )
        seen.add(normalized_name)
        normalized.append(normalized_name)
    if not normalized:
        raise ClassificationValidationError(f"{field} must not be empty")
    return tuple(normalized)


def normalize_classification_system(system: str) -> str:
    """Return the canonical system identifier for a classification stream."""
    normalized = _normalize_non_blank(system, field="classification_system")
    key = normalized.lower()
    canonical = _SYSTEM_ALIASES.get(key)
    if canonical is None:
        raise ClassificationValidationError(
            "classification_system must be one of "
            f"{sorted(CLASSIFICATION_SYSTEMS)} or their display names"
        )
    return canonical


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not CLASSIFICATION_YEAR_RE.fullmatch(normalized):
        raise ClassificationValidationError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _expected_version_for(system: str, year: str) -> str | None:
    canonical_system = normalize_classification_system(system)
    normalized_year = _normalize_year(year)
    return CLASSIFICATION_VERSION_MATRIX.get(canonical_system, {}).get(normalized_year)


def get_expected_classification_version(system: str, year: str) -> str | None:
    """Return the expected classification version for a system/year pair."""
    return _expected_version_for(system, year)


def get_classification_version(system: str, year: str) -> str | None:
    """Alias for ``get_expected_classification_version``."""
    return get_expected_classification_version(system, year)


def get_classification_name(system: str) -> str:
    """Return the display name for a classification system."""
    canonical_system = normalize_classification_system(system)
    return CLASSIFICATION_SYSTEMS[canonical_system]


def get_classification_source_refs(system: str) -> tuple[str, ...]:
    """Return the public source references for a classification system."""
    canonical_system = normalize_classification_system(system)
    return CLASSIFICATION_SOURCE_REFS[canonical_system]


def get_classification_stream(system: str) -> str:
    """Return the primary stream for a classification system."""
    canonical_system = normalize_classification_system(system)
    return CLASSIFICATION_STREAMS[canonical_system]


def get_classification_support_status(system: str) -> str:
    """Return the support-status label for a classification system."""
    canonical_system = normalize_classification_system(system)
    return CLASSIFICATION_SUPPORT_STATUS[canonical_system]


def is_classification_licensed(system: str) -> bool:
    """Return ``True`` when a classification system is licensed."""
    canonical_system = normalize_classification_system(system)
    return canonical_system in LICENSED_CLASSIFICATIONS


def get_transition_years(system: str) -> tuple[str, ...]:
    """Return years where the expected version changes for a system."""
    canonical_system = normalize_classification_system(system)
    versions = CLASSIFICATION_VERSION_MATRIX[canonical_system]
    ordered_years = sorted(versions)
    transitions: list[str] = []
    for index in range(1, len(ordered_years)):
        previous = ordered_years[index - 1]
        current = ordered_years[index]
        if versions[current] != versions[previous]:
            transitions.append(current)
    return tuple(transitions)


def get_supported_classification_years(system: str) -> tuple[str, ...]:
    """Return the supported years for a classification system."""
    canonical_system = normalize_classification_system(system)
    return tuple(
        year
        for year, version in CLASSIFICATION_VERSION_MATRIX[canonical_system].items()
        if version is not None
    )


def get_classification_requirement(
    system: str,
    year: str,
) -> ClassificationRequirement:
    """Build the requirement model for a classification system/year pair."""
    canonical_system = normalize_classification_system(system)
    normalized_year = _normalize_year(year)
    return ClassificationRequirement(
        system=canonical_system,
        display_name=CLASSIFICATION_SYSTEMS[canonical_system],
        pricing_year=normalized_year,
        expected_version=_expected_version_for(canonical_system, normalized_year),
        required_fields=CLASSIFICATION_REQUIRED_FIELDS[canonical_system],
        licensed=canonical_system in LICENSED_CLASSIFICATIONS,
    )


def build_classification_requirement(
    system: str,
    year: str,
) -> ClassificationRequirement:
    """Alias for ``get_classification_requirement``."""
    return get_classification_requirement(system, year)


class ClassificationRequirement(BaseModel):
    """Strict classification contract for a single system/year pair."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    system: str
    display_name: str
    pricing_year: str
    expected_version: str | None
    required_fields: tuple[str, ...]
    licensed: bool

    @field_validator("system")
    @classmethod
    def _validate_system(cls, value: str) -> str:
        canonical = normalize_classification_system(value)
        return canonical

    @field_validator("display_name")
    @classmethod
    def _validate_display_name(cls, value: str) -> str:
        return _normalize_non_blank(value, field="display_name")

    @field_validator("pricing_year")
    @classmethod
    def _validate_pricing_year(cls, value: str) -> str:
        return _normalize_year(value)

    @field_validator("required_fields")
    @classmethod
    def _validate_required_fields(
        cls,
        value: Any,
    ) -> tuple[str, ...]:
        if value is None:
            raise ClassificationValidationError("required_fields must not be empty")
        return _normalize_fields(value, field="required_fields")

    @field_validator("expected_version")
    @classmethod
    def _validate_expected_version(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = _normalize_non_blank(value, field="expected_version")
        if not _CLASSIFICATION_VERSION_RE.fullmatch(normalized):
            raise ClassificationValidationError(
                "expected_version must be a version label such as 'v1.1'"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_consistency(self) -> ClassificationRequirement:
        expected_display_name = CLASSIFICATION_SYSTEMS[self.system]
        if self.display_name != expected_display_name:
            raise ClassificationValidationError(
                f"display_name {self.display_name!r} does not match "
                f"system {self.system!r}"
            )
        required_fields = CLASSIFICATION_REQUIRED_FIELDS[self.system]
        if self.required_fields != required_fields:
            raise ClassificationValidationError(
                f"required_fields for {self.system!r} must be {required_fields!r}"
            )
        expected_version = _expected_version_for(self.system, self.pricing_year)
        if self.expected_version != expected_version:
            raise ClassificationValidationError(
                f"expected_version for {self.system!r} in {self.pricing_year!r} "
                f"must be {expected_version!r}"
            )
        if self.licensed != (self.system in LICENSED_CLASSIFICATIONS):
            raise ClassificationValidationError(
                f"licensed flag for {self.system!r} is inconsistent"
            )
        return self

    def missing_fields(self, observed_fields: Iterable[str]) -> tuple[str, ...]:
        """Return the required classification fields that are absent."""
        observed = _normalize_fields(observed_fields, field="observed_fields")
        observed_set = set(observed)
        return tuple(
            field for field in self.required_fields if field not in observed_set
        )

    def validate_fields(self, observed_fields: Iterable[str]) -> None:
        """Raise when required fields are missing."""
        missing = self.missing_fields(observed_fields)
        if missing:
            raise ClassificationValidationError(
                f"{self.display_name} {self.pricing_year} is missing required fields: "
                + ", ".join(missing)
            )

    def validate_version(self, version: str | None) -> str:
        """Raise when a declared classification version is incompatible."""
        if self.expected_version is None:
            raise ClassificationValidationError(
                f"{self.display_name} is not available for pricing year "
                f"{self.pricing_year}"
            )
        if version is None:
            raise ClassificationValidationError(
                f"{self.display_name} {self.pricing_year} requires an explicit "
                f"classification_version of {self.expected_version}"
            )
        declared_version = _normalize_non_blank(version, field="classification_version")
        if not _CLASSIFICATION_VERSION_RE.fullmatch(declared_version):
            raise ClassificationValidationError(
                "classification_version must be a deterministic version label"
            )
        if declared_version != self.expected_version:
            raise ClassificationValidationError(
                f"{self.display_name} {self.pricing_year} expects "
                f"{self.expected_version}, got {declared_version}"
            )
        return declared_version

    def validate_input(
        self,
        observed_fields: Iterable[str],
        *,
        version: str | None,
    ) -> ClassificationValidationResult:
        """Validate the contract and return a frozen result model."""
        observed = _normalize_fields(observed_fields, field="observed_fields")
        missing = tuple(
            field for field in self.required_fields if field not in set(observed)
        )
        if missing:
            raise ClassificationValidationError(
                f"{self.display_name} {self.pricing_year} is missing required fields: "
                + ", ".join(missing)
            )
        declared_version = self.validate_version(version)
        return ClassificationValidationResult(
            system=self.system,
            display_name=self.display_name,
            pricing_year=self.pricing_year,
            declared_version=declared_version,
            expected_version=self.expected_version or declared_version,
            required_fields=self.required_fields,
            observed_fields=observed,
            missing_fields=missing,
            licensed=self.licensed,
        )


class ClassificationValidationResult(BaseModel):
    """Validated classification input contract outcome."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    system: str
    display_name: str
    pricing_year: str
    declared_version: str
    expected_version: str
    required_fields: tuple[str, ...]
    observed_fields: tuple[str, ...]
    missing_fields: tuple[str, ...]
    licensed: bool

    @field_validator(
        "system",
        "display_name",
        "pricing_year",
        "declared_version",
        "expected_version",
    )
    @classmethod
    def _validate_non_blank(cls, value: str) -> str:
        return _normalize_non_blank(value, field="classification result field")

    @field_validator("required_fields", "observed_fields")
    @classmethod
    def _validate_required_tuples(
        cls,
        value: Any,
    ) -> tuple[str, ...]:
        if value is None:
            raise ClassificationValidationError("field tuples must not be empty")
        return _normalize_fields(value, field="classification result fields")

    @field_validator("missing_fields")
    @classmethod
    def _validate_missing_fields(
        cls,
        value: Any,
    ) -> tuple[str, ...]:
        if value is None:
            raise ClassificationValidationError("missing_fields must not be null")
        if isinstance(value, tuple) and not value:
            return tuple()
        return _normalize_fields(value, field="missing_fields")

    @property
    def is_valid(self) -> bool:
        """Return ``True`` when the validated input had no missing fields."""
        return not self.missing_fields


def get_required_classification_fields(system: str) -> tuple[str, ...]:
    """Return the required classification fields for a system."""
    canonical_system = normalize_classification_system(system)
    return CLASSIFICATION_REQUIRED_FIELDS[canonical_system]


def validate_required_classification_fields(
    observed_fields: Iterable[str],
    required_fields: Iterable[str],
) -> tuple[str, ...]:
    """Raise when required classification fields are missing."""
    observed = _normalize_fields(observed_fields, field="observed_fields")
    required = _normalize_fields(required_fields, field="required_fields")
    observed_set = set(observed)
    missing = tuple(field for field in required if field not in observed_set)
    if missing:
        raise ClassificationValidationError(
            "missing required classification fields: " + ", ".join(missing)
        )
    return missing


def validate_classification_version(
    system: str,
    year: str,
    version: str | None,
) -> str:
    """Raise when a declared classification version is incompatible."""
    requirement = get_classification_requirement(system, year)
    return requirement.validate_version(version)


def validate_classification_input(
    system: str,
    year: str,
    observed_fields: Iterable[str],
    *,
    version: str | None,
) -> ClassificationValidationResult:
    """Validate required fields and version compatibility for a classification."""
    requirement = get_classification_requirement(system, year)
    return requirement.validate_input(observed_fields, version=version)


def validate_ar_drg_input(
    observed_fields: Iterable[str],
    *,
    year: str,
    version: str | None,
) -> ClassificationValidationResult:
    """Validate an AR-DRG classification input surface."""
    return validate_classification_input(
        "ar_drg", year, observed_fields, version=version
    )


def validate_aecc_input(
    observed_fields: Iterable[str],
    *,
    year: str,
    version: str | None,
) -> ClassificationValidationResult:
    """Validate an AECC classification input surface."""
    return validate_classification_input("aecc", year, observed_fields, version=version)


def validate_udg_input(
    observed_fields: Iterable[str],
    *,
    year: str,
    version: str | None,
) -> ClassificationValidationResult:
    """Validate a UDG classification input surface."""
    return validate_classification_input("udg", year, observed_fields, version=version)


def validate_tier_2_input(
    observed_fields: Iterable[str],
    *,
    year: str,
    version: str | None,
) -> ClassificationValidationResult:
    """Validate a Tier 2 classification input surface."""
    return validate_classification_input(
        "tier_2", year, observed_fields, version=version
    )


def validate_amhcc_input(
    observed_fields: Iterable[str],
    *,
    year: str,
    version: str | None,
) -> ClassificationValidationResult:
    """Validate an AMHCC classification input surface."""
    return validate_classification_input(
        "amhcc", year, observed_fields, version=version
    )
