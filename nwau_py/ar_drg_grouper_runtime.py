"""Provider runtime helpers for conservative AR-DRG workflows.

The runtime keeps the provider boundary explicit. It describes supported
precomputed, local command, local service, file exchange, and container
workflows without redistributing proprietary grouper logic.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final, Literal, cast

from .ar_drg_grouper import (
    ARDRGGrouperError,
    ARDRGGrouperReference,
    ARDRGGroupRecord,
    build_ar_drg_group_record_from_reference,
    build_ar_drg_precomputed_group_record,
    build_ar_drg_provenance,
    ensure_ar_drg_grouper_compatibility,
    validate_ar_drg_grouper_compatibility,
)

__all__ = [
    "ARDRGGrouperProviderCompatibilityResult",
    "ARDRGGrouperProviderProfile",
    "build_ar_drg_group_record_from_provider",
    "ensure_ar_drg_grouper_provider_compatibility",
    "list_ar_drg_grouper_provider_profiles",
    "validate_ar_drg_grouper_provider_compatibility",
]

_PROVIDER_TYPES: Final[frozenset[str]] = frozenset(
    {
        "precomputed",
        "local_command",
        "local_service",
        "file_exchange",
        "container",
    }
)
_PROVIDER_STATUSES: Final[frozenset[str]] = frozenset(
    {"source_available", "executable", "validated"}
)
_RESULT_STATUSES: Final[frozenset[str]] = frozenset(
    {"source_available", "executable", "validated", "blocked_licensed", "out_of_scope"}
)
_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")


def _normalize_non_blank(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise ARDRGGrouperError(f"{field} must be a string")
    if not value:
        raise ARDRGGrouperError(f"{field} must not be blank")
    if value.strip() != value:
        raise ARDRGGrouperError(
            f"{field} must not contain leading or trailing whitespace"
        )
    return value


def _normalize_year(year: str) -> str:
    normalized = _normalize_non_blank(year, field="pricing_year")
    if not _YEAR_RE.fullmatch(normalized):
        raise ARDRGGrouperError(
            "pricing_year must be a supported four-digit label between 2013 and 2026"
        )
    return normalized


def _normalize_provider_type(provider_type: str) -> str:
    normalized = _normalize_non_blank(provider_type, field="provider_type").lower()
    return normalized.replace("-", "_").replace(" ", "_")


def _normalize_optional_text(value: str | None, *, field: str) -> str | None:
    if value is None:
        return None
    return _normalize_non_blank(value, field=field)


@dataclass(frozen=True, slots=True)
class ARDRGGrouperProviderProfile:
    """Metadata-only description of a supported AR-DRG provider workflow."""

    provider_type: Literal[
        "precomputed",
        "local_command",
        "local_service",
        "file_exchange",
        "container",
    ]
    support_status: Literal["source_available", "executable", "validated"]
    license_boundary: Literal["local-only", "restricted", "metadata-only"]
    requires_reference: bool
    requires_container_image: bool
    source_refs: tuple[str, ...]
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.provider_type not in _PROVIDER_TYPES:
            raise ARDRGGrouperError(f"unsupported provider_type {self.provider_type!r}")
        if self.support_status not in _PROVIDER_STATUSES:
            raise ARDRGGrouperError(
                f"unsupported provider support_status {self.support_status!r}"
            )
        if self.license_boundary not in {"local-only", "restricted", "metadata-only"}:
            raise ARDRGGrouperError(
                f"unsupported license_boundary {self.license_boundary!r}"
            )
        if self.source_refs:
            object.__setattr__(
                self,
                "source_refs",
                tuple(
                    _normalize_non_blank(item, field="source_refs")
                    for item in self.source_refs
                ),
            )
        else:
            raise ARDRGGrouperError("source_refs must not be empty")
        if self.notes:
            object.__setattr__(
                self,
                "notes",
                tuple(_normalize_non_blank(item, field="notes") for item in self.notes),
            )
        else:
            object.__setattr__(self, "notes", tuple())

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_type": self.provider_type,
            "support_status": self.support_status,
            "license_boundary": self.license_boundary,
            "requires_reference": self.requires_reference,
            "requires_container_image": self.requires_container_image,
            "source_refs": list(self.source_refs),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class ARDRGGrouperProviderCompatibilityResult:
    """Outcome from a provider-runtime compatibility check."""

    provider_type: str
    pricing_year: str
    support_status: str
    compatible: bool
    reason: str | None
    profile: ARDRGGrouperProviderProfile | None = None
    reference: ARDRGGrouperReference | None = None
    container_image: str | None = None
    record: Any | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "provider_type": self.provider_type,
            "pricing_year": self.pricing_year,
            "support_status": self.support_status,
            "compatible": self.compatible,
            "reason": self.reason,
            "profile": None if self.profile is None else self.profile.to_dict(),
            "reference": None if self.reference is None else self.reference.to_dict(),
            "container_image": self.container_image,
            "record": None if self.record is None else self.record.to_dict(),
        }


_PROFILES: Final[tuple[ARDRGGrouperProviderProfile, ...]] = (
    ARDRGGrouperProviderProfile(
        provider_type="precomputed",
        support_status="source_available",
        license_boundary="metadata-only",
        requires_reference=False,
        requires_container_image=False,
        source_refs=(
            "conductor/archive/ar_drg_grouper_integration_20260512/spec.md",
            "nwau_py/docs/calculators.md",
        ),
        notes=(
            "Precomputed AR-DRG values are accepted as provenance-bearing inputs.",
            "The runtime does not regroup or infer missing DRGs.",
        ),
    ),
    ARDRGGrouperProviderProfile(
        provider_type="local_command",
        support_status="executable",
        license_boundary="local-only",
        requires_reference=True,
        requires_container_image=False,
        source_refs=(
            "conductor/archive/ar_drg_grouper_integration_20260512/spec.md",
            "conductor/archive/icd_achi_acs_license_workflow_20260512/spec.md",
        ),
        notes=("User-supplied local command providers remain local-only.",),
    ),
    ARDRGGrouperProviderProfile(
        provider_type="local_service",
        support_status="executable",
        license_boundary="local-only",
        requires_reference=True,
        requires_container_image=False,
        source_refs=(
            "conductor/archive/ar_drg_grouper_integration_20260512/spec.md",
            "conductor/archive/icd_achi_acs_license_workflow_20260512/spec.md",
        ),
        notes=("Locally hosted services remain user-supplied.",),
    ),
    ARDRGGrouperProviderProfile(
        provider_type="file_exchange",
        support_status="validated",
        license_boundary="local-only",
        requires_reference=True,
        requires_container_image=False,
        source_refs=(
            "conductor/archive/ar_drg_grouper_integration_20260512/spec.md",
            "conductor/archive/icd_achi_acs_license_workflow_20260512/spec.md",
        ),
        notes=("File-exchange workflows are validated but remain external.",),
    ),
    ARDRGGrouperProviderProfile(
        provider_type="container",
        support_status="executable",
        license_boundary="local-only",
        requires_reference=False,
        requires_container_image=True,
        source_refs=(
            "conductor/archive/ar_drg_grouper_integration_20260512/spec.md",
            "nwau_py/docs/calculators.md",
        ),
        notes=("Optional container execution is user-supplied and local-only.",),
    ),
)

_PROFILE_BY_TYPE: Final[dict[str, ARDRGGrouperProviderProfile]] = {
    profile.provider_type: profile for profile in _PROFILES
}


def list_ar_drg_grouper_provider_profiles() -> tuple[ARDRGGrouperProviderProfile, ...]:
    """Return all supported provider runtime profiles."""
    return _PROFILES


def _profile_for(provider_type: str) -> ARDRGGrouperProviderProfile | None:
    try:
        normalized = _normalize_provider_type(provider_type)
    except ARDRGGrouperError:
        return None
    return _PROFILE_BY_TYPE.get(normalized)


def _compatibility_result(
    *,
    provider_type: str,
    year: str,
    support_status: str,
    compatible: bool,
    reason: str | None,
    profile: ARDRGGrouperProviderProfile | None,
    reference: ARDRGGrouperReference | None,
    container_image: str | None,
    record: Any | None,
) -> ARDRGGrouperProviderCompatibilityResult:
    return ARDRGGrouperProviderCompatibilityResult(
        provider_type=provider_type,
        pricing_year=_normalize_year(year),
        support_status=support_status,
        compatible=compatible,
        reason=reason,
        profile=profile,
        reference=reference,
        container_image=container_image,
        record=record,
    )


def validate_ar_drg_grouper_provider_compatibility(
    provider_type: str,
    *,
    year: str,
    ar_drg_version: str | None = None,
    icd_10_am_version: str | None = None,
    achi_version: str | None = None,
    acs_version: str | None = None,
    reference: ARDRGGrouperReference | None = None,
    container_image: str | None = None,
) -> ARDRGGrouperProviderCompatibilityResult:
    """Check whether a provider workflow can be consumed safely."""
    normalized_provider_type = _normalize_provider_type(provider_type)
    normalized_year = _normalize_year(year)
    profile = _PROFILE_BY_TYPE.get(normalized_provider_type)
    if profile is None:
        return _compatibility_result(
            provider_type=normalized_provider_type,
            year=normalized_year,
            support_status="out_of_scope",
            compatible=False,
            reason=f"unsupported provider_type {normalized_provider_type!r}",
            profile=None,
            reference=reference,
            container_image=container_image,
            record=None,
        )

    if normalized_provider_type == "precomputed":
        result = validate_ar_drg_grouper_compatibility(
            normalized_year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )
        return _compatibility_result(
            provider_type=normalized_provider_type,
            year=normalized_year,
            support_status=profile.support_status,
            compatible=result.compatible,
            reason=result.reason,
            profile=profile,
            reference=None,
            container_image=None,
            record=result.record,
        )

    if normalized_provider_type in {"local_command", "local_service", "file_exchange"}:
        if reference is None:
            return _compatibility_result(
                provider_type=normalized_provider_type,
                year=normalized_year,
                support_status="blocked_licensed",
                compatible=False,
                reason=f"{normalized_provider_type} provider requires a reference",
                profile=profile,
                reference=None,
                container_image=None,
                record=None,
            )
        result = validate_ar_drg_grouper_compatibility(
            normalized_year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
            reference=reference,
        )
        if not result.compatible:
            return _compatibility_result(
                provider_type=normalized_provider_type,
                year=normalized_year,
                support_status="blocked_licensed",
                compatible=False,
                reason=result.reason,
                profile=profile,
                reference=reference,
                container_image=None,
                record=result.record,
            )
        return _compatibility_result(
            provider_type=normalized_provider_type,
            year=normalized_year,
            support_status=profile.support_status,
            compatible=True,
            reason=None,
            profile=profile,
            reference=reference,
            container_image=None,
            record=result.record,
        )

    if normalized_provider_type == "container":
        if container_image is None:
            return _compatibility_result(
                provider_type=normalized_provider_type,
                year=normalized_year,
                support_status="blocked_licensed",
                compatible=False,
                reason="container provider requires a container_image",
                profile=profile,
                reference=None,
                container_image=None,
                record=None,
            )
        result = validate_ar_drg_grouper_compatibility(
            normalized_year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )
        if not result.compatible:
            return _compatibility_result(
                provider_type=normalized_provider_type,
                year=normalized_year,
                support_status="blocked_licensed",
                compatible=False,
                reason=result.reason,
                profile=profile,
                reference=None,
                container_image=container_image,
                record=result.record,
            )
        return _compatibility_result(
            provider_type=normalized_provider_type,
            year=normalized_year,
            support_status=profile.support_status,
            compatible=True,
            reason=None,
            profile=profile,
            reference=None,
            container_image=container_image,
            record=result.record,
        )

    return _compatibility_result(
        provider_type=normalized_provider_type,
        year=normalized_year,
        support_status="out_of_scope",
        compatible=False,
        reason=f"unsupported provider_type {normalized_provider_type!r}",
        profile=profile,
        reference=reference,
        container_image=container_image,
        record=None,
    )


def ensure_ar_drg_grouper_provider_compatibility(
    provider_type: str,
    *,
    year: str,
    ar_drg_version: str | None = None,
    icd_10_am_version: str | None = None,
    achi_version: str | None = None,
    acs_version: str | None = None,
    reference: ARDRGGrouperReference | None = None,
    container_image: str | None = None,
) -> ARDRGGrouperProviderCompatibilityResult:
    """Raise when a provider workflow is incompatible."""
    result = validate_ar_drg_grouper_provider_compatibility(
        provider_type,
        year=year,
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
        reference=reference,
        container_image=container_image,
    )
    if not result.compatible:
        raise ARDRGGrouperError(result.reason or "provider workflow is invalid")
    return result


def build_ar_drg_group_record_from_provider(
    provider_type: str,
    drg: str,
    *,
    year: str,
    ar_drg_version: str,
    icd_10_am_version: str,
    achi_version: str,
    acs_version: str,
    input_sha256: str,
    provider_version: str | None = None,
    reference: ARDRGGrouperReference | None = None,
    container_image: str | None = None,
    episode_id: str | None = None,
    generated_at: str | None = None,
    notes: tuple[str, ...] = (),
) -> ARDRGGroupRecord:
    """Build a provenance-bearing AR-DRG group record from a provider workflow."""
    result = ensure_ar_drg_grouper_provider_compatibility(
        provider_type,
        year=year,
        ar_drg_version=ar_drg_version,
        icd_10_am_version=icd_10_am_version,
        achi_version=achi_version,
        acs_version=acs_version,
        reference=reference,
        container_image=container_image,
    )
    if not result.compatible:
        raise ARDRGGrouperError(result.reason or "provider workflow is incompatible")

    normalized_provider_type = _normalize_provider_type(provider_type)
    if normalized_provider_type == "precomputed":
        return build_ar_drg_precomputed_group_record(
            drg,
            year=year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
            input_sha256=input_sha256,
            episode_id=episode_id,
            grouper_version=provider_version,
            generated_at=generated_at,
            notes=notes,
        )

    if normalized_provider_type in {"local_command", "local_service", "file_exchange"}:
        reference = cast(ARDRGGrouperReference, reference)
        return build_ar_drg_group_record_from_reference(
            drg,
            year=year,
            reference=reference,
            input_sha256=input_sha256,
            grouper_version=provider_version or reference.reference_id,
            episode_id=episode_id,
            generated_at=generated_at,
            notes=notes,
        )

    if normalized_provider_type == "container":
        ensure_ar_drg_grouper_compatibility(
            year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
        )
        provenance = build_ar_drg_provenance(
            year=year,
            ar_drg_version=ar_drg_version,
            icd_10_am_version=icd_10_am_version,
            achi_version=achi_version,
            acs_version=acs_version,
            input_sha256=input_sha256,
            source_mode="external-reference",
            grouper_version=provider_version or container_image,
            external_reference_id=container_image,
            generated_at=generated_at,
            notes=notes,
        )
        return ARDRGGroupRecord(drg=drg, episode_id=episode_id, provenance=provenance)

    raise ARDRGGrouperError(f"unsupported provider_type {normalized_provider_type!r}")
