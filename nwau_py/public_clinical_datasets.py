"""Public clinical dataset inventory for worked examples.

The records in this module are deliberately metadata-only. They describe
access, license, provenance, and suitability for tutorials, but they do not
download or bundle patient-level data.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal, cast

import pandas as pd
import yaml

__all__ = [
    "LocalCachePolicy",
    "MimicDemoWorkedExampleBundle",
    "PublicClinicalDatasetCandidate",
    "PublicDatasetCacheDiagnostic",
    "PublicDatasetClassificationError",
    "PublicDatasetExpectedFile",
    "PublicDatasetManifest",
    "PublicDatasetManifestError",
    "PublicDatasetPolicyError",
    "build_public_dataset_data_quality_report",
    "build_public_dataset_disclosure_risk_summary",
    "build_public_dataset_provenance_report",
    "diagnose_public_dataset_cache",
    "list_public_dataset_candidates",
    "load_public_dataset_manifest",
    "prepare_mimic_demo_calculator_input",
    "run_mimic_demo_worked_example",
    "scan_public_dataset_paths_for_restricted_assets",
    "select_initial_worked_example",
    "stage_mimic_demo_episodes",
]

InitialRole = Literal[
    "primary",
    "deferred-ed-track",
    "deferred-interop",
    "comparison-synthetic",
]


@dataclass(frozen=True, slots=True)
class PublicClinicalDatasetCandidate:
    """Metadata-only public dataset suitability record."""

    dataset_id: str
    name: str
    version: str
    url: str
    doi: str | None
    citation: str
    license_name: str
    access_policy: str
    required_credentials: str
    redistribution_rules: str
    download_path: str
    file_size: str
    update_cadence: str
    clinical_fields: tuple[str, ...]
    fit_for_nwau_examples: str
    initial_role: InitialRole
    committed_fixture_use: str
    local_download_use: str
    docs_use: str
    runtime_example_use: str
    pros: tuple[str, ...]
    cons: tuple[str, ...]
    risks: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable candidate record."""
        return asdict(self)


class PublicDatasetManifestError(ValueError):
    """Raised when a public dataset manifest is invalid."""


class PublicDatasetPolicyError(ValueError):
    """Raised when public dataset local-only policy is violated."""


class PublicDatasetClassificationError(ValueError):
    """Raised when calculator input lacks Australian classification provenance."""


@dataclass(frozen=True, slots=True)
class PublicDatasetExpectedFile:
    """Expected local file metadata from a public clinical dataset."""

    path: str
    table: str
    required: bool
    patient_level: bool
    description: str
    sha256: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable expected-file record."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class LocalCachePolicy:
    """Local-only cache policy for public clinical data."""

    cache_root_env: str
    allowed_roots: tuple[str, ...]
    raw_data_git_policy: str
    instructions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable cache policy."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PublicDatasetManifest:
    """Committed metadata manifest for a public clinical dataset."""

    dataset_id: str
    name: str
    version: str
    source_url: str
    doi: str | None
    citation: str
    license_name: str
    access_policy: str
    raw_data_git_policy: str
    local_cache_policy: LocalCachePolicy
    expected_files: tuple[PublicDatasetExpectedFile, ...]
    output_classes: Mapping[str, str]
    classification_boundary: Mapping[str, str]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable manifest record."""
        payload = asdict(self)
        payload["output_classes"] = dict(self.output_classes)
        payload["classification_boundary"] = dict(self.classification_boundary)
        return payload


@dataclass(frozen=True, slots=True)
class PublicDatasetCacheDiagnostic:
    """Diagnostic for a local public dataset cache."""

    dataset_id: str
    cache_root: str
    status: str
    present_files: tuple[str, ...]
    missing_files: tuple[str, ...]
    instructions: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable cache diagnostic."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class MimicDemoWorkedExampleBundle:
    """Outputs from the conservative MIMIC-IV Demo worked example."""

    staged: pd.DataFrame
    calculator_input: pd.DataFrame
    calculated: pd.DataFrame
    provenance_report: Mapping[str, object]
    data_quality_report: Mapping[str, object]
    disclosure_risk_summary: Mapping[str, object]
    support_status_summary: Mapping[str, object]
    surface_contract_report: Mapping[str, object]
    mcp_boundary_validation: Mapping[str, object]
    scenario_sensitivity_report: Sequence[Mapping[str, object]]
    written_files: Mapping[str, str]


def _require_mapping(value: object, *, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PublicDatasetManifestError(f"{field} must be a mapping")
    return cast(Mapping[str, Any], value)


def _require_sequence(value: object, *, field: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise PublicDatasetManifestError(f"{field} must be a sequence")
    return value


def _require_str(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise PublicDatasetManifestError(f"{field} must be a non-empty trimmed string")
    return value


def _optional_str(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return _require_str(value, field=field)


def _require_bool(value: object, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise PublicDatasetManifestError(f"{field} must be a boolean")
    return value


def _tuple_of_str(value: object, *, field: str) -> tuple[str, ...]:
    items = _require_sequence(value, field=field)
    return tuple(_require_str(item, field=field) for item in items)


def _expected_file_from_mapping(
    value: object,
    *,
    field: str,
) -> PublicDatasetExpectedFile:
    record = _require_mapping(value, field=field)
    return PublicDatasetExpectedFile(
        path=_require_str(record.get("path"), field=f"{field}.path"),
        table=_require_str(record.get("table"), field=f"{field}.table"),
        required=_require_bool(record.get("required"), field=f"{field}.required"),
        patient_level=_require_bool(
            record.get("patient_level"),
            field=f"{field}.patient_level",
        ),
        description=_require_str(
            record.get("description"),
            field=f"{field}.description",
        ),
        sha256=_optional_str(record.get("sha256"), field=f"{field}.sha256"),
    )


def load_public_dataset_manifest(path: str | Path) -> PublicDatasetManifest:
    """Load a committed public clinical dataset manifest."""
    manifest_path = Path(path)
    raw_payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    payload = _require_mapping(raw_payload, field="manifest")
    cache_policy = _require_mapping(
        payload.get("local_cache_policy"),
        field="local_cache_policy",
    )
    expected_files = tuple(
        _expected_file_from_mapping(item, field=f"expected_files[{index}]")
        for index, item in enumerate(
            _require_sequence(payload.get("expected_files"), field="expected_files")
        )
    )
    if not expected_files:
        raise PublicDatasetManifestError("expected_files must not be empty")
    return PublicDatasetManifest(
        dataset_id=_require_str(payload.get("dataset_id"), field="dataset_id"),
        name=_require_str(payload.get("name"), field="name"),
        version=_require_str(payload.get("version"), field="version"),
        source_url=_require_str(payload.get("source_url"), field="source_url"),
        doi=_optional_str(payload.get("doi"), field="doi"),
        citation=_require_str(payload.get("citation"), field="citation"),
        license_name=_require_str(payload.get("license_name"), field="license_name"),
        access_policy=_require_str(payload.get("access_policy"), field="access_policy"),
        raw_data_git_policy=_require_str(
            payload.get("raw_data_git_policy"),
            field="raw_data_git_policy",
        ),
        local_cache_policy=LocalCachePolicy(
            cache_root_env=_require_str(
                cache_policy.get("cache_root_env"),
                field="local_cache_policy.cache_root_env",
            ),
            allowed_roots=_tuple_of_str(
                cache_policy.get("allowed_roots"),
                field="local_cache_policy.allowed_roots",
            ),
            raw_data_git_policy=_require_str(
                cache_policy.get("raw_data_git_policy"),
                field="local_cache_policy.raw_data_git_policy",
            ),
            instructions=_tuple_of_str(
                cache_policy.get("instructions"),
                field="local_cache_policy.instructions",
            ),
        ),
        expected_files=expected_files,
        output_classes=dict(
            _require_mapping(payload.get("output_classes"), field="output_classes")
        ),
        classification_boundary=dict(
            _require_mapping(
                payload.get("classification_boundary"),
                field="classification_boundary",
            )
        ),
    )


def scan_public_dataset_paths_for_restricted_assets(
    paths: Iterable[str | Path],
) -> list[str]:
    """Fail closed when raw public clinical dataset files are in commit paths."""
    restricted: list[str] = []
    restricted_markers = (
        "reference-data/public-datasets/mimic-iv-demo/raw/",
        "reference-data/public-datasets/mimic-iv-demo/cache/",
        "reference-data/public-datasets/mimic-iv-demo/local/",
        "examples/mimic_demo/local-data/",
        "examples/mimic_demo/output/local-real-data/",
    )
    restricted_suffixes = (
        ".csv",
        ".csv.gz",
        ".parquet",
        ".ndjson",
        ".ndjson.gz",
        ".json.gz",
    )
    for path in paths:
        normalized = Path(path).as_posix()
        has_marker = any(marker in normalized for marker in restricted_markers)
        if has_marker and normalized.endswith(restricted_suffixes):
            restricted.append(normalized)
    if restricted:
        raise PublicDatasetPolicyError(
            "raw public clinical dataset files must remain local-only: "
            + ", ".join(restricted)
        )
    return []


def diagnose_public_dataset_cache(
    manifest: PublicDatasetManifest,
    cache_root: str | Path,
) -> PublicDatasetCacheDiagnostic:
    """Return present/missing expected file diagnostics for a local cache."""
    root = Path(cache_root)
    present: list[str] = []
    missing: list[str] = []
    for expected in manifest.expected_files:
        destination = root / expected.path
        if destination.exists():
            present.append(expected.path)
        elif expected.required:
            missing.append(expected.path)
    status = "ready" if not missing else "missing-files"
    return PublicDatasetCacheDiagnostic(
        dataset_id=manifest.dataset_id,
        cache_root=str(root),
        status=status,
        present_files=tuple(present),
        missing_files=tuple(missing),
        instructions=manifest.local_cache_policy.instructions,
    )


def build_public_dataset_provenance_report(
    manifest: PublicDatasetManifest,
    *,
    local_files: Iterable[str],
    derivation_steps: Iterable[str],
    overlay_status: str,
    support_state: str,
) -> dict[str, object]:
    """Build a provenance report for a public dataset example run."""
    return {
        "dataset_id": manifest.dataset_id,
        "dataset_name": manifest.name,
        "version": manifest.version,
        "source_url": manifest.source_url,
        "doi": manifest.doi,
        "license": manifest.license_name,
        "local_files": list(local_files),
        "derivation_steps": list(derivation_steps),
        "overlay_status": overlay_status,
        "classification_boundary": {
            "support_state": support_state,
            "australian_ar_drg_required": True,
            "message": manifest.classification_boundary.get("message", ""),
        },
    }


def _non_empty_string_mask(series: pd.Series) -> pd.Series:
    return series.fillna("").astype(str).str.strip().ne("")


def build_public_dataset_data_quality_report(df: pd.DataFrame) -> dict[str, object]:
    """Summarize data quality for a staged public dataset frame."""
    required = ("episode_id", "subject_id", "hadm_id", "los_days", "icu_hours")
    missing_required = [column for column in required if column not in df.columns]
    duplicate_episode_ids = (
        int(df["episode_id"].duplicated().sum()) if "episode_id" in df.columns else 0
    )
    negative_los_rows = int((df.get("los_days", pd.Series(dtype=float)) < 0).sum())
    icu_rows = int((df.get("icu_hours", pd.Series(dtype=float)) > 0).sum())
    if "australian_ar_drg" in df.columns and _non_empty_string_mask(
        df["australian_ar_drg"]
    ).any():
        provenance_state = "present"
    elif "synthetic_ar_drg" in df.columns and _non_empty_string_mask(
        df["synthetic_ar_drg"]
    ).any():
        provenance_state = "synthetic-overlay"
    else:
        provenance_state = "missing"
    return {
        "row_count": len(df),
        "missing_required_fields": missing_required,
        "duplicate_episode_ids": duplicate_episode_ids,
        "negative_los_rows": negative_los_rows,
        "icu_rows": icu_rows,
        "icu_coverage_ratio": 0.0 if len(df) == 0 else icu_rows / len(df),
        "classification_provenance_state": provenance_state,
    }


def build_public_dataset_disclosure_risk_summary(
    df: pd.DataFrame,
) -> dict[str, object]:
    """Classify whether a derived output is safe to commit."""
    risk_reasons: list[str] = []
    if len(df) < 10:
        risk_reasons.append("small cell count below commit-safe threshold")
    identifier_columns = {"subject_id", "hadm_id", "stay_id"}
    if identifier_columns.intersection(df.columns):
        risk_reasons.append("direct subject, admission IDs, or stay identifiers")
    date_columns = [
        column for column in df.columns if "time" in column or "date" in column
    ]
    if date_columns:
        risk_reasons.append("date/time columns derived from public patient records")
    joined_clinical = {"mimic_drg_code", "diagnosis_codes", "procedure_codes"}
    if joined_clinical.intersection(df.columns):
        risk_reasons.append("joined clinical classification features")
    return {
        "row_count": len(df),
        "commit_safe": not risk_reasons,
        "safe_output_class": "commit-safe" if not risk_reasons else "local-only",
        "risk_reasons": risk_reasons,
    }


def _read_mimic_table(root: str | Path, filename: str, subdir: str) -> pd.DataFrame:
    base = Path(root)
    candidates = (
        base / filename,
        base / f"{filename}.gz",
        base / subdir / filename,
        base / subdir / f"{filename}.gz",
    )
    for candidate in candidates:
        if candidate.exists():
            return pd.read_csv(
                candidate,
                dtype={
                    "drg_code": "string",
                    "icd_code": "string",
                },
            )
    raise FileNotFoundError(
        f"missing MIMIC demo table {filename!r}; searched "
        + ", ".join(path.as_posix() for path in candidates)
    )


def _join_codes(frame: pd.DataFrame, *, value_column: str = "icd_code") -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["hadm_id", value_column])
    ordered = frame.sort_values(["hadm_id", "seq_num"])
    return (
        ordered.groupby("hadm_id", as_index=False)[value_column]
        .agg(lambda values: ";".join(values.astype(str)))
        .rename(columns={value_column: f"{value_column}s"})
    )


def _aggregate_icu_hours(icustays: pd.DataFrame) -> pd.DataFrame:
    if icustays.empty:
        return pd.DataFrame({"hadm_id": [], "icu_hours": []})
    if "los" in icustays.columns:
        working = icustays.assign(icu_hours=icustays["los"].astype(float) * 24.0)
    else:
        intime = pd.to_datetime(icustays["intime"])
        outtime = pd.to_datetime(icustays["outtime"])
        working = icustays.assign(
            icu_hours=(outtime - intime).dt.total_seconds() / 3600.0
        )
    return working.groupby("hadm_id", as_index=False)["icu_hours"].sum()


def stage_mimic_demo_episodes(root: str | Path) -> pd.DataFrame:
    """Stage episode-level facts from local MIMIC-IV Demo-shaped CSV files."""
    admissions = _read_mimic_table(root, "admissions.csv", "hosp").reset_index()
    diagnoses = _read_mimic_table(root, "diagnoses_icd.csv", "hosp")
    procedures = _read_mimic_table(root, "procedures_icd.csv", "hosp")
    drgcodes = _read_mimic_table(root, "drgcodes.csv", "hosp")
    icustays = _read_mimic_table(root, "icustays.csv", "icu")

    staged = admissions.rename(columns={"index": "admissions_row_id"}).copy()
    staged["admittime"] = pd.to_datetime(staged["admittime"])
    staged["dischtime"] = pd.to_datetime(staged["dischtime"])
    staged["episode_id"] = (
        "mimic-"
        + staged["subject_id"].astype(str)
        + "-"
        + staged["hadm_id"].astype(str)
    )
    staged["los_days"] = (
        (staged["dischtime"] - staged["admittime"]).dt.total_seconds() / 86_400.0
    )

    icu_hours = _aggregate_icu_hours(icustays)
    diagnosis_codes = _join_codes(diagnoses).rename(
        columns={"icd_codes": "diagnosis_codes"}
    )
    procedure_codes = _join_codes(procedures).rename(
        columns={"icd_codes": "procedure_codes"}
    )
    drg_first = (
        drgcodes.sort_values(["hadm_id", "drg_code"])
        .groupby("hadm_id", as_index=False)
        .first()[["hadm_id", "drg_code"]]
        .rename(columns={"drg_code": "mimic_drg_code"})
    )

    staged = staged.merge(icu_hours, on="hadm_id", how="left")
    staged = staged.merge(diagnosis_codes, on="hadm_id", how="left")
    staged = staged.merge(procedure_codes, on="hadm_id", how="left")
    staged = staged.merge(drg_first, on="hadm_id", how="left")
    staged["icu_hours"] = staged["icu_hours"].fillna(0.0)
    staged["diagnosis_codes"] = staged["diagnosis_codes"].fillna("")
    staged["procedure_codes"] = staged["procedure_codes"].fillna("")
    staged["mimic_drg_code"] = staged["mimic_drg_code"].fillna("")
    staged["australian_ar_drg"] = ""
    staged["classification_provenance"] = "missing"
    staged["lineage_source_files"] = (
        "hosp/admissions.csv;hosp/diagnoses_icd.csv;hosp/procedures_icd.csv;"
        "hosp/drgcodes.csv;icu/icustays.csv"
    )
    staged["lineage_row_ids"] = "admissions:" + staged["admissions_row_id"].astype(str)

    columns = [
        "episode_id",
        "subject_id",
        "hadm_id",
        "admittime",
        "dischtime",
        "admission_type",
        "los_days",
        "icu_hours",
        "mimic_drg_code",
        "diagnosis_codes",
        "procedure_codes",
        "australian_ar_drg",
        "classification_provenance",
        "lineage_source_files",
        "lineage_row_ids",
    ]
    return staged[columns].reset_index(drop=True)


def _has_australian_ar_drg(frame: pd.DataFrame) -> pd.Series:
    if "australian_ar_drg" not in frame.columns:
        return pd.Series(False, index=frame.index)
    return _non_empty_string_mask(frame["australian_ar_drg"])


def prepare_mimic_demo_calculator_input(
    staged: pd.DataFrame,
    *,
    synthetic_overlay_path: str | Path | None = None,
    local_ar_drg_path: str | Path | None = None,
    allow_synthetic_overlay: bool = False,
) -> pd.DataFrame:
    """Prepare acute calculator input from staged MIMIC Demo episodes.

    The function fails closed unless Australian AR-DRG provenance is already
    present or an explicitly allowed synthetic overlay is supplied.
    """
    working = staged.copy()
    if synthetic_overlay_path is not None and local_ar_drg_path is not None:
        raise PublicDatasetClassificationError(
            "provide either a synthetic overlay or a local precomputed AR-DRG "
            "overlay, not both"
        )

    if not _has_australian_ar_drg(working).all():
        if local_ar_drg_path is not None:
            overlay = pd.read_csv(
                local_ar_drg_path,
                dtype={
                    "episode_id": "string",
                    "australian_ar_drg": "string",
                    "classification_provenance": "string",
                },
            )
            required_overlay_columns = {
                "episode_id",
                "australian_ar_drg",
                "classification_provenance",
            }
            missing = required_overlay_columns.difference(overlay.columns)
            if missing:
                raise PublicDatasetClassificationError(
                    "local AR-DRG overlay is missing required columns: "
                    + ", ".join(sorted(missing))
                )
            working = working.drop(
                columns=[
                    "australian_ar_drg",
                    "classification_provenance",
                    "classification_provenance_detail",
                    "overlay_is_synthetic",
                ],
                errors="ignore",
            ).merge(
                overlay[
                    [
                        "episode_id",
                        "australian_ar_drg",
                        "classification_provenance",
                    ]
                ],
                on="episode_id",
                how="left",
            )
            if not _has_australian_ar_drg(working).all():
                raise PublicDatasetClassificationError(
                    "local AR-DRG overlay does not cover every staged episode"
                )
            if not _non_empty_string_mask(working["classification_provenance"]).all():
                raise PublicDatasetClassificationError(
                    "local AR-DRG overlay must include classification provenance "
                    "for every staged episode"
                )
            working["classification_provenance_detail"] = (
                "local precomputed Australian AR-DRG; source stays local-only"
            )
            working["overlay_is_synthetic"] = False
        elif synthetic_overlay_path is None:
            raise PublicDatasetClassificationError(
                "Australian AR-DRG provenance is required before MIMIC-derived "
                "episodes can be converted to calculator input."
            )
        elif not allow_synthetic_overlay:
            raise PublicDatasetClassificationError(
                "Synthetic overlay use must be explicitly enabled for runnable "
                "documentation examples."
            )
        else:
            overlay = pd.read_csv(
                synthetic_overlay_path,
                dtype={"episode_id": "string", "australian_ar_drg": "string"},
            )
            required_overlay_columns = {"episode_id", "australian_ar_drg"}
            missing = required_overlay_columns.difference(overlay.columns)
            if missing:
                raise PublicDatasetClassificationError(
                    "synthetic overlay is missing required columns: "
                    + ", ".join(sorted(missing))
                )
            working = working.drop(
                columns=[
                    "australian_ar_drg",
                    "classification_provenance",
                    "classification_provenance_detail",
                    "overlay_is_synthetic",
                ],
                errors="ignore",
            ).merge(
                overlay[["episode_id", "australian_ar_drg"]],
                on="episode_id",
                how="left",
            )
            if not _has_australian_ar_drg(working).all():
                raise PublicDatasetClassificationError(
                    "synthetic overlay does not cover every staged episode"
                )
            working["classification_provenance"] = "synthetic_demo_overlay"
            working["classification_provenance_detail"] = (
                "synthetic Australian AR-DRG overlay for documentation only"
            )
            working["overlay_is_synthetic"] = True
    elif (
        "classification_provenance" not in working.columns
        or not _non_empty_string_mask(working["classification_provenance"]).all()
        or working["classification_provenance"]
        .astype(str)
        .str.strip()
        .eq("missing")
        .any()
    ):
        raise PublicDatasetClassificationError(
            "Australian AR-DRG provenance detail is required for every staged episode"
        )
    elif "classification_provenance_detail" not in working.columns:
        working["classification_provenance_detail"] = (
            "local precomputed Australian AR-DRG"
        )
    if "overlay_is_synthetic" not in working.columns:
        working["overlay_is_synthetic"] = False

    output = pd.DataFrame(
        {
            "episode_id": working["episode_id"],
            "DRG": working["australian_ar_drg"].astype(str),
            "LOS": working["los_days"].astype(float),
            "ICU_HOURS": working["icu_hours"].astype(float),
            "ICU_OTHER": 0,
            "PAT_SAMEDAY_FLAG": (working["los_days"].astype(float) < 1.0).astype(int),
            "PAT_PRIVATE_FLAG": 0,
            "classification_provenance": working["classification_provenance"].astype(
                str
            ),
            "classification_provenance_detail": working[
                "classification_provenance_detail"
            ].astype(str),
            "overlay_is_synthetic": working["overlay_is_synthetic"].astype(bool),
            "source_dataset_id": "mimic-iv-demo-2.2",
        }
    )
    return output


def _clean_acute_weights(path: str | Path) -> pd.DataFrame:
    weights = pd.read_csv(path)
    weights["DRG"] = weights["DRG"].astype(str).str.strip("b'")
    return weights


def _mcp_boundary_validation(
    calculator_input: pd.DataFrame,
    *,
    year: str,
) -> dict[str, object]:
    from nwau_py import mcp_server

    row_payload = (
        calculator_input.iloc[0].to_dict() if not calculator_input.empty else {}
    )
    validation = mcp_server.validate_input(
        {
            "calculatorId": "acute",
            "year": year,
            "inputs": row_payload,
        }
    )
    calculation_boundary = mcp_server.calculate(
        {
            "calculatorId": "acute",
            "year": year,
            "inputs": row_payload,
        }
    )
    return {
        "validation": validation,
        "calculation_boundary": calculation_boundary,
        "runtime_formula_execution": "not_claimed",
    }


def _build_mimic_demo_support_status_summary(
    *,
    mcp_boundary_validation: Mapping[str, object],
) -> dict[str, object]:
    return {
        "source_available": [
            "mimic_iv_demo_manifest",
            "mimic_shaped_synthetic_fixtures",
        ],
        "executable": [
            "mimic_demo_staging",
            "synthetic_overlay_calculator_input_preparation",
            "local_file_output_bundle",
        ],
        "validated": [
            "python_api_acute_runtime_with_fixture_weights",
        ],
        "blocked_licensed": [
            "authoritative_australian_ar_drg_from_mimic_alone",
        ],
        "out_of_scope": [
            "us_drg_or_icd_mapping_to_australian_classifications_as_validated_truth",
        ],
        "mcp_boundary": mcp_boundary_validation,
        "api_openai_contracts": {
            "http_api": "contracts/http-api/openapi.yaml",
            "openai_adapter": "contracts/openai-adapter/tool-definitions.md",
            "formula_execution_claim": "not_claimed_for_public_dataset_example",
        },
    }


def _build_mimic_demo_surface_contract_report(
    *,
    mcp_boundary_validation: Mapping[str, object],
) -> dict[str, object]:
    return {
        "python_api": {
            "status": "validated",
            "entrypoint": (
                "nwau_py.public_clinical_datasets.run_mimic_demo_worked_example"
            ),
        },
        "cli_file_interop": {
            "status": "contract_documented",
            "contract_path": "contracts/interop/cli-file-interop.contract.json",
            "prepared_input": "calculator_input.csv",
            "runtime_note": (
                "The prepared CSV uses the existing acute input columns; CLI "
                "execution still requires user-supplied reference assets."
            ),
        },
        "mcp": {
            "status": "boundary_validated",
            "runtime_formula_execution": "not_claimed",
            "validation": mcp_boundary_validation["validation"],
            "calculation_boundary": mcp_boundary_validation["calculation_boundary"],
        },
        "http_api": {
            "status": "documented_contract_only",
            "contract_path": "contracts/http-api/openapi.yaml",
        },
        "openai_adapter": {
            "status": "documented_contract_only",
            "contract_path": "contracts/openai-adapter/tool-definitions.md",
        },
    }


def _build_mimic_demo_scenario_sensitivity_report(
    *,
    fail_closed_error: str,
    calculated: pd.DataFrame,
    local_precomputed_calculated: pd.DataFrame | None = None,
    year: str,
) -> list[dict[str, object]]:
    nwau_column = f"NWAU{str(year)[-2:]}"
    total_nwau = (
        float(calculated[nwau_column].sum())
        if nwau_column in calculated.columns
        else None
    )
    scenarios: list[dict[str, object]] = [
        {
            "scenario": "missing_australian_ar_drg",
            "status": "blocked_licensed",
            "message": fail_closed_error,
            "authoritative_australian_output": False,
        },
        {
            "scenario": "synthetic_overlay",
            "status": "executable_non_authoritative",
            "row_count": len(calculated),
            "nwau_column": nwau_column,
            "total_nwau": total_nwau,
            "authoritative_australian_output": False,
            "message": (
                "Runs end-to-end only because a synthetic Australian AR-DRG "
                "overlay is explicitly supplied for documentation."
            ),
        },
    ]
    if local_precomputed_calculated is not None:
        local_total_nwau = (
            float(local_precomputed_calculated[nwau_column].sum())
            if nwau_column in local_precomputed_calculated.columns
            else None
        )
        scenarios.append(
            {
                "scenario": "local_precomputed_ar_drg",
                "status": "executable_user_supplied_provenance",
                "row_count": len(local_precomputed_calculated),
                "nwau_column": nwau_column,
                "total_nwau": local_total_nwau,
                "authoritative_australian_output": "depends_on_local_provenance",
                "message": (
                    "Runs only when the user supplies local Australian AR-DRG "
                    "provenance from a licensed or otherwise approved source."
                ),
            }
        )
    return scenarios


def _write_json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )


def run_mimic_demo_worked_example(
    root: str | Path,
    *,
    synthetic_overlay_path: str | Path,
    local_ar_drg_path: str | Path | None = None,
    reference_weights_path: str | Path,
    manifest_path: str | Path = (
        "reference-data/public-datasets/mimic-iv-demo/manifest.yaml"
    ),
    output_dir: str | Path | None = None,
    year: str = "2025",
) -> MimicDemoWorkedExampleBundle:
    """Run the conservative MIMIC-IV Demo worked example with safe fixtures.

    The calculation path requires an explicitly labelled synthetic AR-DRG
    overlay and fixture price weights. It is a runnable tutorial, not
    authoritative Australian classification evidence.
    """
    from nwau_py.calculators import AcuteParams, calculate_acute
    from nwau_py.calculators.acute import AcuteReferenceBundle

    manifest = load_public_dataset_manifest(manifest_path)
    staged = stage_mimic_demo_episodes(root)
    try:
        prepare_mimic_demo_calculator_input(staged)
    except PublicDatasetClassificationError as exc:
        fail_closed_error = str(exc)
    else:  # pragma: no cover - defensive; staging intentionally lacks AR-DRG
        fail_closed_error = "missing Australian AR-DRG was unexpectedly accepted"

    calculator_input = prepare_mimic_demo_calculator_input(
        staged,
        synthetic_overlay_path=synthetic_overlay_path,
        allow_synthetic_overlay=True,
    )
    weights = _clean_acute_weights(reference_weights_path)
    reference_bundle = AcuteReferenceBundle(
        year=year,
        ref_dir=Path(reference_weights_path).parent,
        weights=weights,
    )
    calculated = calculate_acute(
        calculator_input,
        AcuteParams(),
        year=year,
        reference_bundle=reference_bundle,
    )
    local_precomputed_calculated: pd.DataFrame | None = None
    if local_ar_drg_path is not None:
        local_calculator_input = prepare_mimic_demo_calculator_input(
            staged,
            local_ar_drg_path=local_ar_drg_path,
        )
        local_precomputed_calculated = calculate_acute(
            local_calculator_input,
            AcuteParams(),
            year=year,
            reference_bundle=reference_bundle,
        )

    mcp_boundary = _mcp_boundary_validation(calculator_input, year=year)
    support_status = _build_mimic_demo_support_status_summary(
        mcp_boundary_validation=mcp_boundary
    )
    surface_contract = _build_mimic_demo_surface_contract_report(
        mcp_boundary_validation=mcp_boundary
    )
    scenario_report = _build_mimic_demo_scenario_sensitivity_report(
        fail_closed_error=fail_closed_error,
        calculated=calculated,
        local_precomputed_calculated=local_precomputed_calculated,
        year=year,
    )
    provenance = build_public_dataset_provenance_report(
        manifest,
        local_files=(
            "hosp/admissions.csv",
            "hosp/diagnoses_icd.csv",
            "hosp/procedures_icd.csv",
            "hosp/drgcodes.csv",
            "icu/icustays.csv",
        ),
        derivation_steps=(
            "stage_mimic_demo_episodes",
            "prepare_mimic_demo_calculator_input",
            "calculate_acute",
        ),
        overlay_status="synthetic_demo_overlay",
        support_state="executable_non_authoritative",
    )
    data_quality = build_public_dataset_data_quality_report(staged)
    disclosure_risk = build_public_dataset_disclosure_risk_summary(staged)

    written_files: dict[str, str] = {}
    if output_dir is not None:
        destination = Path(output_dir)
        destination.mkdir(parents=True, exist_ok=True)
        csv_outputs = {
            "staged": (destination / "staged.csv", staged),
            "calculator_input": (
                destination / "calculator_input.csv",
                calculator_input,
            ),
            "calculated": (destination / "calculated.csv", calculated),
        }
        for name, (path, frame) in csv_outputs.items():
            frame.to_csv(path, index=False)
            written_files[name] = path.as_posix()
        json_outputs = {
            "provenance_report": (destination / "provenance_report.json", provenance),
            "data_quality_report": (
                destination / "data_quality_report.json",
                data_quality,
            ),
            "disclosure_risk_summary": (
                destination / "disclosure_risk_summary.json",
                disclosure_risk,
            ),
            "support_status_summary": (
                destination / "support_status_summary.json",
                support_status,
            ),
            "surface_contract_report": (
                destination / "surface_contract_report.json",
                surface_contract,
            ),
            "mcp_boundary_validation": (
                destination / "mcp_boundary_validation.json",
                mcp_boundary,
            ),
            "scenario_sensitivity_report": (
                destination / "scenario_sensitivity_report.json",
                scenario_report,
            ),
        }
        for name, (path, payload) in json_outputs.items():
            _write_json(path, payload)
            written_files[name] = path.as_posix()

    return MimicDemoWorkedExampleBundle(
        staged=staged,
        calculator_input=calculator_input,
        calculated=calculated,
        provenance_report=provenance,
        data_quality_report=data_quality,
        disclosure_risk_summary=disclosure_risk,
        support_status_summary=support_status,
        surface_contract_report=surface_contract,
        mcp_boundary_validation=mcp_boundary,
        scenario_sensitivity_report=scenario_report,
        written_files=written_files,
    )


def list_public_dataset_candidates() -> tuple[PublicClinicalDatasetCandidate, ...]:
    """Return the curated candidate list for public worked examples."""
    return (
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-demo-2.2",
            name="MIMIC-IV Clinical Database Demo",
            version="2.2",
            url="https://physionet.org/content/mimic-iv-demo/2.2/",
            doi="https://doi.org/10.13026/dp1f-ex47",
            citation=(
                "Johnson, A., Bulgarelli, L., Pollard, T., Horng, S., "
                "Celi, L. A., & Mark, R. (2023). MIMIC-IV Clinical "
                "Database Demo (version 2.2). PhysioNet. RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules=(
                "Raw files are open under ODbL terms but remain local-only in "
                "this repo; commit only metadata, manifests, and synthetic tiny "
                "fixtures."
            ),
            download_path="https://physionet.org/files/mimic-iv-demo/2.2/",
            file_size="15.5 MB uncompressed; 15.4 MB ZIP",
            update_cadence="versioned PhysioNet release; current version 2.2",
            clinical_fields=(
                "admissions",
                "patients",
                "diagnoses_icd",
                "procedures_icd",
                "drgcodes",
                "transfers",
                "icu_stays",
            ),
            fit_for_nwau_examples="admitted-episode-staging",
            initial_role="primary",
            committed_fixture_use="tiny synthetic MIMIC-shaped CSV fixtures only",
            local_download_use="supported through user-supplied local cache path",
            docs_use="primary tutorial dataset with fail-closed AR-DRG caveats",
            runtime_example_use="local ETL and synthetic-overlay calculator demo",
            pros=(
                "Open-access 100-patient subset with hospital and ICU tables.",
                "Contains admissions, diagnosis/procedure, and DRG metadata.",
                "Small enough for a local tutorial without bundling raw files.",
            ),
            cons=(
                "US MIMIC DRG and ICD fields are not Australian classifications.",
                "Authoritative NWAU requires local AR-DRG provenance or a "
                "clearly synthetic overlay.",
            ),
            risks=(
                "Overclaiming Australian AR-DRG/NWAU support from US data.",
                "Accidentally committing raw deidentified patient-level files.",
            ),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-ed-demo-2.2",
            name="MIMIC-IV-ED Demo",
            version="2.2",
            url="https://physionet.org/content/mimic-iv-ed-demo/2.2/",
            doi="https://doi.org/10.13026/jzz5-vs76",
            citation=(
                "Johnson, A., Bulgarelli, L., Pollard, T., Celi, L. A., "
                "Horng, S., & Mark, R. (2023). MIMIC-IV-ED Demo "
                "(version 2.2). PhysioNet. RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules="Keep raw CSV files local-only; commit metadata only.",
            download_path="https://physionet.org/files/mimic-iv-ed-demo/2.2/",
            file_size="111.8 KB uncompressed; 95.5 KB ZIP",
            update_cadence="versioned PhysioNet release; current version 2.2",
            clinical_fields=(
                "edstays",
                "diagnosis",
                "medrecon",
                "pyxis",
                "triage",
                "vitalsign",
            ),
            fit_for_nwau_examples="emergency-workflow-candidate",
            initial_role="deferred-ed-track",
            committed_fixture_use="future tiny synthetic ED-shaped fixtures",
            local_download_use="future ED tutorial local cache",
            docs_use="future ED example after AECC/UDG scope is separated",
            runtime_example_use="deferred",
            pros=("Open-access ED-specific demo linked to MIMIC-IV Demo subjects.",),
            cons=("ED classification and NWAU workflow differs from acute admitted.",),
            risks=("Bundling ED scope would make the first acute tutorial too broad.",),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-demo-meds-0.0.1",
            name="MIMIC-IV demo data in the Medical Event Data Standard",
            version="0.0.1",
            url="https://physionet.org/content/mimic-iv-demo-meds/0.0.1/",
            doi="https://doi.org/10.13026/t2y8-ea41",
            citation=(
                "van de Water, R. P., Steinberg, E., Wornow, M., "
                "Rockenschaub, P., & McDermott, M. (2025). MIMIC-IV demo "
                "data in the Medical Event Data Standard (version 0.0.1). "
                "PhysioNet. RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules="Keep Parquet event streams local-only.",
            download_path="https://physionet.org/files/mimic-iv-demo-meds/0.0.1/",
            file_size="5.7 MB uncompressed; 4.7 MB ZIP",
            update_cadence="versioned PhysioNet release; current version 0.0.1",
            clinical_fields=(
                "event_stream",
                "codes",
                "subject_splits",
                "dataset_metadata",
            ),
            fit_for_nwau_examples="interop-and-event-stream-candidate",
            initial_role="deferred-interop",
            committed_fixture_use="future tiny synthetic MEDS-shaped fixtures",
            local_download_use="future interop tutorial local cache",
            docs_use="future event-stream interoperability example",
            runtime_example_use="deferred",
            pros=("Useful for event-stream and ML-style interoperability patterns.",),
            cons=("Less direct for admitted-episode staging than relational CSVs.",),
            risks=("Would add a second data model to the first tutorial.",),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="mimic-iv-fhir-demo-2.1.0",
            name="MIMIC-IV Clinical Database Demo on FHIR",
            version="2.1.0",
            url="https://physionet.org/content/mimic-iv-fhir-demo/2.1.0/",
            doi="https://doi.org/10.13026/vphg-y548",
            citation=(
                "Bennett, A., Ulrich, H., Wiedekopf, J., Szul, P., "
                "Grimes, J., & Johnson, A. (2025). MIMIC-IV Clinical "
                "Database Demo on FHIR (version 2.1.0). PhysioNet. "
                "RRID:SCR_007345."
            ),
            license_name="Open Data Commons Open Database License v1.0",
            access_policy="open-access",
            required_credentials="none for direct PhysioNet file access",
            redistribution_rules="Keep NDJSON resources local-only.",
            download_path="https://physionet.org/files/mimic-iv-fhir-demo/2.1.0/",
            file_size="49.5 MB uncompressed; 49.5 MB ZIP",
            update_cadence="versioned PhysioNet release; current version 2.1.0",
            clinical_fields=(
                "FHIR Patient",
                "FHIR Encounter",
                "FHIR Condition",
                "FHIR Procedure",
                "FHIR Observation",
            ),
            fit_for_nwau_examples="fhir-interop-candidate",
            initial_role="deferred-interop",
            committed_fixture_use="future tiny synthetic FHIR NDJSON fixtures",
            local_download_use="future FHIR tutorial local cache",
            docs_use="future FHIR/API boundary example",
            runtime_example_use="deferred",
            pros=("FHIR resources demonstrate API and interoperability boundaries.",),
            cons=("Requires FHIR parsing and mapping before episode staging.",),
            risks=("Could distract from calculator input provenance in phase one.",),
        ),
        PublicClinicalDatasetCandidate(
            dataset_id="synthea",
            name="Synthea synthetic patient records",
            version="current generator or SyntheticMass releases",
            url="https://github.com/synthetichealth/synthea",
            doi=None,
            citation="Synthea synthetic patient generator, MITRE.",
            license_name="Apache-2.0",
            access_policy="open-source synthetic-data generator",
            required_credentials="none",
            redistribution_rules="Synthetic outputs may be regenerated and curated.",
            download_path="https://synthea.mitre.org/downloads",
            file_size="varies by generated cohort; SyntheticMass archive is large",
            update_cadence="open-source releases and generated datasets",
            clinical_fields=(
                "FHIR Patient",
                "FHIR Encounter",
                "FHIR Condition",
                "FHIR Procedure",
                "FHIR Claim",
            ),
            fit_for_nwau_examples="synthetic-comparison",
            initial_role="comparison-synthetic",
            committed_fixture_use="safe candidate for generated synthetic fixtures",
            local_download_use="optional generated cohort",
            docs_use="comparison point for no-real-data examples",
            runtime_example_use="future synthetic-only end-to-end example",
            pros=("No real patient data and no deidentification disclosure risk.",),
            cons=("Not real clinical data and not an Australian funding dataset.",),
            risks=("May look more complete than real-data provenance examples.",),
        ),
    )


def select_initial_worked_example(
    candidates: tuple[PublicClinicalDatasetCandidate, ...],
) -> PublicClinicalDatasetCandidate:
    """Select the first worked-example dataset from assessed candidates."""
    if not candidates:
        raise ValueError("no public dataset candidates were provided")
    primary = [
        candidate for candidate in candidates if candidate.initial_role == "primary"
    ]
    if not primary:
        raise ValueError("no primary public dataset candidate was selected")
    if len(primary) > 1:
        raise ValueError("only one primary public dataset candidate is allowed")
    return primary[0]
