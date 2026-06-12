"""Tests for the opt-in Rust-backed acute 2025 adapter."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PYREADSTAT = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

import nwau_py.calculators.acute as acute  # noqa: E402
from nwau_py import rust_bridge  # noqa: E402

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "golden" / "acute_2025"
INPUT_CSV = FIXTURE_ROOT / "input.csv"
EXPECTED_CSV = FIXTURE_ROOT / "expected.csv"
WEIGHTS_CSV = Path("tests/data/nep25_aa_price_weights.csv")
REF_DIR = Path("tests/data/2025")


def _load_weights(*_args, **_kwargs) -> pd.DataFrame:
    weights = pd.read_csv(WEIGHTS_CSV)
    weights["DRG"] = weights["DRG"].astype(str).str.strip("b'")
    return weights


def _require_rust_extension() -> None:
    try:
        rust_bridge.load_rust_extension()
    except ImportError as exc:
        pytest.skip(f"optional Rust extension unavailable: {exc}")


def test_rust_bridge_loads_the_acute_kernel_label():
    _require_rust_extension()
    assert rust_bridge.kernel_label() == "acute 2025"


def test_rust_opt_in_wrapper_matches_the_acute_golden_fixture(monkeypatch):
    _require_rust_extension()
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    input_df = pd.read_csv(INPUT_CSV)
    expected = pd.read_csv(EXPECTED_CSV)["NWAU25"].to_numpy()

    result = acute.calculate_acute_rust_2025(
        input_df,
        acute.AcuteParams(),
        year="2025",
        ref_dir=REF_DIR,
    )

    assert list(result.columns) == [*list(input_df.columns), "NWAU25"]
    assert result["NWAU25"].to_numpy() == pytest.approx(expected, rel=1e-4, abs=1e-4)


def test_rust_opt_in_wrapper_preserves_the_default_python_path(monkeypatch):
    _require_rust_extension()
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    input_df = pd.read_csv(INPUT_CSV)

    python_result = acute.calculate_acute(
        input_df,
        acute.AcuteParams(),
        year="2025",
        ref_dir=REF_DIR,
    )
    rust_result = acute.calculate_acute_rust_2025(
        input_df,
        acute.AcuteParams(),
        year="2025",
        ref_dir=REF_DIR,
    )

    assert "NWAU25" in rust_result.columns
    assert (result_columns := list(rust_result.columns))
    assert result_columns[: len(input_df.columns)] == list(input_df.columns)
    assert rust_result["NWAU25"].to_numpy() == pytest.approx(
        python_result["NWAU25"].to_numpy(), rel=1e-4, abs=1e-4
    )
