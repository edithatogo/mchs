import pathlib
import sys

from nwau_py import compat as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from nwau_py.groupers import flag_diagnoses, group_readmissions, load_ahr_maps
from nwau_py.scoring import score_readmission

MAP_DIR = pathlib.Path("archive/sas/NEP25_SAS_NWAU_calculator/calculators")
PARAM_DIR = MAP_DIR / "params"
MODEL_DIR = MAP_DIR / "models"


def test_load_maps():
    maps = load_ahr_maps(MAP_DIR)
    assert "08" in maps
    assert "DDX" in maps["08"].columns


def test_flagging_example():
    maps = load_ahr_maps(MAP_DIR)
    df = pd.DataFrame(
        {
            "ddx1": ["A021"],
            "onset1": ["2"],
            "ddx2": ["Z999"],
            "onset2": ["1"],
        }
    )
    flagged = flag_diagnoses(df, maps, "08")
    assert "AHR030c01p01" in flagged.columns
    assert flagged.loc[0, "AHR030c01p01"] in {0, 1}


def test_scorer_runs():
    features = [
        "adm_past_year",
        "agegroup_rm",
        "an110mdc_ra",
        "cc_acute_myocardial_function",
        "cc_arthritis_and_osteoarthritis",
        "cc_cerebral_palsy",
        "cc_chronic_heart_failure",
        "cc_chronic_kidney_disease",
        "cc_chronic_respiratory_failure",
        "cc_congestive_heart_failure",
        "cc_copd",
        "cc_crohns_disease",
        "cc_dementia",
        "cc_depression",
        "cc_diabetes",
        "cc_diabetes_complications",
        "cc_disorder_of_intellectual",
        "cc_downs_syndrome",
        "cc_hypertension",
        "cc_ischaemic_heart_disease",
        "cc_obesity",
        "cc_osteoporosis",
        "cc_pulmonary_disease",
        "cc_renal_disease",
        "cc_severe_liver_disease",
        "cc_spina_bifida",
        "cc_tetplg_prplg_dplg_hmplg_dt",
        "count_proc",
        "drg11_type_m",
        "drug_use",
        "flag_admtransfer",
        "flag_emergency",
        "flag_icu24",
        "indstat_flag",
        "low_los_flag",
        "malnutrition",
        "pacemaker",
        "pat_remoteness",
        "post_transplant",
        "sex_cat",
    ]
    data = pd.DataFrame({c: [0] for c in features})
    scores = score_readmission(data)
    assert scores.filter(like="readm_points").shape[1] == 12


def test_grouping_and_scoring():
    maps = load_ahr_maps(MAP_DIR)
    df = pd.DataFrame(
        {
            "patient_id": ["p1", "p1"],
            "adm_date": ["2024-01-01", "2024-01-03"],
            "sep_date": ["2024-01-02", "2024-01-05"],
            "ddx1": ["Z999", "A021"],
            "onset1": ["1", "2"],
        }
    )
    res = group_readmissions(df, maps, "08")
    assert res.loc[1, "AHR030c02p11_flag"] == 1
    assert res.loc[1, "ahr_flag"] == 1
    assert "dampening1" in res.columns


def test_polars_native_grouping_and_scoring():
    import polars as pl

    maps = load_ahr_maps(MAP_DIR)
    df = pl.DataFrame(
        {
            "patient_id": ["p1", "p1"],
            "adm_date": ["2024-01-01", "2024-01-03"],
            "sep_date": ["2024-01-02", "2024-01-05"],
            "ddx1": ["Z999", "A021"],
            "onset1": ["1", "2"],
        }
    )
    res = group_readmissions(df, maps, "08")
    assert isinstance(res, pl.DataFrame)
    assert res["AHR030c02p11_flag"][1] == 1
    assert res["ahr_flag"][1] == 1
    assert "dampening1" in res.columns
