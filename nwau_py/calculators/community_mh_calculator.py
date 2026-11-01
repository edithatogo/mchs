from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import polars as pl

from nwau_py.classification_validation import (
    get_classification_version,
    validate_amhcc_input,
)
from nwau_py.data.paths import sas_table
from nwau_py.utils import sas_ref_dir

_DEFAULT_YEAR = "2025"


@dataclass
class CommunityMHParams:
    """Configuration options for the community mental health calculator."""

    debug_mode: bool = False


def _safe_read_sas(path: Path) -> pl.DataFrame:
    try:
        import pyreadstat

        if path.exists():
            d, _ = pyreadstat.read_sas7bdat(str(path), output_format="dict")
            return pl.from_dict(d)
    except Exception:
        return pl.DataFrame()
    return pl.DataFrame()


def _load_cmty_weights(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pl.DataFrame:
    """Load the community mental health price-weight table."""
    suffix = year[-2:]
    table_path = Path(
        sas_table(
            f"nep{suffix}_mh_cmty_price_weights.sas7bdat",
            year=year,
            base_dir=ref_dir,
        )
    )
    df = _safe_read_sas(table_path)
    exprs = [
        pl.col(col).str.strip_chars()
        for col in df.columns
        if df[col].dtype in (pl.Utf8, pl.String)
    ]
    if exprs:
        df = df.with_columns(exprs)
    if "amhcc" in df.columns and "AMHCC" not in df.columns:
        df = df.rename({"amhcc": "AMHCC"})
    return df


def calculate_community_mh(
    df: Any,
    params: CommunityMHParams,
    *,
    year: str = _DEFAULT_YEAR,
    ref_dir: Path | None = None,
    cmty_weights: Any | None = None,
) -> Any:
    """Calculate community mental health NWAU.

    This function implements the community substream of the mental health
    calculator. NWAU is computed from service-contact counts multiplied by
    AMHCC-specific community price weights.
    """
    is_pandas = (
        not isinstance(df, pl.DataFrame)
        and hasattr(df, "to_dict")
        and not hasattr(df, "lazy")
    )
    if hasattr(df, "to_polars"):
        df_pl = df.to_polars()
    elif is_pandas:
        df_pl = pl.DataFrame(df)
    else:
        df_pl = df.clone()

    validate_amhcc_input(
        df_pl.columns,
        year=year,
        version=get_classification_version("amhcc", year),
    )

    suffix = year[-2:]
    nwau_col = f"NWAU{suffix}"

    if cmty_weights is None:
        if ref_dir is None:
            ref_dir = sas_ref_dir(year)
        cmty_weights = _load_cmty_weights(ref_dir, year)
    elif hasattr(cmty_weights, "to_polars"):
        cmty_weights = cmty_weights.to_polars()
    elif not isinstance(cmty_weights, pl.DataFrame):
        cmty_weights = pl.DataFrame(cmty_weights)

    merged = df_pl.join(cmty_weights, on="AMHCC", how="left")

    w01_expr = (
        pl.when(
            pl.col("SC_PAT_PUB").is_not_null() & pl.col("SC_NOPAT_PUB").is_not_null()
        )
        .then(
            (
                pl.col("SC_PAT_PUB") * pl.col("_cmty_sc_pat_pw").fill_null(0)
                + pl.col("SC_NOPAT_PUB") * pl.col("_cmty_sc_nopat_pw").fill_null(0)
            )
            .clip(lower_bound=0)
            .round(4)
        )
        .otherwise(0.0)
    )

    merged = merged.with_columns(
        w01_expr.alias("_w01"),
        w01_expr.alias(nwau_col),
    )

    if not params.debug_mode:
        cols_to_drop = [c for c in merged.columns if c.startswith("_")]
        merged = merged.drop(cols_to_drop)

    if is_pandas:
        from nwau_py import compat as pd

        return pd.DataFrame(merged)
    return merged


class CommunityMHCalculator:
    """Top-level calculator for community mental health."""

    def run(
        self,
        df: Any,
        params: CommunityMHParams | None = None,
        **kwargs,
    ) -> Any:
        """Run the community mental health calculation."""
        if params is None:
            params = CommunityMHParams()
        return calculate_community_mh(df, params, **kwargs)
