"""Offline validation gates for IHACPA pricing-year evidence.

The helpers in this module stay conservative by design:

- they only inspect repository-local manifests and fixture packs;
- they do not call out to the network or infer official support status;
- they report gaps and evidence coverage instead of claiming endorsement.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nwau_py.bundles import BundleContractError, load_bundle_manifest
from nwau_py.fixtures import FixtureManifestError, load_fixture_manifest
from nwau_py.reference_manifest import ReferenceManifestError, load_reference_manifest

__all__ = [
    "PricingYearFixtureEvidence",
    "PricingYearValidationReport",
    "format_pricing_year_validation_report",
    "validate_pricing_year",
]

_REFERENCE_DATA_ROOT = "reference-data"
_FIXTURE_EVIDENCE_ROOTS = ("tests/fixtures/bundles", "tests/fixtures/golden")


@dataclass(frozen=True, slots=True)
class PricingYearFixtureEvidence:
    """Validated fixture-pack evidence for a pricing year."""

    pack_type: str
    manifest_path: Path
    fixture_id: str
    payload_paths: tuple[Path, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable evidence record."""
        return {
            "pack_type": self.pack_type,
            "manifest_path": self.manifest_path.as_posix(),
            "fixture_id": self.fixture_id,
            "payload_paths": [path.as_posix() for path in self.payload_paths],
        }


@dataclass(frozen=True, slots=True)
class PricingYearValidationReport:
    """Conservative offline validation result for a pricing year."""

    year: str
    repo_root: Path
    reference_manifest_path: Path
    reference_manifest_status: str
    reference_manifest_current_year: bool
    reference_manifest_parity_claim: bool
    reference_manifest_unresolved_gaps: tuple[str, ...]
    fixture_evidence: tuple[PricingYearFixtureEvidence, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]

    @property
    def passed(self) -> bool:
        """Return whether local evidence validation succeeded."""
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable validation report."""
        return {
            "pricing_year": self.year,
            "repo_root": self.repo_root.as_posix(),
            "reference_manifest_path": self.reference_manifest_path.as_posix(),
            "validation_status": self.reference_manifest_status,
            "current_pricing_year": self.reference_manifest_current_year,
            "parity_claim": self.reference_manifest_parity_claim,
            "unresolved_gaps": list(self.reference_manifest_unresolved_gaps),
            "fixture_evidence": [
                evidence.to_dict() for evidence in self.fixture_evidence
            ],
            "warnings": list(self.warnings),
            "errors": list(self.errors),
            "passed": self.passed,
            "support_claim": "not asserted",
        }


def _validate_year_label(year: str) -> str:
    if year.strip() != year:
        raise ValueError("year must not contain leading or trailing whitespace")
    if len(year) != 4 or not year.isdigit():
        raise ValueError("year must be a four-digit pricing-year label")
    return year


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _reference_manifest_path(repo_root: Path, year: str) -> Path:
    return repo_root / _REFERENCE_DATA_ROOT / year / "manifest.yaml"


def _iter_fixture_manifest_paths(repo_root: Path, year: str) -> list[tuple[str, Path]]:
    manifests: list[tuple[str, Path]] = []
    for pack_type, relative_root in (
        ("bundle", _FIXTURE_EVIDENCE_ROOTS[0]),
        ("golden", _FIXTURE_EVIDENCE_ROOTS[1]),
    ):
        root = repo_root / relative_root
        if not root.is_dir():
            continue
        manifests.extend(
            (pack_type, manifest_path)
            for manifest_path in sorted(root.glob(f"*_{year}/manifest.json"))
        )
    return manifests


def _load_fixture_evidence(
    pack_type: str,
    manifest_path: Path,
    year: str,
) -> PricingYearFixtureEvidence:
    if pack_type == "bundle":
        manifest = load_bundle_manifest(manifest_path)
        fixture_id = manifest.bundle_id
    else:
        manifest = load_fixture_manifest(manifest_path)
        fixture_id = manifest.fixture_id
    if manifest.pricing_year != year:
        raise FixtureManifestError(
            f"{manifest_path} declares pricing_year {manifest.pricing_year!r}, "
            f"expected {year!r}"
        )

    payload_paths = _validated_payload_paths(manifest_path, manifest.payloads)

    return PricingYearFixtureEvidence(
        pack_type=pack_type,
        manifest_path=manifest_path,
        fixture_id=fixture_id,
        payload_paths=tuple(payload_paths),
    )


def _validated_payload_paths(manifest_path: Path, payloads: Any) -> list[Path]:
    payload_paths: list[Path] = []
    for payload in payloads.values():
        payload_path = manifest_path.parent / payload.path
        if not payload_path.is_file():
            raise FixtureManifestError(
                f"{manifest_path} is missing declared payload {payload.path!r}"
            )
        payload_paths.append(payload_path)
    return payload_paths


def _try_load_fixture_evidence(
    pack_type: str,
    manifest_path: Path,
    year: str,
) -> tuple[PricingYearFixtureEvidence | None, str | None]:
    try:
        return _load_fixture_evidence(pack_type, manifest_path, year), None
    except (BundleContractError, FixtureManifestError, ValueError) as exc:
        return None, str(exc)


def validate_pricing_year(
    year: str,
    *,
    repo_root: Path | str | None = None,
) -> PricingYearValidationReport:
    """Validate local evidence for a pricing year without claiming support."""
    normalized_year = _validate_year_label(year)
    root = Path(repo_root) if repo_root is not None else _default_repo_root()

    errors: list[str] = []
    warnings: list[str] = []
    fixture_evidence: list[PricingYearFixtureEvidence] = []

    reference_manifest_path = _reference_manifest_path(root, normalized_year)
    if not reference_manifest_path.is_file():
        errors.append(
            f"missing reference-data manifest at {reference_manifest_path.as_posix()}"
        )
        reference_status = "missing"
        reference_current_year = False
        reference_parity_claim = False
        unresolved_gaps: tuple[str, ...] = ()
    else:
        try:
            manifest = load_reference_manifest(reference_manifest_path)
        except ReferenceManifestError as exc:
            errors.append(str(exc))
            reference_status = "invalid"
            reference_current_year = False
            reference_parity_claim = False
            unresolved_gaps = ()
        else:
            if manifest.pricing_year != normalized_year:
                errors.append(
                    "reference-data manifest pricing_year does not match the "
                    f"requested year {normalized_year!r}"
                )
            reference_status = manifest.validation_status
            reference_current_year = manifest.current_pricing_year
            reference_parity_claim = manifest.validation.parity_claim
            unresolved_gaps = tuple(gap.gap_id for gap in manifest.unresolved_gaps())
            warnings.extend(
                [
                    f"reference-data manifest status: {manifest.validation_status}",
                    f"reference-data parity claim: {manifest.validation.parity_claim}",
                    "reference-data current_pricing_year: "
                    f"{manifest.current_pricing_year}",
                ]
            )
            if unresolved_gaps:
                warnings.append(
                    "reference-data unresolved gaps: " + ", ".join(unresolved_gaps)
                )

    for pack_type, manifest_path in _iter_fixture_manifest_paths(root, normalized_year):
        evidence, error = _try_load_fixture_evidence(
            pack_type,
            manifest_path,
            normalized_year,
        )
        if evidence is not None:
            fixture_evidence.append(evidence)
        if error is not None:
            errors.append(error)

    if not fixture_evidence:
        errors.append(
            "missing fixture evidence under tests/fixtures/bundles or "
            "tests/fixtures/golden"
        )
    else:
        warnings.append(
            "fixture evidence: "
            + ", ".join(
                f"{evidence.pack_type}:{evidence.fixture_id}"
                for evidence in fixture_evidence
            )
        )

    return PricingYearValidationReport(
        year=normalized_year,
        repo_root=root,
        reference_manifest_path=reference_manifest_path,
        reference_manifest_status=reference_status,
        reference_manifest_current_year=reference_current_year,
        reference_manifest_parity_claim=reference_parity_claim,
        reference_manifest_unresolved_gaps=unresolved_gaps,
        fixture_evidence=tuple(fixture_evidence),
        warnings=tuple(warnings),
        errors=tuple(errors),
    )


def format_pricing_year_validation_report(report: PricingYearValidationReport) -> str:
    """Render a human-readable offline validation summary."""
    lines = [
        f"pricing year: {report.year}",
        f"repo root: {report.repo_root.as_posix()}",
        f"reference-data manifest: {report.reference_manifest_path.as_posix()}",
        f"reference-data status: {report.reference_manifest_status}",
        (
            "reference-data current_pricing_year: "
            f"{str(report.reference_manifest_current_year).lower()}"
        ),
        (
            "reference-data parity claim: "
            f"{str(report.reference_manifest_parity_claim).lower()}"
        ),
    ]

    if report.reference_manifest_unresolved_gaps:
        lines.append(
            "reference-data unresolved gaps: "
            + ", ".join(report.reference_manifest_unresolved_gaps)
        )
    else:
        lines.append("reference-data unresolved gaps: none")

    if report.fixture_evidence:
        lines.append(
            "fixture evidence packs: "
            + ", ".join(
                f"{evidence.pack_type}:{evidence.fixture_id}"
                for evidence in report.fixture_evidence
            )
        )
    else:
        lines.append("fixture evidence packs: none")

    if report.warnings:
        lines.append("notes:")
        lines.extend(f"- {warning}" for warning in report.warnings)

    if report.errors:
        lines.append("errors:")
        lines.extend(f"- {error}" for error in report.errors)

    lines.append("local validation gate: " + ("passed" if report.passed else "failed"))
    lines.append("support claim: not asserted")
    return "\n".join(lines)
