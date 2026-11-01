use nwau_core::acute::{
    calculate_acute_2026, AcuteAdjustmentFactorsDecimal, AcuteEpisodeInputDecimal,
    AcuteReferenceRowDecimal, AcuteValidationState,
};
use nwau_core::ed::{
    calculate_ed_decimal, EdAdjustmentFactorsDecimal, EdClassificationOption, EdEligibilityOption,
    EdEpisodeInputDecimal, EdReferenceRowDecimal,
};
use nwau_core::mental_health::{
    calculate_mh_decimal, MhAdjustmentFactorsDecimal, MhAdmittedReferenceRowDecimal,
    MhEpisodeInputDecimal, MhPpsaOption,
};
use nwau_core::outpatients::{
    calculate_outpatients_decimal, OutpatientAdjustmentFactorsDecimal, OutpatientDataType,
    OutpatientEpisodeInputDecimal, OutpatientReferenceRowDecimal,
};
use nwau_core::subacute::{
    calculate_subacute_decimal, SubacuteAdjustmentFactorsDecimal, SubacuteEpisodeInputDecimal,
    SubacutePpsaOption, SubacuteReferenceRowDecimal,
};
use rust_decimal::Decimal;
use std::str::FromStr;
use std::time::Instant;

#[test]
fn test_100k_multi_stream_drift_and_throughput() {
    let n_episodes = 20_000usize; // 20k per stream x 5 streams = 100,000 episodes
    let nep_rate = Some(Decimal::from(6500));

    // 1. Acute Stream Fixture
    let acute_input = AcuteEpisodeInputDecimal {
        drg: "801A",
        los: Decimal::from(10),
        icu_hours: Decimal::ZERO,
        icu_other: Decimal::ZERO,
        pat_sameday_flag: false,
        pat_private_flag: false,
        pat_covid_flag: false,
        eligible_paed_flag: false,
        validation: AcuteValidationState::valid(),
    };
    let acute_ref = AcuteReferenceRowDecimal {
        drg: "801A",
        inlier_lower_bound: Decimal::from(7),
        inlier_upper_bound: Decimal::from(72),
        paediatric_multiplier: Decimal::from_str("1.35").unwrap(),
        same_day_list_flag: false,
        bundled_icu_flag: false,
        same_day_base_weight: Decimal::from_str("0.9527").unwrap(),
        same_day_per_diem: Decimal::from_str("1.1849").unwrap(),
        inlier_weight: Decimal::from_str("9.2472").unwrap(),
        long_stay_per_diem: Decimal::from_str("0.26").unwrap(),
        private_service_adjustment: Decimal::ZERO,
    };
    let acute_adj = AcuteAdjustmentFactorsDecimal::default();
    let single_acute = calculate_acute_2026(acute_input, acute_ref, acute_adj);

    // 2. ED Stream Fixture
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
    let single_ed = calculate_ed_decimal(ed_input, Some(ed_ref), ed_adj, &inscope, nep_rate);

    // 3. Mental Health Stream Fixture
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
    let single_mh = calculate_mh_decimal(
        mh_input,
        Some(mh_ref),
        None,
        mh_adj,
        MhPpsaOption::National,
        nep_rate,
    );

    // 4. Outpatients Stream Fixture
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
    let single_op = calculate_outpatients_decimal(op_input, Some(op_ref), op_adj, nep_rate);

    // 5. Subacute Stream Fixture
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
    let single_sa = calculate_subacute_decimal(
        sa_input,
        Some(sa_ref),
        sa_adj,
        SubacutePpsaOption::National,
        nep_rate,
    );

    // Run 100k Multi-Stream Execution
    let start = Instant::now();
    let mut total_nwau = Decimal::ZERO;
    let mut total_funding = Decimal::ZERO;

    for _ in 0..n_episodes {
        let out_acute = calculate_acute_2026(acute_input, acute_ref, acute_adj);
        let out_ed = calculate_ed_decimal(ed_input, Some(ed_ref), ed_adj, &inscope, nep_rate);
        let out_mh = calculate_mh_decimal(
            mh_input,
            Some(mh_ref),
            None,
            mh_adj,
            MhPpsaOption::National,
            nep_rate,
        );
        let out_op = calculate_outpatients_decimal(op_input, Some(op_ref), op_adj, nep_rate);
        let out_sa = calculate_subacute_decimal(
            sa_input,
            Some(sa_ref),
            sa_adj,
            SubacutePpsaOption::National,
            nep_rate,
        );

        total_nwau += out_acute.nwau + out_ed.nwau + out_mh.nwau + out_op.nwau + out_sa.nwau;
        total_funding += out_acute.total_funding
            + out_ed.total_funding
            + out_mh.total_funding
            + out_op.total_funding
            + out_sa.total_funding;
    }
    let duration = start.elapsed();
    let total_episodes = n_episodes * 5;
    let eps_per_sec = (total_episodes as f64) / duration.as_secs_f64();

    // Invariant Verification: Exact 128-bit Accumulator PARITY (Zero Drift)
    let expected_single_nwau =
        single_acute.nwau + single_ed.nwau + single_mh.nwau + single_op.nwau + single_sa.nwau;
    let expected_total_nwau = expected_single_nwau * Decimal::from(n_episodes);
    assert_eq!(
        total_nwau, expected_total_nwau,
        "Accumulator drift must be strictly 0.00000000 across 100k episodes"
    );

    let expected_single_funding = single_acute.total_funding
        + single_ed.total_funding
        + single_mh.total_funding
        + single_op.total_funding
        + single_sa.total_funding;
    let expected_total_funding = expected_single_funding * Decimal::from(n_episodes);
    assert_eq!(
        total_funding, expected_total_funding,
        "Total funding drift must be strictly $0.00 across 100k episodes"
    );

    println!(
        "Processed {} multi-stream episodes in {:?} ({:.0} eps/sec)",
        total_episodes, duration, eps_per_sec
    );
    assert!(
        eps_per_sec > 50_000.0,
        "Throughput must exceed 50k episodes/sec, achieved: {:.0}",
        eps_per_sec
    );
}
