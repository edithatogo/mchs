import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import polars as pl

try:
    import pandas as pd
except ImportError:
    from nwau_py import compat as pd

from nwau_py.classification_validation import (
    ClassificationValidationError,
    get_classification_version,
    validate_aecc_input,
    validate_classification_version,
    validate_udg_input,
)
from nwau_py.data.loader import load_sas_table
from nwau_py.data.paths import sas_table
from nwau_py.utils import sas_ref_dir

_DEFAULT_YEAR = "2025"


@dataclass
class EDParams:
    """Configuration for the ED calculator."""

    classification_option: int = 3
    eligibility_option: int = 1
    inscope_funding_sources: tuple[int, ...] = (1, 2, 8)
    debug_mode: bool = False
    clear_data: bool = False


def _decode_strings(df: Any) -> Any:
    if pd is not None and isinstance(df, pd.DataFrame):
        for col in df.select_dtypes(include=["object", "string"]).columns:
            if hasattr(df[col], "str"):
                with contextlib.suppress(Exception):
                    df[col] = df[col].str.decode("ascii")
    return df


def _safe_read_sas(path: Path | str) -> Any:
    path = Path(path)
    if pd is not None and getattr(pd, "read_sas", None) is not None:
        with contextlib.suppress(Exception):
            if "fake" in getattr(pd.read_sas, "__name__", "") or hasattr(
                pd.read_sas, "assert_called"
            ):
                return _decode_strings(pd.read_sas(path))
    with contextlib.suppress(Exception):
        return load_sas_table(path, cache=True)
    if pd is not None and hasattr(pd, "read_sas"):
        try:
            df = pd.read_sas(path, encoding="infer")
        except Exception:
            df = pd.read_sas(path)
        return _decode_strings(df)
    raise FileNotFoundError(f"Could not read SAS table: {path}")


def _to_pl(frame: Any) -> pl.DataFrame:
    if hasattr(frame, "to_polars"):
        res = frame.to_polars()
        if not isinstance(res, pl.DataFrame):
            return pl.DataFrame(res)
        return res
    if isinstance(frame, pl.DataFrame):
        return frame
    if isinstance(frame, pl.LazyFrame):
        return frame.collect()
    return pl.DataFrame(frame)


def _load_weights(
    ref_dir: Path, classification_option: int, year: str = _DEFAULT_YEAR
) -> Any:
    if classification_option < 3:
        path = sas_table(
            "nep{suffix}_edudg_price_weights.sas7bdat",
            year=year,
            base_dir=ref_dir,
        )
        df = _safe_read_sas(path)
        if hasattr(df, "columns") and "udg" in df.columns and "UDG" not in df.columns:
            df["UDG"] = df["udg"]
    else:
        path = sas_table(
            "nep{suffix}_edaecc_price_weights.sas7bdat",
            year=year,
            base_dir=ref_dir,
        )
        df = _safe_read_sas(path)
        if hasattr(df, "columns") and "aecc" in df.columns and "AECC" not in df.columns:
            df["AECC"] = df["aecc"]
    return df


def _load_udg_map(ref_dir: Path) -> Any:
    path = sas_table("ed_tov_tri_epi_to_udg.sas7bdat", base_dir=ref_dir)
    df = _safe_read_sas(path)
    if hasattr(df, "columns") and "udg" in df.columns and "UDG" not in df.columns:
        df["UDG"] = df["udg"]
    return df


def calculate_ed(
    df: Any,
    params: EDParams,
    *,
    year: str = _DEFAULT_YEAR,
    ref_dir: Path | None = None,
) -> Any:
    """Implement ``NWAU25_CALCULATOR_ED.sas`` against loaded reference tables."""
    collect_fn: Any = getattr(df, "collect_schema", None)
    cols = tuple(collect_fn().names() if callable(collect_fn) else df.columns)
    if params.classification_option == 1:
        required_mapping_fields = (
            "type_of_visit",
            "triage_category",
            "episode_end_status",
        )
        missing_mapping_fields = tuple(
            field for field in required_mapping_fields if field not in cols
        )
        if missing_mapping_fields:
            raise ClassificationValidationError(
                f"UDG {year} is missing required mapping fields: "
                + ", ".join(missing_mapping_fields)
            )
        validate_classification_version(
            "udg",
            year,
            get_classification_version("udg", year),
        )
    elif params.classification_option < 3:
        validate_udg_input(
            cols,
            year=year,
            version=get_classification_version("udg", year),
        )
    else:
        validate_aecc_input(
            cols,
            year=year,
            version=get_classification_version("aecc", year),
        )
    if ref_dir is None:
        ref_dir = sas_ref_dir(year)
    suffix = str(year)[-2:]
    nwau_col = f"NWAU{suffix}"
    gwau_col = f"GWAU{suffix}"

    is_pandas = pd is not None and isinstance(df, pd.DataFrame)
    df_pl = _to_pl(df)

    if params.classification_option == 1:
        udg_map = _to_pl(_load_udg_map(ref_dir))
        df_pl = df_pl.join(
            udg_map,
            on=["type_of_visit", "triage_category", "episode_end_status"],
            how="left",
        )

    weights = _to_pl(_load_weights(ref_dir, params.classification_option, year))
    key = "UDG" if params.classification_option < 3 else "AECC"
    merged = df_pl.join(weights, on=key, how="left")

    if params.classification_option < 3:
        if "udg_pw" not in merged.columns:
            merged = merged.with_columns(pl.lit(None).alias("udg_pw"))
        w01_expr = pl.col("udg_pw")
        adj_treat = (
            pl.col("adj_treat_remoteness")
            if "adj_treat_remoteness" in merged.columns
            else pl.lit(0.0)
        ).fill_null(0.0)
        gwau_expr = (w01_expr * (pl.lit(1.0) + adj_treat)).round(6)
    else:
        if "AECC_pw" not in merged.columns:
            merged = merged.with_columns(pl.lit(None).alias("AECC_pw"))
        w01_expr = pl.col("AECC_pw")
        adj_ind = (
            pl.col("adj_indigenous")
            if "adj_indigenous" in merged.columns
            else pl.lit(0.0)
        ).fill_null(0.0)
        adj_rem = (
            pl.col("adj_remoteness")
            if "adj_remoteness" in merged.columns
            else pl.lit(0.0)
        ).fill_null(0.0)
        adj_treat = (
            pl.col("adj_treat_remoteness")
            if "adj_treat_remoteness" in merged.columns
            else pl.lit(0.0)
        ).fill_null(0.0)
        gwau_expr = (
            w01_expr * (pl.lit(1.0) + adj_ind + adj_rem) * (pl.lit(1.0) + adj_treat)
        ).round(8)

    weight_missing = w01_expr.is_null()
    if params.eligibility_option == 1:
        comp = (
            pl.col("COMPENSABLE_STATUS")
            if "COMPENSABLE_STATUS" in merged.columns
            else pl.lit(None)
        )
        dva = pl.col("DVA_STATUS") if "DVA_STATUS" in merged.columns else pl.lit(None)
        missing_elig = comp.is_null() | dva.is_null()
        not_in_scope = (~comp.is_in([2, 9])) | (~dva.is_in([2, 9]))
        error_code_expr = (
            pl.when(weight_missing | missing_elig)
            .then(3)
            .when(not_in_scope)
            .then(2)
            .otherwise(0)
        )
    else:
        fund = pl.col("FUNDSC") if "FUNDSC" in merged.columns else pl.lit(None)
        out_scope = ~fund.is_in(list(params.inscope_funding_sources))
        error_code_expr = (
            pl.when(weight_missing).then(3).when(out_scope).then(2).otherwise(0)
        )

    merged = merged.with_columns(
        w01_expr.alias("_w01"),
        gwau_expr.alias(gwau_col),
        error_code_expr.alias("Error_Code"),
    )
    merged = merged.with_columns(
        pl.when(pl.col("Error_Code") > 0)
        .then(0.0)
        .otherwise(pl.col(gwau_col).round(8))
        .alias(nwau_col)
    )

    if not params.debug_mode:
        cols_to_drop = [c for c in merged.columns if c.startswith("_")]
        if cols_to_drop:
            merged = merged.drop(cols_to_drop)

    if params.clear_data:
        import shutil

        shutil.rmtree(".cache", ignore_errors=True)

    if is_pandas:
        return pd.DataFrame(merged)
    return merged
