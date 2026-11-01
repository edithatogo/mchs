"""Unit tests verifying the vectorized Polars expression plugins and PyO3 bindings."""

from __future__ import annotations

from nwau_py import _rust


def test_rust_exports_all_stream_row_calculators():
    """Verify that _rust exports all 5 funding stream row calculators."""
    assert hasattr(_rust, "calculate_acute_2025_row")
    assert hasattr(_rust, "calculate_acute_2026_row")
    assert hasattr(_rust, "calculate_ed_row")
    assert hasattr(_rust, "calculate_mh_admitted_row")
    assert hasattr(_rust, "calculate_mh_community_row")
    assert hasattr(_rust, "calculate_outpatients_row")
    assert hasattr(_rust, "calculate_subacute_row")


def test_ed_row_calculation():
    """Verify ED row calculation through PyO3."""
    res = _rust.calculate_ed_row(
        price_weight=0.1542,
        classification_option=3,
        eligibility_option=1,
        compensable_status=2,
        dva_status=2,
        funding_source=None,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
    )
    assert res["Error_Code"] == 0
    assert abs(res["NWAU"] - 0.1542) < 1e-6


def test_mh_admitted_row_calculation():
    """Verify Admitted Mental Health row calculation through PyO3."""
    res = _rust.calculate_mh_admitted_row(
        amhcc="101A",
        los=5.0,
        price_cat=1,
        inlier_lower_bound=2.0,
        inlier_upper_bound=10.0,
        sso_base_weight=0.5,
        sso_per_diem=0.1,
        inlier_weight=1.2345,
        lso_per_diem=0.08,
        pat_sameday_flag=False,
        pat_private_flag=False,
        state=1,
        specialist_paediatric_multiplier=1.0,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
        private_serv_rate_national=0.0,
        private_accomm_sameday=0.0,
        private_accomm_overnight=0.0,
    )
    assert res["Error_Code"] == 0
    assert abs(res["NWAU"] - 1.2345) < 1e-6


def test_mh_community_row_calculation():
    """Verify Community Mental Health row calculation through PyO3."""
    res = _rust.calculate_mh_community_row(
        amhcc="201A",
        sc_pat_pub=2.0,
        sc_nopat_pub=1.0,
        sc_pat_price_weight=0.12,
        sc_nopat_price_weight=0.08,
        treatment_remoteness_adjustment=0.0,
    )
    assert res["Error_Code"] == 0
    # 2.0 * 0.12 + 1.0 * 0.08 = 0.24 + 0.08 = 0.32
    assert abs(res["NWAU"] - 0.32) < 1e-6


def test_outpatients_row_calculation():
    """Verify Outpatients row calculation through PyO3."""
    res = _rust.calculate_outpatients_row(
        clinic_code="10.01",
        price_weight=0.0825,
        data_type=1,
        multiprovider_flag=False,
        eligible_paediatric_flag=False,
        inscope_flag=True,
        group_event_count=0.0,
        indiv_event_count=1.0,
        multidisciplinary_event_count=0.0,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
        multiprovider_adjustment=0.0,
        paediatric_adjustment=1.0,
    )
    assert res["Error_Code"] == 0
    assert abs(res["NWAU"] - 0.0825) < 1e-6


def test_subacute_row_calculation():
    """Verify Subacute row calculation through PyO3."""
    res = _rust.calculate_subacute_row(
        ansnap="5AA1",
        los=10.0,
        age=65.0,
        pat_sameday_flag=False,
        pat_private_flag=False,
        pat_public_flag=True,
        state=1,
        sameday_list_flag=False,
        inlier_lower_bound=3.0,
        inlier_upper_bound=20.0,
        pw_sameday=0.2,
        pw_sso_perdiem=0.05,
        pw_inlier=1.854,
        pw_lso_perdiem=0.09,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
        radiotherapy_adjustment=0.0,
        dialysis_adjustment=0.0,
        private_serv_rate_national=0.0,
        private_accomm_sameday=0.0,
        private_accomm_overnight=0.0,
    )
    assert res["Error_Code"] == 0
    assert abs(res["NWAU"] - 1.854) < 1e-6


def test_polars_plugin_symbols_registered():
    """Verify that all polars plugin symbols are exported by the dynamic library."""
    from ctypes import CDLL

    library = CDLL(_rust.__file__)
    for expression in (
        "nwau_acute_expr",
        "nwau_ed_expr",
        "nwau_mh_admitted_expr",
        "nwau_mh_community_expr",
        "nwau_outpatients_expr",
        "nwau_subacute_expr",
    ):
        for prefix in ("_polars_plugin_", "_polars_plugin_field_"):
            assert getattr(library, prefix + expression)


def test_ed_missing_price_weight_sets_error_3():
    import polars as pl

    from nwau_py.calculators.ed import EDParams, calculate_ed

    df = pl.DataFrame(
        {
            "AECC": ["UNKNOWN_CODE"],
            "Error_Code": [0],
            "COMPENSABLE_STATUS": [2],
            "DVA_STATUS": [2],
            "adj_indigenous": [0.0],
            "adj_remoteness": [0.0],
            "adj_treat_remoteness": [0.0],
            "FUNDSC": [1],
        }
    )
    res = calculate_ed(df, params=EDParams(classification_option=3))
    assert res["Error_Code"][0] == 3
    assert res["NWAU25"][0] == 0.0
