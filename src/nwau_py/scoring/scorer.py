from __future__ import annotations

from typing import Any

import lightgbm as lgb
import numpy as np
import polars as pl

from nwau_py.utils import sas_ref_dir

_DEFAULT_YEAR = "2025"


def _model_vars(n: int, risk_factors: pl.DataFrame) -> list[str]:
    """Return list of risk factors for the ``n``th readmission category."""
    col_vals = risk_factors[str(n)].drop_nulls().to_list()
    ret = [str(x) for x in col_vals if str(x) != "nan"]
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


def _rescale_to_points(x: np.ndarray, data_min: float, data_max: float) -> np.ndarray:
    """Scale ``x`` to the range 1..100 given ``data_min`` and ``data_max``."""
    return np.clip((((x - data_min) / (data_max - data_min)) * 99 + 1), 1, 100)


def _load_resources(
    year: str = _DEFAULT_YEAR,
) -> tuple[
    pl.DataFrame,
    dict[int, lgb.Booster],
    pl.DataFrame,
    pl.DataFrame,
    pl.DataFrame,
    set[str],
]:
    base_dir = sas_ref_dir(year)
    models_dir = base_dir / "models"
    params_dir = base_dir / "params"
    risk_factors = pl.read_csv(models_dir / "risk_factors.csv")
    models = {
        i: lgb.Booster(
            model_file=str(models_dir / f"model_4year_sta_readm{i}_90_limited.txt")
        )
        for i in range(1, 13)
    }
    scaling_params = pl.read_csv(params_dir / "scaling_params.csv")
    cutoffs = pl.read_csv(params_dir / "cutoffs.csv")
    dampening = pl.read_csv(params_dir / "dampening.csv")
    model_vars_union = set()
    for i in range(1, 13):
        col_vals = risk_factors[str(i)].drop_nulls().to_list()
        model_vars_union.update(str(x) for x in col_vals if str(x) != "nan")
    return risk_factors, models, scaling_params, cutoffs, dampening, model_vars_union


def score_readmission(df: Any, *, year: str = _DEFAULT_YEAR) -> Any:
    """Score readmission risk for ``df``.

    Parameters
    ----------
    df : :class:`polars.DataFrame` or :class:`pandas.DataFrame`
        Input dataframe containing the variables required for the models.

    Returns
    -------
    :class:`polars.DataFrame` or :class:`pandas.DataFrame`
        Dataframe containing ``risk_category1`` .. ``risk_category12`` and
        ``dampening1`` .. ``dampening12`` columns.
    """
    is_pandas = (
        not isinstance(df, pl.DataFrame)
        and hasattr(df, "to_dict")
        and not hasattr(df, "lazy")
    )
    if hasattr(df, "to_polars"):
        data = df.to_polars()
    elif is_pandas:
        data = pl.DataFrame(df)
    else:
        data = df.clone()

    data = data.rename({c: c.lower() for c in data.columns})

    (
        risk_factors,
        models,
        scaling_params,
        cutoffs,
        dampening,
        model_vars_union,
    ) = _load_resources(year)

    if "drg11_type" in data.columns:
        data = data.with_columns(
            (pl.col("drg11_type") == "M").cast(pl.Int8).alias("drg11_type_m")
        )
    if "an110mdc_ra" in data.columns:
        data = data.with_columns(
            pl.col("an110mdc_ra")
            .cast(pl.Utf8)
            .str.replace(".", "99", literal=True)
            .cast(pl.Int64)
            .alias("an110mdc_ra")
        )

    col_exprs = []
    for col in model_vars_union:
        if col not in data.columns:
            col_exprs.append(pl.lit(0).cast(pl.Int64).alias(col))
        else:
            col_exprs.append(pl.col(col).cast(pl.Int64).alias(col))
    if col_exprs:
        data = data.with_columns(col_exprs)

    results_dict: dict[str, np.ndarray] = {}

    for i in range(1, 13):
        vars_i = _model_vars(i, risk_factors)
        arr = data.select(vars_i).to_numpy()
        probs = models[i].predict(arr)
        log_probs = np.log(probs)
        points = _rescale_to_points(
            x=log_probs,
            data_min=float(scaling_params["mins"][i - 1]),
            data_max=float(scaling_params["maxs"][i - 1]),
        )
        c0 = float(cutoffs[str(i)][0])
        c1 = float(cutoffs[str(i)][1])
        d0 = float(dampening[str(i)][0])
        d1 = float(dampening[str(i)][1])
        d2 = float(dampening[str(i)][2])

        conditions = [
            points < c0,
            (points >= c0) & (points < c1),
            points >= c1,
        ]
        choices = [d0, d1, d2]
        choices_cat = [0.0, 1.0, 2.0]

        results_dict[f"readm_points{i}"] = points
        results_dict[f"dampening{i}"] = np.select(conditions, choices, default=np.nan)
        results_dict[f"risk_category{i}"] = np.select(
            conditions, choices_cat, default=np.nan
        )

    results = pl.DataFrame(results_dict)
    if is_pandas:
        from nwau_py import compat as pd

        return pd.DataFrame(results)
    return results


__all__ = ["score_readmission"]
