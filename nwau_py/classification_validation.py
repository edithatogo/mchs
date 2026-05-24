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
from typing import Any, Final

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

__all__ = [
    "AECC_REQUIRED_FIELDS",
    "AMHCC_REQUIRED_FIELDS",
    "AR_DRG_REQUIRED_FIELDS",
    "CLASSIFICATION_REQUIRED_FIELDS",
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

_SYSTEM_ALIASES: Final[dict[str, str]] = {
    "ar-drg": "ar_drg",
    "ar_drg": "ar_drg",
    "ar drg": "ar_drg",
    "aecc": "aecc",
    "udg": "udg",
    "tier-2": "tier_2",
    "tier_2": "tier_2",
    "tier 2": "tier_2",
    "amhcc": "amhcc",
}

CLASSIFICATION_SYSTEMS: Final[dict[str, str]] = {
    "ar_drg": "AR-DRG",
    "aecc": "AECC",
    "udg": "UDG",
    "tier_2": "Tier 2",
    "amhcc": "AMHCC",
}

LICENSED_CLASSIFICATIONS: Final[frozenset[str]] = frozenset({"ar_drg"})

AR_DRG_REQUIRED_FIELDS: Final[tuple[str, ...]] = ("DRG",)
AECC_REQUIRED_FIELDS: Final[tuple[str, ...]] = ("AECC",)
UDG_REQUIRED_FIELDS: Final[tuple[str, ...]] = ("UDG",)
TIER_2_REQUIRED_FIELDS: Final[tuple[str, ...]] = ("TIER2_CLINIC",)
AMHCC_REQUIRED_FIELDS: Final[tuple[str, ...]] = ("AMHCC",)

CLASSIFICATION_REQUIRED_FIELDS: Final[dict[str, tuple[str, ...]]] = {
    "ar_drg": AR_DRG_REQUIRED_FIELDS,
    "aecc": AECC_REQUIRED_FIELDS,
    "udg": UDG_REQUIRED_FIELDS,
    "tier_2": TIER_2_REQUIRED_FIELDS,
    "amhcc": AMHCC_REQUIRED_FIELDS,
}

_YEAR_VERSION_MATRIX: Final[dict[str, dict[str, str | None]]] = {
    "ar_drg": {
        "2013": "v7.0",
        "2014": "v7.0",
        "2015": "v7.0",
        "2016": "v8.0",
        "2017": "v8.0",
        "2018": "v9.0",
        "2019": "v9.0",
        "2020": "v10.0",
        "2021": "v10.0",
        "2022": "v10.0",
        "2023": "v11.0",
        "2024": "v11.0",
        "2025": "v11.0",
        "2026": "v12.0",
    },
    "aecc": {
        "2013": None,
        "2014": None,
        "2015": None,
        "2016": None,
        "2017": None,
        "2018": None,
        "2019": None,
        "2020": "v1.0_shadow",
        "2021": "v1.0",
        "2022": "v1.1",
        "2023": "v1.1",
        "2024": "v1.1",
        "2025": "v1.1",
        "2026": "v1.1",
    },
    "udg": {
        "2013": "URG_v1.4",
        "2014": "URG_v1.4",
        "2015": "URG_v1.4",
        "2016": "URG_v1.4",
        "2017": "URG_v1.4",
        "2018": "URG_v1.4",
        "2019": "URG_v1.4",
        "2020": "URG_v1.4",
        "2021": "UDG_v1.3",
        "2022": "UDG_v1.3",
        "2023": "UDG_v1.3",
        "2024": "UDG_v1.3",
        "2025": "UDG_v1.3",
        "2026": "UDG_v1.3",
    },
    "tier_2": {
        "2013": None,
        "2014": None,
        "2015": None,
        "2016": None,
        "2017": None,
        "2018": None,
        "2019": None,
        "2020": None,
        "2021": None,
        "2022": "v7",
        "2023": "v7",
        "2024": "v7",
        "2025": "v7",
        "2026": "v10.0",
    },
    "amhcc": {
        "2013": None,
        "2014": None,
        "2015": None,
        "2016": None,
        "2017": None,
        "2018": None,
        "2019": None,
        "2020": None,
        "2021": "v1",
        "2022": "v1",
        "2023": "v1",
        "2024": "v1",
        "2025": "v1",
        "2026": "v1",
    },
}

CLASSIFICATION_VERSION_MATRIX: Final[dict[str, dict[str, str | None]]] = (
    _YEAR_VERSION_MATRIX
)


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
