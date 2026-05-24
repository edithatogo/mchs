from collections.abc import Sequence

import pandas as pd


def calculate_adjusted_nwau(
    df: pd.DataFrame,
    *,
    base_nwau_col: str = "nwau25",
    weight_col: str = "_w01",
    ahr_weight_col: str | None = None,
    hac_flag_cols: Sequence[str] | None = None,
    hac_adj_cols: Sequence[str] | None = None,
    hac_point_cols: Sequence[str] | None = None,
    ahr_flag_cols: Sequence[str] | None = None,
    ahr_adj_cols: Sequence[str] | None = None,
    covid_flag_col: str | None = None,
    error_col: str | None = None,
    complexity_df: pd.DataFrame | None = None,
    drop_intermediate: bool = False,
) -> pd.DataFrame:
    """Combine base NWAU with HAC/AHR risk adjustments.

    Parameters
    ----------
    df
        Input table containing base NWAU and adjustment columns.
    base_nwau_col : str, default ``"nwau25"``
        Column with the unadjusted NWAU amount.
    weight_col : str, default ``"_w01"``
        Column representing the underlying weight used for HAC adjustment.
    ahr_weight_col : str, optional
        If provided, the weight used for AHR adjustment. Defaults to
        ``weight_col`` when not supplied.
    hac_flag_cols, hac_adj_cols : sequence of str, optional
        Pairs of flag and adjustment columns for HAC categories. Each flag
        should be 1 when the category applies and 0 otherwise.
    hac_point_cols : sequence of str, optional
        Complexity point columns corresponding to each HAC category.
    ahr_flag_cols, ahr_adj_cols : sequence of str, optional
        Pairs of flag and adjustment columns for AHR categories.
    covid_flag_col : str, optional
        Column indicating COVID episodes. When set to ``1`` all adjustments are
        suppressed.
    error_col : str, optional
        Column used to zero HAC adjustments when non-zero.
    complexity_df
        Mapping of complexity score to risk category for each HAC.
    ahr_flag_cols, ahr_adj_cols : sequence of str, optional
        Pairs of flag and adjustment columns for AHR categories.
    drop_intermediate : bool, default ``False``
        When ``True`` intermediate adjustment columns are removed from the
        returned dataframe (mimicking the SAS ``DEBUG_MODE`` option).

    Returns
    -------
    tabular frame
        ``df`` with new columns ``nwau25_adjusted`` and risk adjustment
        diagnostics such as ``AHRgroup`` and ``HACgroup``. When
        ``complexity_df`` is supplied ``complexity`` and ``complexityGroup`` are
        also included.
    """
    result = df.copy()
    covid_flag = (
        result[covid_flag_col].fillna(0)
        if covid_flag_col and covid_flag_col in result.columns
        else 0
    )

    # ------------------------------------------------------------------
    # AHR risk adjustment
    # ------------------------------------------------------------------
    if ahr_flag_cols and ahr_adj_cols:
        if len(ahr_flag_cols) != len(ahr_adj_cols):
            raise ValueError("AHR flag and adjustment column counts differ")
        ahr_values = [
            result[adj].fillna(0) * result[flag].fillna(0)
            for flag, adj in zip(ahr_flag_cols, ahr_adj_cols, strict=True)
        ]
        ahr_df = pd.concat(ahr_values, axis=1)
        ahr_df.columns = list(ahr_adj_cols)
        ahr_adj = ahr_df.max(axis=1).fillna(0)
        ahr_group = ahr_df.idxmax(axis=1).str.extract(r"(\d+)")[0]
    else:
        ahr_adj = pd.Series(0, index=result.index)
        ahr_group = pd.Series("", index=result.index)

    if isinstance(covid_flag, pd.Series):
        ahr_adj = ahr_adj.where(covid_flag == 0, 0)
        ahr_group = ahr_group.where(covid_flag == 0, "")

    weight_ahr = result[ahr_weight_col] if ahr_weight_col else result[weight_col]
    result["riskAdjustment_AHR"] = weight_ahr.fillna(0) * ahr_adj
    result["AHRgroup"] = ahr_group

    # ------------------------------------------------------------------
    # HAC risk adjustment
    # ------------------------------------------------------------------
    hac_df: pd.DataFrame | None = None
    if hac_flag_cols and hac_adj_cols:
        if len(hac_flag_cols) != len(hac_adj_cols):
            raise ValueError("HAC flag and adjustment column counts differ")
        hac_values = [
            result[adj].fillna(0) * result[flag].fillna(0)
            for flag, adj in zip(hac_flag_cols, hac_adj_cols, strict=True)
        ]
        hac_df = pd.concat(hac_values, axis=1)
        hac_df.columns = list(hac_adj_cols)
        hac_adj = hac_df.max(axis=1).fillna(0)
        hac_group = hac_df.idxmax(axis=1).str.extract(r"(\d+)")[0]
    else:
        hac_adj = pd.Series(0, index=result.index)
        hac_group = pd.Series("", index=result.index)

    if isinstance(covid_flag, pd.Series):
        hac_adj = hac_adj.where(covid_flag == 0, 0)
        hac_group = hac_group.where(covid_flag == 0, "")

    if error_col and error_col in result.columns:
        hac_adj = hac_adj.where(result[error_col].fillna(0) == 0, 0)

    if (
        hac_point_cols
        and complexity_df is not None
        and hac_df is not None
        and hac_adj_cols
    ):
        if len(hac_point_cols) != len(hac_adj_cols):
            raise ValueError("HAC point and adjustment column counts differ")
        points_df = result[hac_point_cols]
        idx = hac_df.values.argmax(axis=1)
        complexity = points_df.to_numpy()[range(len(result)), idx]
        complexity_df_idx = complexity_df.set_index("complexity")
        cols = [f"HAC{int(c.split('hac_adj')[1]):02d}" for c in hac_adj_cols]
        group_vals = complexity_df_idx.loc[
            (complexity.round().clip(1, complexity_df_idx.index.max())).astype(int),
            cols,
        ].to_numpy()
        complexity_group = group_vals[range(len(result)), idx]
        result["complexity"] = complexity
        result["complexityGroup"] = complexity_group
    result["HACgroup"] = hac_group

    result["riskAdjustment_HAC"] = result[weight_col].fillna(0) * hac_adj

    # ------------------------------------------------------------------
    # Final NWAU calculation
    # ------------------------------------------------------------------
    adjusted = (
        result[base_nwau_col].fillna(0)
        - result["riskAdjustment_HAC"]
        - result["riskAdjustment_AHR"]
    ).clip(lower=0)
    result["nwau25_adjusted"] = adjusted

    if drop_intermediate:
        cols_to_drop = list(hac_flag_cols or []) + list(hac_adj_cols or [])
        cols_to_drop += list(ahr_flag_cols or []) + list(ahr_adj_cols or [])
        cols_to_drop += [weight_col]
        if ahr_weight_col:
            cols_to_drop.append(ahr_weight_col)
        cols_to_drop += [
            "riskAdjustment_HAC",
            "riskAdjustment_AHR",
            "AHRgroup",
            "HACgroup",
            "complexity",
            "complexityGroup",
        ]
        cols_to_drop = [c for c in cols_to_drop if c in result.columns]
        result = result.drop(columns=cols_to_drop)

    return result
