"""Comprehensive unit test suite for nwau_py.compat to ensure high test coverage

of the Zero-Pandas compatibility layer.
"""

from __future__ import annotations

import datetime
from io import StringIO
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from nwau_py import compat as pd


def test_timestamp_and_timedelta():
    dt = datetime.datetime(2025, 1, 1, 12, 0)
    assert pd.Timestamp(dt) == dt

    d = datetime.date(2025, 1, 1)
    assert pd.Timestamp(d) == datetime.datetime(2025, 1, 1, 0, 0)

    assert pd.Timestamp("2025-01-01 10:20:30") == datetime.datetime(
        2025, 1, 1, 10, 20, 30
    )
    assert pd.Timestamp("2025-01-01") == datetime.datetime(2025, 1, 1, 0, 0)
    assert pd.Timestamp("2025/01/01 10:20:30") == datetime.datetime(
        2025, 1, 1, 10, 20, 30
    )
    assert pd.Timestamp("2025/01/01") == datetime.datetime(2025, 1, 1, 0, 0)
    assert pd.Timestamp("2025-01-01T12:00:00") == datetime.datetime(2025, 1, 1, 12, 0)

    td = pd.Timedelta(days=5, seconds=30)
    assert td == datetime.timedelta(days=5, seconds=30)


def test_to_datetime():
    s = pd.Series(["2025-01-01", "2025-01-02", None, "None"])
    res = pd.to_datetime(s)
    assert isinstance(res, pd.Series)
    assert res.iloc[0] == datetime.datetime(2025, 1, 1, 0, 0)
    assert res.iloc[2] is None

    lst = pd.to_datetime(["2025-01-01", None])
    assert isinstance(lst, list)
    assert lst[0] == datetime.datetime(2025, 1, 1, 0, 0)

    assert pd.to_datetime(None) is None
    assert pd.to_datetime("") is None
    assert pd.to_datetime("None") is None
    assert pd.to_datetime("nan") is None
    assert pd.to_datetime("2025-01-01") == datetime.datetime(2025, 1, 1, 0, 0)


def test_isna_and_notna():
    s = pd.Series([1.0, np.nan, None, 4.0])
    isna_s = pd.isna(s)
    assert isinstance(isna_s, pd.Series)
    assert list(isna_s) == [False, True, True, False]

    notna_s = pd.notna(s)
    assert list(notna_s) == [True, False, False, True]

    assert pd.isna(None) is True
    assert pd.isna(np.nan) is True
    assert pd.isna(10) is False

    assert pd.notna(None) is False
    assert pd.notna(np.nan) is False
    assert pd.notna(10) is True


def test_datetime_methods():
    tds = pd.Series(
        [
            datetime.timedelta(days=3),
            np.timedelta64(4, "D"),
            10,
        ]
    )
    days = tds.dt.days
    assert list(days) == [3, 4, 0]


def test_string_methods():
    s = pd.Series(["  apple ", "banana", None, "CHERRY  "])
    assert list(s.str.strip()) == ["apple", "banana", "", "CHERRY"]
    assert list(s.str.strip_chars()) == ["apple", "banana", "", "CHERRY"]
    assert list(s.str.upper()) == ["  APPLE ", "BANANA", "", "CHERRY  "]
    assert list(s.str.lower()) == ["  apple ", "banana", "", "cherry  "]

    b_s = pd.Series([b"hello", "world"])
    assert list(b_s.str.decode()) == ["hello", "world"]

    rep_s = pd.Series(["foo-bar", "baz-bar"])
    assert list(rep_s.str.replace("-", "_")) == ["foo_bar", "baz_bar"]
    assert list(rep_s.str.replace({"-": "_"})) == ["foo_bar", "baz_bar"]

    assert list(s.str.startswith("  a")) == [True, False, False, False]
    assert list(s.str.endswith("na")) == [False, True, False, False]
    assert list(s.str.contains("ban")) == [False, True, False, False]
    assert list(s.str.slice(0, 3)) == ["  a", "ban", "", "CHE"]

    extr = pd.Series(["ABC123XYZ", "DEF456UVW"]).str.extract(r"([A-Z]+)(\d+)")
    assert isinstance(extr, pd.DataFrame)


def test_compat_index():
    idx = pd.Index([10, 20, 30])
    assert len(idx) == 3
    assert idx[0] == 10
    assert list(idx) == [10, 20, 30]
    assert idx.tolist() == [10, 20, 30]
    assert idx.to_list() == [10, 20, 30]
    assert idx.max() == 30
    assert idx.min() == 10
    assert 20 in idx
    assert idx.index(20) == 1
    assert isinstance(np.asarray(idx), np.ndarray)


def test_compat_series_math_and_logic():
    s1 = pd.Series([10, 20, 30], name="col1")
    s2 = pd.Series([1, 2, 3], name="col2")

    assert list(s1 + s2) == [11, 22, 33]
    assert list(s1 + 5) == [15, 25, 35]
    assert list(5 + s1) == [15, 25, 35]

    assert list(s1 - s2) == [9, 18, 27]
    assert list(s1 - 5) == [5, 15, 25]
    assert list(50 - s1) == [40, 30, 20]

    assert list(s1 * s2) == [10, 40, 90]
    assert list(s1 * 2) == [20, 40, 60]
    assert list(2 * s1) == [20, 40, 60]

    assert list(s1 / s2) == [10.0, 10.0, 10.0]
    assert list(s1 / 2) == [5.0, 10.0, 15.0]

    # Comparisons
    assert list(s1 == 20) == [False, True, False]
    assert list(s1 != 20) == [True, False, True]
    assert list(s1 < 20) == [True, False, False]
    assert list(s1 <= 20) == [True, True, False]
    assert list(s1 > 20) == [False, False, True]
    assert list(s1 >= 20) == [False, True, True]

    assert list(s1.eq(20)) == [False, True, False]
    assert list(s1.ne(20)) == [True, False, True]
    assert list(s1.lt(20)) == [True, False, False]
    assert list(s1.le(20)) == [True, True, False]
    assert list(s1.gt(20)) == [False, False, True]
    assert list(s1.ge(20)) == [False, True, True]

    # Bitwise
    b1 = pd.Series([True, False, True])
    b2 = pd.Series([False, False, True])
    assert list(b1 & b2) == [False, False, True]
    assert list(b1 | b2) == [True, False, True]
    assert list(~b1) == [False, True, False]


def test_compat_series_aggregations_and_transforms():
    s = pd.Series([10.0, 20.0, 30.0, 20.0], name="test")
    assert s.sum() == 80.0
    assert s.mean() == 20.0
    assert s.min() == 10.0
    assert s.max() == 30.0
    assert s.nunique() == 3

    assert s.any() is True
    assert s.all() is True

    s_nan = pd.Series([10.0, np.nan, 30.0])
    assert list(s_nan.fillna(0.0)) == [10.0, 0.0, 30.0]
    assert list(s_nan.dropna()) == [10.0, 30.0]

    s_comb = pd.Series([1.0, np.nan]).combine_first(pd.Series([9.0, 8.0]))
    assert list(s_comb) == [1.0, 8.0]

    assert list(s.clip(15.0, 25.0)) == [15.0, 20.0, 25.0, 20.0]
    assert list(pd.Series([1.234, 5.678]).round(1)) == [1.2, 5.7]
    assert list(s.isin([10.0, 30.0])) == [True, False, True, False]
    assert list(s.where(s > 15.0, 0.0)) == [0.0, 20.0, 30.0, 20.0]

    # astype
    s_int = pd.Series(["1", "2"]).astype(int)
    assert list(s_int) == [1, 2]
    assert list(s_int.astype(str)) == ["1", "2"]
    assert list(s_int.astype(float)) == [1.0, 2.0]

    assert isinstance(s.to_polars(), pl.Series)
    assert isinstance(s.to_dict(), dict)
    assert isinstance(s.to_numpy(), np.ndarray)
    assert isinstance(s.tolist(), list)
    assert isinstance(s.to_list(), list)
    assert pd.Series([42]).item() == 42
    assert s.get(0) == 10.0
    assert s.get(999, "default") == "default"
    assert len(s) == 4
    assert s.dtype is not None
    assert isinstance(s.index, pd.Index)

    # indexing
    s[0] = 99.0
    assert s[0] == 99.0
    assert s.iloc[0] == 99.0
    s.iloc[0] = 10.0
    assert s.loc[0] == 10.0
    s.loc[0] = 10.0


def test_compat_frame_operations(tmp_path: Path):
    data = {
        "id": [1, 2, 3, 4],
        "name": ["Alice", "Bob", "Charlie", "David"],
        "val": [10.5, 20.0, 15.0, 30.0],
    }
    df = pd.DataFrame(data)
    assert len(df) == 4
    assert df.shape == (4, 3)
    assert list(df.columns) == ["id", "name", "val"]
    assert "id" in df.columns
    assert isinstance(df["name"], pd.Series)
    assert list(df["name"]) == ["Alice", "Bob", "Charlie", "David"]
    assert df.empty is False

    # setitem
    df["flag"] = [True, False, True, False]
    assert "flag" in df.columns
    assert df.get("flag") is not None
    assert df.get("nonexistent", "def") == "def"

    # head / tail
    assert len(df.head(2)) == 2
    assert len(df.tail(2)) == 2

    # copy
    df_copy = df.copy()
    assert len(df_copy) == 4

    # fillna / dropna / drop / rename
    df_nan = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [np.nan, 2.0, 3.0]})
    assert df_nan.fillna(0)["a"].iloc[1] == 0
    assert len(df_nan.dropna()) == 1

    dropped = df.drop(columns=["val"])
    assert "val" not in dropped.columns

    renamed = df.rename(columns={"val": "score"})
    assert "score" in renamed.columns

    # assign
    assigned = df.assign(score=lambda d: d["val"] * 2)
    assert list(assigned["score"]) == [21.0, 40.0, 30.0, 60.0]

    # filter
    filtered = df.filter(like="val")
    assert list(filtered.columns) == ["val"]

    # sort_values / set_index / reset_index
    sorted_df = df.sort_values(by="val")
    assert sorted_df["val"].iloc[0] == 10.5
    indexed_df = df.set_index("name")
    assert len(indexed_df) == 4
    reset_df = indexed_df.reset_index()
    assert len(reset_df) == 4

    # iloc / loc
    assert df.iloc[0]["name"] == "Alice"
    assert len(df.iloc[:2]) == 2
    assert df.loc[0, "name"] == "Alice"
    df.loc[0, "name"] = "Alicia"
    assert df.loc[0, "name"] == "Alicia"

    # with_columns, astype, replace, isin, isna, notna
    df_wc = df.with_columns(pl.lit(1).alias("ones"))
    assert "ones" in df_wc.columns
    df_ast = pd.DataFrame({"x": ["1", "2"]}).astype(int)
    assert df_ast["x"].iloc[0] == 1

    df_rep = pd.DataFrame({"x": ["cat", "dog"]}).replace({"cat": "kitty"})
    assert df_rep["x"].iloc[0] == "kitty"

    assert isinstance(df.isin([1, 2]), pd.DataFrame)
    assert isinstance(df_nan.isna(), pd.DataFrame)
    assert isinstance(df_nan.notna(), pd.DataFrame)
    assert isinstance(~pd.DataFrame({"x": [True, False]}), pd.DataFrame)

    # reductions
    df_num = pd.DataFrame({"a": [1.0, 2.0], "b": [10.0, 20.0]})
    assert df_num.any() is not None
    assert df_num.all() is not None
    assert df_num.max() is not None
    assert df_num.min() is not None
    assert df_num.sum() is not None
    assert df_num.mean() is not None
    assert list(df_num.idxmax(axis=1)) == ["b", "b"]
    assert list(df_num.idxmin(axis=1)) == ["a", "a"]

    # select_dtypes
    assert len(df_num.select_dtypes(include=[np.number]).columns) == 2

    # merge
    df_other = pd.DataFrame({"id": [2, 3], "dept": ["HR", "IT"]})
    merged = df.merge(df_other, on="id", how="inner")
    assert len(merged) == 2
    assert "dept" in merged.columns

    # to_dict, to_polars, to_pandas, to_csv
    assert isinstance(df.to_dict(orient="records"), list)
    assert isinstance(df.to_dict(orient="list"), dict)

    pl_df = df.to_polars()
    assert isinstance(pl_df, pl.DataFrame)
    assert len(pl_df) == 4

    p_df = df.to_pandas()
    assert p_df is not None

    csv_str = df.to_csv()
    assert "Alicia" in csv_str

    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path)
    assert csv_path.exists()

    df_from_csv = pd.read_csv(csv_path)
    assert len(df_from_csv) == 4

    # parquet via polars
    parquet_path = tmp_path / "test.parquet"
    pl_df.write_parquet(parquet_path)
    assert parquet_path.exists()

    df_from_parquet = pd.read_parquet(parquet_path)
    assert len(df_from_parquet) == 4

    # values, to_numpy, index, columns setter
    assert isinstance(df.values, np.ndarray)
    assert isinstance(df.to_numpy(), np.ndarray)
    assert isinstance(df.index, pd.Index)
    df_cols = df.copy()
    df_cols.columns = ["c1", "c2", "c3", "c4"]
    assert list(df_cols.columns) == ["c1", "c2", "c3", "c4"]


def test_concat_and_testing_namespace():
    df1 = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
    df2 = pd.DataFrame({"a": [3, 4], "b": [30, 40]})

    vcat = pd.concat([df1, df2], axis=0)
    assert len(vcat) == 4

    hcat = pd.concat([df1, pd.DataFrame({"c": [100, 200]})], axis=1)
    assert len(hcat.columns) == 3

    s1 = pd.Series([1, 2], name="s")
    s2 = pd.Series([3, 4], name="s")
    s_cat = pd.concat([s1, s2], axis=0)
    assert len(s_cat) == 4

    assert len(pd.concat([])) == 0
    assert pd.read_sas("nonexistent.sas7bdat").empty is True

    # testing namespace
    pd.testing.assert_frame_equal(df1, df1)
    pd.testing.assert_series_equal(s1, s1)

    with pytest.raises(AssertionError):
        pd.testing.assert_frame_equal(df1, df2)

    with pytest.raises(AssertionError):
        pd.testing.assert_series_equal(s1, s2)


def test_indexing_coverage():
    df = pd.DataFrame(
        {"a": [1, 2, 3, 4], "b": [10, 20, 30, 40], "c": [100, 200, 300, 400]}
    )
    # _ILocFrame variations
    assert df.iloc[0, 1] == 10
    row_slice_col_slice = df.iloc[0, :2]
    assert isinstance(row_slice_col_slice, pd.Series)
    assert row_slice_col_slice.iloc[0] == 1
    row_slice_col_list = df.iloc[0, [0, 1]]
    assert isinstance(row_slice_col_list, pd.Series)

    sub_col = df.iloc[:2, 1]
    assert isinstance(sub_col, pd.Series)
    assert len(sub_col) == 2

    sub_frame_slice = df.iloc[:2, 0:2]
    assert isinstance(sub_frame_slice, pd.DataFrame)
    assert sub_frame_slice.shape == (2, 2)

    sub_frame_list = df.iloc[:2, [0, 2]]
    assert isinstance(sub_frame_list, pd.DataFrame)
    assert list(sub_frame_list.columns) == ["a", "c"]

    row_series = df.iloc[0]
    assert isinstance(row_series, pd.Series)
    assert df.iloc[0, 1] == 10

    # _LocFrame variations
    loc_series = df.loc[0:2, "b"]
    assert isinstance(loc_series, pd.Series)

    loc_frame_slice = df.loc[0:2, ["a", "b"]]
    assert isinstance(loc_frame_slice, pd.DataFrame)

    loc_frame_list = df.loc[[0, 1], ["a", "c"]]
    assert isinstance(loc_frame_list, pd.DataFrame)

    loc_single = df.loc[0, "a"]
    assert loc_single == 1

    loc_row_dict = df.loc[0, ["a", "b"]]
    assert isinstance(loc_row_dict, pd.Series)

    # Loc assignments
    df.loc[[True, False, False, False], "a"] = 999
    assert df["a"].iloc[0] == 999
    df.loc[0, "a"] = 1
    assert df["a"].iloc[0] == 1


def test_series_and_dataframe_extended_coverage():
    s = pd.Series([10, 20, 30, 40], index=["w", "x", "y", "z"], name="vals")
    assert s.loc["x"] == 20
    s.loc["x"] = 25
    assert s.loc["x"] == 25
    s.iloc[1] = 20
    assert s.iloc[1] == 20

    # series getitem / setitem slice, list, mask
    assert len(s[:2]) == 2
    assert len(s[[0, 1]]) == 2
    assert len(s[pd.Series([True, False, True, False])]) == 2

    s[:2] = [100, 200]
    assert s.iloc[0] == 100
    s[[0, 1]] = [10, 20]
    assert s.iloc[0] == 10

    # reductions axis=0 and axis=1 on DataFrame
    df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})
    assert df.sum(axis=0)["a"] == 3.0
    assert list(df.sum(axis=1)) == [4.0, 6.0]
    assert df.mean(axis=0)["a"] == 1.5
    assert list(df.mean(axis=1)) == [2.0, 3.0]
    assert df.max(axis=0)["a"] == 2.0
    assert list(df.max(axis=1)) == [3.0, 4.0]
    assert df.min(axis=0)["a"] == 1.0
    assert list(df.min(axis=1)) == [1.0, 2.0]
    assert bool(df.any(axis=0)["a"]) is True
    assert list(df.any(axis=1)) == [True, True]
    assert bool(df.all(axis=0)["a"]) is True
    assert list(df.all(axis=1)) == [True, True]
    assert list(df.idxmax(axis=0)) == [1, 1]
    assert list(df.idxmin(axis=0)) == [0, 0]

    # DataFrame dropna, fillna, drop, merge
    df_nan = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": [np.nan, np.nan, 3.0]})
    assert len(df_nan.dropna()) == 1
    assert len(df_nan.dropna(subset=["a"])) == 2
    assert len(pd.DataFrame().dropna()) == 0

    df1 = pd.DataFrame({"key": [1, 2], "val1": ["x", "y"]})
    df2 = pd.DataFrame({"key": [2, 3], "val2": ["y", "z"]})
    m_left = df1.merge(df2, on="key", how="left")
    assert len(m_left) == 2
    assert "val2" in m_left.columns
    assert df1.merge(None) is not None
    assert df1.merge(pd.DataFrame()) is not None


def test_corner_cases_coverage():
    # dataframe from Series dict, scalar, 2D array, and columns only
    df_s = pd.DataFrame({"a": pd.Series([1, 2]), "b": [10, 20]})
    assert len(df_s) == 2
    assert df_s["b"].iloc[0] == 10

    arr2d = np.array([[10, 20], [30, 40]])
    df_2d = pd.DataFrame(arr2d, columns=["x", "y"])
    assert df_2d.shape == (2, 2)

    df_empty_cols = pd.DataFrame(columns=["c1", "c2"])
    assert list(df_empty_cols.columns) == ["c1", "c2"]

    # series copy constructor, mixed list, and None
    s_orig = pd.Series([1, 2], name="orig")
    s_copy = pd.Series(s_orig)
    assert s_copy.name == "orig"

    s_mixed = pd.Series(["a", 1])
    assert s_mixed.dtype == object

    s_none = pd.Series(None)
    assert len(s_none) == 0

    # astype bool and fallback
    s_bool = pd.Series([True, False]).astype(bool)
    assert s_bool.iloc[0] is np.True_ or s_bool.iloc[0] is True

    # subtraction with None fallback
    s_sub_none = pd.Series([10, None]) - pd.Series([1, 2])
    assert s_sub_none.iloc[0] == 9
    assert s_sub_none.iloc[1] is None

    # combine_first with object type fallback
    s_o1 = pd.Series([1, np.nan])
    s_o2 = pd.Series(["hello", "world"])
    s_comb = s_o1.combine_first(s_o2)
    assert s_comb.iloc[1] == "world"

    # dataframe getitem integer key, bool list, slice, invalid type
    df_int_col = pd.DataFrame()
    df_int_col[0] = [100, 200]
    assert df_int_col[0].iloc[0] == 100

    df_bool_list = df_s[[True, False]]
    assert len(df_bool_list) == 1

    df_slice = df_s[:1]
    assert len(df_slice) == 1

    with pytest.raises(TypeError, match="Invalid column lookup"):
        _ = df_s[1.23]

    # setitem length mismatch error
    with pytest.raises(ValueError, match="Length mismatch"):
        df_s["bad"] = [1, 2, 3, 4]

    # empty dataframe setitem initializes index
    df_emp = pd.DataFrame()
    df_emp["new"] = [1, 2, 3]
    assert len(df_emp) == 3

    # set_index with sequence of keys
    df_multi_idx = df_2d.set_index(["x", "y"], drop=False)
    assert "x" in df_multi_idx.columns

    # to_polars on empty df
    assert len(pd.DataFrame().to_polars()) == 0

    # to_csv with file buffer
    buf = StringIO()
    df_2d.to_csv(buf)
    assert "x,y" in buf.getvalue()

    # concat horizontal with Series
    s_h1 = pd.Series([1, 2], name="s1")
    s_h2 = pd.Series([3, 4], name="s2")
    df_hcat = pd.concat([s_h1, s_h2], axis=1)
    assert df_hcat.shape == (2, 2)


def test_compat_full_gap_closer():
    # _LocSeries
    s = pd.Series([10, 20, 30], index=["x", "y", "z"], name="vals")
    assert len(s.loc[s > 15]) == 2
    assert len(s.loc[["x", "z"]]) == 2
    assert s.loc[0] == 10
    s.loc[0] = 999
    assert s.iloc[0] == 999

    # CompatIndex constructors
    idx1 = pd.Index(pd.Index([1, 2]))
    assert len(idx1) == 2
    idx2 = pd.Index(np.array([1, 2]))
    assert len(idx2) == 2
    idx3 = pd.Index(None)
    assert len(idx3) == 0
    idx4 = pd.Index({1, 2})
    assert len(idx4) == 2

    # _LocFrame gap lines
    df = pd.DataFrame({"col": [10, 20]}, index=["row1", "row2"])
    assert df.loc["nonexistent", "col"].iloc[0] == 10
    assert len(df.loc[[True, False]]) == 1
    assert df.loc["row1"]["col"] == 10
    assert df.loc[0]["col"] == 10

    # merge with polars df and dict
    df_m = pd.DataFrame({"id": [1, 2], "val": [10, 20]})
    m_pl = df_m.merge(pl.DataFrame({"id": [1], "extra": ["a"]}), on="id")
    assert len(m_pl) == 2
    m_dict = df_m.merge({"id": [2], "extra": ["b"]}, on="id")
    assert len(m_dict) == 2

    # filter with no match
    f_empty = df_m.filter(like="nomatch")
    assert len(f_empty.columns) == 0

    # concat with sequences of lists
    c_s = pd.concat([pd.Series([1, 2], name="s"), [3, 4]])
    assert len(c_s) == 4


def test_compat_extra_gaps():
    df = pd.DataFrame({"col": 123})
    assert len(df) == 1
    assert df["col"].iloc[0] == 123

    # df.iloc with numpy array
    df_arr = pd.DataFrame({"a": [1, 2, 3]})
    assert len(df_arr.iloc[np.array([0, 2])]) == 2

    # CompatIndex slicing, dtype, index error
    idx = pd.Index([10, 20, 30])
    sub_idx = idx[:2]
    assert isinstance(sub_idx, pd.Index)
    assert np.asarray(idx, dtype=float).dtype == float
    with pytest.raises(ValueError, match="is not in index"):
        idx.index(999)

    # CompatSeries numpy conversions and membership
    s = pd.Series([1, 2, 3])
    assert s.to_numpy(dtype=float).dtype == float
    assert np.asarray(s, dtype=float).dtype == float
    assert (999 in s) is False
    assert len(s[[0, 2]]) == 2

    # df.to_numpy with dtype and df.loc fallback assignment
    assert df_arr.to_numpy(dtype=float).dtype == float
    df_named = pd.DataFrame({"a": [1, 2, 3]}, index=["r1", "r2", "r3"])
    df_named.loc[0, "a"] = 55
    assert df_named["a"].iloc[0] == 55
