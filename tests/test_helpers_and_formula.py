from pathlib import Path

from nwau_py import compat as pd
from nwau_py.calculators.funding_formula import (
    calculate_funding,
    load_formula,
    load_weights,
)
from nwau_py.data.paths import data_dir, formula_json, sas_table, weights_csv
from nwau_py.utils import impute_adjustment, ra_suffix, sas_ref_dir


def test_funding_formula_helpers(tmp_path):
    weights_path = tmp_path / "weights.csv"
    weights_path.write_text("A\n1\n2\n", encoding="utf-8")
    formula_path = tmp_path / "formula.json"
    formula_path.write_text(
        '{"variables": {"X": "A"}, "steps": ["NWAU25 = X * 2"]}',
        encoding="utf-8",
    )

    weights = load_weights(weights_path)
    formula = load_formula(formula_path)
    result = calculate_funding(pd.DataFrame({"A": [3]}), formula)

    assert list(weights.columns) == ["A"]
    assert formula["variables"] == {"X": "A"}
    assert result.iloc[0] == 6


def test_path_helpers_and_imputation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sas_root = tmp_path / "archive" / "sas" / "NEP25_SAS_NWAU_calculator"
    calculator_dir = sas_root / "calculators"
    calculator_dir.mkdir(parents=True)

    assert ra_suffix("2025") == "ra2021"
    assert data_dir("2025") == Path("excel_calculator/data")
    assert weights_csv("2025") == Path("excel_calculator/data/weights.csv")
    assert formula_json("2025") == Path("excel_calculator/data/formula.json")
    assert sas_table(
        "nep{suffix}_table_{ra}_{ra_year}_{year}.sas7bdat",
        year="2025",
        base_dir=Path("/base"),
    ) == Path("/base/nep25_table_ra2021_2021_2025.sas7bdat")
    assert sas_ref_dir("2025") == Path(
        "archive/sas/NEP25_SAS_NWAU_calculator/calculators"
    )

    table = pd.DataFrame(
        {
            "_pat_ind_flag": [0, 1],
            "adj_indigenous": [0.0, 0.4],
        }
    )
    imputed = impute_adjustment(
        table,
        "_pat_ind_flag",
        "adj_indigenous",
        {0: 0.75, 1: 0.25},
    )

    assert imputed == 0.1
