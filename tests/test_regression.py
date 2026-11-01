from pathlib import Path

import numpy as np
import pytest

import nwau_py.calculators.acute as acute
import nwau_py.calculators.outpatients as outpatients
import nwau_py.calculators.subacute as subacute
from nwau_py import compat as pd
from nwau_py.calculators import (
    AcuteParams,
    OutpatientParams,
    SubacuteParams,
    calculate_acute,
    calculate_outpatients,
    calculate_subacute,
)
from nwau_py.scoring.scorer import score_readmission
from nwau_py.utils import RA_VERSION

YEARS = [y for y in sorted(RA_VERSION.keys()) if int(y) >= 2025]

BASE = Path("tests/data")


@pytest.mark.parametrize("year", YEARS)
def test_acute_matches_sas(monkeypatch, year):
    df = pd.read_csv(BASE / "acute_input.csv")
    expected = pd.read_csv(BASE / "acute_expected.csv")["NWAU25"].values

    def _load(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
        weights = pd.read_csv(BASE / "nep25_aa_price_weights.csv")
        weights["DRG"] = weights["DRG"].str.strip("b'")
        return weights

    monkeypatch.setattr(acute, "_load_price_weights", _load)

    result = calculate_acute(df, AcuteParams(), year=year, ref_dir=BASE / "2025")
    assert np.allclose(result["NWAU25"].values, expected)


@pytest.mark.parametrize("year", YEARS)
def test_subacute_matches_sas(monkeypatch, year):
    df = pd.read_csv(
        BASE / "subacute_input.csv",
        parse_dates=["ADM_DATE", "SEP_DATE", "BIRTH_DATE"],
    )
    expected = pd.read_csv(BASE / "subacute_expected.csv")["NWAU25"].values

    def _load(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
        return pd.read_csv(BASE / "nep25_sa_snap_price_weights.csv").rename(
            columns={"ansnap": "ANSNAP"}
        )

    monkeypatch.setattr(subacute, "_load_weights", _load)

    result = calculate_subacute(df, SubacuteParams(), year=year, ref_dir=BASE)
    assert np.allclose(result["NWAU25"].values, expected)


@pytest.mark.parametrize("year", YEARS)
def test_outpatient_matches_sas(monkeypatch, year):
    pytest.skip("Outpatient data not available")
    df = pd.read_csv(
        BASE / "outpatient_input.csv",
        parse_dates=["SERVICE_DATE", "BIRTH_DATE"],
    )
    expected = pd.read_csv(BASE / "outpatient_expected.csv")["NWAU25"].values

    def _load(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
        return pd.read_csv(BASE / "nep25_op_price_weights.csv").rename(
            columns={"tier2_clinic": "TIER2_CLINIC"}
        )

    monkeypatch.setattr(outpatients, "_load_weights", _load)

    result = calculate_outpatients(df, OutpatientParams(), year=year, ref_dir=BASE)
    assert np.allclose(result["NWAU25"].values, expected)


def test_readmission_scoring_matches_sas():
    df = pd.read_csv(BASE / "readmission_input.csv")
    expected = pd.read_csv(BASE / "readmission_expected.csv")

    result = score_readmission(df)
    pd.testing.assert_frame_equal(result[expected.columns], expected)
