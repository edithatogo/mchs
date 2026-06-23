"""Data loading utilities for NWAU project"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

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
) -> pd.DataFrame:
    """Load a SAS ``.sas7bdat`` table.

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
            return pd.read_parquet(cache_path)
        else:
            return pd.read_csv(cache_path)

    if pyreadstat is None:  # pragma: no cover - dependency guard
        raise ImportError(
            "pyreadstat is required to read SAS files when no cache exists"
        ) from _PYREADSTAT_IMPORT_ERROR

    df, _ = pyreadstat.read_sas7bdat(str(path))

    if cache:
        if cache_format == "parquet":
            df.to_parquet(cache_path, index=False)
        else:
            df.to_csv(cache_path, index=False)
    return df
