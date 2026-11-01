import re
from pathlib import Path

import pytest

import nwau_py.calculators.acute as acute
from nwau_py import compat as pd
from nwau_py.calculators import AcuteParams, calculate_acute
from nwau_py.utils import ra_suffix

DATA_DIR = Path(__file__).resolve().parents[0] / "data"


def test_converted_tables_shapes():
    assert pd.read_csv(DATA_DIR / "drg11_masterlist.csv").shape == (801, 18)
    assert pd.read_csv(DATA_DIR / "nep25_aa_price_weights.csv").shape == (798, 12)
    assert pd.read_csv(DATA_DIR / "p_intercept.csv").shape == (1, 14)


def _fake_load(path: Path, *_, **__) -> pd.DataFrame:
    name = path.name
    match = re.search(r"ra\d{4}", name)
    ra = match.group(0) if match else ra_suffix("2025")
    ra_year = ra[2:]
    if "icu_paed_eligibility_list" in name:
        return pd.DataFrame(
            {
                "APCID": ["HOSP"],
                "_est_eligible_icu_flag": [1],
                "_est_eligible_paed_flag": [1],
            }
        )
    if "aa_adj_icu" in name:
        return pd.DataFrame({"icu_rate": [0.05]})
    if name.startswith(f"postcode_to_{ra}"):
        return pd.DataFrame({"POSTCODE": ["PC1"], ra: [2]})
    if f"hospital_{ra}" in name:
        return pd.DataFrame({"APCID": ["HOSP"], f"_hosp_ra_{ra_year}": [4]})
    return pd.DataFrame()


def test_calculate_nwau_from_sas_weights(monkeypatch):
    weights = pd.read_csv(DATA_DIR / "nep25_aa_price_weights.csv")
    weights["DRG"] = weights["DRG"].str.strip("b'")
    monkeypatch.setattr(acute, "_load_price_weights", lambda *_: weights)
    monkeypatch.setattr(acute, "load_sas_table", _fake_load)

    df = pd.DataFrame(
        {
            "DRG": ["801A"],
            "LOS": [10],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PAT_COVID_FLAG": [0],
        }
    )

    result = acute.calculate_acute(
        df, acute.AcuteParams(), year="2025", ref_dir=Path("tests/data/2025")
    )
    assert result["NWAU25"].iloc[0] * 7258 == pytest.approx(67116.1776, rel=1e-4)
    result = calculate_acute(
        df,
        AcuteParams(),
        year="2025",
        ref_dir=Path("tests/data/2025"),
    )
    funding = result["NWAU25"].iloc[0] * 7258
    assert funding == pytest.approx(67116.1776, rel=1e-4)
