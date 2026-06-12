import pathlib
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from nwau_py.utils import impute_adjustment, ra_suffix, sas_ref_dir


def test_ra_suffix():
    assert ra_suffix("2025") == "ra2021"
    assert ra_suffix("2024") == "ra2021"
    assert ra_suffix("2023") == "ra2016"
    assert ra_suffix("2019") == "ra2011"
    assert ra_suffix("2013") == "ra2006"


def test_sas_ref_dir_discovers_calculator_subdirectory_and_fails_closed(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    calculator = (
        tmp_path / "archive" / "sas" / "NEP25_SAS_NWAU_calculator" / "01 Calculators"
    )
    calculator.mkdir(parents=True)

    assert sas_ref_dir("2025") == pathlib.Path(
        "archive/sas/NEP25_SAS_NWAU_calculator/01 Calculators"
    )

    with pytest.raises(FileNotFoundError, match="No SAS reference directory"):
        sas_ref_dir("2026")

    fallback = tmp_path / "archive" / "sas" / "NWAU26_SAS_Calculator"
    fallback.mkdir(parents=True)
    assert sas_ref_dir("2026") == pathlib.Path("archive/sas/NWAU26_SAS_Calculator")


def test_impute_adjustment_weighted_average_and_empty_inputs():
    table = pd.DataFrame({"key": [1, 2], "value": [0.25, 0.5]})

    assert impute_adjustment(table, "key", "value", {1: 0.8, 2: 0.2}) == pytest.approx(
        0.3
    )
    assert impute_adjustment(table, "key", "value", {3: 1.0}) == 0.0
    assert impute_adjustment(pd.DataFrame(), "key", "value", {1: 1.0}) == 0.0
    assert impute_adjustment(None, "key", "value", {1: 1.0}) == 0.0
