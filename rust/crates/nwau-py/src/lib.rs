//! PyO3 bindings and vectorized Polars expression plugins for the NWAU Rust core.
//!
//! Exposes both PyO3 functions and `#[polars_expr]` zero-copy execution plugins
//! across all 5 funding streams: Acute, ED, Mental Health, Outpatients, and Subacute.

#![allow(clippy::useless_conversion)]
#![allow(clippy::too_many_arguments)]

use nwau_core::Kernel;
use polars::prelude::*;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
use pyo3_polars::derive::polars_expr;

#[inline]
fn get_f64(ca: &Float64Chunked, idx: usize, default: f64) -> f64 {
    ca.get(idx).unwrap_or(default)
}

#[inline]
fn get_bool(ca: &BooleanChunked, idx: usize, default: bool) -> bool {
    ca.get(idx).unwrap_or(default)
}

#[inline]
fn get_i64(ca: &Int64Chunked, idx: usize, default: i64) -> i64 {
    ca.get(idx).unwrap_or(default)
}

#[inline]
fn get_str<'a>(ca: &'a StringChunked, idx: usize, default: &'a str) -> &'a str {
    ca.get(idx).unwrap_or(default)
}

// ============================================================================
// POLARS EXPRESSION PLUGINS (Zero-copy parallel execution inside Polars engine)
// ============================================================================

/// Vectorized Acute NWAU expression plugin.
#[polars_expr(output_type=Float64)]
fn nwau_acute_expr(inputs: &[Series]) -> PolarsResult<Series> {
    let drg_s = inputs[0].str()?;
    let los_s = inputs[1].f64()?;
    let inlier_lb_s = inputs[2].f64()?;
    let inlier_ub_s = inputs[3].f64()?;
    let sameday_base_s = inputs[4].f64()?;
    let sameday_per_diem_s = inputs[5].f64()?;
    let inlier_weight_s = inputs[6].f64()?;
    let long_stay_per_diem_s = inputs[7].f64()?;
    let private_service_adj_s = inputs[8].f64()?;
    let same_day_list_s = inputs[9].bool()?;
    let bundled_icu_s = inputs[10].bool()?;
    let pat_sameday_s = inputs[11].bool()?;
    let pat_private_s = inputs[12].bool()?;
    let pat_covid_s = inputs[13].bool()?;
    let eligible_paed_s = inputs[14].bool()?;
    let paed_multiplier_s = inputs[15].f64()?;
    let icu_hours_s = inputs[16].f64()?;
    let icu_rate_s = inputs[17].f64()?;
    let covid_adj_s = inputs[18].f64()?;
    let indigenous_adj_s = inputs[19].f64()?;
    let remoteness_adj_s = inputs[20].f64()?;
    let treat_remoteness_adj_s = inputs[21].f64()?;
    let radiotherapy_adj_s = inputs[22].f64()?;
    let dialysis_adj_s = inputs[23].f64()?;
    let priv_accomm_sd_s = inputs[24].f64()?;
    let priv_accomm_on_s = inputs[25].f64()?;

    let len = inputs[0].len();
    let mut vals = Vec::with_capacity(len);

    for i in 0..len {
        let drg = get_str(drg_s, i, "");
        let los = get_f64(los_s, i, 0.0);
        let inlier_lower_bound = get_f64(inlier_lb_s, i, 0.0);
        let inlier_upper_bound = get_f64(inlier_ub_s, i, 0.0);
        let same_day_base_weight = get_f64(sameday_base_s, i, 0.0);
        let same_day_per_diem = get_f64(sameday_per_diem_s, i, 0.0);
        let inlier_weight = get_f64(inlier_weight_s, i, 0.0);
        let long_stay_per_diem = get_f64(long_stay_per_diem_s, i, 0.0);
        let private_service_adjustment = get_f64(private_service_adj_s, i, 0.0);
        let same_day_list_flag = get_bool(same_day_list_s, i, false);
        let bundled_icu_flag = get_bool(bundled_icu_s, i, false);
        let pat_sameday_flag = get_bool(pat_sameday_s, i, false);
        let pat_private_flag = get_bool(pat_private_s, i, false);
        let pat_covid_flag = get_bool(pat_covid_s, i, false);
        let eligible_paed_flag = get_bool(eligible_paed_s, i, false);
        let paediatric_multiplier = get_f64(paed_multiplier_s, i, 1.0);
        let icu_hours = get_f64(icu_hours_s, i, 0.0);
        let icu_rate = get_f64(icu_rate_s, i, 0.0);
        let covid_adjustment = get_f64(covid_adj_s, i, 0.0);
        let indigenous_adjustment = get_f64(indigenous_adj_s, i, 0.0);
        let remoteness_adjustment = get_f64(remoteness_adj_s, i, 0.0);
        let treatment_remoteness_adjustment = get_f64(treat_remoteness_adj_s, i, 0.0);
        let radiotherapy_adjustment = get_f64(radiotherapy_adj_s, i, 0.0);
        let dialysis_adjustment = get_f64(dialysis_adj_s, i, 0.0);
        let private_accommodation_same_day = get_f64(priv_accomm_sd_s, i, 0.0);
        let private_accommodation_overnight = get_f64(priv_accomm_on_s, i, 0.0);

        let output = nwau_core::calculate_acute_2025(
            nwau_core::AcuteEpisodeInput {
                drg,
                los,
                icu_hours,
                icu_other: 0.0,
                pat_sameday_flag,
                pat_private_flag,
                pat_covid_flag,
                eligible_paed_flag,
                validation: nwau_core::AcuteValidationState::valid(),
            },
            nwau_core::AcuteReferenceRow {
                drg,
                inlier_lower_bound,
                inlier_upper_bound,
                paediatric_multiplier,
                same_day_list_flag,
                bundled_icu_flag,
                same_day_base_weight,
                same_day_per_diem,
                inlier_weight,
                long_stay_per_diem,
                private_service_adjustment,
            },
            nwau_core::AcuteAdjustmentFactors {
                icu_rate,
                covid_adjustment,
                indigenous_adjustment,
                remoteness_adjustment,
                treatment_remoteness_adjustment,
                radiotherapy_adjustment,
                dialysis_adjustment,
                private_accommodation_same_day,
                private_accommodation_overnight,
            },
        );

        if output.error_code == 0 {
            vals.push(output.nwau25);
        } else {
            vals.push(0.0);
        }
    }

    Ok(Float64Chunked::from_vec("nwau_acute".into(), vals).into_series())
}

/// Vectorized ED NWAU expression plugin.
#[polars_expr(output_type=Float64)]
fn nwau_ed_expr(inputs: &[Series]) -> PolarsResult<Series> {
    let pw_s = inputs[0].f64()?;
    let class_opt_s = inputs[1].i64()?;
    let elig_opt_s = inputs[2].i64()?;
    let comp_status_s = inputs[3].i64()?;
    let dva_status_s = inputs[4].i64()?;
    let fund_src_s = inputs[5].i64()?;
    let ind_adj_s = inputs[6].f64()?;
    let rem_adj_s = inputs[7].f64()?;
    let treat_rem_adj_s = inputs[8].f64()?;

    let len = inputs[0].len();
    let mut vals = Vec::with_capacity(len);

    for i in 0..len {
        let price_weight = get_f64(pw_s, i, 0.0);
        let class_opt = match get_i64(class_opt_s, i, 3) {
            1 => nwau_core::ed::EdClassificationOption::UdgMapped,
            2 => nwau_core::ed::EdClassificationOption::UdgDirect,
            _ => nwau_core::ed::EdClassificationOption::AeccDirect,
        };
        let elig_opt = match get_i64(elig_opt_s, i, 1) {
            2 => nwau_core::ed::EdEligibilityOption::FundingSource,
            _ => nwau_core::ed::EdEligibilityOption::CompensableDva,
        };
        let compensable_status = comp_status_s.get(i).map(|v| v as u8);
        let dva_status = dva_status_s.get(i).map(|v| v as u8);
        let funding_source = fund_src_s.get(i).map(|v| v as u8);
        let indigenous_adjustment = get_f64(ind_adj_s, i, 0.0);
        let remoteness_adjustment = get_f64(rem_adj_s, i, 0.0);
        let treatment_remoteness_adjustment = get_f64(treat_rem_adj_s, i, 0.0);

        let input = nwau_core::ed::EdEpisodeInput {
            code: "",
            classification_option: class_opt,
            eligibility_option: elig_opt,
            compensable_status,
            dva_status,
            funding_source,
        };
        let reference = Some(nwau_core::ed::EdReferenceRow {
            code: "",
            price_weight,
        });
        let adjustments = nwau_core::ed::EdAdjustmentFactors {
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
        };

        let result = nwau_core::ed::calculate_ed(input, reference, adjustments, &[1, 2, 8]);
        if result.error_code == 0 {
            vals.push(result.nwau);
        } else {
            vals.push(0.0);
        }
    }

    Ok(Float64Chunked::from_vec("nwau_ed".into(), vals).into_series())
}

/// Vectorized Admitted Mental Health NWAU expression plugin.
#[polars_expr(output_type=Float64)]
fn nwau_mh_admitted_expr(inputs: &[Series]) -> PolarsResult<Series> {
    let amhcc_s = inputs[0].str()?;
    let los_s = inputs[1].f64()?;
    let price_cat_s = inputs[2].i64()?;
    let inlier_lb_s = inputs[3].f64()?;
    let inlier_ub_s = inputs[4].f64()?;
    let sso_base_s = inputs[5].f64()?;
    let sso_per_diem_s = inputs[6].f64()?;
    let inlier_weight_s = inputs[7].f64()?;
    let lso_per_diem_s = inputs[8].f64()?;
    let pat_sameday_s = inputs[9].bool()?;
    let pat_private_s = inputs[10].bool()?;
    let state_s = inputs[11].i64()?;
    let paed_mult_s = inputs[12].f64()?;
    let ind_adj_s = inputs[13].f64()?;
    let rem_adj_s = inputs[14].f64()?;
    let treat_rem_adj_s = inputs[15].f64()?;
    let priv_serv_s = inputs[16].f64()?;
    let priv_accomm_sd_s = inputs[17].f64()?;
    let priv_accomm_on_s = inputs[18].f64()?;

    let len = inputs[0].len();
    let mut vals = Vec::with_capacity(len);

    for i in 0..len {
        let amhcc = get_str(amhcc_s, i, "");
        let los = get_f64(los_s, i, 0.0);
        let price_cat = get_i64(price_cat_s, i, 1) as u8;
        let inlier_lower_bound = get_f64(inlier_lb_s, i, 0.0);
        let inlier_upper_bound = get_f64(inlier_ub_s, i, 0.0);
        let sso_base_weight = get_f64(sso_base_s, i, 0.0);
        let sso_per_diem = get_f64(sso_per_diem_s, i, 0.0);
        let inlier_weight = get_f64(inlier_weight_s, i, 0.0);
        let lso_per_diem = get_f64(lso_per_diem_s, i, 0.0);
        let pat_sameday_flag = get_bool(pat_sameday_s, i, false);
        let pat_private_flag = get_bool(pat_private_s, i, false);
        let state = get_i64(state_s, i, 1) as u8;
        let specialist_paediatric_multiplier = get_f64(paed_mult_s, i, 1.0);
        let indigenous_adjustment = get_f64(ind_adj_s, i, 0.0);
        let remoteness_adjustment = get_f64(rem_adj_s, i, 0.0);
        let treatment_remoteness_adjustment = get_f64(treat_rem_adj_s, i, 0.0);
        let private_serv_rate_national = get_f64(priv_serv_s, i, 0.0);
        let private_accomm_sameday = get_f64(priv_accomm_sd_s, i, 0.0);
        let private_accomm_overnight = get_f64(priv_accomm_on_s, i, 0.0);

        let input = nwau_core::mental_health::MhEpisodeInput {
            amhcc,
            los,
            pat_sameday_flag,
            pat_private_flag,
            state,
            sc_pat_pub: 0.0,
            sc_nopat_pub: 0.0,
        };
        let reference = Some(nwau_core::mental_health::MhAdmittedReferenceRow {
            amhcc,
            price_cat,
            inlier_lower_bound,
            inlier_upper_bound,
            sso_base_weight,
            sso_per_diem,
            inlier_weight,
            lso_per_diem,
        });
        let adjustments = nwau_core::mental_health::MhAdjustmentFactors {
            specialist_paediatric_multiplier,
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
            private_serv_rate_national,
            private_serv_rate_state: 0.0,
            private_accomm_sameday,
            private_accomm_overnight,
        };

        let result = nwau_core::mental_health::calculate_mh(
            input,
            reference,
            None,
            adjustments,
            nwau_core::mental_health::MhPpsaOption::National,
        );
        if result.error_code == 0 {
            vals.push(result.nwau);
        } else {
            vals.push(0.0);
        }
    }

    Ok(Float64Chunked::from_vec("nwau_mh_admitted".into(), vals).into_series())
}

/// Vectorized Community Mental Health NWAU expression plugin.
#[polars_expr(output_type=Float64)]
fn nwau_mh_community_expr(inputs: &[Series]) -> PolarsResult<Series> {
    let amhcc_s = inputs[0].str()?;
    let sc_pat_pub_s = inputs[1].f64()?;
    let sc_nopat_pub_s = inputs[2].f64()?;
    let sc_pat_pw_s = inputs[3].f64()?;
    let sc_nopat_pw_s = inputs[4].f64()?;
    let treat_rem_adj_s = inputs[5].f64()?;

    let len = inputs[0].len();
    let mut vals = Vec::with_capacity(len);

    for i in 0..len {
        let amhcc = get_str(amhcc_s, i, "");
        let sc_pat_pub = get_f64(sc_pat_pub_s, i, 0.0);
        let sc_nopat_pub = get_f64(sc_nopat_pub_s, i, 0.0);
        let sc_pat_price_weight = get_f64(sc_pat_pw_s, i, 0.0);
        let sc_nopat_price_weight = get_f64(sc_nopat_pw_s, i, 0.0);
        let treatment_remoteness_adjustment = get_f64(treat_rem_adj_s, i, 0.0);

        let input = nwau_core::mental_health::MhEpisodeInput {
            amhcc,
            los: 0.0,
            pat_sameday_flag: false,
            pat_private_flag: false,
            state: 1,
            sc_pat_pub,
            sc_nopat_pub,
        };
        let reference = Some(nwau_core::mental_health::MhCommunityReferenceRow {
            amhcc,
            sc_pat_price_weight,
            sc_nopat_price_weight,
        });
        let adjustments = nwau_core::mental_health::MhAdjustmentFactors {
            specialist_paediatric_multiplier: 1.0,
            indigenous_adjustment: 0.0,
            remoteness_adjustment: 0.0,
            treatment_remoteness_adjustment,
            private_serv_rate_national: 0.0,
            private_serv_rate_state: 0.0,
            private_accomm_sameday: 0.0,
            private_accomm_overnight: 0.0,
        };

        let result = nwau_core::mental_health::calculate_mh(
            input,
            None,
            reference,
            adjustments,
            nwau_core::mental_health::MhPpsaOption::National,
        );
        if result.error_code == 0 {
            vals.push(result.nwau);
        } else {
            vals.push(0.0);
        }
    }

    Ok(Float64Chunked::from_vec("nwau_mh_community".into(), vals).into_series())
}

/// Vectorized Outpatients (Tier 2) NWAU expression plugin.
#[polars_expr(output_type=Float64)]
fn nwau_outpatients_expr(inputs: &[Series]) -> PolarsResult<Series> {
    let clinic_code_s = inputs[0].str()?;
    let price_weight_s = inputs[1].f64()?;
    let data_type_s = inputs[2].i64()?;
    let multiprovider_s = inputs[3].bool()?;
    let eligible_paed_s = inputs[4].bool()?;
    let inscope_s = inputs[5].bool()?;
    let group_cnt_s = inputs[6].f64()?;
    let indiv_cnt_s = inputs[7].f64()?;
    let multidisciplinary_cnt_s = inputs[8].f64()?;
    let ind_adj_s = inputs[9].f64()?;
    let rem_adj_s = inputs[10].f64()?;
    let treat_rem_adj_s = inputs[11].f64()?;
    let multiprovider_adj_s = inputs[12].f64()?;
    let paed_adj_s = inputs[13].f64()?;

    let len = inputs[0].len();
    let mut vals = Vec::with_capacity(len);

    for i in 0..len {
        let clinic_code = get_str(clinic_code_s, i, "");
        let price_weight = get_f64(price_weight_s, i, 0.0);
        let data_type = match get_i64(data_type_s, i, 1) {
            2 => nwau_core::outpatients::OutpatientDataType::AggregateCount,
            _ => nwau_core::outpatients::OutpatientDataType::EventLevel,
        };
        let multiprovider_flag = get_bool(multiprovider_s, i, false);
        let eligible_paediatric_flag = get_bool(eligible_paed_s, i, false);
        let inscope_flag = get_bool(inscope_s, i, true);
        let group_event_count = get_f64(group_cnt_s, i, 0.0);
        let indiv_event_count = get_f64(indiv_cnt_s, i, 0.0);
        let multidisciplinary_event_count = get_f64(multidisciplinary_cnt_s, i, 0.0);
        let indigenous_adjustment = get_f64(ind_adj_s, i, 0.0);
        let remoteness_adjustment = get_f64(rem_adj_s, i, 0.0);
        let treatment_remoteness_adjustment = get_f64(treat_rem_adj_s, i, 0.0);
        let multiprovider_adjustment = get_f64(multiprovider_adj_s, i, 0.0);
        let paediatric_adjustment = get_f64(paed_adj_s, i, 1.0);

        let input = nwau_core::outpatients::OutpatientEpisodeInput {
            clinic_code,
            data_type,
            multiprovider_flag,
            eligible_paediatric_flag,
            inscope_flag,
            group_event_count,
            indiv_event_count,
            multidisciplinary_event_count,
        };
        let reference = Some(nwau_core::outpatients::OutpatientReferenceRow {
            clinic_code,
            price_weight,
            paediatric_adjustment,
        });
        let adjustments = nwau_core::outpatients::OutpatientAdjustmentFactors {
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
            multiprovider_adjustment,
            paediatric_adjustment,
        };

        let result = nwau_core::outpatients::calculate_outpatients(input, reference, adjustments);
        if result.error_code == 0 {
            vals.push(result.nwau);
        } else {
            vals.push(0.0);
        }
    }

    Ok(Float64Chunked::from_vec("nwau_outpatients".into(), vals).into_series())
}

/// Vectorized Subacute NWAU expression plugin.
#[polars_expr(output_type=Float64)]
fn nwau_subacute_expr(inputs: &[Series]) -> PolarsResult<Series> {
    let ansnap_s = inputs[0].str()?;
    let los_s = inputs[1].f64()?;
    let age_s = inputs[2].f64()?;
    let pat_sameday_s = inputs[3].bool()?;
    let pat_private_s = inputs[4].bool()?;
    let pat_public_s = inputs[5].bool()?;
    let state_s = inputs[6].i64()?;
    let sameday_list_s = inputs[7].bool()?;
    let inlier_lb_s = inputs[8].f64()?;
    let inlier_ub_s = inputs[9].f64()?;
    let pw_sameday_s = inputs[10].f64()?;
    let pw_sso_s = inputs[11].f64()?;
    let pw_inlier_s = inputs[12].f64()?;
    let pw_lso_s = inputs[13].f64()?;
    let ind_adj_s = inputs[14].f64()?;
    let rem_adj_s = inputs[15].f64()?;
    let treat_rem_adj_s = inputs[16].f64()?;
    let radio_adj_s = inputs[17].f64()?;
    let dial_adj_s = inputs[18].f64()?;
    let priv_serv_s = inputs[19].f64()?;
    let priv_accomm_sd_s = inputs[20].f64()?;
    let priv_accomm_on_s = inputs[21].f64()?;

    let len = inputs[0].len();
    let mut vals = Vec::with_capacity(len);

    for i in 0..len {
        let ansnap = get_str(ansnap_s, i, "");
        let los = get_f64(los_s, i, 0.0);
        let age = get_f64(age_s, i, 0.0);
        let pat_sameday_flag = get_bool(pat_sameday_s, i, false);
        let pat_private_flag = get_bool(pat_private_s, i, false);
        let pat_public_flag = get_bool(pat_public_s, i, true);
        let state = get_i64(state_s, i, 1) as u8;
        let sameday_list_flag = get_bool(sameday_list_s, i, false);
        let inlier_lower_bound = get_f64(inlier_lb_s, i, 0.0);
        let inlier_upper_bound = get_f64(inlier_ub_s, i, 0.0);
        let pw_sameday = get_f64(pw_sameday_s, i, 0.0);
        let pw_sso_perdiem = get_f64(pw_sso_s, i, 0.0);
        let pw_inlier = get_f64(pw_inlier_s, i, 0.0);
        let pw_lso_perdiem = get_f64(pw_lso_s, i, 0.0);
        let indigenous_adjustment = get_f64(ind_adj_s, i, 0.0);
        let remoteness_adjustment = get_f64(rem_adj_s, i, 0.0);
        let treatment_remoteness_adjustment = get_f64(treat_rem_adj_s, i, 0.0);
        let radiotherapy_adjustment = get_f64(radio_adj_s, i, 0.0);
        let dialysis_adjustment = get_f64(dial_adj_s, i, 0.0);
        let private_serv_rate_national = get_f64(priv_serv_s, i, 0.0);
        let private_accomm_sameday = get_f64(priv_accomm_sd_s, i, 0.0);
        let private_accomm_overnight = get_f64(priv_accomm_on_s, i, 0.0);

        let input = nwau_core::subacute::SubacuteEpisodeInput {
            ansnap,
            los,
            pat_sameday_flag,
            pat_private_flag,
            pat_public_flag,
            age,
            state,
        };
        let reference = Some(nwau_core::subacute::SubacuteReferenceRow {
            ansnap,
            sameday_list_flag,
            inlier_lower_bound,
            inlier_upper_bound,
            pw_sameday,
            pw_sso_perdiem,
            pw_inlier,
            pw_lso_perdiem,
        });
        let adjustments = nwau_core::subacute::SubacuteAdjustmentFactors {
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
            radiotherapy_adjustment,
            dialysis_adjustment,
            private_serv_rate_national,
            private_serv_rate_state: 0.0,
            private_accomm_sameday,
            private_accomm_overnight,
        };

        let result = nwau_core::subacute::calculate_subacute(
            input,
            reference,
            adjustments,
            nwau_core::subacute::SubacutePpsaOption::National,
        );
        if result.error_code == 0 {
            vals.push(result.nwau);
        } else {
            vals.push(0.0);
        }
    }

    Ok(Float64Chunked::from_vec("nwau_subacute".into(), vals).into_series())
}

// ============================================================================
// PYO3 FUNCTIONS (In-process scalar and row dispatcher)
// ============================================================================

#[pyfunction(name = "kernel_label")]
fn kernel_label() -> &'static str {
    nwau_core::kernel_label()
}

#[pyfunction(name = "core_version")]
fn core_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pyfunction(name = "list_calculators")]
fn list_calculators() -> Vec<&'static str> {
    vec!["acute-2025", "acute-2026", "ed", "mental-health", "outpatients", "sub-acute"]
}

#[pyfunction(name = "is_drg_in_scope")]
fn is_drg_in_scope(drg: &str) -> bool {
    let registry = nwau_core::DrgRegistry::new().with_acute_2025_fixtures();
    registry.is_acute_in_scope(drg)
}

#[pyfunction(name = "calculate_acute_2025_row")]
fn calculate_acute_2025_row<'py>(
    py: Python<'py>,
    drg: &'py str,
    los: f64,
    icu_hours: f64,
    icu_other: f64,
    pat_sameday_flag: bool,
    pat_private_flag: bool,
    pat_covid_flag: bool,
    eligible_paed_flag: bool,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
    paediatric_multiplier: f64,
    same_day_list_flag: bool,
    bundled_icu_flag: bool,
    same_day_base_weight: f64,
    same_day_per_diem: f64,
    inlier_weight: f64,
    long_stay_per_diem: f64,
    private_service_adjustment: f64,
    icu_rate: f64,
    covid_adjustment: f64,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
    radiotherapy_adjustment: f64,
    dialysis_adjustment: f64,
    private_accommodation_same_day: f64,
    private_accommodation_overnight: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let validation = nwau_core::AcuteValidationState::valid();
    let output = nwau_core::calculate_acute_2025(
        nwau_core::AcuteEpisodeInput {
            drg,
            los,
            icu_hours,
            icu_other,
            pat_sameday_flag,
            pat_private_flag,
            pat_covid_flag,
            eligible_paed_flag,
            validation,
        },
        nwau_core::AcuteReferenceRow {
            drg,
            inlier_lower_bound,
            inlier_upper_bound,
            paediatric_multiplier,
            same_day_list_flag,
            bundled_icu_flag,
            same_day_base_weight,
            same_day_per_diem,
            inlier_weight,
            long_stay_per_diem,
            private_service_adjustment,
        },
        nwau_core::AcuteAdjustmentFactors {
            icu_rate,
            covid_adjustment,
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
            radiotherapy_adjustment,
            dialysis_adjustment,
            private_accommodation_same_day,
            private_accommodation_overnight,
        },
    );
    let dict = PyDict::new(py);
    dict.set_item("NWAU25", output.nwau25)?;
    dict.set_item("Error_Code", output.error_code)?;
    dict.set_item(
        "Separation_Category",
        output
            .separation_category
            .map(|cat| cat as i32)
            .unwrap_or(0),
    )?;
    dict.set_item("kernel_label", nwau_core::kernel_label())?;
    Ok(dict)
}

#[pyfunction(name = "calculate_acute_2026_row")]
fn calculate_acute_2026_row<'py>(
    py: Python<'py>,
    drg: &'py str,
    los: f64,
    icu_hours: f64,
    icu_other: f64,
    pat_sameday_flag: bool,
    pat_private_flag: bool,
    pat_covid_flag: bool,
    eligible_paed_flag: bool,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
    paediatric_multiplier: f64,
    same_day_list_flag: bool,
    bundled_icu_flag: bool,
    same_day_base_weight: f64,
    same_day_per_diem: f64,
    inlier_weight: f64,
    long_stay_per_diem: f64,
    private_service_adjustment: f64,
    icu_rate: f64,
    covid_adjustment: f64,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
    radiotherapy_adjustment: f64,
    dialysis_adjustment: f64,
    private_accommodation_same_day: f64,
    private_accommodation_overnight: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let validation = nwau_core::AcuteValidationState::valid();
    let output = nwau_core::calculate_acute_2025(
        nwau_core::AcuteEpisodeInput {
            drg,
            los,
            icu_hours,
            icu_other,
            pat_sameday_flag,
            pat_private_flag,
            pat_covid_flag,
            eligible_paed_flag,
            validation,
        },
        nwau_core::AcuteReferenceRow {
            drg,
            inlier_lower_bound,
            inlier_upper_bound,
            paediatric_multiplier,
            same_day_list_flag,
            bundled_icu_flag,
            same_day_base_weight,
            same_day_per_diem,
            inlier_weight,
            long_stay_per_diem,
            private_service_adjustment,
        },
        nwau_core::AcuteAdjustmentFactors {
            icu_rate,
            covid_adjustment,
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
            radiotherapy_adjustment,
            dialysis_adjustment,
            private_accommodation_same_day,
            private_accommodation_overnight,
        },
    );
    let dict = PyDict::new(py);
    dict.set_item("NWAU26", output.nwau25)?;
    dict.set_item("NWAU", output.nwau25)?;
    let total_funding = (output.nwau25 * 7418.0 * 100.0).round() / 100.0;
    dict.set_item("Total_Funding", total_funding)?;
    dict.set_item("Error_Code", output.error_code)?;
    dict.set_item(
        "Separation_Category",
        output
            .separation_category
            .map(|cat| cat as i32)
            .unwrap_or(0),
    )?;
    dict.set_item("W01", output.w01)?;
    dict.set_item("W02", output.w02)?;
    dict.set_item("W03", output.w03)?;
    dict.set_item("W04", output.w04)?;
    dict.set_item("GWAU", output.gwau)?;
    dict.set_item("kernel_label", nwau_core::kernel_label_2026())?;
    Ok(dict)
}

#[pyfunction(name = "calculate_ed_row")]
fn calculate_ed_row<'py>(
    py: Python<'py>,
    price_weight: f64,
    classification_option: i64,
    eligibility_option: i64,
    compensable_status: Option<u8>,
    dva_status: Option<u8>,
    funding_source: Option<u8>,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let class_opt = match classification_option {
        1 => nwau_core::ed::EdClassificationOption::UdgMapped,
        2 => nwau_core::ed::EdClassificationOption::UdgDirect,
        _ => nwau_core::ed::EdClassificationOption::AeccDirect,
    };
    let elig_opt = match eligibility_option {
        2 => nwau_core::ed::EdEligibilityOption::FundingSource,
        _ => nwau_core::ed::EdEligibilityOption::CompensableDva,
    };
    let input = nwau_core::ed::EdEpisodeInput {
        code: "",
        classification_option: class_opt,
        eligibility_option: elig_opt,
        compensable_status,
        dva_status,
        funding_source,
    };
    let reference = Some(nwau_core::ed::EdReferenceRow {
        code: "",
        price_weight,
    });
    let adjustments = nwau_core::ed::EdAdjustmentFactors {
        indigenous_adjustment,
        remoteness_adjustment,
        treatment_remoteness_adjustment,
    };
    let result = nwau_core::ed::calculate_ed(input, reference, adjustments, &[1, 2, 8]);
    let dict = PyDict::new(py);
    dict.set_item("NWAU", result.nwau)?;
    dict.set_item("GWAU", result.gwau)?;
    dict.set_item("W01", result.w01)?;
    dict.set_item("Error_Code", result.error_code)?;
    Ok(dict)
}

#[pyfunction(name = "calculate_mh_admitted_row")]
fn calculate_mh_admitted_row<'py>(
    py: Python<'py>,
    amhcc: &'py str,
    los: f64,
    price_cat: u8,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
    sso_base_weight: f64,
    sso_per_diem: f64,
    inlier_weight: f64,
    lso_per_diem: f64,
    pat_sameday_flag: bool,
    pat_private_flag: bool,
    state: u8,
    specialist_paediatric_multiplier: f64,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
    private_serv_rate_national: f64,
    private_accomm_sameday: f64,
    private_accomm_overnight: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let input = nwau_core::mental_health::MhEpisodeInput {
        amhcc,
        los,
        pat_sameday_flag,
        pat_private_flag,
        state,
        sc_pat_pub: 0.0,
        sc_nopat_pub: 0.0,
    };
    let reference = Some(nwau_core::mental_health::MhAdmittedReferenceRow {
        amhcc,
        price_cat,
        inlier_lower_bound,
        inlier_upper_bound,
        sso_base_weight,
        sso_per_diem,
        inlier_weight,
        lso_per_diem,
    });
    let adjustments = nwau_core::mental_health::MhAdjustmentFactors {
        specialist_paediatric_multiplier,
        indigenous_adjustment,
        remoteness_adjustment,
        treatment_remoteness_adjustment,
        private_serv_rate_national,
        private_serv_rate_state: 0.0,
        private_accomm_sameday,
        private_accomm_overnight,
    };
    let result = nwau_core::mental_health::calculate_mh(
        input,
        reference,
        None,
        adjustments,
        nwau_core::mental_health::MhPpsaOption::National,
    );
    let dict = PyDict::new(py);
    dict.set_item("NWAU", result.nwau)?;
    dict.set_item("GWAU", result.gwau)?;
    dict.set_item("W01", result.w01)?;
    dict.set_item("Error_Code", result.error_code)?;
    Ok(dict)
}

#[pyfunction(name = "calculate_mh_community_row")]
fn calculate_mh_community_row<'py>(
    py: Python<'py>,
    amhcc: &'py str,
    sc_pat_pub: f64,
    sc_nopat_pub: f64,
    sc_pat_price_weight: f64,
    sc_nopat_price_weight: f64,
    treatment_remoteness_adjustment: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let input = nwau_core::mental_health::MhEpisodeInput {
        amhcc,
        los: 0.0,
        pat_sameday_flag: false,
        pat_private_flag: false,
        state: 1,
        sc_pat_pub,
        sc_nopat_pub,
    };
    let reference = Some(nwau_core::mental_health::MhCommunityReferenceRow {
        amhcc,
        sc_pat_price_weight,
        sc_nopat_price_weight,
    });
    let adjustments = nwau_core::mental_health::MhAdjustmentFactors {
        specialist_paediatric_multiplier: 1.0,
        indigenous_adjustment: 0.0,
        remoteness_adjustment: 0.0,
        treatment_remoteness_adjustment,
        private_serv_rate_national: 0.0,
        private_serv_rate_state: 0.0,
        private_accomm_sameday: 0.0,
        private_accomm_overnight: 0.0,
    };
    let result = nwau_core::mental_health::calculate_mh(
        input,
        None,
        reference,
        adjustments,
        nwau_core::mental_health::MhPpsaOption::National,
    );
    let dict = PyDict::new(py);
    dict.set_item("NWAU", result.nwau)?;
    dict.set_item("GWAU", result.gwau)?;
    dict.set_item("W01", result.w01)?;
    dict.set_item("Error_Code", result.error_code)?;
    Ok(dict)
}

#[pyfunction(name = "calculate_outpatients_row")]
fn calculate_outpatients_row<'py>(
    py: Python<'py>,
    clinic_code: &'py str,
    price_weight: f64,
    data_type: i64,
    multiprovider_flag: bool,
    eligible_paediatric_flag: bool,
    inscope_flag: bool,
    group_event_count: f64,
    indiv_event_count: f64,
    multidisciplinary_event_count: f64,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
    multiprovider_adjustment: f64,
    paediatric_adjustment: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let dt = match data_type {
        2 => nwau_core::outpatients::OutpatientDataType::AggregateCount,
        _ => nwau_core::outpatients::OutpatientDataType::EventLevel,
    };
    let input = nwau_core::outpatients::OutpatientEpisodeInput {
        clinic_code,
        data_type: dt,
        multiprovider_flag,
        eligible_paediatric_flag,
        inscope_flag,
        group_event_count,
        indiv_event_count,
        multidisciplinary_event_count,
    };
    let reference = Some(nwau_core::outpatients::OutpatientReferenceRow {
        clinic_code,
        price_weight,
        paediatric_adjustment,
    });
    let adjustments = nwau_core::outpatients::OutpatientAdjustmentFactors {
        indigenous_adjustment,
        remoteness_adjustment,
        treatment_remoteness_adjustment,
        multiprovider_adjustment,
        paediatric_adjustment,
    };
    let result = nwau_core::outpatients::calculate_outpatients(input, reference, adjustments);
    let dict = PyDict::new(py);
    dict.set_item("NWAU", result.nwau)?;
    dict.set_item("GWAU", result.gwau)?;
    dict.set_item("W01", result.w01)?;
    dict.set_item("Error_Code", result.error_code)?;
    Ok(dict)
}

#[pyfunction(name = "calculate_subacute_row")]
fn calculate_subacute_row<'py>(
    py: Python<'py>,
    ansnap: &'py str,
    los: f64,
    age: f64,
    pat_sameday_flag: bool,
    pat_private_flag: bool,
    pat_public_flag: bool,
    state: u8,
    sameday_list_flag: bool,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
    pw_sameday: f64,
    pw_sso_perdiem: f64,
    pw_inlier: f64,
    pw_lso_perdiem: f64,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
    radiotherapy_adjustment: f64,
    dialysis_adjustment: f64,
    private_serv_rate_national: f64,
    private_accomm_sameday: f64,
    private_accomm_overnight: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let input = nwau_core::subacute::SubacuteEpisodeInput {
        ansnap,
        los,
        pat_sameday_flag,
        pat_private_flag,
        pat_public_flag,
        age,
        state,
    };
    let reference = Some(nwau_core::subacute::SubacuteReferenceRow {
        ansnap,
        sameday_list_flag,
        inlier_lower_bound,
        inlier_upper_bound,
        pw_sameday,
        pw_sso_perdiem,
        pw_inlier,
        pw_lso_perdiem,
    });
    let adjustments = nwau_core::subacute::SubacuteAdjustmentFactors {
        indigenous_adjustment,
        remoteness_adjustment,
        treatment_remoteness_adjustment,
        radiotherapy_adjustment,
        dialysis_adjustment,
        private_serv_rate_national,
        private_serv_rate_state: 0.0,
        private_accomm_sameday,
        private_accomm_overnight,
    };
    let result = nwau_core::subacute::calculate_subacute(
        input,
        reference,
        adjustments,
        nwau_core::subacute::SubacutePpsaOption::National,
    );
    let dict = PyDict::new(py);
    dict.set_item("NWAU", result.nwau)?;
    dict.set_item("GWAU", result.gwau)?;
    dict.set_item("W01", result.w01)?;
    dict.set_item("Error_Code", result.error_code)?;
    Ok(dict)
}

#[pyfunction(name = "calculate_batch")]
fn calculate_batch<'py>(
    py: Python<'py>,
    episodes_json: &str,
    reference_json: &str,
) -> Result<Bound<'py, PyList>, PyErr> {
    let episodes: Vec<nwau_core::EpisodeRow> =
        serde_json::from_str(episodes_json).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("invalid episodes JSON: {e}"))
        })?;
    let references: Vec<nwau_core::ReferenceRow> =
        serde_json::from_str(reference_json).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("invalid reference JSON: {e}"))
        })?;
    let kernel = nwau_core::Acute2025Kernel::new();
    let adjustments = nwau_core::AdjustmentFactors::default();
    let results = PyList::new(py, Vec::<Bound<'py, PyDict>>::new())?;
    for ep in &episodes {
        let ref_row = references.iter().find(|r| r.drg == ep.drg).ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(format!("no reference row for DRG: {}", ep.drg))
        })?;
        let output = kernel.calculate(ep, ref_row, &adjustments);
        let d = PyDict::new(py);
        d.set_item("DRG", &ep.drg)?;
        d.set_item("NWAU", output.nwau)?;
        d.set_item("Error_Code", output.error_code)?;
        results.append(d)?;
    }
    Ok(results)
}

#[pymodule]
fn _rust(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add(
        "__doc__",
        "Rust-backed Python bindings and Polars expression plugins for NWAU calculation.",
    )?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add(
        "__all__",
        PyList::new(
            _py,
            [
                "kernel_label",
                "core_version",
                "list_calculators",
                "is_drg_in_scope",
                "calculate_acute_2025_row",
                "calculate_acute_2026_row",
                "calculate_ed_row",
                "calculate_mh_admitted_row",
                "calculate_mh_community_row",
                "calculate_outpatients_row",
                "calculate_subacute_row",
                "calculate_batch",
                "__version__",
            ],
        )?,
    )?;
    m.add_function(wrap_pyfunction!(kernel_label, m)?)?;
    m.add_function(wrap_pyfunction!(core_version, m)?)?;
    m.add_function(wrap_pyfunction!(list_calculators, m)?)?;
    m.add_function(wrap_pyfunction!(is_drg_in_scope, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_acute_2025_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_acute_2026_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_ed_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_mh_admitted_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_mh_community_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_outpatients_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_subacute_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_batch, m)?)?;
    Ok(())
}
