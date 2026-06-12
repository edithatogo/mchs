# ruff: noqa
import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nwau_py.utils import RA_VERSION, ra_suffix

# Editions with verified reference data
YEARS = [y for y in sorted(RA_VERSION.keys()) if int(y) >= 2025]

spec = importlib.util.spec_from_file_location(
    "subacute",
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "subacute.py",
)
subacute = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subacute)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _basic_weights(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
    df = pd.read_csv("tests/data/nep25_sa_snap_price_weights.csv")
    df = df.rename(columns={"ansnap": "ANSNAP"})
    return df


def test_subacute_weight_loader_decodes_and_normalizes_ansnap_columns(monkeypatch):
    frames = [
        pd.DataFrame({"ansnap": [b"5AZ1"], "weight": [1.0]}),
        pd.DataFrame({"snap": [b"5AZ2"], "weight": [2.0]}),
    ]

    def fake_read_sas(_path):
        return frames.pop(0)

    monkeypatch.setattr(pd, "read_sas", fake_read_sas)

    spec = importlib.util.spec_from_file_location(
        "subacute_loader_test",
        Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "subacute.py",
    )
    assert spec is not None and spec.loader is not None
    fresh_subacute = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fresh_subacute)
    ansnap = fresh_subacute._load_weights(Path("ref"), "2025")
    snap = fresh_subacute._load_weights(Path("ref"), "2025")

    assert ansnap.to_dict("records") == [{"ANSNAP": "5AZ1", "weight": 1.0}]
    assert snap.to_dict("records") == [{"ANSNAP": "5AZ2", "weight": 2.0}]


def _fake_load(path: Path, *_, **__):
    name = path.name
    match = re.search(r"ra\d{4}", name)
    ra = match.group(0) if match else ra_suffix("2025")
    ra_year = ra[2:]
    if "aa_sa_adj_rt" in name:
        return pd.DataFrame(
            {"_pat_radiotherapy_flag": [0, 1], "adj_radiotherapy": [0.0, 0.1]}
        )
    if "aa_sa_adj_ds" in name:
        return pd.DataFrame({"_pat_dialysis_flag": [0, 1], "adj_dialysis": [0.0, 0.2]})
    if "radio_codes" in name:
        return pd.DataFrame({"code_ID": [12345]})
    if "dialysis_codes" in name:
        return pd.DataFrame({"code_ID": [22222]})
    match = re.search(r"ra\d{4}", name)
    if match:
        ra = match.group(0)
        ra_year = ra[2:]
        if name.startswith("postcode_to_"):
            return pd.DataFrame({"POSTCODE": ["PC0001"], ra: [1]})
        if any(
            name.startswith(prefix) for prefix in ["sa2_to_", "asgs_to_", "sla_to_"]
        ):
            return pd.DataFrame({"ASGS": [100000001], ra: [1]})
        if "hospital_" in name:
            return pd.DataFrame({"ESTID": ["H1"], f"_hosp_ra_{ra_year}": [1]})
    if f"postcode_to_{ra}" in name:
        return pd.DataFrame({"POSTCODE": ["PC0001"], ra: [1]})
    if any(x in name for x in [f"sa2_to_{ra}", f"asgs_to_{ra}", f"sla_to_{ra}"]):
        return pd.DataFrame({"ASGS": [100000001], ra: [1]})
    if f"hospital_{ra}" in name:
        return pd.DataFrame({"ESTID": ["H1"], f"_hosp_ra_{ra_year}": [1]})
    if "aa_mh_sa_na_ed_adj_ind" in name:
        return pd.DataFrame({"_pat_ind_flag": [0, 1], "adj_indigenous": [0.0, 0.05]})
    if "aa_mh_sa_na_adj_rem" in name:
        return pd.DataFrame({"_pat_remoteness": [0, 1], "adj_remoteness": [0.0, 0.1]})
    if "aa_mh_sa_na_adj_treat_rem" in name:
        return pd.DataFrame(
            {"_treat_remoteness": [0, 1], "adj_treat_remoteness": [0.0, 0.02]}
        )
    if "sa_adj_priv_serv_state" in name:
        return pd.DataFrame(
            {
                "STATE": [1],
                "_care": [3],
                "caretype_adj_privpat_serv_nat": [0.1],
                "caretype_adj_privpat_serv_state": [0.2],
            }
        )
    if "aa_sa_adj_priv_acc" in name:
        return pd.DataFrame(
            {
                "STATE": [1],
                "state_adj_privpat_accomm_sd": [0.0],
                "state_adj_privpat_accomm_on": [0.0],
            }
        )
    raise FileNotFoundError(path)


BASE_DATA = pd.DataFrame(
    {
        "ANSNAP": ["5AZ1"],
        "ADM_DATE": [pd.Timestamp("2024-07-01")],
        "SEP_DATE": [pd.Timestamp("2024-08-10")],
        "LEAVE_DAYS": [0],
        "BIRTH_DATE": [pd.Timestamp("1980-01-01")],
        "PAT_PRIVATE_FLAG": [0],
        "PAT_PUBLIC_FLAG": [1],
        "STATE": [1],
        "CARE_TYPE": [3],
        "PAT_POSTCODE": ["PC0001"],
        "PAT_SA2": [100000001],
        "ESTID": ["H1"],
    }
)
EXPECTED_BASE = 13.4327 * 1.1 * 1.02


@pytest.fixture(autouse=True)
def _patch(monkeypatch):
    monkeypatch.setattr(subacute, "_load_weights", _basic_weights)
    monkeypatch.setattr(subacute, "load_sas_table", _fake_load)


@pytest.mark.parametrize("year", YEARS)
def test_calculate_subacute_basic(year):
    res = subacute.calculate_subacute(
        BASE_DATA.copy(), subacute.SubacuteParams(), year=year, ref_dir=Path("unused")
    )
    assert res["NWAU25"].iloc[0] == pytest.approx(EXPECTED_BASE, rel=1e-4)
    assert res["Error_Code"].iloc[0] == 0

    debug = subacute.calculate_subacute(
        BASE_DATA.copy(),
        subacute.SubacuteParams(debug_mode=True),
        year=year,
        ref_dir=Path("unused"),
    )
    assert any(c.startswith("_") for c in debug.columns)


@pytest.mark.parametrize("year", YEARS)
def test_option_paths(year):
    data = BASE_DATA.copy()
    data["PAT_RADIOTHERAPY_FLAG"] = 1
    data["PAT_DIALYSIS_FLAG"] = 0
    data["EST_REMOTENESS"] = 1
    params = subacute.SubacuteParams(
        radiotherapy_option=2,
        dialysis_option=2,
        est_remoteness_option=2,
    )
    res = subacute.calculate_subacute(data, params, year=year, ref_dir=Path("unused"))
    expected = 13.4327 * (1 + 0.1 + 0.1) * 1.02
    assert res["NWAU25"].iloc[0] == pytest.approx(expected, rel=1e-4)


@pytest.mark.parametrize("year", YEARS)
def test_ppsa_option(year):
    data = BASE_DATA.copy()
    data["PAT_PRIVATE_FLAG"] = 1
    data["PAT_PUBLIC_FLAG"] = 0
    res1 = subacute.calculate_subacute(
        data.copy(),
        subacute.SubacuteParams(ppsa_option=1),
        year=year,
        ref_dir=Path("unused"),
    )
    expected1 = EXPECTED_BASE - 13.4327 * 0.1
    assert res1["NWAU25"].iloc[0] == pytest.approx(expected1, rel=1e-4)

    res2 = subacute.calculate_subacute(
        data.copy(),
        subacute.SubacuteParams(ppsa_option=2),
        year=year,
        ref_dir=Path("unused"),
    )
    expected2 = EXPECTED_BASE - 13.4327 * 0.2
    assert res2["NWAU25"].iloc[0] == pytest.approx(expected2, rel=1e-4)


@pytest.mark.parametrize("year", YEARS)
def test_paediatric_error(year):
    data = BASE_DATA.copy()
    data["BIRTH_DATE"] = pd.Timestamp("2015-01-01")
    res = subacute.calculate_subacute(
        data, subacute.SubacuteParams(), year=year, ref_dir=Path("unused")
    )
    assert res["Error_Code"].iloc[0] == 1
    assert res["NWAU25"].iloc[0] == 0


@pytest.mark.parametrize("year", YEARS)
def test_procedure_flags(year):
    data = BASE_DATA.copy()
    data["PROC1"] = 12345
    data["PROC2"] = 22222
    params = subacute.SubacuteParams(debug_mode=True)
    res = subacute.calculate_subacute(data, params, year=year, ref_dir=Path("unused"))
    assert res["_pat_radiotherapy_flag"].iloc[0] == 1
    assert res["_pat_dialysis_flag"].iloc[0] == 1
    expected = 13.4327 * (1 + 0.1 + 0.1 + 0.2) * 1.02
    assert res["NWAU25"].iloc[0] == pytest.approx(expected, rel=1e-4)
