from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import lru_cache

import pandas as pd
import pyreadstat

from nwau_py.data.paths import sas_table
from nwau_py.utils import sas_ref_dir

_DEFAULT_YEAR = "2025"


@lru_cache
def load_hac_mapping(edition: str = "07", *, year: str = _DEFAULT_YEAR) -> pd.DataFrame:
    """Return diagnosis-to-HAC mapping for the given ICD edition and year."""
    ref_dir = sas_ref_dir(year)
    path = sas_table(f"hac_map_{edition}.sas7bdat", base_dir=ref_dir)
    df, _ = pyreadstat.read_sas7bdat(str(path))
    df["DDX"] = df["DDX"].astype(str)
    return df


def count_hac_diagnoses(
    diagnoses: Iterable[str], *, edition: str = "07", year: str = _DEFAULT_YEAR
) -> Mapping[str, int]:
    """Count HAC sub-condition occurrences for ``diagnoses``.

    Parameters
    ----------
    diagnoses:
        Iterable of diagnosis codes.
    edition:
        ICD-10-AM edition number used to select the mapping table.
    """
    df = load_hac_mapping(edition, year=year).set_index("DDX")
    counts: dict[str, int] = {str(col): 0 for col in df.columns if col != "DDX"}
    for code in diagnoses:
        if code in df.index:
            row = df.loc[code]
            for col, val in row.items():
                if pd.notna(val) and int(val) == 1:
                    counts[col] += 1
    return counts


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
