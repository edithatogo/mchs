import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add project root to path so modules can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

spec = importlib.util.spec_from_file_location(
    "mh",
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "mh.py",
)
mh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mh)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_weights(*_, **__):
    return {
        "adm": pd.DataFrame(
            {
                "AMHCC": ["1001"],
                "priceCat": [1],
                "amhcc_inlier_lb": [3],
                "amhcc_inlier_ub": [5],
                "amhcc_pw_sso_base": [1.0],
                "amhcc_pw_sso_perdiem": [0.2],
                "amhcc_pw_inlier": [1.5],
                "amhcc_pw_lso_perdiem": [0.3],
            }
        ),
        "cmty": pd.DataFrame(
            {
                "AMHCC": ["2001"],
                "_cmty_fixed_pw": [0.0],
                "_cmty_sc_pat_pw": [0.1],
                "_cmty_sc_nopat_pw": [0.2],
            }
        ),
        "ppsa": pd.DataFrame(
            {
                "amhccV1code": ["1001"],
                "state": [1],
                "amhcc_adj_privPat_serv": [0.1],
                "amhcc_adj_privPat_servNat": [0.15],
            }
        ),
        "priv_acc": pd.DataFrame(
            {
                "State": [1],
                "state_adj_privpat_accomm_sd": [0.01],
                "state_adj_privpat_accomm_on": [0.02],
            }
        ),
        "specpaed": pd.DataFrame({"_pat_specpaed": [0], "adj_specpaed": [1]}),
        "adj_ind": pd.DataFrame({"_pat_ind_flag": [0], "adj_indigenous": [0.0]}),
        "adj_rem": pd.DataFrame({"_pat_remoteness": [0], "adj_remoteness": [0.0]}),
        "adj_treat": pd.DataFrame(
            {"_treat_remoteness": [0], "adj_treat_remoteness": [0.0]}
        ),
    }


def test_mh_reference_loader_decodes_all_tables(monkeypatch):
    expected_names = [
        "mh_adm_price_weights",
        "mh_cmty_price_weights",
        "mh_ppsa",
        "mh_adj_priv_acc",
        "mh_adj_specpaed",
        "aa_mh_sa_na_ed_adj_ind",
        "aa_mh_sa_na_adj_rem",
        "aa_mh_sa_na_adj_treat_rem",
    ]
    calls: list[str] = []

    def fake_read_sas(path):
        name = Path(path).name
        calls.append(name)
        return pd.DataFrame({"code": [b"A"], "value": [1.0]})

    monkeypatch.setattr(pd, "read_sas", fake_read_sas)

    spec = importlib.util.spec_from_file_location(
        "mh_loader_test",
        Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "mh.py",
    )
    assert spec is not None and spec.loader is not None
    fresh_mh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fresh_mh)
    tables = fresh_mh._load_weights(Path("ref"), "2025")

    assert set(tables) == {
        "adm",
        "cmty",
        "ppsa",
        "priv_acc",
        "specpaed",
        "adj_ind",
        "adj_rem",
        "adj_treat",
    }
    assert all(table["code"].tolist() == ["A"] for table in tables.values())
    assert all(any(expected in call for call in calls) for expected in expected_names)


DATA = pd.DataFrame(
    {
        "AMHCC": ["1001", "1001", "1001", "2001"],
        "LOS": [2, 4, 7, np.nan],
        "PAT_PRIVATE_FLAG": [0, 1, 0, 0],
        "PAT_SAMEDAY_FLAG": [0, 0, 0, 0],
        "STATE": [1, 1, 1, 1],
        "SC_PAT_PUB": [0, 0, 0, 1],
        "SC_NOPAT_PUB": [0, 0, 0, 0],
        "_pat_specpaed": [0, 0, 0, 0],
        "_pat_ind_flag": [0, 0, 0, 0],
        "_pat_remoteness": [0, 0, 0, 0],
        "_treat_remoteness": [0, 0, 0, 0],
    }
)


@pytest.fixture(autouse=True)
def _patch(monkeypatch):
    monkeypatch.setattr(mh, "_load_weights", _load_weights)


def test_calculate_mh_basic():
    res = mh.calculate_mh(
        DATA.copy(),
        mh.MHParams(debug_mode=True),
        ref_dir=Path("unused"),
    )
    sepcat = res["_pat_separation_category"].tolist()
    assert sepcat[:3] == [2, 3, 4]
    assert np.isnan(sepcat[3])
    assert np.allclose(res["_w01"].values, [1.4, 1.5, 2.1, 0.1])
    assert np.allclose(res["NWAU25"].values, [1.4, 1.195, 2.1, 0.1])


def test_private_patient_service_adjustment():
    res1 = mh.calculate_mh(
        DATA.copy(),
        mh.MHParams(ppsa_option=1),
        ref_dir=Path("unused"),
    )
    res2 = mh.calculate_mh(
        DATA.copy(),
        mh.MHParams(ppsa_option=2),
        ref_dir=Path("unused"),
    )
    assert res1.loc[1, "NWAU25"] == pytest.approx(1.195, rel=1e-4)
    assert res2.loc[1, "NWAU25"] == pytest.approx(1.27, rel=1e-4)


def test_substream_toggles():
    adm_off = mh.calculate_mh(
        DATA.copy(),
        mh.MHParams(adm_sstream=0),
        ref_dir=Path("unused"),
    )
    assert np.allclose(adm_off["NWAU25"].values, [0, 0, 0, 0.1])
    cmty_off = mh.calculate_mh(
        DATA.copy(),
        mh.MHParams(cmty_sstream=0),
        ref_dir=Path("unused"),
    )
    assert cmty_off.loc[3, "NWAU25"] == 0
    assert cmty_off.loc[:2, "NWAU25"].tolist() == pytest.approx([1.4, 1.195, 2.1])
