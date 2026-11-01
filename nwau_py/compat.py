"""Pure Polars-backed tabular compatibility layer.

This module provides a zero-pandas DataFrame and Series interface backed by
Polars and NumPy. It enables the calculator and grouper engines to execute
with full backward-compatible ergonomics while eliminating pandas completely
from dependencies and sys.modules.
"""

from __future__ import annotations

import contextlib
from collections.abc import Mapping, Sequence
from datetime import date, datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import Any, override

import numpy as np
import polars as pl

NA = None


def Timestamp(val: Any) -> datetime:
    """Parse string or date into datetime."""
    if isinstance(val, datetime):
        return val
    if isinstance(val, date):
        return datetime.combine(val, datetime.min.time())
    s = str(val)[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return datetime.fromisoformat(str(val))


def Timedelta(*, days: int = 0, seconds: int = 0) -> timedelta:
    return timedelta(days=days, seconds=seconds)


def to_datetime(arg: Any, **_kwargs: Any) -> Any:
    if isinstance(arg, CompatSeries):
        dates = [
            Timestamp(x) if x is not None and str(x) != "None" else None
            for x in arg._arr
        ]
        return CompatSeries(dates, name=arg.name)
    if isinstance(arg, (list, tuple)):
        return [
            Timestamp(x) if x is not None and str(x) != "None" else None for x in arg
        ]
    if arg is None or str(arg) in ("", "None", "nan"):
        return None
    return Timestamp(arg)


def isna(val: Any) -> Any:
    if isinstance(val, CompatSeries):
        return val.isna()
    if val is None:
        return True
    return bool(isinstance(val, float) and np.isnan(val))


def notna(val: Any) -> Any:
    if isinstance(val, CompatSeries):
        return val.notna()
    return not isna(val)


class _DatetimeMethods:
    def __init__(self, s: CompatSeries):
        self._s = s

    @property
    def days(self) -> CompatSeries:
        def get_days(x: Any) -> int:
            if hasattr(x, "days"):
                val = x.days
                assert isinstance(val, int)
                return val
            if isinstance(x, np.timedelta64):
                return int(x / np.timedelta64(1, "D"))
            return 0

        arr = np.array([get_days(x) for x in self._s._arr])
        return CompatSeries(arr, name=self._s.name)


class _StringMethods:
    def __init__(self, series: CompatSeries):
        self._s = series

    def strip(self, chars: str | None = None) -> CompatSeries:
        arr = np.array(
            [str(x).strip(chars) if x is not None else "" for x in self._s._arr],
            dtype=object,
        )
        return CompatSeries(arr, self._s.name)

    def strip_chars(self, chars: str | None = None) -> CompatSeries:
        return self.strip(chars)

    def upper(self) -> CompatSeries:
        arr = np.array(
            [str(x).upper() if x is not None else "" for x in self._s._arr],
            dtype=object,
        )
        return CompatSeries(arr, self._s.name)

    def lower(self) -> CompatSeries:
        arr = np.array(
            [str(x).lower() if x is not None else "" for x in self._s._arr],
            dtype=object,
        )
        return CompatSeries(arr, self._s.name)

    def decode(self, _encoding: str = "ascii", _errors: str = "ignore") -> CompatSeries:
        arr = np.array(
            [
                x.decode(_encoding, _errors)
                if isinstance(x, (bytes, bytearray))
                else str(x)
                for x in self._s._arr
            ],
            dtype=object,
        )
        return CompatSeries(arr, self._s.name)

    def replace(self, pat: Any, repl: str = "", regex: bool = False) -> CompatSeries:
        if isinstance(pat, dict):
            arr = list(self._s._arr)
            for k, v in pat.items():
                arr = [str(x).replace(str(k), str(v)) for x in arr]
            return CompatSeries(np.array(arr, dtype=object), self._s.name)
        arr = np.array(
            [str(x).replace(str(pat), str(repl)) for x in self._s._arr], dtype=object
        )
        return CompatSeries(arr, self._s.name)

    def startswith(self, prefix: str) -> CompatSeries:
        arr = np.array(
            [
                str(x).startswith(prefix) if x is not None else False
                for x in self._s._arr
            ],
            dtype=bool,
        )
        return CompatSeries(arr, self._s.name)

    def endswith(self, suffix: str) -> CompatSeries:
        arr = np.array(
            [str(x).endswith(suffix) if x is not None else False for x in self._s._arr],
            dtype=bool,
        )
        return CompatSeries(arr, self._s.name)

    def contains(self, pat: str, regex: bool = True) -> CompatSeries:
        import re

        if regex:
            c = re.compile(pat)
            arr = np.array(
                [
                    bool(c.search(str(x))) if x is not None else False
                    for x in self._s._arr
                ],
                dtype=bool,
            )
        else:
            arr = np.array(
                [pat in str(x) if x is not None else False for x in self._s._arr],
                dtype=bool,
            )
        return CompatSeries(arr, self._s.name)

    def slice(
        self, start: int | None = None, stop: int | None = None, step: int | None = None
    ) -> CompatSeries:
        sl = slice(start, stop, step)
        arr = np.array(
            [str(x)[sl] if x is not None else "" for x in self._s._arr], dtype=object
        )
        return CompatSeries(arr, self._s.name)

    def extract(self, pat: str) -> CompatFrame:
        import re

        extracted = []
        for x in self._s._arr:
            m = re.search(pat, str(x))
            extracted.append(m.group(1) if m and m.groups() else "")
        return CompatFrame({0: extracted})


class CompatSeries:
    def __init__(
        self, data: Any = None, index: Any = None, name: Any = "", dtype: Any = None
    ):
        self.name = name or ""
        if isinstance(data, CompatSeries):
            self._arr = data._arr.copy()
            self.name = name or data.name
        elif isinstance(data, pl.Series):
            self._arr = data.to_numpy()
            self.name = name or data.name
        elif isinstance(data, np.ndarray):
            self._arr = data.copy()
        elif isinstance(data, (list, tuple)):
            if dtype is not None:
                self._arr = np.array(data, dtype=dtype)
            else:
                self._arr = np.array(data)
                if self._arr.dtype.kind in ("U", "S") and any(
                    isinstance(x, (int, float, bool)) for x in data
                ):
                    self._arr = np.array(data, dtype=object)
        elif isinstance(data, Mapping):
            self._arr = np.array(
                list(data.values()),
                dtype=object
                if any(isinstance(v, (str, bytes)) for v in data.values())
                and any(isinstance(v, (int, float, bool)) for v in data.values())
                else (dtype or None),
            )
            if index is None:
                index = list(data.keys())
        elif data is None:
            self._arr = np.array([])
        else:
            self._arr = np.array([data])
        if dtype is not None:
            with np.errstate(all="ignore"), contextlib.suppress(Exception):
                self._arr = self._arr.astype(dtype)
        self._index = list(index) if index is not None else list(range(len(self._arr)))

    @property
    def index(self) -> CompatIndex:
        return CompatIndex(self._index)

    @property
    def dtype(self) -> Any:
        return self._arr.dtype

    def to_polars(self) -> pl.Series:
        return pl.Series(self.name, self._arr)

    @property
    def values(self) -> np.ndarray:
        return self._arr

    def to_numpy(self, dtype: Any = None) -> np.ndarray:
        if dtype is not None:
            return self._arr.astype(dtype)
        return self._arr

    def to_list(self) -> list[Any]:
        return self._arr.tolist()

    def tolist(self) -> list[Any]:
        return self.to_list()

    def item(self) -> Any:
        return self._arr.item()

    def to_dict(self) -> dict[Any, Any]:
        return {k: self._arr[i] for i, k in enumerate(self._index)}

    def get(self, key: Any, default: Any = None) -> Any:
        if key in self._index:
            pos = self._index.index(key)
            val = self._arr[pos]
            return val if not (isinstance(val, float) and np.isnan(val)) else default
        return default

    def __len__(self) -> int:
        return len(self._arr)

    def __iter__(self):
        return iter(self._arr)

    def __array__(self, dtype=None, copy=None):
        if dtype is not None:
            return np.asarray(self._arr, dtype=dtype)
        return np.asarray(self._arr)

    def __contains__(self, key: Any) -> bool:
        return key in self._index

    def __getitem__(self, idx: Any) -> Any:
        if isinstance(idx, str):
            if idx in self._index:
                pos = self._index.index(idx)
                return self._arr[pos]
            raise KeyError(idx)
        if isinstance(idx, (CompatSeries, np.ndarray)):
            mask = np.asarray(getattr(idx, "_arr", idx), dtype=bool)
            return CompatSeries(self._arr[mask], name=self.name)
        if isinstance(idx, (list, tuple)):
            mask = np.asarray(idx)
            return CompatSeries(self._arr[mask], name=self.name)
        val = self._arr[idx]
        if isinstance(val, np.ndarray):
            return CompatSeries(val, name=self.name)
        return val

    def __setitem__(self, idx: Any, val: Any) -> None:
        self._arr[idx] = getattr(val, "_arr", val)

    @property
    def iloc(self) -> _ILocSeries:
        return _ILocSeries(self)

    @property
    def loc(self) -> _LocSeries:
        return _LocSeries(self)

    @property
    def dt(self) -> _DatetimeMethods:
        return _DatetimeMethods(self)

    @property
    def str(self) -> _StringMethods:
        return _StringMethods(self)

    def isna(self) -> CompatSeries:
        if self._arr.dtype.kind in "fc":
            return CompatSeries(np.isnan(self._arr.astype(float)), name=self.name)
        return CompatSeries(
            np.array(
                [x is None or str(x) in ("None", "nan") for x in self._arr], dtype=bool
            ),
            name=self.name,
        )

    def notna(self) -> CompatSeries:
        return ~self.isna()

    def dropna(self) -> CompatSeries:
        mask = self.notna()._arr
        return CompatSeries(self._arr[mask], name=self.name)

    def fillna(self, val: Any) -> CompatSeries:
        arr = self._arr.copy()
        mask = self.isna()._arr
        fill_val = getattr(val, "_arr", val)
        try:
            if isinstance(fill_val, np.ndarray):
                arr[mask] = fill_val[mask]
            else:
                arr[mask] = fill_val
        except ValueError, TypeError:
            arr = arr.astype(object)
            if isinstance(fill_val, np.ndarray):
                arr[mask] = fill_val[mask]
            else:
                arr[mask] = fill_val
        return CompatSeries(arr, name=self.name)

    def combine_first(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        mask = self.notna()._arr
        try:
            res = np.where(mask, self._arr, o)
        except Exception:
            self_obj = self._arr.astype(object)
            o_obj = np.asarray(o, dtype=object)
            res = np.where(mask, self_obj, o_obj)
        return CompatSeries(res, name=self.name)

    def astype(self, dtype: Any) -> CompatSeries:
        if dtype is str:
            arr = np.array(
                [str(x) if x is not None else "" for x in self._arr], dtype=object
            )
            return CompatSeries(arr, name=self.name)
        if dtype in (int, "int64", "int32", "int8", np.int64, np.int32, np.int8):
            arr = np.nan_to_num(self._arr.astype(float), nan=0.0).astype(int)
            return CompatSeries(arr, name=self.name)
        if dtype in (float, "float64", "float32", np.float64, np.float32):
            return CompatSeries(self._arr.astype(float), name=self.name)
        try:
            return CompatSeries(self._arr.astype(dtype), name=self.name)
        except Exception:
            return CompatSeries(self._arr, name=self.name)

    def isin(self, values: Any) -> CompatSeries:
        v_list = list(values)
        if hasattr(self._arr, "dtype") and self._arr.dtype == object:
            # check string or direct equality
            s_set = {str(x) for x in v_list}
            arr = np.array(
                [str(x) in s_set or x in v_list for x in self._arr], dtype=bool
            )
        else:
            arr = np.isin(self._arr, v_list)
        return CompatSeries(arr, name=self.name)

    def nunique(self, dropna: bool = True) -> int:
        arr = self._arr
        if dropna:
            arr = self.dropna()._arr
        return len(np.unique(arr))

    def any(self, axis: int = 0) -> bool:
        return bool(np.any(self._arr))

    def all(self, axis: int = 0) -> bool:
        return bool(np.all(self._arr))

    def clip(self, lower: Any = None, upper: Any = None) -> CompatSeries:
        arr = self._arr.astype(float)
        clipped = np.clip(
            arr,
            lower if lower is not None else -np.inf,
            upper if upper is not None else np.inf,
        )
        return CompatSeries(clipped, name=self.name)

    def round(self, decimals: int = 0) -> CompatSeries:
        return CompatSeries(np.round(self._arr.astype(float), decimals), name=self.name)

    def sum(self, axis: int = 0) -> Any:
        return self._arr.sum()

    def mean(self, axis: int = 0) -> Any:
        return self._arr.mean()

    def max(self, axis: int = 0) -> Any:
        return self._arr.max()

    def min(self, axis: int = 0) -> Any:
        return self._arr.min()

    def ge(self, other: Any) -> CompatSeries:
        return self >= other

    def gt(self, other: Any) -> CompatSeries:
        return self > other

    def le(self, other: Any) -> CompatSeries:
        return self <= other

    def lt(self, other: Any) -> CompatSeries:
        return self < other

    def eq(self, other: Any) -> Any:
        return self == other

    def ne(self, other: Any) -> Any:
        return self != other

    def where(self, cond: Any, other: Any = np.nan) -> CompatSeries:
        c = np.asarray(getattr(cond, "_arr", cond), dtype=bool)
        arr = np.where(c, self._arr, other)
        return CompatSeries(arr, name=self.name)

    def __invert__(self) -> CompatSeries:
        return CompatSeries(~self._arr.astype(bool), name=self.name)

    def __and__(self, other: Any) -> CompatSeries:
        o = np.asarray(getattr(other, "_arr", other), dtype=bool)
        return CompatSeries(self._arr.astype(bool) & o, name=self.name)

    def __or__(self, other: Any) -> CompatSeries:
        o = np.asarray(getattr(other, "_arr", other), dtype=bool)
        return CompatSeries(self._arr.astype(bool) | o, name=self.name)

    def __add__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr + o, name=self.name)

    def __radd__(self, other: Any) -> CompatSeries:
        return self.__add__(other)

    def __sub__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        try:
            return CompatSeries(self._arr - o, name=self.name)
        except Exception:
            arr = [
                a - b if a is not None and b is not None else None
                for a, b in zip(self._arr, o, strict=False)
            ]
            return CompatSeries(arr, name=self.name)

    def __rsub__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(o - self._arr, name=self.name)

    def __mul__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr * o, name=self.name)

    def __rmul__(self, other: Any) -> CompatSeries:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr / o, name=self.name)

    @override
    def __eq__(self, other: Any) -> Any:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr == o, name=self.name)

    @override
    def __ne__(self, other: Any) -> Any:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr != o, name=self.name)

    def __lt__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr < o, name=self.name)

    def __le__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr <= o, name=self.name)

    def __gt__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr > o, name=self.name)

    def __ge__(self, other: Any) -> CompatSeries:
        o = getattr(other, "_arr", other)
        return CompatSeries(self._arr >= o, name=self.name)


class _ILocSeries:
    def __init__(self, s: CompatSeries):
        self._s = s

    def __getitem__(self, idx: Any) -> Any:
        return self._s[idx]

    def __setitem__(self, idx: Any, val: Any) -> None:
        self._s[idx] = val


class _LocSeries:
    def __init__(self, s: CompatSeries):
        self._s = s

    def __getitem__(self, idx: Any) -> Any:
        if isinstance(idx, (CompatSeries, np.ndarray)):
            mask = np.asarray(getattr(idx, "_arr", idx), dtype=bool)
            return CompatSeries(self._s._arr[mask], name=self._s.name)
        if isinstance(idx, (list, tuple)) and len(self._s._index) == len(self._s._arr):
            idx_map = {k: i for i, k in enumerate(self._s._index)}
            pos = [idx_map[k] for k in idx if k in idx_map]
            return CompatSeries(self._s._arr[pos], name=self._s.name)
        if self._s._index and idx in self._s._index:
            pos = self._s._index.index(idx)
            return self._s._arr[pos]
        return self._s[idx]

    def __setitem__(self, idx: Any, val: Any) -> None:
        if self._s._index and idx in self._s._index:
            pos = self._s._index.index(idx)
            self._s._arr[pos] = getattr(val, "_arr", val)
        else:
            self._s[idx] = val


class _ILocFrame:
    def __init__(self, df: CompatFrame):
        self._df = df

    def __getitem__(self, idx: Any) -> Any:
        if isinstance(idx, tuple):
            row_idx, col_idx = idx
            if isinstance(row_idx, int) and isinstance(col_idx, int):
                col_name = self._df.columns[col_idx]
                return self._df._data[col_name][row_idx]
            if isinstance(row_idx, int) and isinstance(col_idx, (slice, list, tuple)):
                cols = [
                    self._df.columns[c]
                    for c in (
                        range(len(self._df.columns))[col_idx]
                        if isinstance(col_idx, slice)
                        else col_idx
                    )
                ]
                row_dict = {c: self._df._data[c][row_idx] for c in cols}
                return CompatSeries(
                    list(row_dict.values()), index=list(row_dict.keys())
                )
            sub = self.__getitem__(row_idx)
            if isinstance(sub, CompatFrame):
                if isinstance(col_idx, int):
                    col_name = self._df.columns[col_idx]
                    return sub[col_name]
                if isinstance(col_idx, (list, tuple, slice)):
                    cols = [
                        self._df.columns[c]
                        for c in (
                            range(len(self._df.columns))[col_idx]
                            if isinstance(col_idx, slice)
                            else col_idx
                        )
                    ]
                    return sub[cols]
            elif isinstance(sub, CompatSeries):
                if isinstance(col_idx, int):
                    return sub._arr[col_idx]
            return sub
        if isinstance(idx, int):
            row_dict = {k: v[idx] for k, v in self._df._data.items()}
            return CompatSeries(
                list(row_dict.values()), index=list(row_dict.keys()), dtype=object
            )
        if isinstance(idx, slice):
            return CompatFrame({k: v[idx] for k, v in self._df._data.items()})
        mask = np.asarray(idx)
        return CompatFrame({k: v[mask] for k, v in self._df._data.items()})


class CompatIndex:
    def __init__(self, data: Any = None):
        if isinstance(data, CompatIndex):
            self._arr = data._arr.copy()
        elif isinstance(data, (list, tuple)):
            self._arr = np.array(data)
        elif isinstance(data, np.ndarray):
            self._arr = data.copy()
        elif data is None:
            self._arr = np.array([])
        else:
            self._arr = np.array(list(data))

    def max(self) -> Any:
        return self._arr.max()

    def min(self) -> Any:
        return self._arr.min()

    def __len__(self) -> int:
        return len(self._arr)

    def __iter__(self):
        return iter(self._arr)

    def __array__(self, dtype=None, copy=None):
        if dtype is not None:
            return np.asarray(self._arr, dtype=dtype)
        return np.asarray(self._arr)

    def __getitem__(self, idx: Any) -> Any:
        res = self._arr[idx]
        if isinstance(res, np.ndarray):
            return CompatIndex(res)
        return res

    def to_list(self) -> list[Any]:
        return self._arr.tolist()

    def tolist(self) -> list[Any]:
        return self._arr.tolist()

    def index(self, val: Any) -> int:
        for i, v in enumerate(self._arr):
            if v == val:
                return i
        raise ValueError(f"{val} is not in index")

    def __contains__(self, val: Any) -> bool:
        return val in self._arr


class _LocFrame:
    def __init__(self, df: CompatFrame):
        self._df = df

    def __getitem__(self, idx: Any) -> Any:
        if isinstance(idx, tuple):
            row_idx, col_idx = idx
            target_cols = [col_idx] if isinstance(col_idx, str) else list(col_idx)
            if isinstance(row_idx, slice):
                start = row_idx.start
                stop = row_idx.stop
                step = row_idx.step or 1
                start_i = (
                    self._df._index.index(start)
                    if start is not None and start in self._df._index
                    else (0 if start is None else int(start))
                )
                stop_i = (
                    (self._df._index.index(stop) + 1)
                    if stop is not None and stop in self._df._index
                    else (len(self._df._index) if stop is None else int(stop) + 1)
                )
                pos = list(range(start_i, stop_i, step))
                if isinstance(col_idx, str):
                    return CompatSeries(
                        self._df._data[col_idx][pos],
                        index=[self._df._index[p] for p in pos],
                        name=col_idx,
                    )
                sub_data = {
                    c: self._df._data[c][pos]
                    for c in target_cols
                    if c in self._df._data
                }
                return CompatFrame(sub_data, index=[self._df._index[p] for p in pos])
            if isinstance(row_idx, (CompatSeries, np.ndarray, list, tuple)):
                row_vals = np.asarray(getattr(row_idx, "_arr", row_idx))
                idx_map = {val: i for i, val in enumerate(self._df._index)}
                pos = [idx_map[v] for v in row_vals if v in idx_map]
                sub_data = {
                    c: self._df._data[c][pos]
                    for c in target_cols
                    if c in self._df._data
                }
                return CompatFrame(sub_data, index=[self._df._index[p] for p in pos])
            if row_idx in self._df._index:
                pos = self._df._index.index(row_idx)
                if isinstance(col_idx, str):
                    return self._df._data[col_idx][pos]
                return CompatSeries({c: self._df._data[c][pos] for c in target_cols})
            return self._df[col_idx]
        if isinstance(idx, (CompatSeries, np.ndarray, list)):
            return self._df[idx]
        if idx in self._df._index:
            pos = self._df._index.index(idx)
            return self._df.iloc[pos]
        return self._df.iloc[idx]

    def __setitem__(self, idx: Any, val: Any) -> None:
        if isinstance(idx, tuple):
            row_idx, col_idx = idx
            if isinstance(row_idx, (list, tuple, np.ndarray, CompatSeries)):
                mask = np.asarray(getattr(row_idx, "_arr", row_idx))
                self._df._data[col_idx][mask] = getattr(val, "_arr", val)
            elif row_idx in self._df._index:
                pos = self._df._index.index(row_idx)
                self._df._data[col_idx][pos] = getattr(val, "_arr", val)
            else:
                self._df._data[col_idx][row_idx] = getattr(val, "_arr", val)


class CompatFrame:
    def __init__(
        self, data: Any = None, columns: Sequence[str] | None = None, index: Any = None
    ):
        self._data: dict[str, np.ndarray] = {}
        self._index: list[Any] = []
        if isinstance(data, pl.DataFrame):
            for c in data.columns:
                self._data[c] = data[c].to_numpy()
            self._index = list(range(len(data)))
        elif isinstance(data, CompatFrame):
            self._data = {k: v.copy() for k, v in data._data.items()}
            self._index = list(data._index)
        elif isinstance(data, Mapping):
            for k, v in data.items():
                if isinstance(v, (CompatSeries, pl.Series)):
                    self._data[str(k)] = v.to_numpy()
                elif isinstance(v, np.ndarray):
                    self._data[str(k)] = v.copy()
                elif isinstance(v, (list, tuple)):
                    self._data[str(k)] = np.array(v)
                else:
                    self._data[str(k)] = np.array([v])
            length = len(next(iter(self._data.values()))) if self._data else 0
            self._index = list(index) if index is not None else list(range(length))
        elif isinstance(data, (list, tuple)) and data and isinstance(data[0], Mapping):
            keys = list(columns) if columns is not None else list(data[0].keys())
            for k in keys:
                self._data[str(k)] = np.array([row.get(k) for row in data])
            self._index = list(index) if index is not None else list(range(len(data)))
        elif data is not None:
            arr = np.asarray(data)
            if arr.ndim == 2:
                cols = (
                    list(columns)
                    if columns is not None
                    else [str(i) for i in range(arr.shape[1])]
                )
                for i, c in enumerate(cols):
                    self._data[c] = arr[:, i]
                self._index = (
                    list(index) if index is not None else list(range(arr.shape[0]))
                )
        if columns is not None and not self._data:
            for c in columns:
                self._data[str(c)] = np.array([])
        if index is not None:
            self._index = list(index)

    @property
    def columns(self) -> list[str]:
        return list(self._data.keys())

    @property
    def index(self) -> CompatIndex:
        return CompatIndex(self._index)

    @property
    def values(self) -> np.ndarray:
        if not self._data:
            return np.empty((0, 0))
        return np.column_stack([self._data[c] for c in self.columns])

    def to_numpy(self, dtype: Any = None) -> np.ndarray:
        val = self.values
        if dtype is not None:
            return val.astype(dtype)
        return val

    @columns.setter
    def columns(self, cols: Sequence[str]) -> None:
        new_data = {}
        for old_k, new_k in zip(list(self._data.keys()), cols, strict=False):
            new_data[str(new_k)] = self._data[old_k]
        self._data = new_data

    @property
    def shape(self) -> tuple[int, int]:
        return len(self), len(self._data)

    @property
    def empty(self) -> bool:
        return len(self) == 0

    @property
    def iloc(self) -> _ILocFrame:
        return _ILocFrame(self)

    @property
    def loc(self) -> _LocFrame:
        return _LocFrame(self)

    def __len__(self) -> int:
        if not self._data:
            return 0
        return len(next(iter(self._data.values())))

    def __getitem__(self, key: Any) -> Any:
        if isinstance(key, (str, int)):
            s_key = str(key)
            if s_key in self._data:
                return CompatSeries(self._data[s_key], index=self._index, name=s_key)
            if key in self._data:
                return CompatSeries(self._data[key], index=self._index, name=str(key))
            raise KeyError(key)
        if isinstance(key, (list, tuple)):
            if all(isinstance(k, (str, int)) for k in key) and all(
                str(k) in self._data for k in key
            ):
                return CompatFrame(
                    {str(k): self._data[str(k)] for k in key}, index=self._index
                )
            mask = np.asarray(key, dtype=bool)
            return CompatFrame({k: v[mask] for k, v in self._data.items()})
        if isinstance(key, slice):
            return CompatFrame({k: v[key] for k, v in self._data.items()})
        if isinstance(key, (CompatSeries, np.ndarray)):
            mask = np.asarray(getattr(key, "_arr", key), dtype=bool)
            return CompatFrame({k: v[mask] for k, v in self._data.items()})
        raise TypeError(f"Invalid column lookup: {type(key)}")

    def __setitem__(self, key: str, val: Any) -> None:
        length = len(self)
        if isinstance(val, (CompatSeries, pl.Series)):
            arr = val.to_numpy()
        elif isinstance(val, np.ndarray):
            arr = val
        elif isinstance(val, (list, tuple)):
            arr = np.array(val)
        else:
            arr = np.full(length if length > 0 else 1, val)
        if length > 0 and len(arr) != length:
            if len(arr) == 1:
                arr = np.full(length, arr[0])
            else:
                raise ValueError(f"Length mismatch: {len(arr)} vs {length}")
        self._data[str(key)] = arr
        if not self._index:
            self._index = list(range(len(arr)))

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._data:
            return self[key]
        if default is not None:
            if not isinstance(default, CompatSeries):
                default = CompatSeries([default] * max(len(self), 1))
            return default
        return None

    def with_columns(self, *exprs: Any, **named_exprs: Any) -> CompatFrame:
        pl_df = self.to_polars().with_columns(*exprs, **named_exprs)
        return CompatFrame(pl_df)

    def astype(self, dtype: Any) -> CompatFrame:
        res = self.copy()
        for k in res.columns:
            res[k] = res[k].astype(dtype)
        return res

    def replace(self, to_replace: Any, value: Any = "", **_kwargs: Any) -> CompatFrame:
        res = self.copy()
        for k in res.columns:
            res[k] = res[k].str.replace(to_replace, value)
        return res

    def isin(self, values: Any) -> CompatFrame:
        res = CompatFrame(index=self._index)
        for k in self.columns:
            res[k] = self[k].isin(values)
        return res

    def isna(self) -> CompatFrame:
        res = CompatFrame(index=self._index)
        for k in self.columns:
            res[k] = self[k].isna()
        return res

    def notna(self) -> CompatFrame:
        return ~self.isna()

    def __invert__(self) -> CompatFrame:
        res = CompatFrame(index=self._index)
        for k in self.columns:
            res[k] = ~self[k]
        return res

    def any(self, axis: int = 0) -> Any:
        if axis == 1:
            if not self._data:
                return CompatSeries(np.array([], dtype=bool))
            arrs = [v.astype(bool) for v in self._data.values()]
            combined = np.logical_or.reduce(arrs)
            return CompatSeries(combined, index=self._index)
        vals = [self[k].any() for k in self.columns]
        return CompatSeries(vals, index=list(self.columns))

    def all(self, axis: int = 0) -> Any:
        if axis == 1:
            if not self._data:
                return CompatSeries(np.array([], dtype=bool))
            arrs = [v.astype(bool) for v in self._data.values()]
            combined = np.logical_and.reduce(arrs)
            return CompatSeries(combined, index=self._index)
        vals = [self[k].all() for k in self.columns]
        return CompatSeries(vals, index=list(self.columns))

    def max(self, axis: int = 0) -> Any:
        if axis == 1:
            arrs = [self._data[c] for c in self.columns]
            if not arrs:
                return CompatSeries(np.zeros(len(self)))
            stacked = np.column_stack(arrs).astype(float)
            with np.errstate(all="ignore"):
                return CompatSeries(np.nanmax(stacked, axis=1), index=self._index)
        return {c: np.nanmax(self._data[c].astype(float)) for c in self.columns}

    def min(self, axis: int = 0) -> Any:
        if axis == 1:
            arrs = [self._data[c] for c in self.columns]
            if not arrs:
                return CompatSeries(np.zeros(len(self)))
            stacked = np.column_stack(arrs).astype(float)
            with np.errstate(all="ignore"):
                return CompatSeries(np.nanmin(stacked, axis=1), index=self._index)
        return {c: np.nanmin(self._data[c].astype(float)) for c in self.columns}

    def sum(self, axis: int = 0) -> Any:
        if axis == 1:
            arrs = [self._data[c] for c in self.columns]
            if not arrs:
                return CompatSeries(np.zeros(len(self)))
            stacked = np.column_stack(arrs).astype(float)
            with np.errstate(all="ignore"):
                return CompatSeries(np.nansum(stacked, axis=1), index=self._index)
        return {c: np.nansum(self._data[c].astype(float)) for c in self.columns}

    def mean(self, axis: int = 0) -> Any:
        if axis == 1:
            arrs = [self._data[c] for c in self.columns]
            if not arrs:
                return CompatSeries(np.zeros(len(self)))
            stacked = np.column_stack(arrs).astype(float)
            with np.errstate(all="ignore"):
                return CompatSeries(np.nanmean(stacked, axis=1), index=self._index)
        return {c: np.nanmean(self._data[c].astype(float)) for c in self.columns}

    def idxmax(self, axis: int = 1) -> CompatSeries:
        if axis == 1:
            arrs = [self._data[c] for c in self.columns]
            if not arrs:
                return CompatSeries(np.array([""] * len(self)), index=self._index)
            stacked = np.column_stack(arrs).astype(float)
            best_idx = np.nanargmax(stacked, axis=1)
            col_names = [self.columns[i] for i in best_idx]
            return CompatSeries(np.array(col_names, dtype=object), index=self._index)
        best = {
            c: self._index[int(np.nanargmax(self._data[c].astype(float)))]
            for c in self.columns
        }
        return CompatSeries(best)

    def idxmin(self, axis: int = 1) -> CompatSeries:
        if axis == 1:
            arrs = [self._data[c] for c in self.columns]
            if not arrs:
                return CompatSeries(np.array([""] * len(self)), index=self._index)
            stacked = np.column_stack(arrs).astype(float)
            best_idx = np.nanargmin(stacked, axis=1)
            col_names = [self.columns[i] for i in best_idx]
            return CompatSeries(np.array(col_names, dtype=object), index=self._index)
        best = {
            c: self._index[int(np.nanargmin(self._data[c].astype(float)))]
            for c in self.columns
        }
        return CompatSeries(best)

    def merge(
        self,
        other: Any,
        on: str | Sequence[str] | None = None,
        how: str = "left",
        **_kwargs: Any,
    ) -> CompatFrame:
        if (
            other is None
            or (hasattr(other, "empty") and other.empty)
            or len(other) == 0
        ):
            return self.copy()
        on_cols = [on] if isinstance(on, str) else list(on or [])
        other_cols = set(other.columns) if hasattr(other, "columns") else set()
        if on_cols and not all(c in other_cols for c in on_cols):
            return self.copy()
        if on_cols and not all(c in self.columns for c in on_cols):
            return self.copy()
        pl_self = self.to_polars()
        if isinstance(other, CompatFrame):
            pl_other = other.to_polars()
        elif isinstance(other, pl.DataFrame):
            pl_other = other
        else:
            pl_other = pl.DataFrame(other)
        try:
            how_any: Any = how
            joined = pl_self.join(pl_other, on=on, how=how_any)  # type: ignore[arg-type]
            return CompatFrame(joined)
        except Exception:
            return self.copy()

    def copy(self) -> CompatFrame:
        return CompatFrame(self)

    def drop(
        self, columns: Sequence[str] | None = None, axis: int = 1, **_kwargs: Any
    ) -> CompatFrame:
        cols_to_drop = set(columns if columns is not None else [])
        new_data = {k: v.copy() for k, v in self._data.items() if k not in cols_to_drop}
        return CompatFrame(new_data, index=self._index)

    def dropna(
        self, axis: int = 0, how: str = "any", subset: Sequence[str] | None = None
    ) -> CompatFrame:
        if not self._data:
            return self.copy()
        cols = subset if subset is not None else list(self.columns)
        masks = [self[c].notna()._arr for c in cols if c in self.columns]
        combined = (
            np.logical_and.reduce(masks) if masks else np.ones(len(self), dtype=bool)
        )
        res = self[combined]
        assert isinstance(res, CompatFrame)
        return res

    def rename(self, columns: Mapping[str, str], **_kwargs: Any) -> CompatFrame:
        new_data = {}
        for k, v in self._data.items():
            new_k = columns.get(k, k)
            new_data[new_k] = v.copy()
        return CompatFrame(new_data, index=self._index)

    def select_dtypes(self, include: Any = None, exclude: Any = None) -> CompatFrame:
        inc = (
            set(include if isinstance(include, (list, tuple)) else [include])
            if include
            else set()
        )
        matched = {}
        for k, v in self._data.items():
            k_dtype = v.dtype.kind
            if "object" in inc or "string" in inc:
                if k_dtype in ("O", "U", "S"):
                    matched[k] = v
            elif k_dtype not in ("O", "U", "S"):
                matched[k] = v
        return CompatFrame(matched, index=self._index)

    def sort_values(self, by: str | Sequence[str], **_kwargs: Any) -> CompatFrame:
        pl_df = self.to_polars().sort(by)
        return CompatFrame(pl_df)

    def set_index(self, keys: str | Sequence[str], drop: bool = True) -> CompatFrame:
        if isinstance(keys, str):
            idx = list(self._data[keys])
            cols = {k: v.copy() for k, v in self._data.items() if not drop or k != keys}
            return CompatFrame(cols, index=idx)
        first = keys[0]
        idx = list(self._data[first])
        cols = {k: v.copy() for k, v in self._data.items() if not drop or k not in keys}
        return CompatFrame(cols, index=idx)

    def reset_index(self, drop: bool = True) -> CompatFrame:
        return CompatFrame(self._data, index=list(range(len(self))))

    def assign(self, **kwargs: Any) -> CompatFrame:
        res = self.copy()
        for k, v in kwargs.items():
            res[k] = v(res) if callable(v) else v
        return res

    def fillna(self, val: Any) -> CompatFrame:
        res = self.copy()
        for k in res.columns:
            res[k] = res[k].fillna(val)
        return res

    def head(self, n: int = 5) -> CompatFrame:
        res = self.iloc[:n]
        assert isinstance(res, CompatFrame)
        return res

    def tail(self, n: int = 5) -> CompatFrame:
        res = self.iloc[-n:]
        assert isinstance(res, CompatFrame)
        return res

    def to_dict(self, orient: str = "records") -> Any:
        if orient == "records":
            records = []
            for i in range(len(self)):
                row = {k: self._data[k][i] for k in self._data}
                records.append(row)
            return records
        return {k: self._data[k].tolist() for k in self._data}

    def to_polars(self) -> pl.DataFrame:
        if not self._data:
            return pl.DataFrame()
        return pl.DataFrame(self._data)

    def to_pandas(self) -> Any:
        try:
            import pandas as pd

            return pd.DataFrame(self._data, index=self._index)
        except ImportError:
            return self

    def to_csv(
        self, path_or_buf: Any = None, index: bool = False, **_kwargs: Any
    ) -> str | None:
        pl_df = self.to_polars()
        if path_or_buf is None:
            buf = StringIO()
            pl_df.write_csv(buf)
            return buf.getvalue()
        if hasattr(path_or_buf, "write"):
            pl_df.write_csv(path_or_buf)
            return None
        pl_df.write_csv(path_or_buf)
        return None

    def filter(self, like: str | None = None, **_kwargs: Any) -> CompatFrame:
        if like is not None:
            cols = [c for c in self.columns if like in c]
            res = self[cols]
            assert isinstance(res, CompatFrame)
            return res
        return self


DataFrame = CompatFrame
Series = CompatSeries
Index = CompatIndex


def read_csv(path: str | Path, **_kwargs: Any) -> CompatFrame:
    df_pl = pl.read_csv(path)
    return CompatFrame(df_pl)


def read_parquet(path: str | Path, **_kwargs: Any) -> CompatFrame:
    df_pl = pl.read_parquet(path)
    return CompatFrame(df_pl)


def read_sas(filepath_or_buffer: Any, *args: Any, **kwargs: Any) -> CompatFrame:
    try:
        import pyreadstat

        d, _ = pyreadstat.read_sas7bdat(str(filepath_or_buffer), output_format="dict")
        return CompatFrame(d)
    except Exception:
        return CompatFrame()


def concat(objs: Sequence[Any], axis: int = 0, **_kwargs: Any) -> Any:
    if not objs:
        return CompatFrame()
    if axis == 1:
        # horizontal concat
        data = {}
        for obj in objs:
            if isinstance(obj, CompatFrame):
                data.update(obj._data)
            elif isinstance(obj, CompatSeries):
                data[obj.name] = obj._arr
            elif isinstance(obj, dict):
                data.update(obj)
        return CompatFrame(data)
    # axis == 0: vertical concat
    if isinstance(objs[0], CompatFrame):
        pl_dfs = [
            o.to_polars() if isinstance(o, CompatFrame) else pl.DataFrame(o)
            for o in objs
        ]
        return CompatFrame(pl.concat(pl_dfs, how="vertical"))
    if isinstance(objs[0], CompatSeries):
        arrs = [
            o.to_numpy() if isinstance(o, CompatSeries) else np.asarray(o) for o in objs
        ]
        return CompatSeries(np.concatenate(arrs), name=objs[0].name)
    return CompatFrame()


class _TestingNamespace:
    @staticmethod
    def assert_frame_equal(
        left: Any,
        right: Any,
        check_dtype: bool = False,
        check_exact: bool = False,
        rtol: float = 1e-5,
        atol: float = 1e-8,
        **_kwargs: Any,
    ) -> None:
        l_cols = list(left.columns)
        r_cols = list(right.columns)
        assert l_cols == r_cols, f"Column mismatch: {l_cols} != {r_cols}"
        assert len(left) == len(right), f"Length mismatch: {len(left)} != {len(right)}"
        for col in l_cols:
            l_val = np.asarray(left[col])
            r_val = np.asarray(right[col])
            if np.issubdtype(l_val.dtype, np.number) and np.issubdtype(
                r_val.dtype, np.number
            ):
                assert np.allclose(
                    l_val.astype(float),
                    r_val.astype(float),
                    rtol=rtol,
                    atol=atol,
                    equal_nan=True,
                ), f"Values in column {col} differ"
            else:
                assert (l_val == r_val).all(), f"Values in column {col} differ"

    @staticmethod
    def assert_series_equal(
        left: Any, right: Any, rtol: float = 1e-5, atol: float = 1e-8, **_kwargs: Any
    ) -> None:
        l_val = np.asarray(left)
        r_val = np.asarray(right)
        if np.issubdtype(l_val.dtype, np.number) and np.issubdtype(
            r_val.dtype, np.number
        ):
            assert np.allclose(
                l_val.astype(float),
                r_val.astype(float),
                rtol=rtol,
                atol=atol,
                equal_nan=True,
            )
        else:
            assert (l_val == r_val).all()


testing = _TestingNamespace()

__all__ = [
    "NA",
    "CompatFrame",
    "CompatSeries",
    "DataFrame",
    "Series",
    "Timedelta",
    "Timestamp",
    "concat",
    "isna",
    "notna",
    "read_csv",
    "read_parquet",
    "testing",
    "to_datetime",
]
