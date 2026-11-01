"""Unit tests covering data loader and ed conversion functions."""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

from nwau_py import compat as pd
from nwau_py.calculators import ed
from nwau_py.data.loader import clear_reference_cache, load_sas_table


def test_loader_cache_and_validation(tmp_path: Path):
    cache_dir = tmp_path / "test_cache"

    with pytest.raises(ValueError, match="cache_format must be 'parquet' or 'csv'"):
        load_sas_table("fake.sas7bdat", cache_format="invalid", cache_dir=cache_dir)

    clear_reference_cache(cache_dir)

    # create a mock cached file in cache_dir
    cache_dir.mkdir(parents=True, exist_ok=True)
    csv_file = cache_dir / "sample.csv"
    csv_file.write_text("colA,colB\n1,2\n3,4\n", encoding="utf-8")

    res_pl = load_sas_table(
        "sample.sas7bdat", cache=True, cache_format="csv", cache_dir=cache_dir
    )
    assert isinstance(res_pl, pl.DataFrame)
    assert len(res_pl) == 2

    res_pd = load_sas_table(
        "sample.sas7bdat",
        cache=True,
        cache_format="csv",
        cache_dir=cache_dir,
        as_pandas=True,
    )
    assert isinstance(res_pd, pd.DataFrame)
    assert len(res_pd) == 2

    clear_reference_cache(cache_dir)
    assert not csv_file.exists()


def test_ed_to_pl_conversions():
    df = pl.DataFrame({"a": [1, 2]})
    assert isinstance(ed._to_pl(df.lazy()), pl.DataFrame)
    assert isinstance(ed._to_pl(df), pl.DataFrame)
    assert isinstance(ed._to_pl(pd.DataFrame(df)), pl.DataFrame)
    assert isinstance(ed._to_pl(pd.Series([1, 2])), pl.DataFrame)
