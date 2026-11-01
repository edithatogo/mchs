"""Strict assertion test verifying the zero-pandas invariant across mchs-qualified."""

import sys

import polars as pl
import pytest

from nwau_py.calculators import acute


def test_pandas_not_in_dependencies():
    """Verify pandas cannot be imported in the environment."""
    with pytest.raises(ModuleNotFoundError):
        import pandas  # type: ignore[import-untyped]  # noqa: F401


def test_sys_modules_has_no_pandas():
    """Verify sys.modules has no loaded pandas module."""
    assert "pandas" not in sys.modules, (
        f"pandas was imported into sys.modules: {sys.modules.get('pandas')}"
    )


def test_calculators_execute_pure_polars():
    """Verify calculators execute natively on Polars frames without pandas in sys.modules."""
    df_acute = pl.DataFrame(
        {
            "DRG": ["801A"],
            "LOS": [5],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PAT_COVID_FLAG": [0],
        }
    )
    from nwau_py.utils import sas_ref_dir

    res = acute.calculate_acute(
        df_acute,
        acute.AcuteParams(),
        year="2025",
        ref_dir=sas_ref_dir("2025"),
    )
    assert isinstance(res, pl.DataFrame)
    assert "pandas" not in sys.modules
