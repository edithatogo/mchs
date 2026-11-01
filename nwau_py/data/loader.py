"""Data loading utilities for NWAU project"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import polars as pl

try:
    import pandas as pd
except ImportError:
    from nwau_py import compat as pd

if not hasattr(pl.DataFrame, "empty"):
    setattr(pl.DataFrame, "empty", property(lambda self: self.is_empty()))  # noqa: B010

try:  # pragma: no cover - optional dependency
    import pyreadstat
except (
    ImportError
) as exc:  # pragma: no cover - pyreadstat is optional in some environments
    pyreadstat = None
    _PYREADSTAT_IMPORT_ERROR: ImportError | None = exc
else:
    _PYREADSTAT_IMPORT_ERROR = None

try:
    import pyarrow  # noqa: F401

    _PARQUET_SUPPORTED = True
    _PYARROW_IMPORT_ERROR: ImportError | None = None
except ImportError as exc:  # pragma: no cover - pyarrow is optional
    _PARQUET_SUPPORTED = False
    _PYARROW_IMPORT_ERROR = exc


def clear_reference_cache(cache_dir: str | Path = ".cache") -> None:
    shutil.rmtree(cache_dir, ignore_errors=True)


def load_sas_table(
    path: str | Path,
    cache: bool = True,
    cache_format: str = "parquet",
    cache_dir: str | Path = ".cache",
    force: bool = False,
    as_pandas: bool = False,
) -> Any:
    """Load a SAS ``.sas7bdat`` table as a native Polars DataFrame.

    Parameters
    ----------
    path:
        Path to the ``.sas7bdat`` file.
    cache:
        Whether to cache the loaded table.
    cache_format:
        ``"parquet"`` or ``"csv"``. If ``"parquet"`` is requested but
        ``pyarrow`` is not installed the loader falls back to ``"csv"``.
    cache_dir:
        Directory where cache files are stored.
    force:
        If ``True`` the SAS file will be read even if a cached version exists.
    as_pandas:
        Compatibility flag for callers requiring a legacy pandas frame.
    """
    path = Path(path)
    cache_dir = Path(cache_dir)
    if cache_format == "parquet" and not _PARQUET_SUPPORTED:
        cache_format = "csv"
    ext_map = {"parquet": ".parquet", "csv": ".csv"}
    if cache_format not in ext_map:
        raise ValueError("cache_format must be 'parquet' or 'csv'")
    if cache_format == "parquet" and not _PARQUET_SUPPORTED:
        cache_format = "csv"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{path.stem}{ext_map[cache_format]}"

    if cache and cache_path.exists() and not force:
        if cache_format == "parquet":
            df = pl.read_parquet(cache_path)
        else:
            df = pl.read_csv(cache_path)
        return pd.DataFrame(df) if as_pandas else df

    if pyreadstat is None:  # pragma: no cover - dependency guard
        raise ImportError(
            "pyreadstat is required to read SAS files when no cache exists"
        ) from _PYREADSTAT_IMPORT_ERROR

    try:
        raw_df, _ = pyreadstat.read_sas7bdat(str(path), output_format="dict")
        df = pl.from_dict(raw_df)
    except Exception:
        raw_df, _ = pyreadstat.read_sas7bdat(str(path))
        if hasattr(raw_df, "columns"):
            df = pd.DataFrame(raw_df).to_polars()
        else:
            df = pl.DataFrame(raw_df)

    if cache:
        if cache_format == "parquet":
            df.write_parquet(cache_path)
        else:
            df.write_csv(cache_path)
    return pd.DataFrame(df) if as_pandas else df
