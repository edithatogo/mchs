import pathlib
import sys

from nwau_py import compat as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from nwau_py.calculators.adjust import calculate_adjusted_nwau


def test_adjustment_basic_drop():
    df = pd.DataFrame(
        {
            "nwau25": [10.0],
            "_w01": [10.0],
            "w01_ahr": [10.0],
            "hac_adj01": [0.1],
            "hac_flag01": [1],
            "ahr_adj01": [0.2],
            "ahr_flag01": [1],
        }
    )

    result = calculate_adjusted_nwau(
        df,
        hac_flag_cols=["hac_flag01"],
        hac_adj_cols=["hac_adj01"],
        ahr_flag_cols=["ahr_flag01"],
        ahr_adj_cols=["ahr_adj01"],
        ahr_weight_col="w01_ahr",
        covid_flag_col=None,
        drop_intermediate=True,
    )

    assert "hac_flag01" not in result.columns
    assert "ahr_adj01" not in result.columns
    assert result["nwau25_adjusted"].iloc[0] == 7.0


def test_adjustment_no_drop():
    df = pd.DataFrame(
        {
            "nwau25": [5.0],
            "_w01": [2.0],
            "hac_adj01": [0.1],
            "hac_flag01": [1],
        }
    )

    result = calculate_adjusted_nwau(
        df,
        hac_flag_cols=["hac_flag01"],
        hac_adj_cols=["hac_adj01"],
        drop_intermediate=False,
    )

    assert "hac_flag01" in result.columns
    assert "riskAdjustment_HAC" in result.columns


def test_covid_zeroes_adjustments():
    df = pd.DataFrame(
        {
            "nwau25": [10.0],
            "_w01": [5.0],
            "hac_adj01": [0.2],
            "hac_flag01": [1],
            "PAT_COVID_FLAG": [1],
        }
    )
    result = calculate_adjusted_nwau(
        df,
        hac_flag_cols=["hac_flag01"],
        hac_adj_cols=["hac_adj01"],
        covid_flag_col="PAT_COVID_FLAG",
    )
    assert result["riskAdjustment_HAC"].iloc[0] == 0
    assert result["nwau25_adjusted"].iloc[0] == 10


def test_complexity_scoring():
    df = pd.DataFrame(
        {
            "nwau25": [10.0],
            "_w01": [1.0],
            "hac_adj01": [0.1],
            "hac_flag01": [1],
            "hac_points01": [10],
            "hac_adj02": [0.3],
            "hac_flag02": [1],
            "hac_points02": [60],
        }
    )
    complexity = pd.read_csv("nwau_py/data/complexitygroups_2025.csv")
    result = calculate_adjusted_nwau(
        df,
        hac_flag_cols=["hac_flag01", "hac_flag02"],
        hac_adj_cols=["hac_adj01", "hac_adj02"],
        hac_point_cols=["hac_points01", "hac_points02"],
        complexity_df=complexity,
    )
    assert result["HACgroup"].iloc[0] == "02"
    assert result["complexityGroup"].iloc[0] == 3
