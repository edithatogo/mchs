from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

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


def _load_cmty_weights(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    """Load the community mental health price-weight table."""
    suffix = year[-2:]
    df = pd.read_sas(
        sas_table(
            f"nep{suffix}_mh_cmty_price_weights.sas7bdat",
            year=year,
            base_dir=ref_dir,
        )
    )
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.decode("ascii")
    return df.rename(columns={"amhcc": "AMHCC"})


def calculate_community_mh(
    df: pd.DataFrame,
    params: CommunityMHParams,
    *,
    year: str = _DEFAULT_YEAR,
    ref_dir: Path | None = None,
    cmty_weights: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Calculate community mental health NWAU.

    This function implements the community substream of the mental health
    calculator. NWAU is computed from service-contact counts multiplied by
    AMHCC-specific community price weights.
    """
    validate_amhcc_input(
        df.columns,
        year=year,
        version=get_classification_version("amhcc", year),
    )

    suffix = year[-2:]
    nwau_col = f"NWAU{suffix}"

    if cmty_weights is None:
        if ref_dir is None:
            ref_dir = sas_ref_dir(year)
        cmty_weights = _load_cmty_weights(ref_dir, year)

    result = df.copy()
    result = result.merge(cmty_weights, on="AMHCC", how="left")

    w01 = np.where(
        result["SC_PAT_PUB"].notna() & result["SC_NOPAT_PUB"].notna(),
        np.maximum(
            0,
            result["SC_PAT_PUB"] * result["_cmty_sc_pat_pw"].fillna(0)
            + result["SC_NOPAT_PUB"] * result["_cmty_sc_nopat_pw"].fillna(0),
        ),
        0,
    )
    w01 = np.round(w01, 4)
    result["_w01"] = w01

    result[nwau_col] = w01

    if not params.debug_mode:
        result = result.drop(columns=[c for c in result.columns if c.startswith("_")])

    return result


class CommunityMHCalculator:
    """Top-level calculator for community mental health."""

    def run(
        self,
        df: pd.DataFrame,
        params: CommunityMHParams | None = None,
        **kwargs,
    ) -> pd.DataFrame:
        """Run the community mental health calculation."""
        if params is None:
            params = CommunityMHParams()
        return calculate_community_mh(df, params, **kwargs)
