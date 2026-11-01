from __future__ import annotations

# ruff: noqa: I001

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
from nwau_py import compat as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import validation_tooling as validation
from nwau_py import rust_bridge

PYREADSTAT = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

ACUTE_PATH = (
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "acute.py"
)
SPEC = importlib.util.spec_from_file_location("validation_tooling_acute", ACUTE_PATH)
assert SPEC is not None and SPEC.loader is not None
acute = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acute)

BASE = Path("tests/data")


def _load_weights(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
    weights = pd.read_csv(BASE / "nep25_aa_price_weights.csv")
    weights["DRG"] = weights["DRG"].str.strip("b'")
    return weights


def _acute_frame_strategy(hypothesis):
    st = hypothesis.strategies
    row = st.fixed_dictionaries(
        {
            "DRG": st.sampled_from(["801A", "801B", "801C"]),
            "LOS": st.integers(min_value=1, max_value=90),
            "ICU_HOURS": st.integers(min_value=0, max_value=24),
            "ICU_OTHER": st.integers(min_value=0, max_value=24),
            "PAT_SAMEDAY_FLAG": st.integers(min_value=0, max_value=1),
            "PAT_PRIVATE_FLAG": st.integers(min_value=0, max_value=1),
            "PAT_COVID_FLAG": st.integers(min_value=0, max_value=1),
            "COVID_ADJ_FLAG": st.integers(min_value=0, max_value=1),
            "PAT_RADIOTHERAPY_FLAG": st.integers(min_value=0, max_value=1),
            "PAT_DIALYSIS_FLAG": st.integers(min_value=0, max_value=1),
            "EST_ELIGIBLE_ICU_FLAG": st.integers(min_value=0, max_value=1),
            "EST_ELIGIBLE_PAED_FLAG": st.integers(min_value=0, max_value=1),
            "EST_REMOTENESS": st.integers(min_value=0, max_value=5),
            "STATE": st.integers(min_value=1, max_value=8),
        }
    )
    return st.lists(row, min_size=1, max_size=4).map(
        lambda rows: pd.DataFrame(
            rows,
            columns=[
                "DRG",
                "LOS",
                "ICU_HOURS",
                "ICU_OTHER",
                "PAT_SAMEDAY_FLAG",
                "PAT_PRIVATE_FLAG",
                "PAT_COVID_FLAG",
                "COVID_ADJ_FLAG",
                "PAT_RADIOTHERAPY_FLAG",
                "PAT_DIALYSIS_FLAG",
                "EST_ELIGIBLE_ICU_FLAG",
                "EST_ELIGIBLE_PAED_FLAG",
                "EST_REMOTENESS",
                "STATE",
            ],
        )
    )


def _starter_params() -> acute.AcuteParams:
    return acute.AcuteParams(
        icu_paed_option=2,
        covid_option=2,
        covid_adj_option=2,
        radiotherapy_option=2,
        dialysis_option=2,
        ppservadj=2,
        est_remoteness_option=2,
    )


def test_validation_tooling_mutmut_starter_targets_focus_on_pure_modules():
    assert validation.MUTATION_TARGETS == (
        "nwau_py/calculators/adjust.py",
        "nwau_py/calculators/funding_formula.py",
        "nwau_py/utils.py",
    )
    assert all("loader.py" not in target for target in validation.MUTATION_TARGETS)
    assert all("archive/" not in target for target in validation.MUTATION_TARGETS)
    assert all("tests/" not in target for target in validation.MUTATION_TARGETS)


def test_validation_tooling_scalene_reports_stay_under_cache_tree():
    report_path = validation.scalene_report_path("acute starter profile")
    assert report_path == Path(".cache/validation/scalene/acute_starter_profile.txt")
    assert not report_path.is_absolute()
    assert report_path.parts[:3] == (".cache", "validation", "scalene")


def test_validation_tooling_hypothesis_profile_budget_is_small():
    assert validation.hypothesis_settings_kwargs() == {
        "max_examples": 5,
        "deadline": None,
    }


def test_acute_params_default_flags_match_the_current_contract():
    params = acute.AcuteParams()

    assert params.icu_paed_option == 1
    assert params.covid_option == 1
    assert params.covid_adj_option == 1
    assert params.radiotherapy_option == 1
    assert params.dialysis_option == 1
    assert params.ppservadj == 1
    assert params.est_remoteness_option == 1
    assert params.debug_mode is False
    assert params.clear_data is False


def test_validation_tooling_hypothesis_acute_output_shape_and_finiteness(monkeypatch):
    hypothesis = pytest.importorskip("hypothesis")
    from hypothesis import given, settings

    @given(frame=_acute_frame_strategy(hypothesis))
    @settings(**validation.hypothesis_settings_kwargs())
    def run_case(frame: pd.DataFrame) -> None:
        monkeypatch.setattr(acute, "_load_price_weights", _load_weights)
        result = acute.calculate_acute(
            frame,
            _starter_params(),
            year="2025",
            ref_dir=BASE / "2025",
        )
        assert len(result) == len(frame)
        assert "NWAU25" in result.columns
        assert np.isfinite(result["NWAU25"].astype(float)).all()
        assert result["NWAU25"].ge(0).all()

    run_case()


def test_acute_reference_row_from_weights_normalizes_core_fields():
    row = pd.Series(
        {
            "DRG": "801A",
            "drg_inlier_lb": 1,
            "drg_inlier_ub": 2,
            "drg_adj_paed": 1.5,
            "drg_samedaylist_flag": 1,
            "drg_bundled_icu_flag": 0,
            "drg_pw_sso_base": 3,
            "drg_pw_sso_perdiem": 4,
            "drg_pw_inlier": 5,
            "drg_pw_lso_perdiem": 6,
            "drg_adj_privpat_serv": 7,
        }
    )

    result = acute._acute_reference_row_from_weights(row)

    assert result == {
        "drg": "801A",
        "inlier_lower_bound": 1.0,
        "inlier_upper_bound": 2.0,
        "paediatric_multiplier": 1.5,
        "same_day_list_flag": True,
        "bundled_icu_flag": False,
        "same_day_base_weight": 3.0,
        "same_day_per_diem": 4.0,
        "inlier_weight": 5.0,
        "long_stay_per_diem": 6.0,
        "private_service_adjustment": 7.0,
    }


def test_acute_reference_row_from_weights_fills_missing_optional_values():
    row = pd.Series({"DRG": "801B"})

    result = acute._acute_reference_row_from_weights(row)

    assert result == {
        "drg": "801B",
        "inlier_lower_bound": 0.0,
        "inlier_upper_bound": 0.0,
        "paediatric_multiplier": 1.0,
        "same_day_list_flag": False,
        "bundled_icu_flag": False,
        "same_day_base_weight": 0.0,
        "same_day_per_diem": 0.0,
        "inlier_weight": 0.0,
        "long_stay_per_diem": 0.0,
        "private_service_adjustment": 0.0,
    }


def test_acute_input_validation_reports_missing_required_columns():
    frame = pd.DataFrame(
        {
            "DRG": ["801A"],
            "LOS": [1],
            "ICU_HOURS": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
        }
    )

    with pytest.raises(acute.AcuteContractError, match="ICU_OTHER"):
        acute.validate_acute_input_frame(frame)


def test_validate_acute_input_frame_accepts_a_complete_frame():
    frame = pd.DataFrame(
        {
            "DRG": ["801A"],
            "LOS": [1],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
        }
    )

    assert acute.validate_acute_input_frame(frame) is None


def test_acute_input_contract_exposes_expected_schema_defaults():
    contract = acute.AcuteInputContract()

    assert contract.required_columns == (
        "DRG",
        "LOS",
        "ICU_HOURS",
        "ICU_OTHER",
        "PAT_SAMEDAY_FLAG",
        "PAT_PRIVATE_FLAG",
    )
    assert contract.allow_extra_columns is True
    assert "PAT_COVID_FLAG" in contract.optional_columns
    assert "STATE" in contract.optional_columns


def test_load_price_weights_decodes_ascii_drg_values(monkeypatch):
    weights = pd.DataFrame({"DRG": [b"801A", b"801B"]})

    monkeypatch.setattr(
        acute,
        "load_sas_table",
        lambda path, cache=True: weights.copy(),
    )
    monkeypatch.setattr(
        acute,
        "sas_table",
        lambda *args, **kwargs: Path("tests/data/nep25_aa_price_weights.sas7bdat"),
    )

    result = acute._load_price_weights(Path("tests/data/2025"), "2025")

    assert result["DRG"].tolist() == ["801A", "801B"]


def test_build_acute_contract_uses_explicit_reference_bundle():
    bundle = acute.AcuteReferenceBundle(
        year="2025",
        ref_dir=Path("tests/data/2025"),
        weights=pd.DataFrame({"DRG": ["801A"]}),
    )
    contract = acute.build_acute_contract(
        params=acute.AcuteParams(debug_mode=True),
        year="2024",
        ref_dir=Path("tests/data/2024"),
        reference_bundle=bundle,
    )

    assert contract.year == "2025"
    assert contract.reference_bundle is bundle
    assert contract.params.debug_mode is True


def test_build_acute_contract_derives_reference_bundle_from_ref_dir():
    contract = acute.build_acute_contract(ref_dir=Path("tests/data/2025"))

    assert contract.year == "2025"
    assert contract.reference_bundle is not None
    assert contract.reference_bundle.ref_dir == Path("tests/data/2025")


def test_build_acute_contract_defaults_to_acut_params_and_input_contract():
    contract = acute.build_acute_contract()

    assert contract.year == "2025"
    assert isinstance(contract.params, acute.AcuteParams)
    assert isinstance(contract.input_contract, acute.AcuteInputContract)
    assert contract.reference_bundle is not None


def test_resolve_acute_reference_bundle_prefers_explicit_bundle():
    bundle = acute.AcuteReferenceBundle(
        year="2025",
        ref_dir=Path("tests/data/2025"),
        weights=pd.DataFrame({"DRG": ["801A"]}),
    )

    resolved = acute._resolve_acute_reference_bundle(
        year="2024",
        ref_dir=Path("tests/data/2024"),
        reference_bundle=bundle,
    )

    assert resolved is bundle


def test_resolve_acute_reference_bundle_builds_from_year_and_ref_dir():
    resolved = acute._resolve_acute_reference_bundle(
        year="2025",
        ref_dir=Path("tests/data/2025"),
        reference_bundle=None,
    )

    assert resolved.year == "2025"
    assert resolved.ref_dir == Path("tests/data/2025")
    assert resolved.weights is None


def test_resolve_acute_reference_bundle_uses_default_sas_directory(monkeypatch):
    monkeypatch.setattr(acute, "sas_ref_dir", lambda year: Path(f"/tmp/{year}"))

    resolved = acute._resolve_acute_reference_bundle(
        year="2025",
        ref_dir=None,
        reference_bundle=None,
    )

    assert resolved.year == "2025"
    assert resolved.ref_dir == Path("/tmp/2025")


def test_acute_rust_adjustments_return_the_expected_zeroed_contract():
    adjustments = acute._acute_rust_adjustments(acute.AcuteParams())

    assert adjustments == {
        "icu_rate": 0.0,
        "covid_adjustment": 0.0,
        "indigenous_adjustment": 0.0,
        "remoteness_adjustment": 0.0,
        "treatment_remoteness_adjustment": 0.0,
        "radiotherapy_adjustment": 0.0,
        "dialysis_adjustment": 0.0,
        "private_accommodation_same_day": 0.0,
        "private_accommodation_overnight": 0.0,
    }


def test_acute_rust_adjustments_ignore_parameter_values():
    params = acute.AcuteParams(
        icu_paed_option=99,
        covid_option=99,
        covid_adj_option=99,
        radiotherapy_option=99,
        dialysis_option=99,
        ppservadj=99,
        est_remoteness_option=99,
    )

    assert acute._acute_rust_adjustments(params) == acute._acute_rust_adjustments(
        acute.AcuteParams()
    )


def test_rust_bridge_row_loader_rejects_kwargs_and_wrong_arity():
    with pytest.raises(TypeError, match="accepts positional arguments only"):
        rust_bridge.calculate_acute_2025_row(row={}, reference={}, adjustments={})

    with pytest.raises(TypeError, match="expects row, reference, and adjustments"):
        rust_bridge.calculate_acute_2025_row({"DRG": "801A"}, {"drg": "801A"})


def test_calculate_acute_rust_2025_uses_bridge_and_preserves_columns(monkeypatch):
    frame = pd.DataFrame(
        {
            "DRG": ["801A"],
            "LOS": [1],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PAT_COVID_FLAG": [0],
        }
    )

    weights = pd.DataFrame(
        {
            "DRG": ["801A"],
            "drg_inlier_lb": [1.0],
            "drg_inlier_ub": [2.0],
            "drg_adj_paed": [1.0],
            "drg_samedaylist_flag": [0],
            "drg_bundled_icu_flag": [0],
            "drg_pw_sso_base": [0.0],
            "drg_pw_sso_perdiem": [0.0],
            "drg_pw_inlier": [0.0],
            "drg_pw_lso_perdiem": [0.0],
            "drg_adj_privpat_serv": [0.0],
        }
    )

    calls: list[tuple[dict, dict, dict]] = []

    def fake_row(row, reference, adjustments):
        calls.append((row, reference, adjustments))
        return {"NWAU25": 3.5}

    monkeypatch.setattr(
        acute, "_load_price_weights", lambda ref_dir, year="2025": weights
    )
    monkeypatch.setattr(acute, "_rust_calculate_acute_2025_row", fake_row)

    result = acute.calculate_acute_rust_2025(
        frame,
        acute.AcuteParams(debug_mode=True),
        year="2025",
        ref_dir=BASE / "2025",
    )

    assert list(result.columns) == [*list(frame.columns), "NWAU25"]
    assert result["NWAU25"].tolist() == [3.5]
    assert calls and calls[0][0]["DRG"] == "801A"
    assert calls[0][1]["drg"] == "801A"
    assert calls[0][2]["icu_rate"] == 0.0


def test_calculate_acute_rust_2025_drops_internal_columns_when_not_debug(monkeypatch):
    frame = pd.DataFrame(
        {
            "DRG": ["801A"],
            "LOS": [1],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PAT_COVID_FLAG": [0],
        }
    )
    weights = pd.DataFrame(
        {
            "DRG": ["801A"],
            "drg_inlier_lb": [1.0],
            "drg_inlier_ub": [2.0],
            "drg_adj_paed": [1.0],
            "drg_samedaylist_flag": [0],
            "drg_bundled_icu_flag": [0],
            "drg_pw_sso_base": [0.0],
            "drg_pw_sso_perdiem": [0.0],
            "drg_pw_inlier": [0.0],
            "drg_pw_lso_perdiem": [0.0],
            "drg_adj_privpat_serv": [0.0],
        }
    )

    monkeypatch.setattr(
        acute, "_load_price_weights", lambda ref_dir, year="2025": weights
    )
    monkeypatch.setattr(
        acute, "_rust_calculate_acute_2025_row", lambda *args, **kwargs: {"NWAU25": 1}
    )

    result = acute.calculate_acute_rust_2025(
        frame,
        acute.AcuteParams(debug_mode=False),
        year="2025",
        ref_dir=BASE / "2025",
    )

    assert "_drg_inscope_flag" not in result.columns
    assert "_pat_covid_flag" not in result.columns
    assert list(result.columns) == [*list(frame.columns), "NWAU25"]
