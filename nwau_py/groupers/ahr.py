"""Avoidable Hospital Readmission (AHR) Grouper in Python.

This module mirrors the SAS script ``Avoidable Hospital Readmission
Grouper 030.sas``. It loads the ICD-to-AHR mappings distributed with the
IHACPA SAS calculator and applies them to patient level data. The
grouper also exposes an interface to the LightGBM based scorer used by
IHACPA.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

import polars as pl
import pyreadstat

from nwau_py.scoring import score_readmission

AHR_THRESHOLD_DAYS = {
    "AHR030c01p01": 14,
    "AHR030c01p02": 7,
    "AHR030c01p03": 14,
    "AHR030c01p04": 14,
    "AHR030c01p05": 14,
    "AHR030c02p01": 7,
    "AHR030c02p02": 30,
    "AHR030c02p03": 7,
    "AHR030c02p04": 2,
    "AHR030c02p05": 2,
    "AHR030c02p06": 2,
    "_AHR030c02p06": 2,
    "AHR030c02p07": 90,
    "AHR030c02p08": 30,
    "AHR030c02p09": 2,
    "AHR030c02p10": 28,
    "AHR030c02p11": 2,
    "AHR030c03p01": 28,
    "AHR030c03p02": 28,
    "AHR030c03p03": 28,
    "AHR030c03p04": 28,
    "AHR030c03p05": 14,
    "AHR030c03p06": 28,
    "AHR030c04p01": 21,
    "AHR030c04p02": 14,
    "AHR030c04p03": 30,
    "AHR030c05p01": 90,
    "AHR030c06p01": 21,
    "AHR030c07p01": 2,
    "AHR030c08p01": 2,
    "AHR030c08p02": 4,
    "_AHR030c08p02": 4,
    "AHR030c08p03": 14,
    "AHR030c08p04": 14,
    "AHR030c09p01": 10,
    "AHR030c10p01": 30,
    "AHR030c10p02": 30,
    "AHR030c10p03": 14,
    "AHR030c10p04": 30,
    "AHR030c11p01": 14,
    "AHR030c12p01": 7,
}

_AGG_MAP = {
    "AHR030c01_flag": [f"AHR030c01p0{i}_flag" for i in range(1, 6)],
    "AHR030c02_flag": [
        "AHR030c02p01_flag",
        "AHR030c02p02_flag",
        "AHR030c02p03_flag",
        "AHR030c02p04_flag",
        "AHR030c02p05_flag",
        "AHR030c02p06_flag",
        "AHR030c02p07_flag",
        "AHR030c02p08_flag",
        "AHR030c02p09_flag",
        "AHR030c02p10_flag",
        "AHR030c02p11_flag",
    ],
    "AHR030c03_flag": [f"AHR030c03p0{i}_flag" for i in range(1, 7)],
    "AHR030c04_flag": [f"AHR030c04p0{i}_flag" for i in range(1, 4)],
    "AHR030c05_flag": ["AHR030c05p01_flag"],
    "AHR030c06_flag": ["AHR030c06p01_flag"],
    "AHR030c07_flag": ["AHR030c07p01_flag"],
    "AHR030c08_flag": [f"AHR030c08p0{i}_flag" for i in range(1, 5)],
    "AHR030c09_flag": ["AHR030c09p01_flag"],
    "AHR030c10_flag": [f"AHR030c10p0{i}_flag" for i in range(1, 5)],
    "AHR030c11_flag": ["AHR030c11p01_flag"],
    "AHR030c12_flag": ["AHR030c12p01_flag"],
}


def _parse_dt(v: Any) -> date:
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = str(v)[:10]
    return datetime.strptime(s, "%Y-%m-%d").date()


def load_ahr_maps(maps_dir: Path) -> dict[str, pl.DataFrame]:
    """Load all ``ahr_map_XX.sas7bdat`` files found in ``maps_dir`` using pyreadstat."""
    maps: dict[str, pl.DataFrame] = {}
    for path in sorted(maps_dir.glob("ahr_map_*.sas7bdat")):
        edition = path.stem.split("_")[-1]
        data, _ = pyreadstat.read_sas7bdat(str(path), output_format="dict")
        maps[edition] = pl.from_dict(data)
    return maps


def flag_diagnoses(
    episode_df: Any,
    maps: dict[str, Any],
    edition: str,
    diag_prefix: str = "ddx",
    onset_prefix: str = "onset",
) -> Any:
    """Flag diagnoses using the AHR mapping tables.

    ``episode_df`` must contain columns ``ddx1``-``ddx100`` and matching
    ``onset1``-``onset100`` values. Only diagnoses with onset value ``"2"``
    (condition arose in hospital) trigger flags.
    """
    is_pandas = (
        not isinstance(episode_df, pl.DataFrame)
        and hasattr(episode_df, "to_dict")
        and not hasattr(episode_df, "lazy")
    )
    if hasattr(episode_df, "to_polars"):
        df_pl = episode_df.to_polars()
    elif is_pandas:
        df_pl = pl.DataFrame(episode_df)
    else:
        df_pl = episode_df

    map_df = maps[edition]
    if hasattr(map_df, "to_polars"):
        map_df = map_df.to_polars()
    elif not isinstance(map_df, pl.DataFrame):
        map_df = pl.DataFrame(map_df)
    map_df = map_df.with_columns(
        pl.col("DDX").cast(pl.Utf8).str.strip_chars().str.to_uppercase()
    )
    flag_cols = [c for c in map_df.columns if c.startswith("AHR")]

    flag_code_sets = {
        col: set(map_df.filter(pl.col(col) > 0)["DDX"].to_list()) for col in flag_cols
    }

    pairs: list[tuple[str, str | None]] = []
    for i in range(1, 101):
        dcol = f"{diag_prefix}{i}"
        ocol = f"{onset_prefix}{i}"
        if dcol not in df_pl.columns:
            break
        pairs.append((dcol, ocol if ocol in df_pl.columns else None))

    row_active_codes: list[set[str]] = []
    for row in df_pl.iter_rows(named=True):
        codes = set()
        for dcol, ocol in pairs:
            code = row.get(dcol)
            if (
                code is not None
                and str(code).strip() != ""
                and str(code).strip() != "None"
            ):
                onset = row.get(ocol) if ocol is not None else None
                if onset is None or str(onset).strip() in {"2", "2.0"}:
                    codes.add(str(code).strip().upper())
        row_active_codes.append(codes)

    flag_data = {}
    for col in flag_cols:
        target_set = flag_code_sets[col]
        flag_data[col] = [
            1 if (codes & target_set) else 0 for codes in row_active_codes
        ]

    result_flags = pl.DataFrame(flag_data)
    out = pl.concat([df_pl, result_flags], how="horizontal")
    if is_pandas:
        from nwau_py import compat as pd

        return pd.DataFrame(out)
    return out


def past_admissions(episodes: Any, patient_col: str, date_col: str) -> Any:
    """Count admissions in the previous 365 days for each episode."""
    is_pandas = (
        not isinstance(episodes, pl.DataFrame)
        and hasattr(episodes, "to_dict")
        and not hasattr(episodes, "lazy")
    )
    if hasattr(episodes, "to_polars"):
        df_pl = episodes.to_polars()
    elif is_pandas:
        df_pl = pl.DataFrame(episodes)
    else:
        df_pl = episodes

    episodes_with_idx = df_pl.with_columns(
        __orig_idx=pl.arange(0, len(df_pl), dtype=pl.Int64)
    )
    episodes_sorted = episodes_with_idx.sort([patient_col, date_col])

    pids = episodes_sorted[patient_col].to_list()
    dates = [_parse_dt(v) for v in episodes_sorted[date_col].to_list()]
    orig_indices = episodes_sorted["__orig_idx"].to_list()

    counts_at_orig = [0] * len(df_pl)
    current_pid = None
    patient_start = 0
    for idx in range(len(pids)):
        pid = pids[idx]
        if pid != current_pid:
            current_pid = pid
            patient_start = idx
        curr_date = dates[idx]
        cnt = 0
        for k in range(patient_start, idx):
            delta_days = (curr_date - dates[k]).days
            if 0 < delta_days <= 365:
                cnt += 1
        counts_at_orig[orig_indices[idx]] = cnt

    if is_pandas:
        from nwau_py import compat as pd

        return pd.Series(counts_at_orig, index=getattr(episodes, "index", None))
    return pl.Series("adm_past_year", counts_at_orig)


def group_readmissions(
    episodes: Any,
    maps: dict[str, Any],
    edition: str,
    patient_col: str = "patient_id",
    adm_col: str = "adm_date",
    sep_col: str = "sep_date",
) -> Any:
    """Group episodes into AHR categories.

    The input must be sorted by ``patient_id`` and ``adm_date``. Diagnostic flags
    are derived using :func:`flag_diagnoses` and time between episodes determines
    whether a readmission occurred.
    """
    is_pandas = (
        not isinstance(episodes, pl.DataFrame)
        and hasattr(episodes, "to_dict")
        and not hasattr(episodes, "lazy")
    )

    df = flag_diagnoses(episodes, maps, edition)
    if hasattr(df, "to_polars"):
        df_pl = df.to_polars()
    elif is_pandas:
        df_pl = pl.DataFrame(df)
    else:
        df_pl = df
    df_pl = df_pl.sort([patient_col, adm_col])

    flags: dict[str, set[int]] = {c: set() for c in AHR_THRESHOLD_DAYS}
    ahr_times: list[int | None] = []
    prev_sep: date | None = None
    prev_pid = None

    rows = df_pl.iter_rows(named=True)
    for idx, row in enumerate(rows):
        pid = row[patient_col]
        if pid != prev_pid:
            prev_sep = None
        if prev_sep is not None:
            delta = (_parse_dt(row[adm_col]) - prev_sep).days
            ahr_times.append(delta)
            for col, days in AHR_THRESHOLD_DAYS.items():
                if row.get(col) == 1 and delta <= days:
                    flags[col].add(idx)
        else:
            ahr_times.append(None)
        prev_sep = _parse_dt(row[sep_col])
        prev_pid = pid

    new_cols = [pl.Series("ahr_time", ahr_times, dtype=pl.Int64)]
    for col in AHR_THRESHOLD_DAYS:
        target_indices = flags[col]
        col_flags = [1 if i in target_indices else 0 for i in range(len(df_pl))]
        new_cols.append(pl.Series(f"{col}_flag", col_flags, dtype=pl.Int64))

    # Past admissions
    past_adm_series = past_admissions(df_pl, patient_col, adm_col)
    if not isinstance(past_adm_series, pl.Series):
        past_adm_series = pl.Series("adm_past_year", past_adm_series.to_list())
    new_cols.append(past_adm_series.alias("adm_past_year"))

    df_pl = df_pl.with_columns(new_cols)

    # aggregate sub-condition flags
    agg_exprs = []
    for agg, sub in _AGG_MAP.items():
        cols = [c for c in sub if c in df_pl.columns]
        if cols:
            agg_exprs.append(pl.max_horizontal(cols).alias(agg))
    if agg_exprs:
        df_pl = df_pl.with_columns(agg_exprs)

    # overall AHR flag and count
    sub_cols = [
        c for sublist in _AGG_MAP.values() for c in sublist if c in df_pl.columns
    ]
    if sub_cols:
        df_pl = df_pl.with_columns(
            pl.max_horizontal(sub_cols).alias("ahr_flag"),
            pl.sum_horizontal(sub_cols).alias("ahrs"),
        )
    else:
        df_pl = df_pl.with_columns(
            pl.lit(0).alias("ahr_flag"),
            pl.lit(0).alias("ahrs"),
        )

    # risk adjustment scores
    scores = score_readmission(df_pl)
    if isinstance(scores, pl.DataFrame):
        df_pl = pl.concat([df_pl, scores], how="horizontal")
    elif hasattr(scores, "to_polars"):
        df_pl = pl.concat([df_pl, scores.to_polars()], how="horizontal")
    else:
        scores_pl = pl.DataFrame(scores)
        df_pl = pl.concat([df_pl, scores_pl], how="horizontal")

    if is_pandas:
        from nwau_py import compat as pd

        return pd.DataFrame(df_pl)
    return df_pl


__all__ = ["flag_diagnoses", "group_readmissions", "load_ahr_maps", "past_admissions"]
