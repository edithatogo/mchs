"""Helpers for evaluating formula contracts against tabular weight inputs.

Uses Polars and Narwhals for zero-pandas tabular expression evaluation.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import narwhals as nw
import polars as pl


class _ColumnsList(list[str]):
    """List subclass that supports .tolist() for compatibility."""

    def tolist(self) -> list[str]:
        return list(self)


def load_weights(
    csv_path: str | bytes | os.PathLike[str],
    *,
    as_polars: bool = False,
) -> Any:
    """Load a weight table from ``csv_path`` and normalize header text."""
    path_arg: Any = Path(csv_path) if isinstance(csv_path, os.PathLike) else csv_path
    df_pl = pl.read_csv(path_arg)
    clean_cols = [c.replace("\n", " ").strip() for c in df_pl.columns]
    df_pl = df_pl.rename(dict(zip(df_pl.columns, clean_cols, strict=False)))
    if as_polars:
        return df_pl
    from nwau_py import compat as pd

    return pd.DataFrame(df_pl)


def load_formula(json_path: str | bytes | os.PathLike[str]) -> dict[str, Any]:
    """Return the JSON formula contract from ``json_path``."""
    with open(json_path) as fh:
        return json.load(fh)


def calculate_funding(weights_df: Any, formula: dict[str, Any]) -> Any:
    """Evaluate ``formula`` against ``weights_df`` via Polars/Narwhals."""
    is_compat = hasattr(weights_df, "to_polars")
    if is_compat:
        weights_df = weights_df.to_polars()
    is_native_polars = isinstance(weights_df, (pl.DataFrame, pl.LazyFrame))
    nw_df = nw.from_native(weights_df)

    # Extract mapped series
    env: dict[str, Any] = {sym: nw_df[col] for sym, col in formula["variables"].items()}
    target_key = "NWAU25" if "NWAU25" in str(formula.get("steps", "")) else "NWAU"

    for step in formula["steps"]:
        lhs, expr = step.split("=")
        lhs = lhs.strip()
        expr = expr.strip()
        tokens = expr.split()
        if len(tokens) == 3:
            left_sym, op, right_sym = tokens
            left_val = env[left_sym] if left_sym in env else float(left_sym)
            right_val = env[right_sym] if right_sym in env else float(right_sym)
            if op == "*":
                env[lhs] = left_val * right_val
            elif op == "+":
                env[lhs] = left_val + right_val
            elif op == "-":
                env[lhs] = left_val - right_val
            elif op == "/":
                env[lhs] = left_val / right_val
            else:
                raise ValueError(f"Unsupported formula operator: {op}")
        elif len(tokens) == 1:
            sym = tokens[0]
            env[lhs] = env[sym] if sym in env else float(sym)
        else:
            # Multi-token algebraic evaluation using sandboxed Python arithmetic
            env[lhs] = eval(expr, {"__builtins__": {}}, env)  # nosec B307 # noqa: S307

    res = env.get(target_key, next(reversed(env.values())))
    native_res = res.to_native() if hasattr(res, "to_native") else res
    if is_compat:
        from nwau_py import compat as pd

        return pd.Series(native_res)
    if is_native_polars:
        return pl.Series(native_res)
    return nw.to_native(res)
