"""Metadata-only abstraction doctrine registry and validation helpers.

The doctrine is intentionally strict:

- allowed architecture boundaries are declared as metadata, not inferred;
- direct dependencies and crosswalk assumptions are rejected unless the
  declared relationship is explicitly metadata-only; and
- the registry fails closed when a surface pair is not listed.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal, cast

AbstractionSurface = Literal[
    "formula",
    "parameter",
    "classifier",
    "fixture",
    "binding",
    "docs",
    "app",
    "release",
]
DependencyKind = Literal["metadata-only", "direct", "crosswalk"]

__all__ = [
    "ABSTRACTION_BOUNDARIES",
    "ABSTRACTION_BOUNDARY_INDEX",
    "ABSTRACTION_BOUNDARY_MATRIX",
    "ABSTRACTION_BOUNDARY_REGISTRY",
    "ABSTRACTION_DOCTRINE",
    "ABSTRACTION_DOCTRINE_BOUNDARIES",
    "ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS",
    "ABSTRACTION_SURFACES",
    "AbstractionBoundary",
    "AbstractionBoundaryError",
    "AbstractionDependency",
    "AbstractionDoctrine",
    "AbstractionSurface",
    "DependencyKind",
    "describe_abstraction_doctrine",
    "get_abstraction_boundary",
    "get_allowed_target_surfaces",
    "validate_abstraction_boundary",
    "validate_abstraction_dependencies",
    "validate_abstraction_dependency",
]

ABSTRACTION_SURFACES: tuple[AbstractionSurface, ...] = (
    "formula",
    "parameter",
    "classifier",
    "fixture",
    "binding",
    "docs",
    "app",
    "release",
)
ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS: tuple[str, ...] = (
    "direct-dependency",
    "crosswalk-assumption",
    "formula-duplication",
)
ABSTRACTION_BOUNDARY_MATRIX: dict[
    AbstractionSurface, tuple[AbstractionSurface, ...]
] = {
    "formula": ("parameter", "classifier", "fixture"),
    "parameter": ("formula", "classifier", "fixture"),
    "classifier": ("formula", "parameter", "fixture"),
    "fixture": ("formula", "parameter", "classifier"),
    "binding": ("formula", "parameter", "classifier", "fixture"),
    "docs": (
        "formula",
        "parameter",
        "classifier",
        "fixture",
        "binding",
        "app",
        "release",
    ),
    "app": ("formula", "parameter", "classifier", "fixture", "binding", "release"),
    "release": (
        "formula",
        "parameter",
        "classifier",
        "fixture",
        "binding",
        "docs",
        "app",
    ),
}


class AbstractionBoundaryError(ValueError):
    """Raised when a dependency violates the abstraction doctrine."""


@dataclass(frozen=True, slots=True)
class AbstractionBoundary:
    """A registered metadata-only relationship between two surfaces."""

    source_surface: AbstractionSurface
    target_surface: AbstractionSurface
    dependency_kind: DependencyKind = "metadata-only"
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_surface": self.source_surface,
            "target_surface": self.target_surface,
            "dependency_kind": self.dependency_kind,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class AbstractionDependency:
    """A declared relationship that can be validated against the doctrine."""

    source_surface: str
    target_surface: str
    dependency_kind: str = "metadata-only"
    declared_in: str | None = None
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_surface": self.source_surface,
            "target_surface": self.target_surface,
            "dependency_kind": self.dependency_kind,
            "declared_in": self.declared_in,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class AbstractionDoctrine:
    """Immutable registry of the repository's allowed surface boundaries."""

    surfaces: tuple[AbstractionSurface, ...]
    boundary_matrix: dict[AbstractionSurface, tuple[AbstractionSurface, ...]]
    boundaries: tuple[AbstractionBoundary, ...]
    forbidden_shortcuts: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "surfaces": list(self.surfaces),
            "boundary_matrix": {
                source: list(targets)
                for source, targets in self.boundary_matrix.items()
            },
            "boundaries": [boundary.to_dict() for boundary in self.boundaries],
            "forbidden_shortcuts": list(self.forbidden_shortcuts),
        }


_BOUNDARY_NOTES: dict[
    tuple[AbstractionSurface, AbstractionSurface], tuple[str, ...]
] = {
    ("formula", "parameter"): (
        "Formula kernels may consume parameter metadata only through explicit bundles.",
    ),
    ("formula", "classifier"): (
        "Formula kernels may reference classifier metadata but must not embed "
        "classifier logic.",
    ),
    ("formula", "fixture"): (
        "Fixtures may validate formula outputs, but they must not host formula code.",
    ),
    ("parameter", "formula"): (
        "Parameter bundles may point at formula metadata, but not carry "
        "executable formula logic.",
    ),
    ("parameter", "classifier"): (
        "Parameter bundles may declare classifier references as metadata only.",
    ),
    ("parameter", "fixture"): (
        "Parameter bundles may be evidenced by fixtures without importing "
        "fixture implementation details.",
    ),
    ("classifier", "formula"): (
        "Classifier metadata may annotate formula kernels, but must not "
        "reimplement them.",
    ),
    ("classifier", "parameter"): (
        "Classifier metadata may reference parameter bundles as declarative inputs.",
    ),
    ("classifier", "fixture"): (
        "Classifier registries may be exercised by fixtures without duplicating "
        "classifier logic.",
    ),
    ("fixture", "formula"): (
        "Fixtures may cite formulas for validation, but never carry formula "
        "implementation.",
    ),
    ("fixture", "parameter"): (
        "Fixtures may reference parameter bundles as evidence metadata only.",
    ),
    ("fixture", "classifier"): (
        "Fixtures may reference classifier metadata as evidence metadata only.",
    ),
    ("binding", "formula"): (
        "Bindings may call kernels, but they must not embed direct formula "
        "calculations.",
    ),
    ("binding", "parameter"): (
        "Bindings may transport parameter metadata as declared payloads only.",
    ),
    ("binding", "classifier"): (
        "Bindings may invoke classifier registries without duplicating "
        "classifier rules.",
    ),
    ("binding", "fixture"): (
        "Bindings may use fixtures for contract checks, not as a shortcut to "
        "runtime logic.",
    ),
    ("docs", "formula"): (
        "Documentation may describe formulas, but it must not embed executable "
        "formula logic.",
    ),
    ("docs", "parameter"): (
        "Documentation may point at parameter bundles as metadata references.",
    ),
    ("docs", "classifier"): (
        "Documentation may describe classifier registries without recreating "
        "classifier behavior.",
    ),
    ("docs", "fixture"): (
        "Documentation may link to fixtures as examples or proofs of boundary "
        "behavior.",
    ),
    ("docs", "binding"): (
        "Documentation may reference bindings as adapter surfaces, not as "
        "implementation copies.",
    ),
    ("docs", "app"): (
        "Documentation may reference app orchestration surfaces as metadata only.",
    ),
    ("docs", "release"): (
        "Documentation may reference release metadata, but not collapse release "
        "provenance into code.",
    ),
    ("app", "formula"): (
        "Apps may orchestrate formula kernels, but they must not duplicate "
        "formula logic.",
    ),
    ("app", "parameter"): (
        "Apps may route parameter bundles as metadata-only inputs.",
    ),
    ("app", "classifier"): (
        "Apps may invoke classifier metadata without embedding classifier rules.",
    ),
    ("app", "fixture"): (
        "Apps may use fixtures for smoke checks, not as a substitute for the "
        "kernel boundary.",
    ),
    ("app", "binding"): (
        "Apps may depend on binding adapters, but not on duplicated "
        "implementation logic.",
    ),
    ("app", "release"): ("Apps may read release metadata only as published context.",),
    ("release", "formula"): (
        "Release metadata may enumerate formula kernels, but it must not "
        "contain formula code.",
    ),
    ("release", "parameter"): (
        "Release metadata may enumerate parameter bundles as published artifacts.",
    ),
    ("release", "classifier"): (
        "Release metadata may enumerate classifier registries without "
        "reproducing their logic.",
    ),
    ("release", "fixture"): (
        "Release metadata may enumerate fixture packs as evidence artifacts.",
    ),
    ("release", "binding"): (
        "Release metadata may enumerate bindings as deliverables, not as "
        "inline implementation.",
    ),
    ("release", "docs"): (
        "Release metadata may enumerate documentation surfaces as published evidence.",
    ),
    ("release", "app"): (
        "Release metadata may enumerate app surfaces as published deliverables.",
    ),
}


def _normalize_surface(value: Any, *, field_name: str) -> AbstractionSurface:
    if not isinstance(value, str):
        raise AbstractionBoundaryError(f"{field_name} must be a string")
    normalized = value.strip().lower()
    if normalized != value:
        raise AbstractionBoundaryError(
            f"{field_name} must be a trimmed lowercase surface name"
        )
    if normalized not in ABSTRACTION_SURFACES:
        raise AbstractionBoundaryError(
            f"{field_name} must be one of {list(ABSTRACTION_SURFACES)}"
        )
    return cast(AbstractionSurface, normalized)


def _normalize_dependency_kind(value: Any) -> DependencyKind:
    if not isinstance(value, str):
        raise AbstractionBoundaryError("dependency_kind must be a string")
    normalized = value.strip().lower().replace("_", "-")
    if normalized in {"metadata-only", "metadata only", "metadata"}:
        return "metadata-only"
    if normalized in {"direct", "direct-dependency", "dependency"}:
        return "direct"
    if normalized in {"crosswalk", "crosswalk-assumption", "crosswalk assumption"}:
        return "crosswalk"
    raise AbstractionBoundaryError(
        "dependency_kind must be one of metadata-only, direct, or crosswalk"
    )


def _build_boundaries() -> tuple[AbstractionBoundary, ...]:
    boundaries: list[AbstractionBoundary] = []
    for source_surface, target_surfaces in ABSTRACTION_BOUNDARY_MATRIX.items():
        boundaries.extend(
            AbstractionBoundary(
                source_surface=source_surface,
                target_surface=target_surface,
                notes=_BOUNDARY_NOTES[(source_surface, target_surface)],
            )
            for target_surface in target_surfaces
        )
    return tuple(boundaries)


ABSTRACTION_BOUNDARY_REGISTRY: tuple[AbstractionBoundary, ...] = _build_boundaries()
ABSTRACTION_BOUNDARY_INDEX: dict[
    tuple[AbstractionSurface, AbstractionSurface], AbstractionBoundary
] = {
    (boundary.source_surface, boundary.target_surface): boundary
    for boundary in ABSTRACTION_BOUNDARY_REGISTRY
}
ABSTRACTION_BOUNDARIES = ABSTRACTION_BOUNDARY_REGISTRY
ABSTRACTION_DOCTRINE_BOUNDARIES = ABSTRACTION_BOUNDARY_REGISTRY
ABSTRACTION_DOCTRINE = AbstractionDoctrine(
    surfaces=ABSTRACTION_SURFACES,
    boundary_matrix=ABSTRACTION_BOUNDARY_MATRIX,
    boundaries=ABSTRACTION_BOUNDARY_REGISTRY,
    forbidden_shortcuts=ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS,
)


def _validate_registry() -> None:
    matrix_sources = set(ABSTRACTION_BOUNDARY_MATRIX)
    surface_set = set(ABSTRACTION_SURFACES)
    if matrix_sources != surface_set:
        raise AbstractionBoundaryError(
            "abstraction boundary matrix must declare every supported surface"
        )
    for source_surface, target_surfaces in ABSTRACTION_BOUNDARY_MATRIX.items():
        if source_surface in target_surfaces:
            raise AbstractionBoundaryError(
                f"{source_surface!r} must not depend on itself"
            )
        if len(target_surfaces) != len(set(target_surfaces)):
            raise AbstractionBoundaryError(
                f"{source_surface!r} must not declare duplicate target surfaces"
            )
        for target_surface in target_surfaces:
            if target_surface not in surface_set:
                raise AbstractionBoundaryError(
                    f"unknown target surface {target_surface!r} in doctrine matrix"
                )
            if (source_surface, target_surface) not in ABSTRACTION_BOUNDARY_INDEX:
                raise AbstractionBoundaryError(
                    "missing boundary record for "
                    f"{source_surface!r} -> {target_surface!r}"
                )


_validate_registry()


def get_allowed_target_surfaces(source_surface: str) -> tuple[AbstractionSurface, ...]:
    """Return the explicitly allowed target surfaces for a source surface."""
    source = _normalize_surface(source_surface, field_name="source_surface")
    return ABSTRACTION_BOUNDARY_MATRIX[source]


def get_abstraction_boundary(
    source_surface: str,
    target_surface: str,
) -> AbstractionBoundary:
    """Return the registered boundary for a surface pair."""
    source = _normalize_surface(source_surface, field_name="source_surface")
    target = _normalize_surface(target_surface, field_name="target_surface")
    try:
        return ABSTRACTION_BOUNDARY_INDEX[(source, target)]
    except KeyError as exc:
        raise AbstractionBoundaryError(
            f"no abstraction boundary is registered for {source!r} -> {target!r}"
        ) from exc


def validate_abstraction_boundary(
    source_surface: str,
    target_surface: str,
    *,
    dependency_kind: str = "metadata-only",
) -> AbstractionBoundary:
    """Validate a declared surface relationship against the registry.

    The check is fail-closed: unregistered edges, self-dependencies, direct
    dependencies, and crosswalk assumptions all raise.
    """
    kind = _normalize_dependency_kind(dependency_kind)
    if kind != "metadata-only":
        raise AbstractionBoundaryError(
            "direct dependencies and crosswalk assumptions are forbidden; "
            "declare metadata-only relationships instead"
        )
    boundary = get_abstraction_boundary(source_surface, target_surface)
    if boundary.dependency_kind != "metadata-only":
        raise AbstractionBoundaryError(
            f"boundary {boundary.source_surface!r} -> {boundary.target_surface!r} "
            "is not metadata-only"
        )
    return boundary


def _coerce_dependency(
    dependency: AbstractionDependency | Mapping[str, Any],
) -> AbstractionDependency:
    if isinstance(dependency, AbstractionDependency):
        return dependency
    if not isinstance(dependency, Mapping):
        raise AbstractionBoundaryError(
            "dependency must be an AbstractionDependency or a mapping"
        )
    try:
        source_surface = dependency["source_surface"]
        target_surface = dependency["target_surface"]
    except KeyError as exc:
        raise AbstractionBoundaryError(
            "dependency mapping must include source_surface and target_surface"
        ) from exc
    dependency_kind = dependency.get("dependency_kind", "metadata-only")
    declared_in = dependency.get("declared_in")
    notes = dependency.get("notes", ())
    if isinstance(notes, str):
        notes = (notes,)
    if isinstance(notes, list):
        notes = tuple(notes)
    if not isinstance(notes, tuple):
        raise AbstractionBoundaryError("dependency.notes must be a tuple or list")
    normalized_notes: list[str] = []
    for note in notes:
        if not isinstance(note, str) or not note.strip():
            raise AbstractionBoundaryError(
                "dependency.notes must contain non-empty strings"
            )
        normalized_notes.append(note)
    if declared_in is not None and (
        not isinstance(declared_in, str) or not declared_in.strip()
    ):
        raise AbstractionBoundaryError("declared_in must be a non-empty string")
    return AbstractionDependency(
        source_surface=str(source_surface),
        target_surface=str(target_surface),
        dependency_kind=str(dependency_kind),
        declared_in=declared_in,
        notes=tuple(normalized_notes),
    )


def validate_abstraction_dependency(
    dependency: AbstractionDependency | Mapping[str, Any],
) -> AbstractionBoundary:
    """Validate a single declared dependency.

    Any direct dependency or crosswalk assumption fails closed.
    """
    coerced = _coerce_dependency(dependency)
    boundary = validate_abstraction_boundary(
        coerced.source_surface,
        coerced.target_surface,
        dependency_kind=coerced.dependency_kind,
    )
    return boundary


def validate_abstraction_dependencies(
    dependencies: Iterable[AbstractionDependency | Mapping[str, Any]],
) -> tuple[AbstractionBoundary, ...]:
    """Validate a batch of dependencies against the doctrine."""
    return tuple(
        validate_abstraction_dependency(dependency) for dependency in dependencies
    )


def describe_abstraction_doctrine() -> dict[str, Any]:
    """Return a serializable description of the doctrine registry."""
    return {
        "surfaces": list(ABSTRACTION_DOCTRINE.surfaces),
        "boundary_matrix": {
            source: list(targets)
            for source, targets in ABSTRACTION_DOCTRINE.boundary_matrix.items()
        },
        "boundaries": [
            boundary.to_dict() for boundary in ABSTRACTION_BOUNDARY_REGISTRY
        ],
        "forbidden_shortcuts": list(ABSTRACTION_DOCTRINE_FORBIDDEN_SHORTCUTS),
    }
