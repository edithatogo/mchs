from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path
from typing import Final

from nwau_py.reference_manifest import (
    ReferenceDataManifest,
    ReferenceManifestError,
    load_reference_manifest,
)

__all__ = [
    "NEC26",
    "NEC26_SOURCE",
    "NEC_BY_YEAR",
    "NEP26",
    "NEP26_SOURCE",
    "NEP_BY_YEAR",
    "PRICING_CONSTANTS_SCHEMA_VERSION",
    "NecPricing",
    "PricingConstantSource",
    "get_nec",
    "get_nep",
    "get_supported_pricing_years",
]

PRICING_CONSTANTS_SCHEMA_VERSION: Final[str] = "1.0"
_REFERENCE_DATA_ROOT: Final[str] = "reference-data"


@dataclass(frozen=True, slots=True)
class PricingConstantSource:
    """Conservative source metadata for a published IHACPA pricing constant."""

    resource_url: str
    artifact_url: str
    published_on: date
    last_updated_on: date | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class NecPricing:
    """Fixed-plus-variable NEC headline values for a pricing year."""

    fixed_cost_dollars: int
    variable_cost_per_nwau: int
    in_scope_hospitals: int
    source: PricingConstantSource


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _reference_data_root(repo_root: Path | str | None = None) -> Path:
    root = Path(repo_root) if repo_root is not None else _default_repo_root()
    return root / _REFERENCE_DATA_ROOT


def _reference_manifest_path(repo_root: Path | str | None, year: str) -> Path:
    return _reference_data_root(repo_root) / year / "manifest.yaml"


@cache
def _load_reference_manifest_cached(manifest_path: str) -> ReferenceDataManifest:
    return load_reference_manifest(Path(manifest_path))


def _load_pricing_year_manifest(
    year: str,
    *,
    repo_root: Path | str | None = None,
) -> ReferenceDataManifest:
    manifest_path = _reference_manifest_path(repo_root, year)
    if not manifest_path.is_file():
        raise ReferenceManifestError(
            f"missing reference-data manifest at {manifest_path.as_posix()}"
        )
    return _load_reference_manifest_cached(manifest_path.as_posix())


def _pricing_year_nep_value(manifest: ReferenceDataManifest) -> int:
    nep_record = manifest.constants.get("nep")
    if not isinstance(nep_record, dict):
        raise ReferenceManifestError(
            "reference manifest validation failed:\n"
            "- constants.nep: missing pricing constant record"
        )
    value = nep_record.get("value")
    if not isinstance(value, int) or isinstance(value, bool):
        raise ReferenceManifestError(
            "reference manifest validation failed:\n"
            "- constants.nep.value: must be an integer"
        )
    return value


def _build_nep_by_year(*, repo_root: Path | str | None = None) -> dict[str, int]:
    root = _reference_data_root(repo_root)
    if not root.is_dir():
        raise ReferenceManifestError(
            f"missing reference-data directory at {root.as_posix()}"
        )

    pricing_years: dict[str, int] = {}
    for manifest_path in sorted(root.glob("*/manifest.yaml")):
        if not manifest_path.parent.name.isdigit():
            continue
        manifest = _load_reference_manifest_cached(manifest_path.as_posix())
        if manifest.pricing_year in pricing_years:
            raise ReferenceManifestError(
                "reference manifest validation failed:\n"
                f"- pricing_year: duplicate manifest for {manifest.pricing_year!r}"
            )
        pricing_years[manifest.pricing_year] = _pricing_year_nep_value(manifest)

    if not pricing_years:
        raise ReferenceManifestError(
            f"no reference-data manifests were found under {root.as_posix()}"
        )
    return dict(sorted(pricing_years.items()))


def _build_pricing_constant_source(
    manifest: ReferenceDataManifest,
    *,
    resource_url: str,
    artifact_url: str,
    notes: tuple[str, ...],
) -> PricingConstantSource:
    return PricingConstantSource(
        resource_url=resource_url,
        artifact_url=artifact_url,
        published_on=manifest.source_register.resource_page_published_on,
        last_updated_on=manifest.source_register.resource_page_last_updated_on,
        notes=notes,
    )


_NEP26_MANIFEST = _load_pricing_year_manifest("2026")

# NEP (National Efficient Price) per NWAU by pricing year.
NEP_BY_YEAR: Final[dict[str, int]] = _build_nep_by_year()
NEP26: Final[int] = NEP_BY_YEAR["2026"]
NEP26_SOURCE: Final[PricingConstantSource] = _build_pricing_constant_source(
    _NEP26_MANIFEST,
    resource_url=_NEP26_MANIFEST.source_register.resource_page_url,
    artifact_url=_NEP26_MANIFEST.source_register.resource_page_url,
    notes=(
        "Loaded from reference-data/2026/manifest.yaml.",
        "The resource page also links the official PDF and price-weight tables.",
    ),
)

NEC26_SOURCE: Final[PricingConstantSource] = PricingConstantSource(
    resource_url="https://www.ihacpa.gov.au/resources/national-efficient-cost-determination-2026-27",
    artifact_url="https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_cost_determination_2026-27.pdf",
    published_on=date(2026, 3, 11),
    last_updated_on=date(2026, 3, 13),
    notes=(
        "Headline NEC26 values are published as a fixed-plus-variable model.",
        "Fixed cost: $3.127m. Variable cost: $8,003.",
    ),
)

NEC26: Final[NecPricing] = NecPricing(
    fixed_cost_dollars=3_127_000,
    variable_cost_per_nwau=8_003,
    in_scope_hospitals=364,
    source=NEC26_SOURCE,
)

# NEC (National Efficient Cost) by pricing year.
NEC_BY_YEAR: Final[dict[str, NecPricing | None]] = {
    "2025": None,
    "2026": NEC26,
}


def get_nep(year: str) -> int | None:
    """Return the NEP price per NWAU for a pricing year, if available."""
    return NEP_BY_YEAR.get(year)


def get_nec(year: str) -> NecPricing | None:
    """Return the NEC headline components for a pricing year, if available."""
    return NEC_BY_YEAR.get(year)


def get_supported_pricing_years() -> list[str]:
    """Return supported pricing years in ascending order."""
    return sorted(NEP_BY_YEAR)
