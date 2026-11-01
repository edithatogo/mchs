# ruff: noqa
import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402

import numpy as np
from nwau_py import compat as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nwau_py.utils import RA_VERSION, ra_suffix, sas_ref_dir

# Only editions with verified unit tests
YEARS = [y for y in sorted(RA_VERSION.keys()) if int(y) >= 2025]

spec = importlib.util.spec_from_file_location(
    "acute",
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "acute.py",
)
acute = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acute)


DATA = pd.DataFrame(
    {
        "DRG": ["801A", "801A", "801A"],
        "LOS": [5, 10, 80],
        "ICU_HOURS": [0, 0, 0],
        "ICU_OTHER": [0, 0, 0],
        "PAT_SAMEDAY_FLAG": [0, 0, 0],
        "PAT_PRIVATE_FLAG": [0, 0, 0],
        "PAT_COVID_FLAG": [0, 0, 0],
    }
)

EXPECTED = np.array([6.8772, 9.2472, 11.3272])


@pytest.mark.parametrize("year", YEARS)
def test_calculate_acute_matches_sas_weights(monkeypatch, year):
    def _load_csv(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
        suffix = str(year)[-2:]
        path = Path("tests/data") / str(year) / f"nep{suffix}_aa_price_weights.csv"
        if not path.exists() or year == "2018":
            path = Path("tests/data/nep25_aa_price_weights.csv")
        df = pd.read_csv(path)
        df["DRG"] = df["DRG"].str.strip("b'")
        return df

    monkeypatch.setattr(acute, "_load_price_weights", _load_csv)

    ref_dir = Path("tests/data")
    ref_dir = Path("tests/data") / str(year)
    if not ref_dir.exists():
        ref_dir = Path("tests/data/2025")
    result = acute.calculate_acute(
        DATA.copy(),
        acute.AcuteParams(),
        year=year,
        ref_dir=ref_dir,
    )
    assert np.allclose(result["NWAU25"].values, EXPECTED)


def _mock_load(
    path: Path,
    cache: bool = True,
    cache_format: str | None = None,
    cache_dir: Path | None = None,
) -> pd.DataFrame:
    name = path.name
    if "aa_price_weights" in name:
        df = pd.read_csv("tests/data/nep25_aa_price_weights.csv")
        df["DRG"] = df["DRG"].str.strip("b'")
        return df
    if "aa_adj_covid" in name:
        return pd.DataFrame({"_pat_covid_treat_flag": [0, 1], "adj_covid": [0.0, 0.23]})
    if "aa_adj_icu" in name:
        return pd.DataFrame({"icu_rate": [0.05]})
    return pd.DataFrame()


@pytest.mark.parametrize("year", YEARS)
def test_covid_flags_from_diagnosis(monkeypatch, year):
    monkeypatch.setattr(
        acute,
        "_load_price_weights",
        lambda r, year="2025": pd.read_csv(
            "tests/data/nep25_aa_price_weights.csv"
        ).assign(DRG=lambda x: x["DRG"].str.strip("b'")),
    )
    monkeypatch.setattr(acute, "load_sas_table", _mock_load)

    df = pd.DataFrame(
        {
            "DRG": ["T63A", "801A", "T63B"],
            "LOS": [5, 5, 5],
            "ICU_HOURS": [0, 0, 0],
            "ICU_OTHER": [0, 0, 0],
            "PAT_SAMEDAY_FLAG": [0, 0, 0],
            "PAT_PRIVATE_FLAG": [0, 0, 0],
            "DX1": ["U0712", "U0711", "A000"],
        }
    )

    params = acute.AcuteParams(
        icu_paed_option=2,
        radiotherapy_option=1,
        dialysis_option=1,
        est_remoteness_option=2,
        covid_option=1,
        covid_adj_option=1,
        debug_mode=True,
    )

    result = acute.calculate_acute(
        df, params, year=year, ref_dir=Path("tests/data/2025")
    )
    assert result["_pat_covid_flag"].tolist() == [1, 1, 0]
    assert result["_pat_covid_treat_flag"].tolist() == [1, 0, 0]
    assert result["adj_covid"][0] == 0.23


@pytest.mark.parametrize("year", YEARS)
def test_covid_flags_provided(monkeypatch, year):
    monkeypatch.setattr(
        acute,
        "_load_price_weights",
        lambda r, year="2025": pd.read_csv(
            "tests/data/nep25_aa_price_weights.csv"
        ).assign(DRG=lambda x: x["DRG"].str.strip("b'")),
    )
    monkeypatch.setattr(acute, "load_sas_table", _mock_load)

    df = pd.DataFrame(
        {
            "DRG": ["T63A"],
            "LOS": [5],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PAT_COVID_FLAG": [1],
            "COVID_ADJ_FLAG": [1],
        }
    )

    params = acute.AcuteParams(
        icu_paed_option=2,
        radiotherapy_option=1,
        dialysis_option=1,
        est_remoteness_option=2,
        covid_option=2,
        covid_adj_option=2,
        debug_mode=True,
    )

    result = acute.calculate_acute(
        df, params, year=year, ref_dir=Path("tests/data/2025")
    )
    assert result["_pat_covid_flag"][0] == 1
    assert result["_pat_covid_treat_flag"][0] == 1
    assert result["adj_covid"][0] == 0.23

    assert any(col.startswith("_") for col in result.columns)

    debug = acute.calculate_acute(
        DATA.copy(),
        acute.AcuteParams(debug_mode=True),
        year=year,
        ref_dir=Path("tests/data/2025"),
    )
    assert any(col.startswith("_") for col in debug.columns)


@pytest.mark.parametrize("year", YEARS)
def test_calculate_acute_option_paths(monkeypatch, year):
    def _load_csv(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
        df = pd.read_csv("tests/data/nep25_aa_price_weights.csv")
        df["DRG"] = df["DRG"].str.strip("b'")
        return df

    monkeypatch.setattr(acute, "_load_price_weights", _load_csv)

    data = DATA.copy()
    data["PAT_RADIOTHERAPY_FLAG"] = 0
    data["PAT_DIALYSIS_FLAG"] = 0
    data["EST_ELIGIBLE_ICU_FLAG"] = 0
    data["EST_ELIGIBLE_PAED_FLAG"] = 0
    data["EST_REMOTENESS"] = 0

    params = acute.AcuteParams(
        icu_paed_option=2,
        radiotherapy_option=2,
        dialysis_option=2,
        est_remoteness_option=2,
    )

    result = acute.calculate_acute(
        data,
        params,
        year=year,
        ref_dir=Path("tests/data/2025"),
    )
    assert np.allclose(result["NWAU25"].values, EXPECTED)


def test_calculate_acute_2018_runs(monkeypatch):
    """Ensure the calculator runs for a pre-2021 year."""
    pytest.skip("2018 edition not supported")


@pytest.mark.parametrize(
    "year,weights_path",
    [
        ("2016", "tests/data/2016/weights.csv"),
        ("2018", "tests/data/2018/nep18_aa_price_weights.csv"),
    ],
)
def test_calculate_acute_legacy_runs(monkeypatch, year, weights_path):
    """Ensure the calculator runs for selected pre-2021 years."""
    dir_path = sas_ref_dir(year)
    assert Path(dir_path).exists()

    monkeypatch.setattr(
        acute,
        "_load_price_weights",
        lambda *_args, **_kwargs: pd.read_csv(weights_path),
    )
    monkeypatch.setattr(
        acute,
        "load_sas_table",
        lambda *_a, **_k: (_ for _ in ()).throw(FileNotFoundError()),
    )

    df = DATA[:1]
    res = acute.calculate_acute(
        df,
        acute.AcuteParams(),
        year=year,
        ref_dir=Path(dir_path),
    )
    col = f"NWAU{year[-2:]}"
    assert res[col][0] > 0


# ---------------------------------------------------------------------------
# Additional helpers for adjustment testing
# ---------------------------------------------------------------------------


def _make_weights(*_, **overrides) -> pd.DataFrame:
    data = {
        "DRG": ["AAA"],
        "drg_inlier_lb": [2],
        "drg_inlier_ub": [10],
        "drg_adj_paed": [1.2],
        "drg_samedaylist_flag": [0],
        "drg_bundled_icu_flag": [0],
        "drg_pw_sd": [0.5],
        "drg_pw_sso_base": [0.6],
        "drg_pw_sso_perdiem": [0.1],
        "drg_pw_inlier": [1.0],
        "drg_pw_lso_perdiem": [0.2],
        "drg_adj_privpat_serv": [0.1],
        "state_adj_privpat_accomm_sd": [0.02],
        "state_adj_privpat_accomm_on": [0.01],
        "icu_rate": [0.05],
        "adj_radiotherapy": [0.0],
        "adj_dialysis": [0.0],
        "adj_remoteness": [0.0],
        "adj_treat_remoteness": [0.0],
    }
    for k, v in overrides.items():
        data[k] = [v]
    return pd.DataFrame(data)


def _fake_load(path: Path, *_, **__):
    name = path.name
    match = re.search(r"ra\d{4}", name)
    ra = match.group(0) if match else ra_suffix("2025")
    ra_year = ra[2:]
    if "radio_codes" in name:
        return pd.DataFrame({"code_ID": [11111]})
    if "dialysis_codes" in name:
        return pd.DataFrame({"code_ID": [22222]})
    if "icu_paed_eligibility_list" in name:
        return pd.DataFrame(
            {
                "APCID": ["HOSP"],
                "_est_eligible_icu_flag": [1],
                "_est_eligible_paed_flag": [1],
            }
        )
    match = re.search(r"ra\d{4}", name)
    if match:
        ra = match.group(0)
        ra_year = ra[2:]
        if name.startswith("postcode_to_"):
            return pd.DataFrame({"POSTCODE": ["PC1"], ra: [2]})
        if any(
            name.startswith(prefix) for prefix in ["sa2_to_", "asgs_to_", "sla_to_"]
        ):
            return pd.DataFrame({"ASGS": [123], ra: [3]})
        if "hospital_" in name:
            return pd.DataFrame({"APCID": ["HOSP"], f"_hosp_ra_{ra_year}": [4]})
    if f"postcode_to_{ra}" in name:
        return pd.DataFrame({"POSTCODE": ["PC1"], ra: [2]})
    if any(x in name for x in [f"sa2_to_{ra}", f"asgs_to_{ra}", f"sla_to_{ra}"]):
        return pd.DataFrame({"ASGS": [123], ra: [3]})
    if f"hospital_{ra}" in name:
        return pd.DataFrame({"APCID": ["HOSP"], f"_hosp_ra_{ra_year}": [4]})
    if "aa_adj_icu" in name:
        return pd.DataFrame({"icu_rate": [0.05]})
    if "aa_sa_adj_rt" in name:
        return pd.DataFrame()
    if "aa_sa_adj_ds" in name:
        return pd.DataFrame()
    return pd.DataFrame()


@pytest.mark.parametrize("year", YEARS)
def test_proc_adjustments(monkeypatch, year):
    monkeypatch.setattr(
        acute,
        "_load_price_weights",
        lambda *_: _make_weights(adj_radiotherapy=0.1, adj_dialysis=0.2),
    )
    monkeypatch.setattr(acute, "load_sas_table", _fake_load)

    df = pd.DataFrame(
        {
            "DRG": ["AAA"],
            "LOS": [3],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PROC1": [11111],
            "PROC2": [22222],
        }
    )

    res = acute.calculate_acute(
        df, acute.AcuteParams(icu_paed_option=2), year=year, ref_dir=Path("unused")
    )
    assert res["adj_radiotherapy"][0] == 0.1
    assert res["adj_dialysis"][0] == 0.2
    assert res["NWAU25"][0] == pytest.approx(1.3, rel=1e-4)


@pytest.mark.parametrize("year", YEARS)
def test_icu_and_paediatric(monkeypatch, year):
    monkeypatch.setattr(acute, "_load_price_weights", _make_weights)
    monkeypatch.setattr(acute, "load_sas_table", _fake_load)

    df = pd.DataFrame(
        {
            "DRG": ["AAA"],
            "LOS": [5],
            "ICU_HOURS": [48],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "APCID": ["HOSP"],
        }
    )

    res = acute.calculate_acute(
        df, acute.AcuteParams(debug_mode=True), year=year, ref_dir=Path("unused")
    )
    assert res["_est_eligible_icu_flag"][0] == 1
    assert res["_est_eligible_paed_flag"][0] == 1
    assert res["NWAU25"][0] == pytest.approx(3.4, rel=1e-4)


@pytest.mark.parametrize("year", YEARS)
def test_private_patient_deductions(monkeypatch, year):
    monkeypatch.setattr(acute, "_load_price_weights", _make_weights)
    monkeypatch.setattr(acute, "load_sas_table", _fake_load)

    base = pd.DataFrame(
        {
            "DRG": ["AAA"],
            "LOS": [4],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [1],
            "STATE": [1],
        }
    )

    res1 = acute.calculate_acute(
        base.copy(), acute.AcuteParams(ppservadj=1), year=year, ref_dir=Path("unused")
    )
    assert res1["NWAU25"][0] == pytest.approx(0.86, rel=1e-4)

    res2 = acute.calculate_acute(
        base.copy(), acute.AcuteParams(ppservadj=2), year=year, ref_dir=Path("unused")
    )
    assert res2["NWAU25"][0] == pytest.approx(0.86, rel=1e-4)


@pytest.mark.parametrize("year", YEARS)
def test_remoteness_adjustments(monkeypatch, year):
    monkeypatch.setattr(
        acute,
        "_load_price_weights",
        lambda *_: _make_weights(adj_remoteness=0.2, adj_treat_remoteness=0.05),
    )
    monkeypatch.setattr(acute, "load_sas_table", _fake_load)

    df = pd.DataFrame(
        {
            "DRG": ["AAA"],
            "LOS": [3],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "APCID": ["HOSP"],
            "PAT_POSTCODE": ["PC1"],
            "PAT_SA2": [123],
        }
    )

    res = acute.calculate_acute(
        df, acute.AcuteParams(debug_mode=True), year=year, ref_dir=Path("unused")
    )
    assert res["_pat_remoteness"][0] == 3
    assert res["_treat_remoteness"][0] == 4
    assert res["NWAU25"][0] == pytest.approx(1.26, rel=1e-4)


def test_calculate_acute_polars_native_input_and_output(monkeypatch):
    import polars as pl

    weights = pl.DataFrame(
        {
            "DRG": ["801A"],
            "drg_inlier_lb": [2.0],
            "drg_inlier_ub": [20.0],
            "drg_adj_paed": [1.0],
            "drg_samedaylist_flag": [0],
            "drg_bundled_icu_flag": [0],
            "drg_pw_sso_base": [1.0],
            "drg_pw_sso_perdiem": [0.5],
            "drg_pw_inlier": [5.0],
            "drg_pw_lso_perdiem": [0.2],
            "drg_adj_privpat_serv": [0.0],
        }
    )
    monkeypatch.setattr(acute, "_load_price_weights", lambda *_: weights)

    df_pl = pl.DataFrame(
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

    res_rust = acute.calculate_acute_rust_2025(
        df_pl,
        acute.AcuteParams(),
        year="2025",
        ref_dir=Path("tests/data/2025"),
    )
    assert isinstance(res_rust, pl.DataFrame)
    assert "NWAU25" in res_rust.columns
    assert res_rust["NWAU25"][0] == pytest.approx(6.8772)

    res_py = acute.calculate_acute(
        df_pl,
        acute.AcuteParams(),
        year="2025",
        ref_dir=Path("tests/data/2025"),
    )
    assert isinstance(res_py, pl.DataFrame)
    assert "NWAU25" in res_py.columns
    assert res_py["NWAU25"][0] == pytest.approx(6.8772)
