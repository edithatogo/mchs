from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from nwau_py.data.loader import load_sas_table
from nwau_py.data.paths import sas_table
from nwau_py.utils import impute_adjustment, ra_suffix, sas_ref_dir

_DEFAULT_YEAR = "2025"


@dataclass
class SubacuteParams:
    radiotherapy_option: int = 1
    dialysis_option: int = 1
    est_remoteness_option: int = 1
    remoteness_distribution: dict[str, float] | None = None
    indigenous_distribution: dict[int, float] | None = None
    debug_mode: bool = False
    clear_data: bool = False
    ppsa_option: int = 1


def _load_weights(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    df = pd.read_sas(
        sas_table(
            "nep{suffix}_sa_snap_price_weights.sas7bdat",
            year=year,
            base_dir=ref_dir,
        )
    )
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.decode("ascii")
    if "ansnap" in df.columns:
        df = df.rename(columns={"ansnap": "ANSNAP"})
    elif "snap" in df.columns:
        df = df.rename(columns={"snap": "ANSNAP"})
    return df


def calculate_subacute(
    df: pd.DataFrame,
    params: SubacuteParams,
    *,
    year: str = _DEFAULT_YEAR,
    ref_dir: Path | None = None,
) -> pd.DataFrame:
    """Calculate NWAU25 for subacute episodes.

    This function mirrors ``NWAU25_CALCULATOR_SUBACUTE.sas`` through loaded
    reference tables. ``df`` should contain at least the columns ``ANSNAP``,
    ``ADM_DATE``, ``SEP_DATE``, ``LEAVE_DAYS`` and ``BIRTH_DATE``.
    Private/public flags are expected in ``PAT_PRIVATE_FLAG`` and
    ``PAT_PUBLIC_FLAG``.
    """
    if ref_dir is None:
        ref_dir = sas_ref_dir(year)
    suffix = str(year)[-2:]
    nwau_col = f"NWAU{suffix}"
    ra = ra_suffix(year)
    ra_year = ra[2:]
    weights = _load_weights(ref_dir, year)
    merged = df.merge(weights, on="ANSNAP", how="left")

    # --------------------------------------------------------------
    # Radiotherapy and dialysis flags
    # --------------------------------------------------------------
    proc_cols = [
        c for c in merged.columns if "srg" in c.lower() or c.lower().startswith("proc")
    ]

    def _flag_procs(codes: set[str]) -> pd.Series:
        if not proc_cols:
            return pd.Series(0, index=merged.index)
        proc_df = merged[proc_cols].fillna("").astype(str)
        proc_df = proc_df.replace({"/": "", "-": "", " ": ""}, regex=True)
        return proc_df.isin(codes).any(axis=1).astype(int)

    try:
        radio_codes = load_sas_table(
            sas_table("nep{suffix}_radio_codes.sas7bdat", year=year, base_dir=ref_dir)
        )
        radio_set = set(radio_codes["code_ID"].astype(int).astype(str))
    except Exception:
        radio_set = set()

    try:
        dialysis_codes = load_sas_table(
            sas_table(
                "nep{suffix}_dialysis_codes.sas7bdat",
                year=year,
                base_dir=ref_dir,
            )
        )
        dialysis_set = set(dialysis_codes["code_ID"].astype(int).astype(str))
    except Exception:
        dialysis_set = set()

    if params.radiotherapy_option == 2:
        merged["_pat_radiotherapy_flag"] = merged.get(
            "PAT_RADIOTHERAPY_FLAG", 0
        ).fillna(0)
    else:
        merged["_pat_radiotherapy_flag"] = _flag_procs(radio_set)

    if params.dialysis_option == 2:
        merged["_pat_dialysis_flag"] = merged.get("PAT_DIALYSIS_FLAG", 0).fillna(0)
    else:
        merged["_pat_dialysis_flag"] = _flag_procs(dialysis_set)

    try:
        rt_adj = load_sas_table(
            sas_table("nep{suffix}_aa_sa_adj_rt.sas7bdat", year=year, base_dir=ref_dir)
        )
        merged = merged.merge(rt_adj, on="_pat_radiotherapy_flag", how="left")
    except Exception:
        merged["adj_radiotherapy"] = 0

    try:
        ds_adj = load_sas_table(
            sas_table("nep{suffix}_aa_sa_adj_ds.sas7bdat", year=year, base_dir=ref_dir)
        )
        merged = merged.merge(ds_adj, on="_pat_dialysis_flag", how="left")
    except Exception:
        merged["adj_dialysis"] = 0

    # --------------------------------------------------------------
    # Remoteness calculations
    if params.est_remoteness_option == 1:
        treat = np.nan
        if "ESTID" in merged.columns:
            try:
                hosp_df = load_sas_table(
                    sas_table(
                        "nep{suffix}_hospital_{ra}.sas7bdat",
                        year=year,
                        base_dir=ref_dir,
                    )
                )
                apc_col = next(
                    (c for c in hosp_df.columns if c.lower().startswith("apcid")),
                    None,
                )
                if apc_col:
                    hosp_df = hosp_df.rename(columns={apc_col: "ESTID"})
                ra_col = next(
                    (
                        c
                        for c in hosp_df.columns
                        if c.lower() in {ra.lower(), f"_hosp_ra_{ra_year}"}
                    ),
                    None,
                )
                hosp_ra_col = f"_hosp_ra_{ra_year}"
                if ra_col:
                    merged = merged.merge(
                        hosp_df[["ESTID", ra_col]].rename(
                            columns={ra_col: hosp_ra_col}
                        ),
                        on="ESTID",
                        how="left",
                    )
                    treat = merged[hosp_ra_col]
                else:
                    treat = np.nan
                    merged[hosp_ra_col] = np.nan
            except Exception:
                treat = np.nan
                hosp_ra_col = f"_hosp_ra_{ra_year}"
                merged[hosp_ra_col] = np.nan
        if isinstance(treat, pd.Series):
            merged["_treat_remoteness"] = treat.fillna(0)
        else:
            merged["_treat_remoteness"] = pd.Series(treat, index=merged.index).fillna(0)
    else:
        merged["_treat_remoteness"] = merged.get(
            "EST_REMOTENESS", pd.Series(0, index=merged.index)
        ).fillna(0)

    pat_pc = next(
        (c for c in ["PAT_POSTCODE", "POSTCODE"] if c in merged.columns),
        None,
    )
    pat_sa2 = next(
        (
            c
            for c in ["PAT_SA2", "SA2", "PAT_ASGS", "ASGS", "PAT_SLA", "SLA"]
            if c in merged.columns
        ),
        None,
    )
    if params.est_remoteness_option == 1:
        pat_ra_col = f"PAT_{ra}"
        sa2_ra_col = f"SA2_{ra}"
        hosp_ra_col = f"_hosp_ra_{ra_year}"
        if pat_pc:
            try:
                pc_df = load_sas_table(
                    sas_table("postcode_to_{ra}.sas7bdat", year=year, base_dir=ref_dir)
                )
                ra_col = next((c for c in pc_df.columns if c.lower() == ra.lower()), ra)
                pc_df = pc_df.rename(columns={"POSTCODE": pat_pc, ra_col: pat_ra_col})
                merged = merged.merge(
                    pc_df[[pat_pc, pat_ra_col]], on=pat_pc, how="left"
                )
            except Exception:
                merged[pat_ra_col] = np.nan
        else:
            merged[pat_ra_col] = np.nan

        if pat_sa2:
            try:
                paths = [
                    sas_table("sa2_to_{ra}.sas7bdat", year=year, base_dir=ref_dir),
                    sas_table("asgs_to_{ra}.sas7bdat", year=year, base_dir=ref_dir),
                    sas_table("sla_to_{ra}.sas7bdat", year=year, base_dir=ref_dir),
                ]
                for path in paths:
                    try:
                        sa2_df = load_sas_table(path)
                        break
                    except FileNotFoundError:
                        continue
                else:
                    raise FileNotFoundError(paths[0])
                key_col = next(
                    (c for c in ["SA2", "ASGS", "SLA"] if c in sa2_df.columns),
                    None,
                )
                ra_col = next(
                    (c for c in sa2_df.columns if c.lower() == ra.lower()), ra
                )
                if key_col:
                    sa2_df = sa2_df.rename(
                        columns={key_col: pat_sa2, ra_col: sa2_ra_col}
                    )
                    merged = merged.merge(
                        sa2_df[[pat_sa2, sa2_ra_col]], on=pat_sa2, how="left"
                    )
                else:
                    merged[sa2_ra_col] = np.nan
            except Exception:
                merged[sa2_ra_col] = np.nan
        else:
            merged[sa2_ra_col] = np.nan

        merged["_pat_remoteness"] = (
            merged.get(sa2_ra_col)
            .combine_first(merged.get(pat_ra_col))
            .combine_first(
                merged.get(hosp_ra_col, pd.Series(np.nan, index=merged.index))
            )
        )
    else:
        merged["_pat_remoteness"] = merged.get("EST_REMOTENESS", np.nan)

    adm = pd.to_datetime(merged["ADM_DATE"])
    sep = pd.to_datetime(merged["SEP_DATE"])
    leave = merged.get("LEAVE_DAYS", 0).fillna(0)
    los = (sep - adm).dt.days - leave
    los = los.clip(lower=1)
    los = np.where(adm.isna() | sep.isna() | (adm > sep), np.nan, los)
    merged["pat_los"] = los
    merged["_pat_sameday_flag"] = (adm == sep).astype(int)

    birth = pd.to_datetime(merged["BIRTH_DATE"])
    age = np.floor(((adm - birth).dt.days) / 365.25)
    merged["_pat_age_years"] = age

    ind_col = merged.get("INDSTAT", pd.Series(0, index=merged.index))
    merged["_pat_ind_flag"] = ind_col.isin([1, 2, 3]).astype(int)
    merged["_pat_private_flag"] = merged.get("PAT_PRIVATE_FLAG", 0)
    merged["_pat_public_flag"] = merged.get("PAT_PUBLIC_FLAG", 0)

    # --------------------------------------------------------------
    # Merge adjustment tables
    # --------------------------------------------------------------
    ind_adj = None
    try:
        ind_adj = load_sas_table(
            sas_table(
                "nep{suffix}_aa_mh_sa_na_ed_adj_ind.sas7bdat",
                year=year,
                base_dir=ref_dir,
            )
        )
        merged = merged.merge(ind_adj, on="_pat_ind_flag", how="left")
    except Exception:
        merged["adj_indigenous"] = 0
    if (
        params.indigenous_distribution is not None
        and bool(params.indigenous_distribution)
    ) and ind_adj is not None:
        imputed = impute_adjustment(
            ind_adj,
            "_pat_ind_flag",
            "adj_indigenous",
            params.indigenous_distribution,
        )
        merged["adj_indigenous"] = merged["adj_indigenous"].fillna(imputed)

    pat_adj = None
    try:
        pat_adj = load_sas_table(
            sas_table(
                "nep{suffix}_aa_mh_sa_na_adj_rem.sas7bdat",
                year=year,
                base_dir=ref_dir,
            )
        )
        merged = merged.merge(pat_adj, on="_pat_remoteness", how="left")
    except Exception:
        merged["adj_remoteness"] = 0
    if (
        params.remoteness_distribution is not None
        and bool(params.remoteness_distribution)
    ) and pat_adj is not None:
        imputed = impute_adjustment(
            pat_adj,
            "_pat_remoteness",
            "adj_remoteness",
            params.remoteness_distribution,
        )
        merged["adj_remoteness"] = merged["adj_remoteness"].fillna(imputed)

    treat_adj = None
    try:
        treat_adj = load_sas_table(
            sas_table(
                "nep{suffix}_aa_mh_sa_na_adj_treat_rem.sas7bdat",
                year=year,
                base_dir=ref_dir,
            )
        )
        merged = merged.merge(treat_adj, on="_treat_remoteness", how="left")
    except Exception:
        merged["adj_treat_remoteness"] = 0
    if (
        params.remoteness_distribution is not None
        and bool(params.remoteness_distribution)
    ) and treat_adj is not None:
        imputed = impute_adjustment(
            treat_adj,
            "_treat_remoteness",
            "adj_treat_remoteness",
            params.remoteness_distribution,
        )
        merged["adj_treat_remoteness"] = merged["adj_treat_remoteness"].fillna(imputed)

    # Private patient service adjustment
    merged["_care"] = (
        merged.get("CARE_TYPE", pd.Series(0, index=merged.index))
        .fillna(0)
        .astype(float)
        .astype(int)
    )
    try:
        ppsa = load_sas_table(
            sas_table(
                "nep{suffix}_sa_adj_priv_serv_state.sas7bdat",
                year=year,
                base_dir=ref_dir,
            )
        )
        ppsa = ppsa.rename(columns={"caretype": "_care", "state": "STATE"})
        merged = merged.merge(ppsa, on=["STATE", "_care"], how="left")
    except Exception:
        merged["caretype_adj_privpat_serv_state"] = 0
        merged["caretype_adj_privpat_serv_nat"] = 0

    try:
        acc = load_sas_table(
            sas_table(
                "nep{suffix}_aa_sa_adj_priv_acc.sas7bdat",
                year=year,
                base_dir=ref_dir,
            )
        )
        acc = acc.rename(columns={"state": "STATE"})
        merged = merged.merge(acc, on="STATE", how="left")
    except Exception:
        merged["state_adj_privpat_accomm_sd"] = 0
        merged["state_adj_privpat_accomm_on"] = 0

    error_code = np.select(
        [
            (age >= 0)
            & (age <= 17)
            & ~merged["ANSNAP"].isin(
                [
                    "5F01",
                    "5F02",
                    "5F03",
                    "5F04",
                    "5F05",
                    "5O01",
                    "5G01",
                    "5G02",
                    "5G03",
                    "5G04",
                    "5P01",
                    "5ES4",
                    "5EL1",
                ]
            ),
            merged["ANSNAP"].isna()
            | adm.isna()
            | sep.isna()
            | merged.get("STATE").isna(),
            adm > sep,
            (merged["_pat_public_flag"] + merged["_pat_private_flag"]) == 0,
            merged["ANSNAP"].isin(["5J01", "5O01", "5K01", "5P01", "5L01", "5M01"])
            & ((los > 1) | (merged["ansnap_samedaylist_flag"] != 1)),
        ],
        [1, 3, 1, 2, 4],
        default=0,
    )
    merged["Error_Code"] = error_code.astype(int)

    merged["_pat_separation_category"] = np.select(
        [
            merged["ansnap_samedaylist_flag"] == 1,
            los < merged["ansnap_inlier_lb"],
            los <= merged["ansnap_inlier_ub"],
            los > merged["ansnap_inlier_ub"],
        ],
        [1, 2, 3, 4],
        default=np.nan,
    )

    w01 = np.select(
        [
            merged["_pat_separation_category"] == 1,
            merged["_pat_separation_category"] == 2,
            merged["_pat_separation_category"] == 3,
            merged["_pat_separation_category"] == 4,
        ],
        [
            merged["ansnap_pw_sd"],
            los * merged["ansnap_pw_sso_perdiem"].fillna(0),
            merged["ansnap_pw_inlier"],
            merged["ansnap_pw_inlier"]
            + (los - merged["ansnap_inlier_ub"])
            * merged["ansnap_pw_lso_perdiem"].fillna(0),
        ],
        default=0,
    )
    merged["_w01"] = w01.round(4)

    gwau = (
        merged["_w01"]
        * (
            1
            + merged.get("adj_indigenous", 0)
            + merged.get("adj_remoteness", 0)
            + merged.get("adj_radiotherapy", 0)
            + merged.get("adj_dialysis", 0)
        )
        * (1 + merged.get("adj_treat_remoteness", 0))
    )

    if params.ppsa_option == 1:
        priv_serv_rate = merged.get("caretype_adj_privpat_serv_nat", 0)
    else:
        priv_serv_rate = merged.get("caretype_adj_privpat_serv_state", 0)
    adj_priv_serv = merged["_pat_private_flag"] * priv_serv_rate * merged["_w01"]
    adj_priv_accomm = merged["_pat_private_flag"] * (
        merged["_pat_sameday_flag"] * merged.get("state_adj_privpat_accomm_sd", 0)
        + (1 - merged["_pat_sameday_flag"])
        * los
        * merged.get("state_adj_privpat_accomm_on", 0)
    )

    nwau = np.where(
        merged["Error_Code"] > 0,
        0,
        np.maximum(0, gwau - adj_priv_serv - adj_priv_accomm),
    )
    merged[nwau_col] = nwau

    result = merged
    if not params.debug_mode:
        result = result.drop(columns=[c for c in result.columns if c.startswith("_")])
    if params.clear_data:
        import shutil

        shutil.rmtree(".cache", ignore_errors=True)

    return result
