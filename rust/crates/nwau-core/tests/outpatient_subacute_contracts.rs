use nwau_core::outpatients::{
    calculate_outpatients, calculate_outpatients_decimal, OutpatientAdjustmentFactors,
    OutpatientAdjustmentFactorsDecimal, OutpatientDataType, OutpatientEpisodeInput,
    OutpatientEpisodeInputDecimal, OutpatientReferenceRow, OutpatientReferenceRowDecimal,
};
use nwau_core::subacute::{
    calculate_subacute, calculate_subacute_decimal, SubacuteAdjustmentFactors,
    SubacuteAdjustmentFactorsDecimal, SubacuteEpisodeInput, SubacuteEpisodeInputDecimal,
    SubacutePpsaOption, SubacuteReferenceRow, SubacuteReferenceRowDecimal,
    SubacuteSeparationCategory,
};
use rust_decimal::Decimal;
use std::str::FromStr;

#[test]
fn test_outpatients_metamorphic_multiprov_exemption() {
    let adj = OutpatientAdjustmentFactors {
        multiprovider_adjustment: 0.35,
        ..Default::default()
    };
    let ref_row = OutpatientReferenceRow {
        clinic_code: "20.48", // Exempt clinic
        price_weight: 0.2500,
        paediatric_adjustment: 1.0,
    };

    let input_no_multi = OutpatientEpisodeInput {
        clinic_code: "20.48",
        data_type: OutpatientDataType::EventLevel,
        multiprovider_flag: false,
        eligible_paediatric_flag: false,
        inscope_flag: true,
        group_event_count: 0.0,
        indiv_event_count: 0.0,
        multidisciplinary_event_count: 0.0,
    };

    let input_multi = OutpatientEpisodeInput {
        clinic_code: "20.48",
        data_type: OutpatientDataType::EventLevel,
        multiprovider_flag: true,
        eligible_paediatric_flag: false,
        inscope_flag: true,
        group_event_count: 0.0,
        indiv_event_count: 0.0,
        multidisciplinary_event_count: 0.0,
    };

    let out_no_multi = calculate_outpatients(input_no_multi, Some(ref_row), adj);
    let out_multi = calculate_outpatients(input_multi, Some(ref_row), adj);

    assert_eq!(
        out_no_multi.nwau, out_multi.nwau,
        "Exempt clinic 20.48 must not receive multiprovider adjustment"
    );
}

#[test]
fn test_outpatients_metamorphic_multiprov_boost() {
    let adj = OutpatientAdjustmentFactors {
        multiprovider_adjustment: 0.35,
        ..Default::default()
    };
    let ref_row = OutpatientReferenceRow {
        clinic_code: "10.01", // Standard clinic
        price_weight: 0.2500,
        paediatric_adjustment: 1.0,
    };

    let input_no_multi = OutpatientEpisodeInput {
        clinic_code: "10.01",
        data_type: OutpatientDataType::EventLevel,
        multiprovider_flag: false,
        eligible_paediatric_flag: false,
        inscope_flag: true,
        group_event_count: 0.0,
        indiv_event_count: 0.0,
        multidisciplinary_event_count: 0.0,
    };

    let input_multi = OutpatientEpisodeInput {
        clinic_code: "10.01",
        data_type: OutpatientDataType::EventLevel,
        multiprovider_flag: true,
        eligible_paediatric_flag: false,
        inscope_flag: true,
        group_event_count: 0.0,
        indiv_event_count: 0.0,
        multidisciplinary_event_count: 0.0,
    };

    let out_no_multi = calculate_outpatients(input_no_multi, Some(ref_row), adj);
    let out_multi = calculate_outpatients(input_multi, Some(ref_row), adj);

    assert!(
        out_multi.nwau > out_no_multi.nwau,
        "Multiprovider flag must boost standard clinic NWAU"
    );
}

#[test]
fn test_subacute_metamorphic_inlier_constancy() {
    let ref_row = SubacuteReferenceRow {
        ansnap: "5A11",
        sameday_list_flag: false,
        inlier_lower_bound: 5.0,
        inlier_upper_bound: 15.0,
        pw_sameday: 0.5,
        pw_sso_perdiem: 0.1,
        pw_inlier: 2.2000,
        pw_lso_perdiem: 0.12,
    };
    let adj = SubacuteAdjustmentFactors::default();

    let input_los6 = SubacuteEpisodeInput {
        ansnap: "5A11",
        los: 6.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        pat_public_flag: true,
        age: 50.0,
        state: 1,
    };

    let input_los14 = SubacuteEpisodeInput {
        ansnap: "5A11",
        los: 14.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        pat_public_flag: true,
        age: 50.0,
        state: 1,
    };

    let out6 = calculate_subacute(input_los6, Some(ref_row), adj, SubacutePpsaOption::National);
    let out14 = calculate_subacute(
        input_los14,
        Some(ref_row),
        adj,
        SubacutePpsaOption::National,
    );

    assert_eq!(
        out6.separation_category,
        Some(SubacuteSeparationCategory::Inlier)
    );
    assert_eq!(
        out14.separation_category,
        Some(SubacuteSeparationCategory::Inlier)
    );
    assert_eq!(
        out6.w01, out14.w01,
        "All inlier LOS values must have the identical base price weight"
    );
    assert_eq!(out6.nwau, out14.nwau);
}

#[test]
fn test_subacute_metamorphic_lso_monotonicity() {
    let ref_row = SubacuteReferenceRow {
        ansnap: "5A11",
        sameday_list_flag: false,
        inlier_lower_bound: 5.0,
        inlier_upper_bound: 15.0,
        pw_sameday: 0.5,
        pw_sso_perdiem: 0.1,
        pw_inlier: 2.2000,
        pw_lso_perdiem: 0.15,
    };
    let adj = SubacuteAdjustmentFactors::default();

    let input_los16 = SubacuteEpisodeInput {
        ansnap: "5A11",
        los: 16.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        pat_public_flag: true,
        age: 50.0,
        state: 1,
    };

    let input_los20 = SubacuteEpisodeInput {
        ansnap: "5A11",
        los: 20.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        pat_public_flag: true,
        age: 50.0,
        state: 1,
    };

    let out16 = calculate_subacute(
        input_los16,
        Some(ref_row),
        adj,
        SubacutePpsaOption::National,
    );
    let out20 = calculate_subacute(
        input_los20,
        Some(ref_row),
        adj,
        SubacutePpsaOption::National,
    );

    assert_eq!(
        out16.separation_category,
        Some(SubacuteSeparationCategory::LongStayOutlier)
    );
    assert_eq!(
        out20.separation_category,
        Some(SubacuteSeparationCategory::LongStayOutlier)
    );
    assert!(
        out20.nwau > out16.nwau,
        "Subacute LSO NWAU must increase monotonically with LOS"
    );
}

#[test]
fn test_subacute_and_outpatient_decimal_exact() {
    let op_input = OutpatientEpisodeInputDecimal {
        clinic_code: "10.01",
        data_type: OutpatientDataType::EventLevel,
        multiprovider_flag: false,
        eligible_paediatric_flag: false,
        inscope_flag: true,
        group_event_count: Decimal::ZERO,
        indiv_event_count: Decimal::ZERO,
        multidisciplinary_event_count: Decimal::ZERO,
    };
    let op_ref = OutpatientReferenceRowDecimal {
        clinic_code: "10.01",
        price_weight: Decimal::from_str("0.1742").unwrap(),
        paediatric_adjustment: Decimal::ONE,
    };
    let op_adj = OutpatientAdjustmentFactorsDecimal::default();
    let nep_rate = Some(Decimal::from(6500));

    let op_out = calculate_outpatients_decimal(op_input, Some(op_ref), op_adj, nep_rate);
    assert_eq!(op_out.error_code, 0);
    assert_eq!(op_out.total_funding, Decimal::from_str("1132.30").unwrap());

    let sa_input = SubacuteEpisodeInputDecimal {
        ansnap: "5A11",
        los: Decimal::from(8),
        pat_sameday_flag: false,
        pat_private_flag: false,
        pat_public_flag: true,
        age: Decimal::from(62),
        state: 1,
    };
    let sa_ref = SubacuteReferenceRowDecimal {
        ansnap: "5A11",
        sameday_list_flag: false,
        inlier_lower_bound: Decimal::from(4),
        inlier_upper_bound: Decimal::from(16),
        pw_sameday: Decimal::from_str("0.4").unwrap(),
        pw_sso_perdiem: Decimal::from_str("0.1").unwrap(),
        pw_inlier: Decimal::from_str("2.1000").unwrap(),
        pw_lso_perdiem: Decimal::from_str("0.12").unwrap(),
    };
    let sa_adj = SubacuteAdjustmentFactorsDecimal::default();
    let sa_out = calculate_subacute_decimal(
        sa_input,
        Some(sa_ref),
        sa_adj,
        SubacutePpsaOption::National,
        nep_rate,
    );
    assert_eq!(sa_out.error_code, 0);
    assert_eq!(sa_out.w01, Decimal::from_str("2.1000").unwrap());
    assert_eq!(sa_out.total_funding, Decimal::from_str("13650.00").unwrap());
}
