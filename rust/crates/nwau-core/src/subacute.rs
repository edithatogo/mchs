//! Subacute and Non-Acute Care (AN-SNAP v5.0) kernel.
//!
//! Implements the funding formulas specified in IHACPA NEP determinations:
//! - AN-SNAP v5.0 branch valuation (Same-Day, Short Stay Outlier, Inlier, Long Stay Outlier).
//! - Radiotherapy and dialysis procedure adjustments.
//! - Specialist paediatric, Indigenous, remoteness, and treatment remoteness adjustments.
//! - Private patient service and accommodation deductions.

use rust_decimal::Decimal;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SubacuteSeparationCategory {
    SameDay = 1,
    ShortStayOutlier = 2,
    Inlier = 3,
    LongStayOutlier = 4,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SubacutePpsaOption {
    National = 1,
    StateLevel = 2,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SubacuteEpisodeInput<'a> {
    pub ansnap: &'a str,
    pub los: f64,
    pub pat_sameday_flag: bool,
    pub pat_private_flag: bool,
    pub pat_public_flag: bool,
    pub age: f64,
    pub state: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub struct SubacuteAdjustmentFactors {
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub radiotherapy_adjustment: f64,
    pub dialysis_adjustment: f64,
    pub private_serv_rate_national: f64,
    pub private_serv_rate_state: f64,
    pub private_accomm_sameday: f64,
    pub private_accomm_overnight: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SubacuteReferenceRow<'a> {
    pub ansnap: &'a str,
    pub sameday_list_flag: bool,
    pub inlier_lower_bound: f64,
    pub inlier_upper_bound: f64,
    pub pw_sameday: f64,
    pub pw_sso_perdiem: f64,
    pub pw_inlier: f64,
    pub pw_lso_perdiem: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct SubacuteEpisodeOutput {
    pub error_code: u8,
    pub separation_category: Option<SubacuteSeparationCategory>,
    pub w01: f64,
    pub gwau: f64,
    pub private_service_deduction: f64,
    pub private_accommodation_deduction: f64,
    pub nwau: f64,
}

fn round_to(value: f64, decimals: i32) -> f64 {
    let factor = 10f64.powi(decimals);
    (value * factor).round() / factor
}

/// Allowable paediatric AN-SNAP classes (for ages 0 to 17).
pub fn is_allowable_paediatric_ansnap(code: &str) -> bool {
    matches!(
        code,
        "5F01"
            | "5F02"
            | "5F03"
            | "5F04"
            | "5F05"
            | "5O01"
            | "5G01"
            | "5G02"
            | "5G03"
            | "5G04"
            | "5P01"
            | "5ES4"
            | "5EL1"
    )
}

/// Validate subacute input conditions according to NEP specification.
pub fn validate_subacute_episode(
    input: &SubacuteEpisodeInput<'_>,
    reference: Option<&SubacuteReferenceRow<'_>>,
) -> u8 {
    let Some(ref_row) = reference else {
        return 3;
    };
    if input.ansnap.is_empty() || input.los < 0.0 || input.state == 0 {
        return 3;
    }
    if !input.pat_public_flag && !input.pat_private_flag {
        return 2;
    }
    if input.age >= 0.0 && input.age <= 17.0 && !is_allowable_paediatric_ansnap(input.ansnap) {
        return 1;
    }
    if matches!(input.ansnap, "5J01" | "5K01" | "5L01" | "5M01")
        && (input.los > 1.0 || !ref_row.sameday_list_flag)
    {
        return 4;
    }
    0
}

/// Calculate Subacute NWAU using IEEE 754 floating-point arithmetic.
pub fn calculate_subacute(
    input: SubacuteEpisodeInput<'_>,
    reference: Option<SubacuteReferenceRow<'_>>,
    adjustments: SubacuteAdjustmentFactors,
    ppsa_option: SubacutePpsaOption,
) -> SubacuteEpisodeOutput {
    let error_code = validate_subacute_episode(&input, reference.as_ref());
    let Some(ref_row) = reference else {
        return SubacuteEpisodeOutput {
            error_code: 3,
            separation_category: None,
            w01: 0.0,
            gwau: 0.0,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau: 0.0,
        };
    };

    if error_code > 0 {
        return SubacuteEpisodeOutput {
            error_code,
            separation_category: None,
            w01: 0.0,
            gwau: 0.0,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau: 0.0,
        };
    }

    let sep_cat = if ref_row.sameday_list_flag {
        SubacuteSeparationCategory::SameDay
    } else if input.los < ref_row.inlier_lower_bound {
        SubacuteSeparationCategory::ShortStayOutlier
    } else if input.los <= ref_row.inlier_upper_bound {
        SubacuteSeparationCategory::Inlier
    } else {
        SubacuteSeparationCategory::LongStayOutlier
    };

    let w01_raw = match sep_cat {
        SubacuteSeparationCategory::SameDay => ref_row.pw_sameday,
        SubacuteSeparationCategory::ShortStayOutlier => input.los * ref_row.pw_sso_perdiem,
        SubacuteSeparationCategory::Inlier => ref_row.pw_inlier,
        SubacuteSeparationCategory::LongStayOutlier => {
            ref_row.pw_inlier + (input.los - ref_row.inlier_upper_bound) * ref_row.pw_lso_perdiem
        }
    };
    let w01 = round_to(w01_raw, 4);

    let gwau = w01
        * (1.0
            + adjustments.indigenous_adjustment
            + adjustments.remoteness_adjustment
            + adjustments.radiotherapy_adjustment
            + adjustments.dialysis_adjustment)
        * (1.0 + adjustments.treatment_remoteness_adjustment);

    let (priv_service_deduction, priv_accomm_deduction) = if input.pat_private_flag {
        let priv_serv_rate = match ppsa_option {
            SubacutePpsaOption::National => adjustments.private_serv_rate_national,
            SubacutePpsaOption::StateLevel => adjustments.private_serv_rate_state,
        };
        let serv_ded = priv_serv_rate * w01;
        let accomm_ded = if input.pat_sameday_flag {
            adjustments.private_accomm_sameday
        } else {
            input.los * adjustments.private_accomm_overnight
        };
        (serv_ded, accomm_ded)
    } else {
        (0.0, 0.0)
    };

    let nwau = (gwau - priv_service_deduction - priv_accomm_deduction).max(0.0);

    SubacuteEpisodeOutput {
        error_code: 0,
        separation_category: Some(sep_cat),
        w01,
        gwau,
        private_service_deduction: priv_service_deduction,
        private_accommodation_deduction: priv_accomm_deduction,
        nwau,
    }
}

// ============================================================================
// 128-bit Exact Fixed-Point Decimal Arithmetic Engine (rust_decimal)
// ============================================================================

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SubacuteEpisodeInputDecimal<'a> {
    pub ansnap: &'a str,
    pub los: Decimal,
    pub pat_sameday_flag: bool,
    pub pat_private_flag: bool,
    pub pat_public_flag: bool,
    pub age: Decimal,
    pub state: u8,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SubacuteAdjustmentFactorsDecimal {
    pub indigenous_adjustment: Decimal,
    pub remoteness_adjustment: Decimal,
    pub treatment_remoteness_adjustment: Decimal,
    pub radiotherapy_adjustment: Decimal,
    pub dialysis_adjustment: Decimal,
    pub private_serv_rate_national: Decimal,
    pub private_serv_rate_state: Decimal,
    pub private_accomm_sameday: Decimal,
    pub private_accomm_overnight: Decimal,
}

impl Default for SubacuteAdjustmentFactorsDecimal {
    fn default() -> Self {
        Self {
            indigenous_adjustment: Decimal::ZERO,
            remoteness_adjustment: Decimal::ZERO,
            treatment_remoteness_adjustment: Decimal::ZERO,
            radiotherapy_adjustment: Decimal::ZERO,
            dialysis_adjustment: Decimal::ZERO,
            private_serv_rate_national: Decimal::ZERO,
            private_serv_rate_state: Decimal::ZERO,
            private_accomm_sameday: Decimal::ZERO,
            private_accomm_overnight: Decimal::ZERO,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SubacuteReferenceRowDecimal<'a> {
    pub ansnap: &'a str,
    pub sameday_list_flag: bool,
    pub inlier_lower_bound: Decimal,
    pub inlier_upper_bound: Decimal,
    pub pw_sameday: Decimal,
    pub pw_sso_perdiem: Decimal,
    pub pw_inlier: Decimal,
    pub pw_lso_perdiem: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SubacuteEpisodeOutputDecimal {
    pub error_code: u8,
    pub separation_category: Option<SubacuteSeparationCategory>,
    pub w01: Decimal,
    pub gwau: Decimal,
    pub private_service_deduction: Decimal,
    pub private_accommodation_deduction: Decimal,
    pub nwau: Decimal,
    pub total_funding: Decimal,
}

/// Calculate Subacute NWAU with 128-bit exact fixed-point decimal arithmetic.
pub fn calculate_subacute_decimal(
    input: SubacuteEpisodeInputDecimal<'_>,
    reference: Option<SubacuteReferenceRowDecimal<'_>>,
    adjustments: SubacuteAdjustmentFactorsDecimal,
    ppsa_option: SubacutePpsaOption,
    nep_rate: Option<Decimal>,
) -> SubacuteEpisodeOutputDecimal {
    let Some(ref_row) = reference else {
        return SubacuteEpisodeOutputDecimal {
            error_code: 3,
            separation_category: None,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            private_service_deduction: Decimal::ZERO,
            private_accommodation_deduction: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    };

    if input.ansnap.is_empty() || input.los < Decimal::ZERO || input.state == 0 {
        return SubacuteEpisodeOutputDecimal {
            error_code: 3,
            separation_category: None,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            private_service_deduction: Decimal::ZERO,
            private_accommodation_deduction: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    }

    if !input.pat_public_flag && !input.pat_private_flag {
        return SubacuteEpisodeOutputDecimal {
            error_code: 2,
            separation_category: None,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            private_service_deduction: Decimal::ZERO,
            private_accommodation_deduction: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    }

    if input.age >= Decimal::ZERO
        && input.age <= Decimal::from(17)
        && !is_allowable_paediatric_ansnap(input.ansnap)
    {
        return SubacuteEpisodeOutputDecimal {
            error_code: 1,
            separation_category: None,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            private_service_deduction: Decimal::ZERO,
            private_accommodation_deduction: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    }

    let sep_cat = if ref_row.sameday_list_flag {
        SubacuteSeparationCategory::SameDay
    } else if input.los < ref_row.inlier_lower_bound {
        SubacuteSeparationCategory::ShortStayOutlier
    } else if input.los <= ref_row.inlier_upper_bound {
        SubacuteSeparationCategory::Inlier
    } else {
        SubacuteSeparationCategory::LongStayOutlier
    };

    let w01_raw = match sep_cat {
        SubacuteSeparationCategory::SameDay => ref_row.pw_sameday,
        SubacuteSeparationCategory::ShortStayOutlier => input.los * ref_row.pw_sso_perdiem,
        SubacuteSeparationCategory::Inlier => ref_row.pw_inlier,
        SubacuteSeparationCategory::LongStayOutlier => {
            ref_row.pw_inlier + (input.los - ref_row.inlier_upper_bound) * ref_row.pw_lso_perdiem
        }
    };
    let w01 = w01_raw.round_dp(4);

    let gwau = w01
        * (Decimal::ONE
            + adjustments.indigenous_adjustment
            + adjustments.remoteness_adjustment
            + adjustments.radiotherapy_adjustment
            + adjustments.dialysis_adjustment)
        * (Decimal::ONE + adjustments.treatment_remoteness_adjustment);

    let (priv_service_deduction, priv_accomm_deduction) = if input.pat_private_flag {
        let priv_serv_rate = match ppsa_option {
            SubacutePpsaOption::National => adjustments.private_serv_rate_national,
            SubacutePpsaOption::StateLevel => adjustments.private_serv_rate_state,
        };
        let serv_ded = priv_serv_rate * w01;
        let accomm_ded = if input.pat_sameday_flag {
            adjustments.private_accomm_sameday
        } else {
            input.los * adjustments.private_accomm_overnight
        };
        (serv_ded, accomm_ded)
    } else {
        (Decimal::ZERO, Decimal::ZERO)
    };

    let nwau = (gwau - priv_service_deduction - priv_accomm_deduction).max(Decimal::ZERO);
    let total_funding = match nep_rate {
        Some(rate) => (nwau * rate).round_dp(2),
        None => Decimal::ZERO,
    };

    SubacuteEpisodeOutputDecimal {
        error_code: 0,
        separation_category: Some(sep_cat),
        w01,
        gwau,
        private_service_deduction: priv_service_deduction,
        private_accommodation_deduction: priv_accomm_deduction,
        nwau,
        total_funding,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::str::FromStr;

    #[test]
    fn test_subacute_inlier_pricing() {
        let input = SubacuteEpisodeInput {
            ansnap: "5A11",
            los: 10.0,
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_public_flag: true,
            age: 45.0,
            state: 1,
        };
        let ref_row = SubacuteReferenceRow {
            ansnap: "5A11",
            sameday_list_flag: false,
            inlier_lower_bound: 5.0,
            inlier_upper_bound: 20.0,
            pw_sameday: 0.5,
            pw_sso_perdiem: 0.1,
            pw_inlier: 2.4500,
            pw_lso_perdiem: 0.15,
        };
        let adj = SubacuteAdjustmentFactors::default();

        let out = calculate_subacute(input, Some(ref_row), adj, SubacutePpsaOption::National);
        assert_eq!(out.error_code, 0);
        assert_eq!(
            out.separation_category,
            Some(SubacuteSeparationCategory::Inlier)
        );
        assert_eq!(out.w01, 2.4500);
        assert_eq!(out.nwau, 2.4500);
    }

    #[test]
    fn test_subacute_decimal_exact() {
        let input = SubacuteEpisodeInputDecimal {
            ansnap: "5A11",
            los: Decimal::from(10),
            pat_sameday_flag: false,
            pat_private_flag: false,
            pat_public_flag: true,
            age: Decimal::from(45),
            state: 1,
        };
        let ref_row = SubacuteReferenceRowDecimal {
            ansnap: "5A11",
            sameday_list_flag: false,
            inlier_lower_bound: Decimal::from(5),
            inlier_upper_bound: Decimal::from(20),
            pw_sameday: Decimal::from_str("0.5").unwrap(),
            pw_sso_perdiem: Decimal::from_str("0.1").unwrap(),
            pw_inlier: Decimal::from_str("2.4500").unwrap(),
            pw_lso_perdiem: Decimal::from_str("0.15").unwrap(),
        };
        let adj = SubacuteAdjustmentFactorsDecimal::default();
        let nep_rate = Some(Decimal::from(6500));

        let out = calculate_subacute_decimal(
            input,
            Some(ref_row),
            adj,
            SubacutePpsaOption::National,
            nep_rate,
        );
        assert_eq!(out.error_code, 0);
        assert_eq!(out.w01, Decimal::from_str("2.4500").unwrap());
        assert_eq!(out.nwau, Decimal::from_str("2.4500").unwrap());
        // 2.4500 * 6500 = 15925
        assert_eq!(out.total_funding, Decimal::from(15925));
    }
}
