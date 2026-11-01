from collections.abc import Mapping
from pathlib import Path
from typing import Any

import numpy as np
import polars as pl

# Mapping from NEP/NWAU pricing year to the corresponding
# remoteness area (RA) classification year.  The mapping is
# derived from the directory names of the archived SAS
# calculators under ``archive/sas``.
RA_VERSION = {
    # 2025 onwards use the 2021 remoteness classification
    "2025": "2021",
    "2024": "2021",
    # Editions 2020-2023 reference the 2016 remoteness areas
    "2023": "2016",
    "2022": "2016",
    "2021": "2016",
    "2020": "2016",
    # The 2014-2019 calculators use the 2011 remoteness areas
    "2019": "2011",
    "2018": "2011",
    "2017": "2011",
    "2016": "2011",
    "2015": "2011",
    "2014": "2011",
    # Earlier editions fall back to the 2006 classification
    "2013": "2006",
}


def sas_ref_dir(year: str = "2025") -> Path:
    """Return path to SAS calculators for a given year.

    Parameters
    ----------
    year:
        The NEP/NWAU edition year, e.g. ``"2025"``.

    The folder structure of archived SAS releases has changed over the years.
    ``sas_ref_dir`` therefore searches for possible directory patterns and
    returns the first match.
    """
    suffix = str(year)[-2:]
    base = Path("archive") / "sas"

    patterns = [
        f"NEP{suffix}_SAS_NWAU_calculator",
        f"NWAU{suffix}_SAS_Calculator",
        f"NEP{suffix} SAS NWAU Calculator",
    ]

    for pattern in patterns:
        candidate = base / pattern
        if candidate.exists():
            # Look for a subdirectory containing the calculator tables.  The
            # name has varied between releases (e.g. ``calculators``,
            # ``Calculator``, ``01 Calculators``).
            for sub in candidate.iterdir():
                if sub.is_dir() and "calculator" in sub.name.lower():
                    return sub
            return candidate

    raise FileNotFoundError(f"No SAS reference directory found for year {year}")


def ra_suffix(year: str = "2025") -> str:
    """Return the remoteness area suffix for ``year``.

    ``ra2021`` applies from the 2024 edition onwards. ``ra2016`` covers 2020
    through 2023.  Editions from 2014 through 2019 use ``ra2011`` while older
    calculators rely on ``ra2006``.
    """
    year_int = int(year)
    if year_int >= 2024:
        return "ra2021"
    if year_int >= 2020:
        return "ra2016"
    if year_int >= 2014:
        return "ra2011"
    return "ra2006"


def impute_adjustment(
    table: Any,
    key_col: str,
    value_col: str,
    distribution: Mapping[Any, float],
) -> float:
    """Return a weighted average adjustment for missing values.

    Parameters
    ----------
    table:
        Adjustment table containing ``key_col`` and ``value_col`` columns.
    key_col:
        Column with the adjustment key, e.g. ``"_pat_remoteness"``.
    value_col:
        Column with the adjustment value.
    distribution:
        Mapping from key values to population proportions.

    Returns
    -------
    float
        Weighted average of ``value_col`` using ``distribution`` as weights.
        Returns ``0.0`` when no keys overlap.
    """
    if table is None or len(table) == 0:
        return 0.0

    if isinstance(table, pl.DataFrame):
        keys = table[key_col].to_list()
        vals = table[value_col].to_list()
    elif hasattr(table, "to_dict"):
        keys = list(table[key_col])
        vals = list(table[value_col])
    else:
        return 0.0

    mapping = dict(zip(keys, vals, strict=False))
    total = 0.0
    for k, prop in distribution.items():
        if k in mapping:
            val = mapping[k]
            if val is not None and not (isinstance(val, float) and np.isnan(val)):
                total += float(prop) * float(val)
    return float(total)
