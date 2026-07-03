from __future__ import annotations

import lightgbm as lgb
import numpy as np
import pandas as pd

from nwau_py.utils import sas_ref_dir

_DEFAULT_YEAR = "2025"


def _model_vars(n: int, risk_factors_df: pd.DataFrame) -> list[str]:
    """Return list of risk factors for the ``n``th readmission category."""
    ret = [x for x in risk_factors_df[str(n)].dropna().tolist() if str(x) != "nan"]
    common = [
        "an110mdc_ra",
        "agegroup_rm",
        "flag_emergency",
        "pat_remoteness",
        "indstat_flag",
        "count_proc",
        "adm_past_year",
    ]
    for risk in common:
        if risk not in ret:
            ret.append(risk)
    return ret


def _rescale_to_points(x: pd.Series, data_min: float, data_max: float) -> pd.Series:
    """Scale ``x`` to the range 1..100 given ``data_min`` and ``data_max``."""
    return (((x - data_min) / (data_max - data_min)) * 99 + 1).clip(1, 100)


def _load_resources(
    year: str = _DEFAULT_YEAR,
) -> tuple[
    pd.DataFrame,
    dict[int, lgb.Booster],
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    set[str],
]:
    base_dir = sas_ref_dir(year)
    models_dir = base_dir / "models"
    params_dir = base_dir / "params"
    risk_factors = pd.read_csv(models_dir / "risk_factors.csv", index_col=0)
    models = {
        i: lgb.Booster(
            model_file=str(models_dir / f"model_4year_sta_readm{i}_90_limited.txt")
        )
        for i in range(1, 13)
    }
    scaling_params = pd.read_csv(params_dir / "scaling_params.csv", index_col=0)
    cutoffs = pd.read_csv(params_dir / "cutoffs.csv", index_col=0)
    dampening = pd.read_csv(params_dir / "dampening.csv", index_col=0)
    model_vars_union = set().union(
        *(risk_factors[str(i)].dropna().tolist() for i in range(1, 13))
    )
    return risk_factors, models, scaling_params, cutoffs, dampening, model_vars_union


def score_readmission(df: pd.DataFrame, *, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    """Score readmission risk for ``df``.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        Input dataframe containing the variables required for the models.

    Returns
    -------
    :class:`pandas.DataFrame`
        Dataframe containing ``risk_category1`` .. ``risk_category12`` and
        ``dampening1`` .. ``dampening12`` columns.
    """
    (
        risk_factors,
        models,
        scaling_params,
        cutoffs,
        dampening,
        model_vars_union,
    ) = _load_resources(year)

    data = df.copy()
    data.columns = data.columns.str.lower()

    if "drg11_type" in data.columns:
        data["drg11_type_m"] = (data["drg11_type"] == "M").astype(np.int8)
    if "an110mdc_ra" in data.columns:
        data["an110mdc_ra"] = data["an110mdc_ra"].replace(".", "99")

    for col in model_vars_union:
        if col not in data.columns:
            data[col] = 0
        data[col] = data[col].astype(np.int64)

    for col in data.columns:
        if col not in {"count_proc", "adm_past_year"}:
            data[col] = data[col].astype("category")
        else:
            data[col] = data[col].astype(np.int32)

    results = pd.DataFrame(index=data.index)

    for i in range(1, 13):
        vars_i = _model_vars(i, risk_factors)
        probs = models[i].predict(data[vars_i])
        log_probs = np.log(probs)
        points = _rescale_to_points(
            x=log_probs,
            data_min=scaling_params.loc[i, "mins"],
            data_max=scaling_params.loc[i, "maxs"],
        )
        conditions = [
            points < cutoffs.iloc[0, i - 1],
            (points >= cutoffs.iloc[0, i - 1]) & (points < cutoffs.iloc[1, i - 1]),
            points >= cutoffs.iloc[1, i - 1],
        ]
        choices = [
            dampening.iloc[0, i - 1],
            dampening.iloc[1, i - 1],
            dampening.iloc[2, i - 1],
        ]
        choices_cat = [0, 1, 2]
        results[f"readm_points{i}"] = points
        results[f"dampening{i}"] = np.select(conditions, choices, default=np.nan)
        results[f"risk_category{i}"] = np.select(
            conditions, choices_cat, default=np.nan
        )

    return results


__all__ = ["score_readmission"]
