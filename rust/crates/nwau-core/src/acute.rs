#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AcuteValidationState {
    pub has_required_fields: bool,
    pub has_public_or_private_flag: bool,
    pub is_acute: bool,
    pub drg_in_scope: bool,
}

impl AcuteValidationState {
    pub const fn valid() -> Self {
        Self {
            has_required_fields: true,
            has_public_or_private_flag: true,
            is_acute: true,
            drg_in_scope: true,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct AcuteEpisodeInput<'a> {
    pub drg: &'a str,
    pub los: f64,
    pub icu_hours: f64,
    pub icu_other: f64,
    pub pat_sameday_flag: bool,
    pub pat_private_flag: bool,
    pub pat_covid_flag: bool,
    pub eligible_paed_flag: bool,
    pub validation: AcuteValidationState,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct AcuteReferenceRow<'a> {
    pub drg: &'a str,
    pub inlier_lower_bound: f64,
    pub inlier_upper_bound: f64,
    pub paediatric_multiplier: f64,
    pub same_day_list_flag: bool,
    pub bundled_icu_flag: bool,
    pub same_day_base_weight: f64,
    pub same_day_per_diem: f64,
    pub inlier_weight: f64,
    pub long_stay_per_diem: f64,
    pub private_service_adjustment: f64,
}

#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub struct AcuteAdjustmentFactors {
    pub icu_rate: f64,
    pub covid_adjustment: f64,
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub radiotherapy_adjustment: f64,
    pub dialysis_adjustment: f64,
    pub private_accommodation_same_day: f64,
    pub private_accommodation_overnight: f64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SeparationCategory {
    SameDay = 1,
    BelowInlierLowerBound = 2,
    Inlier = 3,
    AboveInlierUpperBound = 4,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct AcuteEpisodeOutput {
    pub error_code: u8,
    pub separation_category: Option<SeparationCategory>,
    pub eligible_icu_hours: f64,
    pub los_icu_removed: f64,
    pub w01: f64,
    pub w02: f64,
    pub w03: f64,
    pub w04: f64,
    pub gwau: f64,
    pub private_service_deduction: f64,
    pub private_accommodation_deduction: f64,
    pub nwau25: f64,
}

pub fn acute_error_code(validation: AcuteValidationState) -> u8 {
    if !validation.has_required_fields {
        3
    } else if !validation.has_public_or_private_flag {
        2
    } else if !validation.is_acute || !validation.drg_in_scope {
        1
    } else {
        0
    }
}

fn round_to(value: f64, decimals: i32) -> f64 {
    let factor = 10f64.powi(decimals);
    (value * factor).round() / factor
}

fn separation_category(
    pat_sameday_flag: bool,
    same_day_list_flag: bool,
    los_icu_removed: f64,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
) -> Option<SeparationCategory> {
    if pat_sameday_flag && same_day_list_flag {
        return Some(SeparationCategory::SameDay);
    }

    if los_icu_removed < inlier_lower_bound {
        Some(SeparationCategory::BelowInlierLowerBound)
    } else if los_icu_removed <= inlier_upper_bound {
        Some(SeparationCategory::Inlier)
    } else {
        Some(SeparationCategory::AboveInlierUpperBound)
    }
}

pub fn calculate_acute_2025(
    input: AcuteEpisodeInput<'_>,
    reference: AcuteReferenceRow<'_>,
    adjustments: AcuteAdjustmentFactors,
) -> AcuteEpisodeOutput {
    debug_assert_eq!(
        input.drg, reference.drg,
        "acute kernel input and reference row must share the same DRG"
    );
    let error_code = acute_error_code(input.validation);
    if error_code > 0 {
        return AcuteEpisodeOutput {
            error_code,
            separation_category: None,
            eligible_icu_hours: 0.0,
            los_icu_removed: 0.0,
            w01: 0.0,
            w02: 0.0,
            w03: 0.0,
            w04: 0.0,
            gwau: 0.0,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau25: 0.0,
        };
    }

    let eligible_icu_hours = if reference.bundled_icu_flag {
        0.0
    } else if input.pat_covid_flag {
        input.icu_hours + input.icu_other
    } else {
        input.icu_hours
    };

    let los_icu_removed = (input.los - (eligible_icu_hours / 24.0).floor()).max(1.0);
    let separation_category = separation_category(
        input.pat_sameday_flag,
        reference.same_day_list_flag,
        los_icu_removed,
        reference.inlier_lower_bound,
        reference.inlier_upper_bound,
    );

    let w01 = match separation_category {
        Some(SeparationCategory::SameDay) => reference.same_day_base_weight,
        Some(SeparationCategory::BelowInlierLowerBound) => {
            reference.same_day_base_weight + los_icu_removed * reference.same_day_per_diem
        }
        Some(SeparationCategory::Inlier) => reference.inlier_weight,
        Some(SeparationCategory::AboveInlierUpperBound) => {
            reference.inlier_weight
                + (los_icu_removed - reference.inlier_upper_bound) * reference.long_stay_per_diem
        }
        None => 0.0,
    };
    let w01 = round_to(w01, 4);

    let w02 = if input.eligible_paed_flag {
        reference.paediatric_multiplier * w01
    } else {
        w01
    };

    let w03 = w02
        * (1.0
            + adjustments.indigenous_adjustment
            + adjustments.remoteness_adjustment
            + adjustments.radiotherapy_adjustment
            + adjustments.dialysis_adjustment)
        * (1.0 + adjustments.treatment_remoteness_adjustment);

    let w04 = w03 * (1.0 + adjustments.covid_adjustment);
    let gwau = (w04 + eligible_icu_hours * adjustments.icu_rate).max(0.0);

    let private_service_deduction = if input.pat_private_flag {
        reference.private_service_adjustment * (w01 + eligible_icu_hours * adjustments.icu_rate)
    } else {
        0.0
    };
    let private_accommodation_deduction = if input.pat_private_flag {
        if input.pat_sameday_flag {
            adjustments.private_accommodation_same_day
        } else {
            input.los * adjustments.private_accommodation_overnight
        }
    } else {
        0.0
    };

    let nwau25 = (gwau - private_service_deduction - private_accommodation_deduction).max(0.0);

    AcuteEpisodeOutput {
        error_code,
        separation_category,
        eligible_icu_hours,
        los_icu_removed,
        w01,
        w02,
        w03,
        w04,
        gwau,
        private_service_deduction,
        private_accommodation_deduction,
        nwau25,
    }
}

// ---------------------------------------------------------------------------
// 128-bit Exact Fixed-Point Decimal Arithmetic Engine (rust_decimal)
// ---------------------------------------------------------------------------

use rust_decimal::Decimal;
use rust_decimal_macros::dec;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AcuteEpisodeInputDecimal<'a> {
    pub drg: &'a str,
    pub los: Decimal,
    pub icu_hours: Decimal,
    pub icu_other: Decimal,
    pub pat_sameday_flag: bool,
    pub pat_private_flag: bool,
    pub pat_covid_flag: bool,
    pub eligible_paed_flag: bool,
    pub validation: AcuteValidationState,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AcuteReferenceRowDecimal<'a> {
    pub drg: &'a str,
    pub inlier_lower_bound: Decimal,
    pub inlier_upper_bound: Decimal,
    pub paediatric_multiplier: Decimal,
    pub same_day_list_flag: bool,
    pub bundled_icu_flag: bool,
    pub same_day_base_weight: Decimal,
    pub same_day_per_diem: Decimal,
    pub inlier_weight: Decimal,
    pub long_stay_per_diem: Decimal,
    pub private_service_adjustment: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct AcuteAdjustmentFactorsDecimal {
    pub icu_rate: Decimal,
    pub covid_adjustment: Decimal,
    pub indigenous_adjustment: Decimal,
    pub remoteness_adjustment: Decimal,
    pub treatment_remoteness_adjustment: Decimal,
    pub radiotherapy_adjustment: Decimal,
    pub dialysis_adjustment: Decimal,
    pub private_accommodation_same_day: Decimal,
    pub private_accommodation_overnight: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AcuteEpisodeOutputDecimal {
    pub error_code: u8,
    pub separation_category: Option<SeparationCategory>,
    pub eligible_icu_hours: Decimal,
    pub los_icu_removed: Decimal,
    pub w01: Decimal,
    pub w02: Decimal,
    pub w03: Decimal,
    pub w04: Decimal,
    pub gwau: Decimal,
    pub private_service_deduction: Decimal,
    pub private_accommodation_deduction: Decimal,
    pub nwau: Decimal,
    pub total_funding: Decimal,
}

fn separation_category_decimal(
    pat_sameday_flag: bool,
    same_day_list_flag: bool,
    los_icu_removed: Decimal,
    inlier_lower_bound: Decimal,
    inlier_upper_bound: Decimal,
) -> Option<SeparationCategory> {
    if pat_sameday_flag && same_day_list_flag {
        return Some(SeparationCategory::SameDay);
    }

    if los_icu_removed < inlier_lower_bound {
        Some(SeparationCategory::BelowInlierLowerBound)
    } else if los_icu_removed <= inlier_upper_bound {
        Some(SeparationCategory::Inlier)
    } else {
        Some(SeparationCategory::AboveInlierUpperBound)
    }
}

/// Calculate acute NWAU and total funding using exact 128-bit decimal arithmetic.
pub fn calculate_acute_decimal(
    input: AcuteEpisodeInputDecimal<'_>,
    reference: AcuteReferenceRowDecimal<'_>,
    adjustments: AcuteAdjustmentFactorsDecimal,
    nep_rate: Option<Decimal>,
) -> AcuteEpisodeOutputDecimal {
    debug_assert_eq!(
        input.drg, reference.drg,
        "acute kernel input and reference row must share the same DRG"
    );
    let error_code = acute_error_code(input.validation);
    if error_code > 0 {
        return AcuteEpisodeOutputDecimal {
            error_code,
            separation_category: None,
            eligible_icu_hours: Decimal::ZERO,
            los_icu_removed: Decimal::ZERO,
            w01: Decimal::ZERO,
            w02: Decimal::ZERO,
            w03: Decimal::ZERO,
            w04: Decimal::ZERO,
            gwau: Decimal::ZERO,
            private_service_deduction: Decimal::ZERO,
            private_accommodation_deduction: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    }

    let eligible_icu_hours = if reference.bundled_icu_flag {
        Decimal::ZERO
    } else if input.pat_covid_flag {
        input.icu_hours + input.icu_other
    } else {
        input.icu_hours
    };

    let icu_days = (eligible_icu_hours / dec!(24)).floor();
    let los_icu_removed = (input.los - icu_days).max(Decimal::ONE);

    let separation_category = separation_category_decimal(
        input.pat_sameday_flag,
        reference.same_day_list_flag,
        los_icu_removed,
        reference.inlier_lower_bound,
        reference.inlier_upper_bound,
    );

    let w01 = match separation_category {
        Some(SeparationCategory::SameDay) => reference.same_day_base_weight,
        Some(SeparationCategory::BelowInlierLowerBound) => {
            reference.same_day_base_weight + los_icu_removed * reference.same_day_per_diem
        }
        Some(SeparationCategory::Inlier) => reference.inlier_weight,
        Some(SeparationCategory::AboveInlierUpperBound) => {
            reference.inlier_weight
                + (los_icu_removed - reference.inlier_upper_bound) * reference.long_stay_per_diem
        }
        None => Decimal::ZERO,
    };
    let w01 = w01.round_dp(4);

    let w02 = if input.eligible_paed_flag {
        (reference.paediatric_multiplier * w01).round_dp(4)
    } else {
        w01
    };

    let patient_adjustment_sum = Decimal::ONE
        + adjustments.indigenous_adjustment
        + adjustments.remoteness_adjustment
        + adjustments.radiotherapy_adjustment
        + adjustments.dialysis_adjustment;

    let w03 = (w02
        * patient_adjustment_sum
        * (Decimal::ONE + adjustments.treatment_remoteness_adjustment))
        .round_dp(4);

    let w04 = (w03 * (Decimal::ONE + adjustments.covid_adjustment)).round_dp(4);
    let gwau = (w04 + eligible_icu_hours * adjustments.icu_rate).max(Decimal::ZERO);

    let private_service_deduction = if input.pat_private_flag {
        reference.private_service_adjustment * (w01 + eligible_icu_hours * adjustments.icu_rate)
    } else {
        Decimal::ZERO
    };

    let private_accommodation_deduction = if input.pat_private_flag {
        if input.pat_sameday_flag {
            adjustments.private_accommodation_same_day
        } else {
            input.los * adjustments.private_accommodation_overnight
        }
    } else {
        Decimal::ZERO
    };

    let nwau =
        (gwau - private_service_deduction - private_accommodation_deduction).max(Decimal::ZERO);
    let nep = nep_rate.unwrap_or(dec!(7418));
    let total_funding = (nwau * nep).round_dp(2);

    AcuteEpisodeOutputDecimal {
        error_code,
        separation_category,
        eligible_icu_hours,
        los_icu_removed,
        w01,
        w02,
        w03,
        w04,
        gwau,
        private_service_deduction,
        private_accommodation_deduction,
        nwau,
        total_funding,
    }
}

/// Official NEP26 Acute Admitted Calculator with standard NEP = $7,418.00.
pub fn calculate_acute_2026(
    input: AcuteEpisodeInputDecimal<'_>,
    reference: AcuteReferenceRowDecimal<'_>,
    adjustments: AcuteAdjustmentFactorsDecimal,
) -> AcuteEpisodeOutputDecimal {
    calculate_acute_decimal(input, reference, adjustments, Some(dec!(7418)))
}

// ---------------------------------------------------------------------------
// Tests: Metamorphic Relations & Numerical Precision Verification
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_nep26_reference() -> AcuteReferenceRowDecimal<'static> {
        AcuteReferenceRowDecimal {
            drg: "801A",
            inlier_lower_bound: dec!(7),
            inlier_upper_bound: dec!(72),
            paediatric_multiplier: dec!(1.35),
            same_day_list_flag: false,
            bundled_icu_flag: false,
            same_day_base_weight: dec!(0.9527),
            same_day_per_diem: dec!(1.1849),
            inlier_weight: dec!(9.2472),
            long_stay_per_diem: dec!(0.2600),
            private_service_adjustment: dec!(0.1500),
        }
    }

    #[test]
    fn test_metamorphic_mr1_los_monotonicity() {
        let reference = sample_nep26_reference();
        let adj = AcuteAdjustmentFactorsDecimal::default();

        let input_a = AcuteEpisodeInputDecimal {
            drg: "801A",
            los: dec!(75),
            icu_hours: Decimal::ZERO,
            icu_other: Decimal::ZERO,
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_covid_flag: false,
            eligible_paed_flag: false,
            validation: AcuteValidationState::valid(),
        };

        let mut input_b = input_a;
        input_b.los = dec!(80);

        let out_a = calculate_acute_2026(input_a, reference, adj);
        let out_b = calculate_acute_2026(input_b, reference, adj);

        assert_eq!(
            out_a.separation_category,
            Some(SeparationCategory::AboveInlierUpperBound)
        );
        assert_eq!(
            out_b.separation_category,
            Some(SeparationCategory::AboveInlierUpperBound)
        );
        assert!(
            out_b.nwau > out_a.nwau,
            "MR1 violation: longer stay must increase NWAU in long stay"
        );
        assert_eq!(out_b.nwau - out_a.nwau, dec!(5) * dec!(0.2600));
    }

    #[test]
    fn test_metamorphic_mr2_icu_additivity() {
        let reference = sample_nep26_reference();
        let adj = AcuteAdjustmentFactorsDecimal {
            icu_rate: dec!(0.05),
            ..Default::default()
        };

        let input_no_icu = AcuteEpisodeInputDecimal {
            drg: "801A",
            los: dec!(10),
            icu_hours: Decimal::ZERO,
            icu_other: Decimal::ZERO,
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_covid_flag: false,
            eligible_paed_flag: false,
            validation: AcuteValidationState::valid(),
        };

        let mut input_with_icu = input_no_icu;
        input_with_icu.icu_hours = dec!(48);

        let out_no = calculate_acute_2026(input_no_icu, reference, adj);
        let out_icu = calculate_acute_2026(input_with_icu, reference, adj);

        // los = 10, icu = 48 hours = 2 days -> los_icu_removed = 8 days (still inlier 7..72)
        assert_eq!(out_icu.los_icu_removed, dec!(8));
        let expected_delta_gwau = dec!(48) * dec!(0.05);
        assert_eq!(
            out_icu.gwau - out_no.gwau,
            expected_delta_gwau,
            "MR2 violation: ICU hours additivity"
        );
    }

    #[test]
    fn test_metamorphic_mr3_private_deduction_bounded() {
        let reference = sample_nep26_reference();
        let adj = AcuteAdjustmentFactorsDecimal {
            private_accommodation_overnight: dec!(0.02),
            ..Default::default()
        };

        let input_public = AcuteEpisodeInputDecimal {
            drg: "801A",
            los: dec!(10),
            icu_hours: Decimal::ZERO,
            icu_other: Decimal::ZERO,
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_covid_flag: false,
            eligible_paed_flag: false,
            validation: AcuteValidationState::valid(),
        };

        let mut input_private = input_public;
        input_private.pat_private_flag = true;

        let out_pub = calculate_acute_2026(input_public, reference, adj);
        let out_priv = calculate_acute_2026(input_private, reference, adj);

        assert!(
            out_priv.nwau < out_pub.nwau,
            "MR3 violation: private patient must have deductions >= 0"
        );
        assert!(out_priv.private_service_deduction > Decimal::ZERO);
        assert_eq!(
            out_priv.private_accommodation_deduction,
            dec!(10) * dec!(0.02)
        );
    }

    #[test]
    fn test_metamorphic_mr4_permutation_invariance() {
        let reference = sample_nep26_reference();
        let adj = AcuteAdjustmentFactorsDecimal::default();

        let e1 = AcuteEpisodeInputDecimal {
            drg: "801A",
            los: dec!(5),
            icu_hours: Decimal::ZERO,
            icu_other: Decimal::ZERO,
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_covid_flag: false,
            eligible_paed_flag: false,
            validation: AcuteValidationState::valid(),
        };
        let e2 = AcuteEpisodeInputDecimal {
            los: dec!(10),
            ..e1
        };
        let e3 = AcuteEpisodeInputDecimal {
            los: dec!(80),
            ..e1
        };

        let list_forward = [e1, e2, e3];
        let list_reversed = [e3, e2, e1];

        let sum_forward: Decimal = list_forward
            .iter()
            .map(|e| calculate_acute_2026(*e, reference, adj).total_funding)
            .sum();
        let sum_reversed: Decimal = list_reversed
            .iter()
            .map(|e| calculate_acute_2026(*e, reference, adj).total_funding)
            .sum();

        assert_eq!(
            sum_forward, sum_reversed,
            "MR4 violation: batch total must be permutation invariant"
        );
    }

    #[test]
    fn test_numerical_precision_accumulator_drift() {
        let reference = sample_nep26_reference();
        let adj = AcuteAdjustmentFactorsDecimal::default();
        let input = AcuteEpisodeInputDecimal {
            drg: "801A",
            los: dec!(10),
            icu_hours: Decimal::ZERO,
            icu_other: Decimal::ZERO,
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_covid_flag: false,
            eligible_paed_flag: false,
            validation: AcuteValidationState::valid(),
        };

        let single = calculate_acute_2026(input, reference, adj);
        let n_episodes = 100_000;
        let mut total_decimal = Decimal::ZERO;
        for _ in 0..n_episodes {
            total_decimal += single.total_funding;
        }

        let expected_product = single.total_funding * Decimal::from(n_episodes);
        assert_eq!(
            total_decimal, expected_product,
            "128-bit decimal arithmetic must have 0 accumulator drift"
        );
    }
}
