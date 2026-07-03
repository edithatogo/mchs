"""Generated capability matrix for runtime truth across repo surfaces."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nwau_py.classification_validation import get_expected_classification_version
from nwau_py.reference_manifest import ReferenceDataManifest, load_reference_manifest

__all__ = [
    "CapabilityMatrixEntry",
    "build_capability_matrix",
    "capability_matrix_path",
    "format_capability_matrix_report",
    "load_capability_matrix",
]

_SCHEMA_VERSION = "1.0"
_REFERENCE_DATA_ROOT = "reference-data"
_CAPABILITY_MATRIX_RELATIVE_PATH = (
    Path("contracts/support") / "calculator-capability-matrix.json"
)
_SUPPORTED_YEARS = ("2025", "2026")
_STREAMS = (
    "acute",
    "ed",
    "mh",
    "community_mh",
    "subacute",
    "outpatients",
    "adjust",
)
_CLASSIFIERS = ("ar_drg", "aecc", "udg", "tier_2", "amhcc")
_SURFACES = ("library", "cli", "mcp", "http_api", "docs")
_CLASSIFIER_DISPLAY_NAMES = {
    "ar_drg": "AR-DRG",
    "aecc": "AECC",
    "udg": "UDG",
    "tier_2": "Tier 2",
    "amhcc": "AMHCC",
}
_SURFACE_STATUS = {
    "library": "executable",
    "cli": "executable",
    "mcp": "validated",
    "http_api": "out_of_scope",
    "docs": "source_available",
}
_STREAM_STATUS = {
    "acute": {"2025": "validated", "2026": "executable"},
    "community_mh": {"2025": "source_available", "2026": "source_available"},
}
_DEFAULT_STREAM_STATUS = "executable"
_CLASSIFIER_STATUS = {"ar_drg": "blocked_licensed"}
_DEFAULT_CLASSIFIER_STATUS = "executable"
_YEAR_NOTE_CURRENT = (
    "This is the current pricing year in the committed reference-data set."
)
_YEAR_NOTE_GAP = (
    "The manifest is source-backed but not yet a validated parity record."
)
_STREAM_NOTE_ACUTE = (
    "The acute 2025 path has local parity fixtures and validation coverage."
)
_STREAM_NOTE_COMMUNITY = (
    "Community mental health remains source-backed with explicit validation "
    "gaps."
)
_CLASSIFIER_NOTE_AR = (
    "Proprietary grouping logic is not redistributed; only metadata and "
    "integration hooks are tracked."
)
_SURFACE_NOTE_LIBRARY = (
    "Python calculator entry points execute the supported calculator surface."
)
_SURFACE_NOTE_CLI = (
    "The CLI delegates to the same calculator implementation as the library."
)
_SURFACE_NOTE_MCP = (
    "The MCP surface validates calculator requests and reports support status "
    "from the generated matrix."
)
_SURFACE_NOTE_DOCS = (
    "The public docs are generated from the committed capability matrix."
)
_CAPABILITY_MATRIX_EVIDENCE_SOURCE = (
    "contracts/support/calculator-capability-matrix.json"
)
_STATIC_NOTES = {
    "surface.mcp": (
        "The MCP tool validates requests and provenance but does not duplicate "
        "calculator formula execution."
    ),
    "surface.http_api": (
        "No HTTP API runtime is deployed in this repository; the contract-only "
        "surface remains out of scope."
    ),
}


@dataclass(frozen=True, slots=True)
class CapabilityMatrixEntry:
    """Immutable row in the generated capability matrix."""

    id: str
    dimension: str
    subject: str
    status: str
    evidence: dict[str, Any]
    notes: tuple[str, ...] = ()
    year: str | None = None
    version: str | None = None
    metadata: dict[str, Any] | None = None
    linked_track: str | None = None
    linked_issue_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable row."""
        payload: dict[str, Any] = {
            "id": self.id,
            "dimension": self.dimension,
            "subject": self.subject,
            "status": self.status,
            "evidence": self.evidence,
            "notes": list(self.notes),
        }
        if self.year is not None:
            payload["year"] = self.year
        if self.version is not None:
            payload["version"] = self.version
        if self.metadata is not None:
            payload["metadata"] = self.metadata
        if self.linked_track is not None:
            payload["linked_track"] = self.linked_track
        if self.linked_issue_url is not None:
            payload["linked_issue_url"] = self.linked_issue_url
        return payload


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def capability_matrix_path(repo_root: Path | str | None = None) -> Path:
    """Return the committed capability matrix path."""
    root = Path(repo_root) if repo_root is not None else _default_repo_root()
    return root / _CAPABILITY_MATRIX_RELATIVE_PATH


def _reference_manifest_path(repo_root: Path, year: str) -> Path:
    return repo_root / _REFERENCE_DATA_ROOT / year / "manifest.yaml"


def _load_reference_manifests(repo_root: Path) -> dict[str, ReferenceDataManifest]:
    manifests: dict[str, ReferenceDataManifest] = {}
    for year in _SUPPORTED_YEARS:
        manifest_path = _reference_manifest_path(repo_root, year)
        if manifest_path.is_file():
            manifests[year] = load_reference_manifest(manifest_path)
    return manifests


def _source_evidence(manifest: ReferenceDataManifest) -> dict[str, Any]:
    return {
        "source": manifest.canonical_path.as_posix(),
        "validation": manifest.validation_status,
        "source_only": manifest.validation.source_only,
        "parity_claim": manifest.validation.parity_claim,
    }


def _year_entry(manifest: ReferenceDataManifest) -> CapabilityMatrixEntry:
    status = (
        "validated"
        if manifest.validation_status == "validated"
        else "source_available"
    )
    constants = manifest.constants
    nep = constants.get("nep", {})
    nec = constants.get("nec")
    metadata = {
        "pricing_year": manifest.pricing_year,
        "financial_year": manifest.financial_year,
        "calculator": manifest.calculator,
        "current_pricing_year": manifest.current_pricing_year,
        "nep": None if not isinstance(nep, dict) else nep.get("value"),
        "nec": nec,
        "coding_sets": {
            item.name: {
                "version": item.version,
                "status": item.status,
            }
            for item in manifest.coding_sets
        },
        "validation_status": manifest.validation_status,
    }
    notes = [
        f"NEP{manifest.pricing_year[-2:]} comes from the reference-data manifest.",
    ]
    if manifest.current_pricing_year:
        notes.append(_YEAR_NOTE_CURRENT)
    if manifest.validation_status != "validated":
        notes.append(_YEAR_NOTE_GAP)
    return CapabilityMatrixEntry(
        id=f"year.{manifest.pricing_year}",
        dimension="year",
        subject=manifest.pricing_year,
        status=status,
        evidence=_source_evidence(manifest),
        notes=tuple(notes),
        year=manifest.pricing_year,
        metadata=metadata,
    )


def _stream_entry(
    year: str,
    stream: str,
    manifest: ReferenceDataManifest,
) -> CapabilityMatrixEntry:
    status = _STREAM_STATUS.get(stream, {}).get(year, _DEFAULT_STREAM_STATUS)
    notes = [
        f"Stream truth is generated from the {year} reference-data manifest.",
    ]
    if stream == "acute" and year == "2025":
        notes.append(_STREAM_NOTE_ACUTE)
    if stream == "community_mh":
        notes.append(_STREAM_NOTE_COMMUNITY)
    metadata: dict[str, Any] = {
        "year": year,
        "manifest_status": manifest.validation_status,
        "calculator": stream,
    }
    return CapabilityMatrixEntry(
        id=f"stream.{stream}.{year}",
        dimension="stream",
        subject=stream,
        status=status,
        evidence=_source_evidence(manifest),
        notes=tuple(notes),
        year=year,
        metadata=metadata,
        linked_track=(
            "ihacpa_calculator_surface_incorporation_20260703"
            if status == "source_available"
            else None
        ),
        linked_issue_url=(
            "https://github.com/edithatogo/mchs/issues/202"
            if status == "source_available"
            else None
        ),
    )


def _classifier_entry(
    year: str,
    classifier: str,
    manifest: ReferenceDataManifest,
) -> CapabilityMatrixEntry:
    status = _CLASSIFIER_STATUS.get(classifier, _DEFAULT_CLASSIFIER_STATUS)
    expected_version = get_expected_classification_version(classifier, year)
    version = next(
        (
            item.version
            for item in manifest.coding_sets
            if item.name == _CLASSIFIER_DISPLAY_NAMES[classifier]
        ),
        expected_version,
    )
    notes = [
        f"Classifier support is derived from the {year} reference-data manifest.",
    ]
    if classifier == "ar_drg":
        notes.append(_CLASSIFIER_NOTE_AR)
    metadata = {
        "year": year,
        "expected_version": expected_version,
        "manifest_version": version,
    }
    return CapabilityMatrixEntry(
        id=f"classifier.{classifier}.{year}",
        dimension="classifier",
        subject=classifier,
        status=status,
        evidence=_source_evidence(manifest),
        notes=tuple(notes),
        year=year,
        version=version,
        metadata=metadata,
        linked_track=(
            "ar_drg_grouper_provider_runtime_20260703"
            if classifier == "ar_drg"
            else None
        ),
        linked_issue_url=(
            "https://github.com/edithatogo/mchs/issues/206"
            if classifier == "ar_drg"
            else None
        ),
    )


def _surface_entry(
    surface: str,
    manifest: ReferenceDataManifest | None,
) -> CapabilityMatrixEntry:
    status = _SURFACE_STATUS[surface]
    notes = list(_STATIC_NOTES.get(f"surface.{surface}", ()))
    if surface == "library":
        notes.append(_SURFACE_NOTE_LIBRARY)
    if surface == "cli":
        notes.append(_SURFACE_NOTE_CLI)
    if surface == "mcp":
        notes.append(_SURFACE_NOTE_MCP)
    if surface == "docs":
        notes.append(_SURFACE_NOTE_DOCS)
    evidence = (
        {
            "source": _CAPABILITY_MATRIX_EVIDENCE_SOURCE,
            "validation": "generated",
        }
        if manifest is None
        else _source_evidence(manifest)
    )
    return CapabilityMatrixEntry(
        id=f"surface.{surface}",
        dimension="surface",
        subject=surface,
        status=status,
        evidence=evidence,
        notes=tuple(notes),
        metadata={"surface": surface},
        linked_track=(
            "ihacpa_capability_matrix_runtime_truth_20260703"
            if surface in {"mcp", "http_api", "docs"}
            else None
        ),
        linked_issue_url=(
            "https://github.com/edithatogo/mchs/issues/203"
            if surface in {"mcp", "http_api", "docs"}
            else None
        ),
    )


def build_capability_matrix(
    *,
    repo_root: Path | str | None = None,
) -> dict[str, Any]:
    """Build the generated capability matrix from repository-local sources."""
    root = Path(repo_root) if repo_root is not None else _default_repo_root()
    manifests = _load_reference_manifests(root)
    rows: list[CapabilityMatrixEntry] = []

    for year in _SUPPORTED_YEARS:
        manifest = manifests.get(year)
        if manifest is None:
            continue
        rows.append(_year_entry(manifest))
        rows.extend(_stream_entry(year, stream, manifest) for stream in _STREAMS)
        rows.extend(
            _classifier_entry(year, classifier, manifest)
            for classifier in _CLASSIFIERS
        )

    latest_manifest = manifests.get(max(manifests) if manifests else "2026")
    rows.extend(_surface_entry(surface, latest_manifest) for surface in _SURFACES)

    return {
        "schema_version": _SCHEMA_VERSION,
        "source_manifests": [
            _reference_manifest_path(root, year).relative_to(root).as_posix()
            for year in _SUPPORTED_YEARS
            if year in manifests
        ],
        "summary": {
            "total_rows": len(rows),
            "by_status": {
                status: sum(1 for row in rows if row.status == status)
                for status in (
                    "validated",
                    "executable",
                    "source_available",
                    "blocked_licensed",
                    "out_of_scope",
                )
            },
        },
        "rows": [row.to_dict() for row in rows],
    }


def load_capability_matrix(
    *,
    repo_root: Path | str | None = None,
) -> dict[str, Any]:
    """Load the committed capability matrix or generate it if missing."""
    path = capability_matrix_path(repo_root)
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return build_capability_matrix(repo_root=repo_root)


def format_capability_matrix_report(matrix: dict[str, Any]) -> str:
    """Return a compact human-readable summary for CLI output."""
    lines = [
        "Capability matrix",
        f"schema_version: {matrix['schema_version']}",
        f"source_manifests: {', '.join(matrix['source_manifests'])}",
        f"rows: {matrix['summary']['total_rows']}",
    ]
    for status, count in sorted(matrix["summary"]["by_status"].items()):
        lines.append(f"- {status}: {count}")
    return "\n".join(lines)
