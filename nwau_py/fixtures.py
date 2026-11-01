"""Shared loaders for self-describing golden fixture packs.

The fixture packs are intentionally runner-neutral: a JSON manifest describes
the calculator contract and points at small tabular payloads that can be read
by Python, C#, or web tooling without embedding harness-specific objects.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl

SUPPORTED_MANIFEST_SCHEMA_VERSION = "1.0"
SUPPORTED_PRIVACY_CLASSIFICATIONS = {"synthetic", "deidentified", "public"}
SUPPORTED_PAYLOAD_FORMATS = {"csv", "parquet"}
SUPPORTED_SERVICE_STREAMS = {
    "admitted acute",
    "subacute",
    "emergency department",
    "non-admitted",
    "mental health",
    "community mental health",
    "readmission",
}
SUPPORTED_SOURCE_BASIS_KINDS = {
    "synthetic_sample",
    "regression_sample",
    "derived_sample",
    "source_extract",
}
SUPPORTED_ROUNDING_POLICIES = {
    "compare exact decimal values after calculator output rounding",
}


class FixtureManifestError(ValueError):
    """Raised when a fixture manifest is missing required contract metadata."""


@dataclass(frozen=True, slots=True)
class FixtureTolerance:
    """Tolerance contract for fixture comparisons."""

    absolute: float
    relative: float


@dataclass(frozen=True, slots=True)
class FixtureSourceBasis:
    """Provenance metadata for a fixture pack."""

    kind: str
    description: str
    input_source: str
    expected_output_source: str


@dataclass(frozen=True, slots=True)
class FixturePayload:
    """Metadata for a single payload in the fixture pack."""

    role: str
    path: Path
    format: str
    row_count: int
    columns: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FixturePrecision:
    """Precision and rounding policy for a fixture pack."""

    rounding_policy: str
    tolerance: FixtureTolerance


@dataclass(frozen=True, slots=True)
class FixtureManifest:
    """Normalized, validated fixture manifest."""

    schema_version: str
    fixture_id: str
    calculator: str
    pricing_year: str
    service_stream: str
    cross_language_ready: bool
    privacy_classification: str
    source_basis: FixtureSourceBasis
    payloads: dict[str, FixturePayload]
    precision: FixturePrecision
    provenance: dict[str, Any]


@dataclass(frozen=True, slots=True)
class FixturePack:
    """Validated fixture pack with manifest and resolved payload paths."""

    manifest_path: Path
    pack_dir: Path
    manifest: FixtureManifest

    @property
    def input_payload(self) -> FixturePayload:
        return self.manifest.payloads["input"]

    @property
    def expected_output_payload(self) -> FixturePayload:
        return self.manifest.payloads["expected_output"]

    def payload_path(self, role: str) -> Path:
        return self.pack_dir / self.manifest.payloads[role].path


@dataclass(frozen=True, slots=True)
class FixtureCase:
    """A runnable fixture pack entry for a specific calculator."""

    pack: FixturePack
    calculator: Callable[..., Any]
    calculator_params: Any
    result_column: str
    parity_type: str = "output parity"

    @property
    def fixture_id(self) -> str:
        return self.pack.manifest.fixture_id

    @property
    def tolerance(self) -> FixtureTolerance:
        return self.pack.manifest.precision.tolerance

    @property
    def provenance_label(self) -> str:
        return (
            f"fixture={self.pack.manifest.fixture_id} "
            f"calculator={self.pack.manifest.calculator} "
            f"parity={self.parity_type}"
        )


@dataclass(frozen=True, slots=True)
class FixtureRunResult:
    """Executed fixture case with captured payloads."""

    case: FixtureCase
    result: Any
    expected: Any | None = None


@dataclass(frozen=True, slots=True)
class FixtureRunner:
    """Runner-neutral execution wrapper for a set of fixture cases."""

    execute_case: Callable[[FixtureCase], Any] | None = None

    def run_case(self, case: FixtureCase) -> FixtureRunResult:
        """Execute a single fixture case and wrap the result."""
        executor = self.execute_case or run_fixture_case
        return FixtureRunResult(case=case, result=executor(case))

    def run_cases(self, cases: Iterable[FixtureCase]) -> list[FixtureRunResult]:
        """Execute a batch of fixture cases in order."""
        return [self.run_case(case) for case in cases]


def _require_mapping(value: Any, *, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise FixtureManifestError(f"{field} must be a mapping")
    return value


def _require_str(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FixtureManifestError(f"{field} must be a non-empty string")
    return value


def _require_bool(value: Any, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise FixtureManifestError(f"{field} must be a boolean")
    return value


def _require_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise FixtureManifestError(f"{field} must be an integer")
    return value


def _require_float(value: Any, *, field: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise FixtureManifestError(f"{field} must be numeric")
    return float(value)


def _require_choice(
    value: Any,
    *,
    field: str,
    choices: set[str],
    message: str | None = None,
) -> str:
    value_str = _require_str(value, field=field)
    if value_str not in choices:
        if message is not None:
            raise FixtureManifestError(message)
        raise FixtureManifestError(f"{field} must be one of {sorted(choices)}")
    return value_str


def _parse_payload(role: str, payload: dict[str, Any]) -> FixturePayload:
    path = Path(_require_str(payload.get("path"), field=f"payloads.{role}.path"))
    format_ = _require_str(payload.get("format"), field=f"payloads.{role}.format")
    if format_ not in SUPPORTED_PAYLOAD_FORMATS:
        raise FixtureManifestError(
            f"payloads.{role}.format must be one of {sorted(SUPPORTED_PAYLOAD_FORMATS)}"
        )
    row_count = _require_int(
        payload.get("row_count"), field=f"payloads.{role}.row_count"
    )
    columns_raw = payload.get("columns")
    if not isinstance(columns_raw, list) or not all(
        isinstance(column, str) and column.strip() for column in columns_raw
    ):
        raise FixtureManifestError(f"payloads.{role}.columns must be a list of strings")
    return FixturePayload(
        role=role,
        path=path,
        format=format_,
        row_count=row_count,
        columns=tuple(columns_raw),
    )


def load_fixture_manifest(manifest_path: str | Path) -> FixtureManifest:
    """Load and validate a golden-fixture manifest."""
    path = Path(manifest_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    manifest = _require_mapping(payload, field="manifest")

    schema_version = _require_str(
        manifest.get("schema_version"), field="schema_version"
    )
    if schema_version != SUPPORTED_MANIFEST_SCHEMA_VERSION:
        raise FixtureManifestError(
            f"unsupported schema_version {schema_version!r}; "
            f"expected {SUPPORTED_MANIFEST_SCHEMA_VERSION!r}"
        )

    fixture_id = _require_str(manifest.get("fixture_id"), field="fixture_id")
    calculator = _require_str(manifest.get("calculator"), field="calculator")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", calculator):
        raise FixtureManifestError(
            "calculator identifier should be constrained to lowercase snake_case"
        )
    pricing_year = _require_str(manifest.get("pricing_year"), field="pricing_year")
    if not re.fullmatch(r"\d{4}", pricing_year):
        raise FixtureManifestError("pricing_year should remain a simple year label")
    service_stream = _require_choice(
        manifest.get("service_stream"),
        field="service_stream",
        choices=SUPPORTED_SERVICE_STREAMS,
        message="service_stream should be constrained",
    )
    cross_language_ready = _require_bool(
        manifest.get("cross_language_ready"), field="cross_language_ready"
    )
    if not cross_language_ready:
        raise FixtureManifestError("cross_language_ready must be true")
    privacy_classification = _require_str(
        manifest.get("privacy_classification"), field="privacy_classification"
    )
    if privacy_classification not in SUPPORTED_PRIVACY_CLASSIFICATIONS:
        raise FixtureManifestError(
            "privacy_classification must be one of "
            f"{sorted(SUPPORTED_PRIVACY_CLASSIFICATIONS)}"
        )

    source_basis_raw = _require_mapping(
        manifest.get("source_basis"), field="source_basis"
    )
    source_basis = FixtureSourceBasis(
        kind=_require_choice(
            source_basis_raw.get("kind"),
            field="source_basis.kind",
            choices=SUPPORTED_SOURCE_BASIS_KINDS,
            message="source_basis.kind should be constrained",
        ),
        description=_require_str(
            source_basis_raw.get("description"), field="source_basis.description"
        ),
        input_source=_require_str(
            source_basis_raw.get("input_source"), field="source_basis.input_source"
        ),
        expected_output_source=_require_str(
            source_basis_raw.get("expected_output_source"),
            field="source_basis.expected_output_source",
        ),
    )

    precision_raw = _require_mapping(manifest.get("precision"), field="precision")
    tolerance_raw = _require_mapping(
        precision_raw.get("tolerance"), field="precision.tolerance"
    )
    tolerance = FixtureTolerance(
        absolute=_require_float(
            tolerance_raw.get("absolute"), field="precision.tolerance.absolute"
        ),
        relative=_require_float(
            tolerance_raw.get("relative"), field="precision.tolerance.relative"
        ),
    )
    if tolerance.absolute < 0 or tolerance.relative < 0:
        raise FixtureManifestError("tolerances must be non-negative")
    precision = FixturePrecision(
        rounding_policy=_require_choice(
            precision_raw.get("rounding_policy"),
            field="precision.rounding_policy",
            choices=SUPPORTED_ROUNDING_POLICIES,
            message="rounding_policy should be constrained",
        ),
        tolerance=tolerance,
    )

    payloads_raw = _require_mapping(manifest.get("payloads"), field="payloads")
    payloads = {
        role: _parse_payload(role, _require_mapping(value, field=f"payloads.{role}"))
        for role, value in payloads_raw.items()
    }
    if "input" not in payloads or "expected_output" not in payloads:
        raise FixtureManifestError("payloads must include input and expected_output")

    provenance_raw = _require_mapping(manifest.get("provenance"), field="provenance")
    created_from = _require_str(
        provenance_raw.get("created_from"), field="provenance.created_from"
    )
    notes_raw = provenance_raw.get("notes")
    if not isinstance(notes_raw, list) or not notes_raw:
        raise FixtureManifestError("provenance.notes must be a non-empty list")
    if not all(isinstance(note, str) and note.strip() for note in notes_raw):
        raise FixtureManifestError(
            "provenance.notes must be a non-empty list of strings"
        )
    provenance = {
        "created_from": created_from,
        "notes": tuple(notes_raw),
    }

    return FixtureManifest(
        schema_version=schema_version,
        fixture_id=fixture_id,
        calculator=calculator,
        pricing_year=pricing_year,
        service_stream=service_stream,
        cross_language_ready=cross_language_ready,
        privacy_classification=privacy_classification,
        source_basis=source_basis,
        payloads=payloads,
        precision=precision,
        provenance=provenance,
    )


def load_fixture_pack(manifest_path: str | Path) -> FixturePack:
    """Load a fixture pack and resolve its payload paths."""
    manifest_path = Path(manifest_path)
    manifest = load_fixture_manifest(manifest_path)
    return FixturePack(
        manifest_path=manifest_path,
        pack_dir=manifest_path.parent,
        manifest=manifest,
    )


def _safe_load_fixture_pack(manifest_path: str | Path) -> FixturePack | None:
    try:
        return load_fixture_pack(manifest_path)
    except FixtureManifestError:
        return None


def discover_fixture_packs(root: str | Path) -> list[FixturePack]:
    """Return every validated fixture pack below ``root``."""
    root_path = Path(root)
    packs: list[FixturePack] = []
    if not root_path.exists():
        return packs
    for manifest_path in sorted(root_path.rglob("manifest.json")):
        pack = _safe_load_fixture_pack(manifest_path)
        if pack is not None:
            packs.append(pack)
    return packs


def iter_fixture_cases(
    packs: Iterable[FixturePack],
    *,
    calculator_map: dict[str, tuple[Callable[..., Any], Any, str]],
) -> list[FixtureCase]:
    """Return runnable fixture cases for the requested packs."""
    cases: list[FixtureCase] = []
    for pack in packs:
        manifest = pack.manifest
        if manifest.calculator not in calculator_map:
            continue
        calculator, params, result_column = calculator_map[manifest.calculator]
        cases.append(
            FixtureCase(
                pack=pack,
                calculator=calculator,
                calculator_params=params,
                result_column=result_column,
            )
        )
    return cases


def fixture_case_param_id(case: FixtureCase) -> str:
    """Return a stable pytest id for a fixture case."""
    return (
        f"{case.pack.manifest.fixture_id}"
        f"[{case.pack.manifest.calculator}]"
        f"/{case.result_column}"
        f"/{case.parity_type.replace(' ', '_')}"
    )


def fixture_case_params(cases: Iterable[FixtureCase]) -> list[Any]:
    """Return pytest parameter sets for fixture cases with stable ids.

    The pytest import is intentionally local so the helper remains usable in
    non-pytest runners.
    """
    import pytest

    return [pytest.param(case, id=fixture_case_param_id(case)) for case in cases]


def iter_fixture_pytest_params(
    cases: Iterable[FixtureCase],
) -> list[Any]:
    """Return pytest parameters for a fixture-case iterable."""
    import pytest

    return [pytest.param(case, id=case.fixture_id) for case in cases]


def iter_fixture_pytest_params_from_root(
    root: str | Path,
    *,
    calculator_map: dict[str, tuple[Callable[..., Any], Any, str]],
) -> list[Any]:
    """Return pytest parameters for every valid fixture pack under ``root``."""
    packs = discover_fixture_packs(root)
    cases = iter_fixture_cases(packs, calculator_map=calculator_map)
    return iter_fixture_pytest_params(cases)


def run_fixture_case(case: FixtureCase) -> Any:
    """Execute a fixture case and return the calculator output frame."""
    input_df = read_payload_frame(case.pack, "input")
    return case.calculator(
        input_df,
        case.calculator_params,
        year=case.pack.manifest.pricing_year,
    )


def run_fixture_suite(cases: Iterable[FixtureCase]) -> list[FixtureRunResult]:
    """Execute and validate a collection of fixture cases."""
    results: list[FixtureRunResult] = []
    for case in cases:
        result = run_fixture_case(case)
        expected = read_payload_frame(case.pack, "expected_output")
        assert_fixture_case_output(case, result, expected)
        results.append(
            FixtureRunResult(
                case=case,
                result=result,
                expected=expected,
            )
        )
    return results


def run_fixture_suite_from_root(
    root: str | Path,
    *,
    calculator_map: dict[str, tuple[Callable[..., Any], Any, str]],
) -> list[FixtureRunResult]:
    """Discover, materialize, and execute fixture cases from a fixture root."""
    packs = discover_fixture_packs(root)
    cases = iter_fixture_cases(packs, calculator_map=calculator_map)
    return run_fixture_suite(cases)


def assert_fixture_case_output(
    case: FixtureCase,
    result: Any,
    expected: Any,
) -> None:
    """Assert parity for a fixture case with manifest-backed provenance."""
    tolerance = case.tolerance
    result_cols = (
        result.columns
        if isinstance(result.columns, (list, tuple))
        else list(result.columns)
    )
    expected_cols = (
        expected.columns
        if isinstance(expected.columns, (list, tuple))
        else list(expected.columns)
    )
    if case.result_column not in result_cols:
        raise FixtureManifestError(
            f"{case.provenance_label} missing result column {case.result_column!r}"
        )
    if case.result_column not in expected_cols:
        raise FixtureManifestError(
            f"{case.provenance_label} missing expected column {case.result_column!r}"
        )
    actual = result[case.result_column]
    reference = expected[case.result_column]
    actual_arr = (
        actual.to_numpy() if hasattr(actual, "to_numpy") else np.asarray(actual)
    )
    reference_arr = (
        reference.to_numpy()
        if hasattr(reference, "to_numpy")
        else np.asarray(reference)
    )
    if len(actual_arr) != len(reference_arr):
        raise FixtureManifestError(
            f"{case.provenance_label} length mismatch: "
            f"{len(actual_arr)} != {len(reference_arr)}"
        )
    actual_float = np.asarray(actual_arr, dtype=float)
    reference_float = np.asarray(reference_arr, dtype=float)
    matched = np.isclose(
        actual_float,
        reference_float,
        rtol=tolerance.relative,
        atol=tolerance.absolute,
        equal_nan=True,
    )
    if not matched.all():
        first_bad = int(np.flatnonzero(~matched)[0])
        raise FixtureManifestError(
            f"{case.provenance_label} exceeded tolerance "
            f"at index {first_bad}: actual={actual_float[first_bad]!r} "
            f"expected={reference_float[first_bad]!r} "
            f"abs={tolerance.absolute} rel={tolerance.relative}"
        )


def read_payload_frame(pack: FixturePack, role: str) -> pl.DataFrame:
    """Read a payload frame from a validated fixture pack as native Polars."""
    payload = pack.manifest.payloads[role]
    path = pack.payload_path(role)
    if not path.exists():
        raise FixtureManifestError(f"missing payload file: {path}")
    if payload.format == "csv":
        frame = pl.read_csv(path)
    elif payload.format == "parquet":
        frame = pl.read_parquet(path)
    else:  # pragma: no cover - guarded by validation
        raise FixtureManifestError(f"unsupported payload format: {payload.format}")
    if list(frame.columns) != list(payload.columns):
        raise FixtureManifestError(
            f"{role} columns do not match manifest: {list(frame.columns)!r}"
        )
    if len(frame) != payload.row_count:
        raise FixtureManifestError(
            f"{role} row count {len(frame)} does not match manifest {payload.row_count}"
        )
    return frame
