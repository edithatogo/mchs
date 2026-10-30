from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from nwau_py.classification_validation import (
    get_classification_version,
    validate_amhcc_input,
)
from nwau_py.data.paths import sas_table
from nwau_py.utils import impute_adjustment, sas_ref_dir

_DEFAULT_YEAR = "2025"


@dataclass
class MHParams:
    """Configuration options for the mental health calculator."""

    # ``ppsa_option`` selects whether the private patient service adjustment is
    # applied using the national (1) or state-level (2) reference tables.
    ppsa_option: int = 1

    # Flags indicating whether admitted and community substreams should be
    # processed. Both are enabled by default to match the source calculator
    # defaults.
    adm_sstream: int = 1
    cmty_sstream: int = 1
    remoteness_distribution: dict[str, float] | None = None
    indigenous_distribution: dict[int, float] | None = None
    debug_mode: bool = False
    clear_data: bool = False


def _load_weights(ref_dir: Path, year: str = _DEFAULT_YEAR) -> dict[str, pd.DataFrame]:
    """Load reference tables used by the MH calculator."""

    def _read(name: str) -> pd.DataFrame:
        df = pd.read_sas(
            sas_table(f"nep{{suffix}}_{name}.sas7bdat", year=year, base_dir=ref_dir)
        )
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].str.decode("ascii")
        return df

    tables = {
        "adm": _read("mh_adm_price_weights"),
        "cmty": _read("mh_cmty_price_weights"),
        "ppsa": _read("mh_ppsa"),
        "priv_acc": _read("mh_adj_priv_acc"),
        "specpaed": _read("mh_adj_specpaed"),
        "adj_ind": _read("aa_mh_sa_na_ed_adj_ind"),
        "adj_rem": _read("aa_mh_sa_na_adj_rem"),
        "adj_treat": _read("aa_mh_sa_na_adj_treat_rem"),
    }

    return tables


def calculate_mh(
    df: pd.DataFrame,
    params: MHParams,
    *,
    year: str = _DEFAULT_YEAR,
    ref_dir: Path | None = None,
) -> pd.DataFrame:
    """Calculate mental health NWAU.

    This function mirrors the logic of ``NWAU25_CALCULATOR_MH.sas`` through
    loaded reference tables and tabular joins. The input frame should contain
    the patient-level variables referenced below (e.g. ``AMHCC``, ``LOS``,
    ``PAT_PRIVATE_FLAG`` etc.).
    """
    validate_amhcc_input(
        tuple(df.columns),
        year=year,
        version=get_classification_version("amhcc", year),
    )
    if ref_dir is None:
        ref_dir = sas_ref_dir(year)
    suffix = str(year)[-2:]
    nwau_col = f"NWAU{suffix}"

    tables = _load_weights(ref_dir, year)

    result = df.copy()

    # ------------------------------------------------------------------
    # Merge price weights and adjustment tables
    # ------------------------------------------------------------------
    result = result.merge(tables["adm"], on="AMHCC", how="left")
    result = result.merge(tables["cmty"], on="AMHCC", how="left")

    ppsa = tables["ppsa"].rename(columns={"amhccV1code": "AMHCC", "state": "STATE"})
    result = result.merge(ppsa, on=["AMHCC", "STATE"], how="left")

    priv_acc = tables["priv_acc"].rename(columns={"State": "STATE"})
    result = result.merge(priv_acc, on="STATE", how="left")

    result = result.merge(tables["specpaed"], on="_pat_specpaed", how="left")
    result = result.merge(tables["adj_ind"], on="_pat_ind_flag", how="left")
    result = result.merge(tables["adj_rem"], on="_pat_remoteness", how="left")
    result = result.merge(tables["adj_treat"], on="_treat_remoteness", how="left")

    if params.indigenous_distribution is not None and bool(
        params.indigenous_distribution
    ):
        imputed = impute_adjustment(
            tables["adj_ind"],
            "_pat_ind_flag",
            "adj_indigenous",
            params.indigenous_distribution,
        )
        result["adj_indigenous"] = result["adj_indigenous"].fillna(imputed)
    if params.remoteness_distribution is not None and bool(
        params.remoteness_distribution
    ):
        imputed = impute_adjustment(
            tables["adj_rem"],
            "_pat_remoteness",
            "adj_remoteness",
            params.remoteness_distribution,
        )
        result["adj_remoteness"] = result["adj_remoteness"].fillna(imputed)
        imputed = impute_adjustment(
            tables["adj_treat"],
            "_treat_remoteness",
            "adj_treat_remoteness",
            params.remoteness_distribution,
        )
        result["adj_treat_remoteness"] = result["adj_treat_remoteness"].fillna(imputed)

    # Fill missing adjustment values with defaults
    result["adj_specpaed"] = result["adj_specpaed"].fillna(1)
    for col in ["adj_indigenous", "adj_remoteness", "adj_treat_remoteness"]:
        result[col] = result[col].fillna(0)

    # ------------------------------------------------------------------
    # Separation category for admitted activity
    # ------------------------------------------------------------------
    sepcat = np.select(
        [
            result["LOS"].isna()
            | result["amhcc_inlier_lb"].isna()
            | result["amhcc_inlier_ub"].isna(),
            result["LOS"] < result["amhcc_inlier_lb"],
            result["LOS"] <= result["amhcc_inlier_ub"],
            result["LOS"] > result["amhcc_inlier_ub"],
        ],
        [np.nan, 2, 3, 4],
    )
    result["_pat_separation_category"] = sepcat

    # ------------------------------------------------------------------
    # Base price weight (W01)
    # ------------------------------------------------------------------
    mask_adm = (result["AMHCC"].str.startswith("1")) & (params.adm_sstream == 1)
    mask_cmty = (result["AMHCC"].str.startswith("2")) & (params.cmty_sstream == 1)

    w01_adm = np.where(
        mask_adm & (result["priceCat"] == 0),
        result["amhcc_pw_sso_base"] + result["LOS"] * result["amhcc_pw_lso_perdiem"],
        0,
    )

    w01_adm = np.where(
        mask_adm & (result["priceCat"] == 1) & (sepcat == 2),
        result["amhcc_pw_sso_base"].fillna(0)
        + result["LOS"] * result["amhcc_pw_sso_perdiem"],
        w01_adm,
    )

    w01_adm = np.where(
        mask_adm & (result["priceCat"] == 1) & (sepcat == 3),
        result["amhcc_pw_inlier"],
        w01_adm,
    )

    w01_adm = np.where(
        mask_adm & (result["priceCat"] == 1) & (sepcat == 4),
        result["amhcc_pw_inlier"]
        + (result["LOS"] - result["amhcc_inlier_ub"])
        * result["amhcc_pw_lso_perdiem"].fillna(0),
        w01_adm,
    )

    w01_adm = np.round(w01_adm, 4)

    w01_cmty = np.where(
        mask_cmty,
        np.maximum(
            0,
            result["SC_PAT_PUB"] * result["_cmty_sc_pat_pw"]
            + result["SC_NOPAT_PUB"] * result["_cmty_sc_nopat_pw"],
        ),
        0,
    )
    w01_cmty = np.round(w01_cmty, 4)

    result["_w01"] = w01_adm + w01_cmty

    # ------------------------------------------------------------------
    # GWAU calculation
    # ------------------------------------------------------------------
    gwau = (
        result["_w01"]
        * result["adj_specpaed"]
        * (1 + result["adj_indigenous"] + result["adj_remoteness"])
        * (1 + result["adj_treat_remoteness"])
    )

    # ------------------------------------------------------------------
    # Private patient deductions (admitted only)
    # ------------------------------------------------------------------
    if params.ppsa_option == 1:
        priv_serv_rate = result["amhcc_adj_privPat_servNat"].fillna(0)
    else:
        priv_serv_rate = result["amhcc_adj_privPat_serv"].fillna(0)

    adj_priv_serv = result["PAT_PRIVATE_FLAG"] * priv_serv_rate * w01_adm
    adj_priv_accomm = result["PAT_PRIVATE_FLAG"] * (
        result["PAT_SAMEDAY_FLAG"] * result["state_adj_privpat_accomm_sd"].fillna(0)
        + (1 - result["PAT_SAMEDAY_FLAG"])
        * result["LOS"]
        * result["state_adj_privpat_accomm_on"].fillna(0)
    )

    nwau = np.where(
        mask_adm,
        np.maximum(0, gwau - adj_priv_serv - adj_priv_accomm),
        gwau,
    )

    nwau = np.where(result.get("Error_Code", 0) > 0, 0, nwau)

    result[nwau_col] = nwau

    if not params.debug_mode:
        result = result.drop(columns=[c for c in result.columns if c.startswith("_")])
    if params.clear_data:
        import shutil

        shutil.rmtree(".cache", ignore_errors=True)

    return result
