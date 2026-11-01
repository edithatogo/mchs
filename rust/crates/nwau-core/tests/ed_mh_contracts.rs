use nwau_core::ed::{
    calculate_ed, calculate_ed_decimal, EdAdjustmentFactors, EdAdjustmentFactorsDecimal,
    EdClassificationOption, EdEligibilityOption, EdEpisodeInput, EdEpisodeInputDecimal,
    EdReferenceRow, EdReferenceRowDecimal,
};
use nwau_core::mental_health::{
    calculate_mh, calculate_mh_decimal, MhAdjustmentFactors, MhAdjustmentFactorsDecimal,
    MhAdmittedReferenceRow, MhAdmittedReferenceRowDecimal, MhCommunityReferenceRow, MhEpisodeInput,
    MhEpisodeInputDecimal, MhPpsaOption, MhSeparationCategory, MhSubstream,
};
use rust_decimal::Decimal;
use std::str::FromStr;

#[test]
fn test_ed_metamorphic_monotonicity_of_weights() {
    let adj = EdAdjustmentFactors {
        indigenous_adjustment: 0.05,
        remoteness_adjustment: 0.10,
        treatment_remoteness_adjustment: 0.08,
    };
    let inscope = [1, 2, 8];

    let input_high = EdEpisodeInput {
        code: "E0110A",
        classification_option: EdClassificationOption::AeccDirect,
        eligibility_option: EdEligibilityOption::FundingSource,
        compensable_status: None,
        dva_status: None,
        funding_source: Some(1),
    };
    let ref_high = EdReferenceRow {
        code: "E0110A",
        price_weight: 0.8500,
    };

    let input_low = EdEpisodeInput {
        code: "E0110B",
        classification_option: EdClassificationOption::AeccDirect,
        eligibility_option: EdEligibilityOption::FundingSource,
        compensable_status: None,
        dva_status: None,
        funding_source: Some(1),
    };
    let ref_low = EdReferenceRow {
        code: "E0110B",
        price_weight: 0.4200,
    };

    let out_high = calculate_ed(input_high, Some(ref_high), adj, &inscope);
    let out_low = calculate_ed(input_low, Some(ref_low), adj, &inscope);

    assert_eq!(out_high.error_code, 0);
    assert_eq!(out_low.error_code, 0);
    assert!(
        out_high.nwau > out_low.nwau,
        "Higher weight must produce higher NWAU"
    );
}

#[test]
fn test_ed_metamorphic_eligibility_zeroing() {
    let adj = EdAdjustmentFactors::default();
    let inscope = [1, 2, 8];

    let ref_row = EdReferenceRow {
        code: "E0110A",
        price_weight: 0.2837,
    };

    let input_inscope = EdEpisodeInput {
        code: "E0110A",
        classification_option: EdClassificationOption::AeccDirect,
        eligibility_option: EdEligibilityOption::FundingSource,
        compensable_status: None,
        dva_status: None,
        funding_source: Some(2),
    };

    let input_outscope = EdEpisodeInput {
        code: "E0110A",
        classification_option: EdClassificationOption::AeccDirect,
        eligibility_option: EdEligibilityOption::FundingSource,
        compensable_status: None,
        dva_status: None,
        funding_source: Some(99),
    };

    let out_in = calculate_ed(input_inscope, Some(ref_row), adj, &inscope);
    let out_out = calculate_ed(input_outscope, Some(ref_row), adj, &inscope);

    assert_eq!(out_in.error_code, 0);
    assert!(out_in.nwau > 0.0);
    assert_eq!(out_out.error_code, 2);
    assert_eq!(out_out.nwau, 0.0);
}

#[test]
fn test_mh_metamorphic_los_monotonicity_in_lso() {
    let ref_row = MhAdmittedReferenceRow {
        amhcc: "1001",
        price_cat: 1,
        inlier_lower_bound: 3.0,
        inlier_upper_bound: 5.0,
        sso_base_weight: 1.0,
        sso_per_diem: 0.2,
        inlier_weight: 1.5,
        lso_per_diem: 0.35,
    };
    let adj = MhAdjustmentFactors::default();

    let input_los6 = MhEpisodeInput {
        amhcc: "1001",
        los: 6.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub: 0.0,
        sc_nopat_pub: 0.0,
    };

    let input_los10 = MhEpisodeInput {
        amhcc: "1001",
        los: 10.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub: 0.0,
        sc_nopat_pub: 0.0,
    };

    let out6 = calculate_mh(input_los6, Some(ref_row), None, adj, MhPpsaOption::National);
    let out10 = calculate_mh(
        input_los10,
        Some(ref_row),
        None,
        adj,
        MhPpsaOption::National,
    );

    assert_eq!(
        out6.separation_category,
        Some(MhSeparationCategory::LongStayOutlier)
    );
    assert_eq!(
        out10.separation_category,
        Some(MhSeparationCategory::LongStayOutlier)
    );
    assert!(
        out10.nwau > out6.nwau,
        "NWAU must increase monotonically with LOS in LSO category"
    );
}

#[test]
fn test_mh_metamorphic_private_deduction_bounded() {
    let ref_row = MhAdmittedReferenceRow {
        amhcc: "1001",
        price_cat: 1,
        inlier_lower_bound: 2.0,
        inlier_upper_bound: 8.0,
        sso_base_weight: 0.8,
        sso_per_diem: 0.2,
        inlier_weight: 2.0,
        lso_per_diem: 0.3,
    };
    let adj = MhAdjustmentFactors {
        specialist_paediatric_multiplier: 1.0,
        indigenous_adjustment: 0.0,
        remoteness_adjustment: 0.0,
        treatment_remoteness_adjustment: 0.0,
        private_serv_rate_national: 0.15,
        private_serv_rate_state: 0.15,
        private_accomm_sameday: 0.02,
        private_accomm_overnight: 0.03,
    };

    let input_pub = MhEpisodeInput {
        amhcc: "1001",
        los: 4.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub: 0.0,
        sc_nopat_pub: 0.0,
    };

    let input_priv = MhEpisodeInput {
        amhcc: "1001",
        los: 4.0,
        pat_sameday_flag: false,
        pat_private_flag: true,
        state: 1,
        sc_pat_pub: 0.0,
        sc_nopat_pub: 0.0,
    };

    let out_pub = calculate_mh(input_pub, Some(ref_row), None, adj, MhPpsaOption::National);
    let out_priv = calculate_mh(input_priv, Some(ref_row), None, adj, MhPpsaOption::National);

    assert!(
        out_priv.nwau < out_pub.nwau,
        "Private patient NWAU must be less than public"
    );
    assert!(
        out_priv.nwau >= 0.0,
        "Private patient NWAU must remain non-negative"
    );
    assert!(out_priv.private_service_deduction > 0.0);
    assert!(out_priv.private_accommodation_deduction > 0.0);
}

#[test]
fn test_mh_community_contact_linearity() {
    let ref_row = MhCommunityReferenceRow {
        amhcc: "2001",
        sc_pat_price_weight: 0.1250,
        sc_nopat_price_weight: 0.0750,
    };
    let adj = MhAdjustmentFactors::default();

    let input1 = MhEpisodeInput {
        amhcc: "2001",
        los: 0.0,
        pat_sameday_flag: true,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub: 2.0,
        sc_nopat_pub: 0.0,
    };

    let input2 = MhEpisodeInput {
        amhcc: "2001",
        los: 0.0,
        pat_sameday_flag: true,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub: 4.0,
        sc_nopat_pub: 0.0,
    };

    let out1 = calculate_mh(input1, None, Some(ref_row), adj, MhPpsaOption::National);
    let out2 = calculate_mh(input2, None, Some(ref_row), adj, MhPpsaOption::National);

    assert_eq!(out1.substream, MhSubstream::Community);
    assert_eq!(out2.substream, MhSubstream::Community);
    assert!(
        (out2.nwau - 2.0 * out1.nwau).abs() < 1e-6,
        "Community funding scales linearly with contacts"
    );
}

#[test]
fn test_ed_and_mh_decimal_exact_fixed_point_invariants() {
    let ed_input = EdEpisodeInputDecimal {
        code: "E0110A",
        classification_option: EdClassificationOption::AeccDirect,
        eligibility_option: EdEligibilityOption::FundingSource,
        compensable_status: None,
        dva_status: None,
        funding_source: Some(1),
    };
    let ed_ref = EdReferenceRowDecimal {
        code: "E0110A",
        price_weight: Decimal::from_str("0.2837").unwrap(),
    };
    let ed_adj = EdAdjustmentFactorsDecimal::default();
    let inscope = [1, 2, 8];
    let nep_rate = Some(Decimal::from_str("6500.00").unwrap());

    let ed_out = calculate_ed_decimal(ed_input, Some(ed_ref), ed_adj, &inscope, nep_rate);
    assert_eq!(ed_out.error_code, 0);
    assert_eq!(ed_out.total_funding, Decimal::from_str("1844.05").unwrap());

    // MH Decimal test
    let mh_input = MhEpisodeInputDecimal {
        amhcc: "1001",
        los: Decimal::from(5),
        pat_sameday_flag: false,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub: Decimal::ZERO,
        sc_nopat_pub: Decimal::ZERO,
    };
    let mh_ref = MhAdmittedReferenceRowDecimal {
        amhcc: "1001",
        price_cat: 1,
        inlier_lower_bound: Decimal::from(2),
        inlier_upper_bound: Decimal::from(6),
        sso_base_weight: Decimal::ONE,
        sso_per_diem: Decimal::from_str("0.2").unwrap(),
        inlier_weight: Decimal::from_str("1.8500").unwrap(),
        lso_per_diem: Decimal::from_str("0.3").unwrap(),
    };
    let mh_adj = MhAdjustmentFactorsDecimal::default();
    let mh_out = calculate_mh_decimal(
        mh_input,
        Some(mh_ref),
        None,
        mh_adj,
        MhPpsaOption::National,
        nep_rate,
    );
    assert_eq!(mh_out.error_code, 0);
    assert_eq!(mh_out.w01, Decimal::from_str("1.8500").unwrap());
    assert_eq!(mh_out.total_funding, Decimal::from_str("12025.00").unwrap());
}
