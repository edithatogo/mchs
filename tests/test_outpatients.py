from pathlib import Path

import pandas as pd

import nwau_py.calculators.outpatients as outpatients


def _weights(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "TIER2_CLINIC": [20.48, 20.5, 20.56, 40.62],
            "clinic_pw": [1.0, 2.0, 3.0, 4.0],
            "tier2_adj_paed": [1.1, 1.2, 1.3, 1.4],
        }
    )


def _sequence(*frames: pd.DataFrame):
    state = {"index": 0}

    def _loader(*_args, **_kwargs):
        index = state["index"]
        state["index"] = index + 1
        if index < len(frames):
            return frames[index].copy()
        return pd.DataFrame()

    return _loader


def _load_multi_prov_adj(*_args, **_kwargs) -> float:
    return 0.1


def _load_hospital_ra(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame(
        {"APCID": ["A1", "A2", "A3", "A4"], "_hosp_ra_2021": [1, 1, 1, 1]}
    )


def _load_postcode_ra(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame({"POSTCODE": ["P1"], "ra2021": [1]})


def _load_sa2_ra(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame({"SA2": [100], "ra2021": [1]})


def _load_icu_list(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame(
        {"APCID": ["A1", "A2", "A3", "A4"], "_est_eligible_paed_flag": [1, 1, 1, 1]}
    )


def _load_ind_adj(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame({"_pat_ind_flag": [0, 1], "adj_indigenous": [0.0, 0.2]})


def _load_pat_rem_adj(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame({"_pat_remoteness": [1], "adj_remoteness": [0.1]})


def _load_treat_rem_adj(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame({"_treat_remoteness": [1], "adj_treat_remoteness": [0.05]})


def _load_weights_alt(*_args, **_kwargs) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "TIER2_CLINIC": [20.5],
            "clinic_pw": [1.5],
            "tier2_adj_paed": [1.0],
        }
    )


def _patch_common(monkeypatch):
    monkeypatch.setattr(outpatients, "_load_weights", _weights)
    monkeypatch.setattr(outpatients, "_load_multi_prov_adj", _load_multi_prov_adj)
    monkeypatch.setattr(outpatients, "_load_hospital_ra", _load_hospital_ra)
    monkeypatch.setattr(outpatients, "_load_postcode_ra", _load_postcode_ra)
    monkeypatch.setattr(outpatients, "_load_sa2_ra", _load_sa2_ra)
    monkeypatch.setattr(outpatients, "_load_icu_list", _load_icu_list)
    monkeypatch.setattr(
        outpatients,
        "_load_ind_adj",
        _sequence(pd.DataFrame(), pd.DataFrame(), _load_ind_adj(), pd.DataFrame()),
    )
    monkeypatch.setattr(
        outpatients,
        "_load_pat_rem_adj",
        _sequence(pd.DataFrame(), _load_pat_rem_adj(), pd.DataFrame()),
    )
    monkeypatch.setattr(
        outpatients,
        "_load_treat_rem_adj",
        _sequence(pd.DataFrame(), _load_treat_rem_adj(), pd.DataFrame()),
    )


def test_calculate_outpatients_basic_and_branch_coverage(monkeypatch):
    _patch_common(monkeypatch)
    data = pd.DataFrame(
        {
            "TIER2_CLINIC": [20.5, 20.48, 20.5, 20.5],
            "APCID": ["A1", "A2", "A3", "A4"],
            "PAT_POSTCODE": ["P1", "P1", "P1", "P1"],
            "PAT_SA2": [100, 100, 100, 100],
            "SERVICE_DATE": [
                pd.Timestamp("2024-07-01"),
                pd.Timestamp("2024-07-01"),
                pd.Timestamp("2024-07-01"),
                pd.Timestamp("2024-07-01"),
            ],
            "BIRTH_DATE": [
                pd.Timestamp("2015-01-01"),
                pd.Timestamp("2015-01-01"),
                pd.Timestamp("1980-01-01"),
                pd.Timestamp("2015-01-01"),
            ],
            "INDSTAT": [1, 0, 0, 1],
            "FUNDSC": [1, 1, 1, 1],
            "PAT_MULTIPROV_FLAG": [1, 1, 1, 0],
            "EST_REMOTENESS": [1, 1, 1, 1],
        }
    )

    result = outpatients.calculate_outpatients(
        data,
        outpatients.OutpatientParams(debug_mode=True),
        year="2025",
        ref_dir=Path("unused"),
    )

    assert len(result) == 4
    assert result["Error_Code"].tolist() == [0, 0, 0, 0]
    assert result["_pat_eligible_paed_flag"].tolist() == [1, 1, 0, 1]
    assert result["_pat_remoteness"].tolist() == [1, 1, 1, 1]
    assert result["NWAU25"].gt(0).all()
    assert result["NWAU25"].nunique() > 1


def test_calculate_outpatients_data_type_two(monkeypatch):
    _patch_common(monkeypatch)
    monkeypatch.setattr(outpatients, "_load_weights", _load_weights_alt)
    data = pd.DataFrame(
        {
            "TIER2_CLINIC": [20.5],
            "GROUP_EVENT_COUNT": [1],
            "INDIV_EVENT_COUNT": [2],
            "MULTI_DISP_CONF_COUNT": [3],
            "FUNDSC": [1],
            "PAT_MULTIPROV_FLAG": [1],
            "EST_REMOTENESS": [1],
        }
    )

    result = outpatients.calculate_outpatients(
        data,
        outpatients.OutpatientParams(
            data_type=2,
            est_remoteness_option=2,
            paed_option=2,
            debug_mode=True,
        ),
        year="2025",
        ref_dir=Path("unused"),
    )

    assert result["Error_Code"].iloc[0] == 0
    assert result["NWAU25"].iloc[0] > 0


def test_outpatient_reference_loaders_decode_and_normalize_tables(monkeypatch):
    read_sas_calls: list[Path] = []
    load_sas_calls: list[Path] = []

    def fake_read_sas(path):
        read_sas_calls.append(Path(path))
        name = Path(path).name
        if "price_weights" in name:
            return pd.DataFrame(
                {
                    "clinic_code": [b"20.48"],
                    "description": [b"Synthetic clinic"],
                    "clinic_pw": [1.0],
                }
            )
        return pd.DataFrame(
            {
                "APCID_VALUE": [b"A1"],
                "_est_eligible_paed_flag": [1],
            }
        )

    def fake_load_sas_table(path):
        load_sas_calls.append(Path(path))
        name = Path(path).name
        if "hospital" in name:
            return pd.DataFrame({"APCID_CODE": [b"A1"], "RA2021": [2]})
        if "postcode" in name:
            return pd.DataFrame({"POSTCODE": [b"2000"], "RA2021": [1]})
        if "sa2_to" in name:
            raise FileNotFoundError(path)
        if "asgs_to" in name:
            return pd.DataFrame({"ASGS": [100], "RA2021": [3]})
        if "multi_prov" in name:
            return pd.DataFrame({"adj_multiprov": [0.25], "note": [b"ok"]})
        if "adj_ind" in name:
            return pd.DataFrame({"_pat_ind_flag": [1], "adj_indigenous": [0.2]})
        if "adj_rem" in name:
            return pd.DataFrame({"_pat_remoteness": [1], "adj_remoteness": [0.1]})
        if "treat_rem" in name:
            return pd.DataFrame(
                {"_treat_remoteness": [1], "adj_treat_remoteness": [0.05]}
            )
        raise AssertionError(f"unexpected path: {path}")

    monkeypatch.setattr(pd, "read_sas", fake_read_sas)
    monkeypatch.setattr(outpatients, "load_sas_table", fake_load_sas_table)

    weights = outpatients._load_weights(Path("ref"), "2025")
    hospital = outpatients._load_hospital_ra(Path("ref"), "2025")
    postcode = outpatients._load_postcode_ra(Path("ref"), "2025")
    sa2 = outpatients._load_sa2_ra(Path("ref"), "2025")
    icu = outpatients._load_icu_list(Path("ref"), "2025")

    assert weights["TIER2_CLINIC"].tolist() == ["20.48"]
    assert weights["description"].tolist() == ["Synthetic clinic"]
    assert hospital.to_dict("records") == [{"APCID": "A1", "_hosp_ra_2021": 2}]
    assert postcode[["POSTCODE", "ra2021"]].to_dict("records") == [
        {"POSTCODE": "2000", "ra2021": 1}
    ]
    assert sa2.to_dict("records") == [{"SA2": 100, "ra2021": 3}]
    assert icu.to_dict("records") == [{"APCID": "A1", "_est_eligible_paed_flag": 1}]
    assert outpatients._load_multi_prov_adj(Path("ref"), "2025") == 0.25
    assert outpatients._load_ind_adj(Path("ref"), "2025")["adj_indigenous"].iloc[0] == 0.2
    assert outpatients._load_pat_rem_adj(Path("ref"), "2025")["adj_remoteness"].iloc[0] == 0.1
    assert (
        outpatients._load_treat_rem_adj(Path("ref"), "2025")[
            "adj_treat_remoteness"
        ].iloc[0]
        == 0.05
    )
    assert read_sas_calls
    assert load_sas_calls


def test_outpatient_optional_reference_loaders_fail_closed(monkeypatch):
    def missing(*_args, **_kwargs):
        raise FileNotFoundError("missing")

    def broken(*_args, **_kwargs):
        raise RuntimeError("broken")

    monkeypatch.setattr(outpatients, "load_sas_table", missing)
    assert outpatients._load_multi_prov_adj(Path("ref"), "2025") == 0.0
    assert outpatients._load_ind_adj(Path("ref"), "2025").empty
    assert outpatients._load_pat_rem_adj(Path("ref"), "2025").empty
    assert outpatients._load_treat_rem_adj(Path("ref"), "2025").empty

    monkeypatch.setattr(outpatients, "load_sas_table", broken)
    assert outpatients._load_multi_prov_adj(Path("ref"), "2025") == 0.0
    assert outpatients._load_ind_adj(Path("ref"), "2025").empty
    assert outpatients._load_pat_rem_adj(Path("ref"), "2025").empty
    assert outpatients._load_treat_rem_adj(Path("ref"), "2025").empty
