"""Versioned formula and parameter bundle contracts.

The bundle format is intentionally narrow and reviewable:

- a bundle carries explicit provenance and evidence references;
- weights, formulas, and adjustments are split into dedicated sections;
- validation remains strict and rejects unexpected fields;
- canonical JSON helpers keep bundle diffs stable across runs.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

__all__ = [
    "AdjustmentRecord",
    "BundleValidation",
    "FormulaParameterBundle",
    "FormulaRecord",
    "ParameterBundleError",
    "ResolvedFormulaParameterBundle",
    "SourceEvidence",
    "WeightRecord",
    "bundle_diff",
    "bundle_sha256",
    "bundle_to_canonical_dict",
    "bundle_to_canonical_json",
    "load_acute_2025_canary_bundle",
    "load_formula_parameter_bundle",
    "parameter_bundle_root",
    "resolve_formula_parameter_bundle",
]

SUPPORTED_SCHEMA_VERSION = "1.0"
SUPPORTED_STATUS = ("source-only", "schema-complete", "validated", "deprecated")
SUPPORTED_EVIDENCE_STATUS = ("captured", "linked", "synthetic")
_YEAR_RE = re.compile(r"^(?:201[3-9]|202[0-6])$")
_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_MANIFEST_NAME = "bundle.json"


class ParameterBundleError(ValueError):
    """Raised when a formula or parameter bundle violates the contract."""


JsonValue = str | int | float | bool | None


def _non_blank(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    if value.strip() != value or not value:
        raise ValueError(f"{field_name} must be a non-empty trimmed string")
    return value


def _year(value: Any) -> str:
    year = _non_blank(value, "pricing_year")
    if not _YEAR_RE.fullmatch(year):
        raise ValueError("pricing_year must be a supported four-digit label")
    return year


def _tuple_of_strings(value: Any, field_name: str) -> tuple[str, ...]:
    if isinstance(value, tuple):
        items = value
    elif isinstance(value, list):
        items = tuple(value)
    else:
        raise ValueError(f"{field_name} must be a list of strings")
    if not items:
        return ()
    return tuple(_non_blank(item, field_name) for item in items)


def _mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be a mapping")
    return value


class StrictModel(BaseModel):
    """Shared strict pydantic configuration for bundle models."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class SourceEvidence(StrictModel):
    """Source evidence or provenance reference for a bundle record."""

    evidence_id: str
    source_type: Literal[
        "official-page",
        "workbook",
        "table",
        "fixture",
        "archive",
        "synthetic",
    ]
    source_ref: str
    locator: str | None = None
    status: Literal["captured", "linked", "synthetic"]
    note: str

    @field_validator("evidence_id", "source_type", "source_ref", "status", "note")
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("locator")
    @classmethod
    def _validate_locator(cls, value: Any) -> str | None:
        if value is None:
            return None
        return _non_blank(value, "locator")


class BundleValidation(StrictModel):
    """Validation status and evidence notes for a bundle."""

    status: Literal["source-only", "schema-complete", "validated", "deprecated"]
    parity_claim: bool
    source_only: bool
    notes: tuple[str, ...] = Field(default_factory=tuple)

    @field_validator("notes", mode="before")
    @classmethod
    def _validate_notes(cls, value: Any) -> tuple[str, ...]:
        return _tuple_of_strings(value, "validation.notes")


class BundleProvenance(StrictModel):
    """Bundle generation provenance."""

    created_at: str
    created_by: str
    source_artifact_id: str
    source_evidence_ids: tuple[str, ...]
    notes: tuple[str, ...] = Field(default_factory=tuple)

    @field_validator(
        "created_at",
        "created_by",
        "source_artifact_id",
    )
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("source_evidence_ids", "notes", mode="before")
    @classmethod
    def _validate_tuple_fields(cls, value: Any, info: Any) -> tuple[str, ...]:
        return _tuple_of_strings(value, info.field_name)


class WeightRecord(StrictModel):
    """One weight row or parameter row in a bundle."""

    record_id: str
    label: str
    status: Literal["source-only", "synthetic", "validated"]
    source_evidence_ids: tuple[str, ...]
    parameters: dict[str, JsonValue]

    @field_validator("record_id", "label", "status")
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("source_evidence_ids", mode="before")
    @classmethod
    def _validate_source_ids(cls, value: Any) -> tuple[str, ...]:
        return _tuple_of_strings(value, "source_evidence_ids")

    @field_validator("parameters", mode="before")
    @classmethod
    def _validate_parameters(cls, value: Any) -> dict[str, JsonValue]:
        mapping = _mapping(value, "parameters")
        for key, item in mapping.items():
            _non_blank(key, "parameters key")
            if not isinstance(item, (str, int, float, bool)) and item is not None:
                raise ValueError(
                    "parameters must contain JSON-serializable scalar values"
                )
        return {
            key: item
            for key, item in mapping.items()
            if isinstance(item, (str, int, float, bool)) or item is None
        }


class FormulaRecord(StrictModel):
    """A versioned formula definition."""

    formula_id: str
    label: str
    target: str
    status: Literal["source-only", "synthetic", "validated"]
    source_evidence_ids: tuple[str, ...]
    variables: dict[str, str]
    steps: tuple[str, ...]
    expression: str

    @field_validator(
        "formula_id",
        "label",
        "target",
        "status",
        "expression",
    )
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("source_evidence_ids", "steps", mode="before")
    @classmethod
    def _validate_strings(cls, value: Any, info: Any) -> tuple[str, ...]:
        return _tuple_of_strings(value, info.field_name)

    @field_validator("variables", mode="before")
    @classmethod
    def _validate_variables(cls, value: Any) -> dict[str, str]:
        mapping = _mapping(value, "variables")
        for key, item in mapping.items():
            _non_blank(key, "variables key")
            _non_blank(item, f"variables.{key}")
        return {
            key: _non_blank(item, f"variables.{key}") for key, item in mapping.items()
        }


class AdjustmentRecord(StrictModel):
    """A named adjustment bundle row."""

    adjustment_id: str
    label: str
    kind: Literal["scalar-map", "additive", "multiplicative", "flag"]
    status: Literal["source-only", "synthetic", "validated"]
    source_evidence_ids: tuple[str, ...]
    parameters: dict[str, JsonValue]

    @field_validator(
        "adjustment_id",
        "label",
        "kind",
        "status",
    )
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        return _non_blank(value, info.field_name)

    @field_validator("source_evidence_ids", mode="before")
    @classmethod
    def _validate_source_ids(cls, value: Any) -> tuple[str, ...]:
        return _tuple_of_strings(value, "source_evidence_ids")

    @field_validator("parameters", mode="before")
    @classmethod
    def _validate_parameters(cls, value: Any) -> dict[str, JsonValue]:
        mapping = _mapping(value, "parameters")
        for key, item in mapping.items():
            _non_blank(key, "parameters key")
            if not isinstance(item, (str, int, float, bool)) and item is not None:
                raise ValueError(
                    "parameters must contain JSON-serializable scalar values"
                )
        return {
            key: item
            for key, item in mapping.items()
            if isinstance(item, (str, int, float, bool)) or item is None
        }


class FormulaParameterBundle(StrictModel):
    """Validated formula and parameter bundle manifest."""

    schema_version: str
    bundle_id: str
    bundle_version: str
    calculator: str
    pricing_year: str
    stream: str
    status: Literal["source-only", "schema-complete", "validated", "deprecated"]
    source_evidence: tuple[SourceEvidence, ...]
    provenance: BundleProvenance
    weights: tuple[WeightRecord, ...]
    formulas: tuple[FormulaRecord, ...]
    adjustments: tuple[AdjustmentRecord, ...]
    validation: BundleValidation

    @field_validator("schema_version")
    @classmethod
    def _validate_schema_version(cls, value: Any) -> str:
        schema_version = _non_blank(value, "schema_version")
        if schema_version != SUPPORTED_SCHEMA_VERSION:
            raise ValueError(
                f"unsupported schema_version {schema_version!r}; "
                f"expected {SUPPORTED_SCHEMA_VERSION!r}"
            )
        return schema_version

    @field_validator(
        "bundle_id",
        "bundle_version",
        "calculator",
        "pricing_year",
        "stream",
        "status",
    )
    @classmethod
    def _validate_text(cls, value: Any, info: Any) -> str:
        if info.field_name == "pricing_year":
            return _year(value)
        return _non_blank(value, info.field_name)

    @field_validator(
        "source_evidence",
        "weights",
        "formulas",
        "adjustments",
        mode="before",
    )
    @classmethod
    def _ensure_tuple(cls, value: Any, info: Any) -> tuple[Any, ...]:
        if not isinstance(value, (list, tuple)):
            raise ValueError(f"{info.field_name} must be a list")
        return tuple(value)

    @model_validator(mode="after")
    def _validate_cross_references(self) -> FormulaParameterBundle:
        evidence_ids = [item.evidence_id for item in self.source_evidence]
        duplicated_evidence = {
            evidence_id
            for evidence_id in evidence_ids
            if evidence_ids.count(evidence_id) > 1
        }
        if duplicated_evidence:
            raise ValueError(
                "source_evidence contains duplicate evidence_id values: "
                + ", ".join(sorted(duplicated_evidence))
            )

        def _validate_records(records: tuple[Any, ...], field_name: str) -> None:
            ids = [getattr(record, field_name) for record in records]
            duplicates = {item for item in ids if ids.count(item) > 1}
            if duplicates:
                raise ValueError(
                    f"{field_name}s contains duplicate {field_name} values: "
                    + ", ".join(sorted(duplicates))
                )

        _validate_records(self.weights, "record_id")
        _validate_records(self.formulas, "formula_id")
        _validate_records(self.adjustments, "adjustment_id")

        known_evidence = set(evidence_ids)
        referenced_evidence: set[str] = set(self.provenance.source_evidence_ids)
        for record in (*self.weights, *self.formulas, *self.adjustments):
            referenced_evidence.update(record.source_evidence_ids)

        missing = sorted(referenced_evidence - known_evidence)
        if missing:
            raise ValueError(
                "bundle references unknown evidence ids: " + ", ".join(missing)
            )

        if self.status != self.validation.status:
            raise ValueError("validation.status must match top-level status")
        if self.validation.source_only and self.status != "source-only":
            raise ValueError("source-only validations must use source-only status")
        return self

    def weights_frame(self) -> pd.DataFrame:
        """Return the weight section as a pandas dataframe."""
        return pd.DataFrame([record.parameters for record in self.weights])


@dataclass(frozen=True, slots=True)
class ResolvedFormulaParameterBundle:
    """Bundle manifest plus its on-disk location."""

    manifest_path: Path
    bundle_dir: Path
    bundle: FormulaParameterBundle

    def weights_frame(self) -> pd.DataFrame:
        return self.bundle.weights_frame()


def parameter_bundle_root(
    base_dir: Path | str | None = None,
    *,
    year: str,
    stream: str,
) -> Path:
    """Return the canonical root directory for a year/stream bundle set."""
    year = _year(year)
    stream = _non_blank(stream, "stream")
    base = Path(base_dir) if base_dir is not None else _REPO_ROOT
    return base / "reference-data" / year / "parameter-bundles" / stream


def _bundle_path(
    root: Path,
    *,
    bundle_id: str | None,
    bundle_version: str | None,
) -> Path:
    if bundle_id is not None and bundle_version is not None:
        return root / bundle_id / bundle_version / _DEFAULT_MANIFEST_NAME

    candidates = sorted(root.glob("*/*/" + _DEFAULT_MANIFEST_NAME))
    if not candidates:
        raise FileNotFoundError(f"no parameter bundle manifests found in {root}")
    if bundle_id is None and bundle_version is None and len(candidates) == 1:
        return candidates[0]
    if bundle_id is None:
        raise ValueError("bundle_id must be provided when multiple bundles exist")

    matching = [
        path
        for path in candidates
        if path.parent.parent.name == bundle_id
        and (bundle_version is None or path.parent.name == bundle_version)
    ]
    if not matching:
        raise FileNotFoundError(
            f"no parameter bundle found for bundle_id={bundle_id!r} "
            f"bundle_version={bundle_version!r}"
        )
    if len(matching) > 1:
        raise ValueError(
            "ambiguous parameter bundle selection; provide bundle_version explicitly"
        )
    return matching[0]


def load_formula_parameter_bundle(
    manifest_path: str | Path,
) -> ResolvedFormulaParameterBundle:
    """Load and validate a formula/parameter bundle manifest."""
    path = Path(manifest_path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - malformed file guard
        raise ParameterBundleError(
            f"failed to parse formula bundle manifest at {path}: {exc}"
        ) from exc
    if not isinstance(payload, dict):
        raise ParameterBundleError("formula bundle manifest must be a JSON object")
    try:
        bundle = FormulaParameterBundle.model_validate(payload)
    except ValidationError as exc:
        raise ParameterBundleError(str(exc)) from exc
    return ResolvedFormulaParameterBundle(
        manifest_path=path,
        bundle_dir=path.parent,
        bundle=bundle,
    )


def resolve_formula_parameter_bundle(
    base_dir: Path | str | None = None,
    *,
    year: str,
    stream: str,
    bundle_id: str | None = None,
    bundle_version: str | None = None,
) -> ResolvedFormulaParameterBundle:
    """Resolve a single bundle manifest from disk and validate it."""
    root = parameter_bundle_root(base_dir, year=year, stream=stream)
    path = _bundle_path(root, bundle_id=bundle_id, bundle_version=bundle_version)
    return load_formula_parameter_bundle(path)


def _canonical_payload(
    bundle: FormulaParameterBundle | ResolvedFormulaParameterBundle,
) -> dict[str, Any]:
    if isinstance(bundle, ResolvedFormulaParameterBundle):
        model = bundle.bundle
    else:
        model = bundle
    return model.model_dump(mode="json")


def bundle_to_canonical_dict(
    bundle: FormulaParameterBundle | ResolvedFormulaParameterBundle,
) -> dict[str, Any]:
    """Return a canonical JSON-friendly dictionary for a bundle."""
    return _canonical_payload(bundle)


def bundle_to_canonical_json(
    bundle: FormulaParameterBundle | ResolvedFormulaParameterBundle,
    *,
    indent: int = 2,
) -> str:
    """Return stable, sorted JSON for reviewable bundle diffs."""
    return json.dumps(
        _canonical_payload(bundle),
        sort_keys=True,
        indent=indent,
        ensure_ascii=True,
    )


def bundle_sha256(
    bundle: FormulaParameterBundle | ResolvedFormulaParameterBundle,
) -> str:
    """Return the sha256 digest of the canonical JSON representation."""
    payload = json.dumps(
        _canonical_payload(bundle),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def bundle_diff(
    left: FormulaParameterBundle | ResolvedFormulaParameterBundle,
    right: FormulaParameterBundle | ResolvedFormulaParameterBundle,
    *,
    from_name: str = "left",
    to_name: str = "right",
) -> str:
    """Return a unified diff for two canonical bundle serializations."""
    left_json = bundle_to_canonical_json(left).splitlines(keepends=True)
    right_json = bundle_to_canonical_json(right).splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            left_json,
            right_json,
            fromfile=from_name,
            tofile=to_name,
        )
    )


def load_acute_2025_canary_bundle(
    base_dir: Path | str | None = None,
) -> ResolvedFormulaParameterBundle:
    """Load the committed acute 2025 canary bundle."""
    path = (
        parameter_bundle_root(base_dir, year="2025", stream="acute")
        / "acute-2025-canary"
        / "v1"
        / _DEFAULT_MANIFEST_NAME
    )
    if not path.is_file():
        raise FileNotFoundError(f"acute 2025 canary bundle not found at {path}")
    return load_formula_parameter_bundle(path)
