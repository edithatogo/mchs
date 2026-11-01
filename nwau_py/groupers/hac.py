from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import lru_cache
from typing import Any

import polars as pl
import pyreadstat

from nwau_py.data.paths import sas_table
from nwau_py.utils import sas_ref_dir

_DEFAULT_YEAR = "2025"


@lru_cache
def load_hac_mapping_pl(
    edition: str = "07", *, year: str = _DEFAULT_YEAR
) -> pl.DataFrame:
    """Return diagnosis-to-HAC mapping as Polars DataFrame for ICD edition/year."""
    ref_dir = sas_ref_dir(year)
    path = sas_table(f"hac_map_{edition}.sas7bdat", base_dir=ref_dir)
    df_dict, _ = pyreadstat.read_sas7bdat(str(path), output_format="dict")
    df = pl.from_dict(df_dict)
    return df.with_columns(pl.col("DDX").cast(pl.Utf8).str.strip_chars())


@lru_cache
def load_hac_mapping(edition: str = "07", *, year: str = _DEFAULT_YEAR) -> Any:
    """Return diagnosis-to-HAC mapping as native Polars DataFrame."""
    return load_hac_mapping_pl(edition, year=year)


def count_hac_diagnoses(
    diagnoses: Iterable[str], *, edition: str = "07", year: str = _DEFAULT_YEAR
) -> Mapping[str, int]:
    """Count HAC sub-condition occurrences for ``diagnoses`` using vectorized Polars."""
    df = load_hac_mapping_pl(edition, year=year)
    diag_set = [str(d).strip() for d in diagnoses]
    condition_cols = [c for c in df.columns if c != "DDX"]

    matched = df.filter(pl.col("DDX").is_in(diag_set))
    if len(matched) == 0:
        return {col: 0 for col in condition_cols}

    sums = matched.select(
        [pl.col(c).fill_null(0).cast(pl.Int64).sum() for c in condition_cols]
    ).to_dicts()[0]
    return {str(k): int(v) for k, v in sums.items()}


def create_hac_flags(counts: Mapping[str, int]) -> Mapping[str, int]:
    """Aggregate sub-condition ``counts`` into HAC flags."""
    categories: dict[str, int] = {}
    for cond, val in counts.items():
        cat = cond[:9]  # e.g. ``hac032c04``
        categories[cat] = categories.get(cat, 0) + val
    flags = {f"{cat}_flag": int(total > 0) for cat, total in categories.items()}
    flags["hac032_flag"] = int(any(flags.values()))
    return flags


def flag_hacs(
    diagnoses: Iterable[str],
    procedures: Iterable[str] | None = None,
    *,
    edition: str = "07",
    year: str = _DEFAULT_YEAR,
) -> Mapping[str, int]:
    """Return HAC flags for ``diagnoses``.

    ``procedures`` is accepted for API compatibility but is not used as
    the current implementation only relies on diagnosis codes.
    """
    counts = count_hac_diagnoses(diagnoses, edition=edition, year=year)
    return create_hac_flags(counts)
