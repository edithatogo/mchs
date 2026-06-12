from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

try:  # pragma: no cover - optional dependency
    import pyreadstat
except Exception:  # pragma: no cover - pyreadstat is optional for CSV-backed tests
    pyreadstat = None

from nwau_py.classification_validation import (
    get_classification_version,
    validate_tier_2_input,
)
from nwau_py.data.loader import clear_reference_cache, load_sas_table
from nwau_py.data.paths import sas_table
from nwau_py.utils import impute_adjustment, ra_suffix, sas_ref_dir

_DEFAULT_YEAR = "2025"
_READSTAT_ERRORS: tuple[type[BaseException], ...] = ()
if pyreadstat is not None:  # pragma: no branch - import-time optional dependency guard
    _READSTAT_ERRORS = tuple(
        error_type
        for error_type in (
            getattr(pyreadstat, "ReadstatError", None),
            getattr(getattr(pyreadstat, "_readstat_parser", None), "PyreadstatError", None),
        )
        if isinstance(error_type, type)
    )
_OPTIONAL_REFERENCE_ERRORS = (FileNotFoundError, KeyError, ValueError) + _READSTAT_ERRORS


@dataclass
class OutpatientParams:
    paed_option: int = 1
    est_remoteness_option: int = 1
    remoteness_distribution: dict[str, float] | None = None
    indigenous_distribution: dict[int, float] | None = None
    debug_mode: bool = False
    clear_data: bool = False
    data_type: int = 1
    inscope_funding_sources: tuple[int, ...] = (1, 2, 8)


def _load_weights(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    df = pd.read_sas(
        sas_table("nep{suffix}_op_price_weights.sas7bdat", year=year, base_dir=ref_dir)
    )
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.decode("ascii")
    if "tier2_clinic" in df.columns:
        df = df.rename(columns={"tier2_clinic": "TIER2_CLINIC"})
    elif "clinic_code" in df.columns:
        df = df.rename(columns={"clinic_code": "TIER2_CLINIC"})
    return df


def _load_hospital_ra(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    ra = ra_suffix(year)
    ra_year = ra[2:]
    df = load_sas_table(
        sas_table("nep{suffix}_hospital_{ra}.sas7bdat", year=year, base_dir=ref_dir)
    )
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.decode("ascii")
    apc_col = next(c for c in df.columns if c.startswith("APCID"))
    ra_col = next((c for c in df.columns if c.lower() == ra.lower()), ra)
    df = df.rename(columns={apc_col: "APCID", ra_col: f"_hosp_ra_{ra_year}"})
    return df[["APCID", f"_hosp_ra_{ra_year}"]]


def _load_postcode_ra(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    ra = ra_suffix(year)
    df = load_sas_table(
        sas_table("postcode_to_{ra}.sas7bdat", year=year, base_dir=ref_dir)
    )
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.decode("ascii")
    ra_col = next((c for c in df.columns if c.lower() == ra.lower()), ra)
    return df.rename(columns={"POSTCODE": "POSTCODE", ra_col: ra})


def _load_sa2_ra(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    ra = ra_suffix(year)
    paths = [
        sas_table("sa2_to_{ra}.sas7bdat", year=year, base_dir=ref_dir),
        sas_table("asgs_to_{ra}.sas7bdat", year=year, base_dir=ref_dir),
        sas_table("sla_to_{ra}.sas7bdat", year=year, base_dir=ref_dir),
    ]
    for path in paths:
        try:
            df = load_sas_table(path)
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError(paths[0])
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.decode("ascii")
    key_col = next((c for c in ["SA2", "ASGS", "SLA"] if c in df.columns), "SA2")
    ra_col = next((c for c in df.columns if c.lower() == ra.lower()), ra)
    return df.rename(columns={key_col: "SA2", ra_col: ra})[["SA2", ra]]


def _load_icu_list(ref_dir: Path, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    df = pd.read_sas(
        sas_table(
            "nep{suffix}_icu_paed_eligibility_list.sas7bdat",
            year=year,
            base_dir=ref_dir,
        )
    )
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.decode("ascii")
    apc_col = next(c for c in df.columns if c.startswith("APCID"))
    return df.rename(columns={apc_col: "APCID"})[["APCID", "_est_eligible_paed_flag"]]


def _load_multi_prov_adj(ref_dir: Path, year: str) -> float:
    path = sas_table(
        "nep{suffix}_op_multi_prov_adj.sas7bdat",
        year=year,
        base_dir=ref_dir,
    )
    try:
        df = load_sas_table(path)
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.decode("ascii")
        return float(df.loc[0, "adj_multiprov"])
    except _OPTIONAL_REFERENCE_ERRORS:
        return 0.0
    except Exception:
        return 0.0


def _load_ind_adj(ref_dir: Path, year: str) -> pd.DataFrame:
    path = sas_table(
        "nep{suffix}_aa_mh_sa_na_adj_ind.sas7bdat",
        year=year,
        base_dir=ref_dir,
    )
    try:
        df = load_sas_table(path)
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.decode("ascii")
        return df
    except _OPTIONAL_REFERENCE_ERRORS:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def _load_pat_rem_adj(ref_dir: Path, year: str) -> pd.DataFrame:
    path = sas_table(
        "nep{suffix}_aa_mh_sa_na_adj_rem.sas7bdat",
        year=year,
        base_dir=ref_dir,
    )
    try:
        df = load_sas_table(path)
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.decode("ascii")
        return df
    except _OPTIONAL_REFERENCE_ERRORS:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def _load_treat_rem_adj(ref_dir: Path, year: str) -> pd.DataFrame:
    path = sas_table(
        "nep{suffix}_aa_mh_sa_na_adj_treat_rem.sas7bdat",
        year=year,
        base_dir=ref_dir,
    )
    try:
        df = load_sas_table(path)
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.decode("ascii")
        return df
    except _OPTIONAL_REFERENCE_ERRORS:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def calculate_outpatients(
    df: pd.DataFrame,
    params: OutpatientParams,
    *,
    year: str = _DEFAULT_YEAR,
    ref_dir: Path | None = None,
) -> pd.DataFrame:
    """Calculate NWAU25 for outpatient activity using resolved reference data."""
    validate_tier_2_input(
        tuple(df.columns),
        year=year,
        version=get_classification_version("tier_2", year),
    )
    if ref_dir is None:
        ref_dir = sas_ref_dir(year)
    suffix = str(year)[-2:]
    nwau_col = f"NWAU{suffix}"
    ra = ra_suffix(year)
    ra_year = ra[2:]

    weights = _load_weights(ref_dir, year)
    merged = df.merge(weights, on="TIER2_CLINIC", how="left")

    try:
        adj_multi_val = _load_multi_prov_adj(ref_dir, year)
    except (FileNotFoundError, KeyError, ValueError):
        adj_multi_val = 0.0
    adj_multi_series = merged.get(
        "adj_multiprov",
        pd.Series(adj_multi_val, index=merged.index),
    ).fillna(adj_multi_val)
    merged["adj_multiprov"] = adj_multi_series

    # --------------------------------------------------------------
    # Load adjustment tables (primarily for caching)
    # --------------------------------------------------------------
    _load_ind_adj(ref_dir, year)
    _load_pat_rem_adj(ref_dir, year)
    _load_treat_rem_adj(ref_dir, year)
    adj_multi = adj_multi_val
    ind_df = _load_ind_adj(ref_dir, year)

    adj_multi_val = adj_multi
    merged["adj_multiprov"] = merged.get(
        "adj_multiprov", pd.Series(adj_multi_val, index=merged.index)
    ).fillna(adj_multi_val)
    adj_multi_series = merged["adj_multiprov"].fillna(adj_multi_val)

    adj_multi = _load_multi_prov_adj(ref_dir, year)
    ind_df = _load_ind_adj(ref_dir, year)
    pat_rem = _load_pat_rem_adj(ref_dir, year)
    treat_rem = _load_treat_rem_adj(ref_dir, year)
    merged["adj_multiprov"] = merged.get("adj_multiprov", adj_multi).fillna(adj_multi)
    adj_multi_series = merged["adj_multiprov"].fillna(adj_multi)

    # --------------------------------------------------------------
    # Establishment remoteness lookups
    # --------------------------------------------------------------
    if params.est_remoteness_option == 1:
        hosp_col = f"_hosp_ra_{ra_year}"
        if "APCID" in merged.columns:
            try:
                hosp_df = _load_hospital_ra(ref_dir, year)
                merged = merged.merge(hosp_df, on="APCID", how="left")
            except (FileNotFoundError, KeyError, ValueError):
                merged[hosp_col] = np.nan
        else:
            merged[hosp_col] = np.nan

        pat_pc = next(
            (c for c in ["PAT_POSTCODE", "POSTCODE"] if c in merged.columns),
            None,
        )
        pat_sa2 = next(
            (c for c in ["PAT_SA2", "SA2"] if c in merged.columns),
            None,
        )

        pat_ra_col = f"PAT_{ra}"
        sa2_ra_col = f"SA2_{ra}"
        hosp_ra_col = hosp_col
        if pat_pc:
            try:
                pc_df = _load_postcode_ra(ref_dir, year)
                ra_col = next(
                    (c for c in pc_df.columns if c.lower() == ra.lower()),
                    ra,
                )
                pc_df = pc_df.rename(columns={"POSTCODE": pat_pc, ra_col: pat_ra_col})
                pc_df = pc_df.rename(columns={"POSTCODE": pat_pc, ra_col: pat_ra_col})
                merged = merged.merge(
                    pc_df[[pat_pc, pat_ra_col]],
                    on=pat_pc,
                    how="left",
                )
            except (FileNotFoundError, KeyError, ValueError):
                merged[pat_ra_col] = np.nan
        else:
            merged[pat_ra_col] = np.nan

        if pat_sa2:
            try:
                sa2_df = _load_sa2_ra(ref_dir, year)
                key_col = next(
                    (c for c in ["SA2", "ASGS", "SLA"] if c in sa2_df.columns),
                    None,
                )
                ra_col = next(
                    (c for c in sa2_df.columns if c.lower() == ra.lower()),
                    ra,
                )
                if key_col:
                    sa2_df = sa2_df.rename(
                        columns={key_col: pat_sa2, ra_col: sa2_ra_col}
                    )
                    merged = merged.merge(
                        sa2_df[[pat_sa2, sa2_ra_col]],
                        on=pat_sa2,
                        how="left",
                    )
                else:
                    merged[sa2_ra_col] = np.nan
            except (FileNotFoundError, KeyError, ValueError):
                merged[sa2_ra_col] = np.nan
        else:
            merged[sa2_ra_col] = np.nan

        merged["_pat_remoteness"] = (
            merged[sa2_ra_col]
            .combine_first(merged[pat_ra_col])
            .combine_first(merged[hosp_ra_col])
        )
        merged["_treat_remoteness"] = merged[hosp_ra_col].fillna(0)
    else:
        merged["_pat_remoteness"] = merged.get(
            "PAT_REMOTENESS", merged.get("EST_REMOTENESS", np.nan)
        )
        merged["_treat_remoteness"] = merged.get("EST_REMOTENESS", 0)

    if params.data_type == 1:
        service = pd.to_datetime(merged.get("SERVICE_DATE"))
        birth = pd.to_datetime(merged.get("BIRTH_DATE"))
        age = np.floor(((service - birth).dt.days) / 365.25)
        merged["_pat_age_years"] = age

        if params.paed_option == 1 and "APCID" in merged.columns:
            try:
                paed_df = _load_icu_list(ref_dir, year)
                merged = merged.merge(paed_df, on="APCID", how="left")
            except (FileNotFoundError, KeyError, ValueError):
                merged["_est_eligible_paed_flag"] = 0
        else:
            merged["_est_eligible_paed_flag"] = merged.get("EST_ELIGIBLE_PAED_FLAG", 0)

        est_flag = merged.get("_est_eligible_paed_flag", 0)
        merged["_pat_eligible_paed_flag"] = (
            (age >= 0) & (age <= 17) & (est_flag == 1)
        ).astype(int)
    else:
        merged["_pat_age_years"] = np.nan
        merged["_pat_eligible_paed_flag"] = 0

    merged["_pat_remoteness"] = merged.get(
        "PAT_REMOTENESS", merged.get("EST_REMOTENESS", 0)
    )
    ind_col = merged.get("INDSTAT", pd.Series(0, index=merged.index))
    merged["_pat_ind_flag"] = ind_col.isin([1, 2, 3]).astype(int)

    if not ind_df.empty:
        merged = merged.merge(ind_df, on="_pat_ind_flag", how="left")
    if not pat_rem.empty:
        merged = merged.merge(pat_rem, on="_pat_remoteness", how="left")
    if not treat_rem.empty:
        merged = merged.merge(treat_rem, on="_treat_remoteness", how="left")

    merged["adj_indigenous"] = merged.get(
        "adj_indigenous", pd.Series(0, index=merged.index)
    ).fillna(0)
    merged["adj_remoteness"] = merged.get(
        "adj_remoteness", pd.Series(0, index=merged.index)
    ).fillna(0)
    merged["adj_treat_remoteness"] = merged.get(
        "adj_treat_remoteness", pd.Series(0, index=merged.index)
    ).fillna(0)
    if params.data_type == 1:
        try:
            ind_adj = _load_ind_adj(ref_dir, year)
            merged = merged.merge(ind_adj, on="_pat_ind_flag", how="left")
        except Exception:
            merged["adj_indigenous"] = 0
        try:
            rem_adj = _load_pat_rem_adj(ref_dir, year)
            merged = merged.merge(rem_adj, on="_pat_remoteness", how="left")
        except Exception:
            merged["adj_remoteness"] = 0
    merged["adj_indigenous"] = merged.get(
        "adj_indigenous", pd.Series(0, index=merged.index)
    ).fillna(0)
    merged["adj_remoteness"] = merged.get(
        "adj_remoteness", pd.Series(0, index=merged.index)
    ).fillna(0)
    try:
        ind_df = _load_ind_adj(ref_dir, year)
        if not ind_df.empty:
            merged = merged.merge(ind_df, on="_pat_ind_flag", how="left")
    except Exception:
        if "adj_indigenous" not in merged.columns:
            merged["adj_indigenous"] = 0
    pat_rem_df = pd.DataFrame()
    treat_rem_df = pd.DataFrame()
    try:
        pat_rem_df = _load_pat_rem_adj(ref_dir, year)
        if not pat_rem_df.empty:
            merged = merged.merge(pat_rem_df, on="_pat_remoteness", how="left")
    except Exception:
        if "adj_remoteness" not in merged.columns:
            merged["adj_remoteness"] = 0
    try:
        treat_rem_df = _load_treat_rem_adj(ref_dir, year)
        if not treat_rem_df.empty:
            merged = merged.merge(treat_rem_df, on="_treat_remoteness", how="left")
    except Exception:
        if "adj_treat_remoteness" not in merged.columns:
            merged["adj_treat_remoteness"] = 0
    if params.indigenous_distribution and not ind_df.empty:
        imputed = impute_adjustment(
            ind_df,
            "_pat_ind_flag",
            "adj_indigenous",
            params.indigenous_distribution,
        )
        merged["adj_indigenous"] = merged["adj_indigenous"].fillna(imputed)
    if params.remoteness_distribution and not pat_rem_df.empty:
        imputed = impute_adjustment(
            pat_rem_df,
            "_pat_remoteness",
            "adj_remoteness",
            params.remoteness_distribution,
        )
        merged["adj_remoteness"] = merged["adj_remoteness"].fillna(imputed)
    if params.remoteness_distribution and not treat_rem_df.empty:
        imputed = impute_adjustment(
            treat_rem_df,
            "_treat_remoteness",
            "adj_treat_remoteness",
            params.remoteness_distribution,
        )
        merged["adj_treat_remoteness"] = merged["adj_treat_remoteness"].fillna(imputed)
    for col in ["adj_indigenous", "adj_remoteness", "adj_treat_remoteness"]:
        merged[col] = merged[col].fillna(0)

    if "FUNDSC" in merged.columns:
        out_scope = ~merged["FUNDSC"].isin(params.inscope_funding_sources)
    else:
        out_scope = merged.get("INSCOPE_FLAG", 1) == 0

    error_code = np.select(
        [merged["clinic_pw"].isna(), out_scope, merged["clinic_pw"] == 0],
        [3, 2, 1],
        default=0,
    )
    merged["Error_Code"] = error_code.astype(int)

    multiprov_flag = merged.get("PAT_MULTIPROV_FLAG", 0)
    cond1 = (
        (merged["_pat_eligible_paed_flag"] == 1)
        & (multiprov_flag == 1)
        & ~merged["TIER2_CLINIC"].isin([20.48, 20.56, 40.62])
    )
    cond2 = (
        (merged["_pat_eligible_paed_flag"] == 1)
        & (multiprov_flag == 1)
        & merged["TIER2_CLINIC"].isin([20.48, 20.56, 40.62])
    )
    cond3 = (
        (merged["_pat_eligible_paed_flag"] != 1)
        & (multiprov_flag == 1)
        & ~merged["TIER2_CLINIC"].isin([20.48, 20.56, 40.62])
    )
    cond4 = (merged["_pat_eligible_paed_flag"] == 1) & (multiprov_flag != 1)

    w01 = merged["clinic_pw"]

    if params.data_type == 1:
        base = 1 + merged.get("adj_indigenous", 0) + merged.get("adj_remoteness", 0)
        treat = 1 + merged.get("adj_treat_remoteness", 0)
        gwau = np.select(
            [cond1, cond2, cond3, cond4],
            [
                w01 * merged["tier2_adj_paed"] * (base + adj_multi) * treat,
                w01 * merged["tier2_adj_paed"] * base * treat,
                w01 * (base + adj_multi) * treat,
                w01 * merged["tier2_adj_paed"] * base * treat,
            ],
            default=w01 * base * treat,
        )
    else:
        treat = 1 + merged.get("adj_treat_remoteness", 0)
        counts = (
            merged.get("GROUP_EVENT_COUNT", 0).fillna(0)
            + merged.get("INDIV_EVENT_COUNT", 0).fillna(0)
            + merged.get(
                "GROUP_EVENT_COUNT",
                pd.Series(0, index=merged.index),
            ).fillna(0)
            + merged.get(
                "INDIV_EVENT_COUNT",
                pd.Series(0, index=merged.index),
            ).fillna(0)
        )
        counts_multi = counts + merged.get(
            "MULTI_DISP_CONF_COUNT",
            pd.Series(0, index=merged.index),
        ).fillna(0)
        gwau = np.select(
            [
                (multiprov_flag == 1)
                & ~merged["TIER2_CLINIC"].isin([20.48, 20.56, 40.62]),
                (multiprov_flag == 1)
                & merged["TIER2_CLINIC"].isin([20.48, 20.56, 40.62]),
            ],
            [w01 * (1 + adj_multi) * treat * counts_multi, w01 * treat * counts_multi],
            default=w01 * treat * counts,
        )

    nwau = np.where(merged["Error_Code"] > 0, 0, gwau)
    merged[nwau_col] = nwau

    result = merged
    if not params.debug_mode:
        result = result.drop(columns=[c for c in result.columns if c.startswith("_")])
    if params.clear_data:
        clear_reference_cache()

    return result
