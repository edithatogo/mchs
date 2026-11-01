//! Emergency Department (ED) kernel for AECC and UDG valuation.
//!
//! Implements the funding formulas specified in IHACPA NEP determinations:
//! - Option 1: UDG mapped from type_of_visit, triage_category, and episode_end_status.
//! - Option 2: Direct UDG price weight lookup.
//! - Option 3: AECC price weight lookup with patient and treatment remoteness adjustments.

use rust_decimal::Decimal;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EdClassificationOption {
    UdgMapped = 1,
    UdgDirect = 2,
    AeccDirect = 3,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EdEligibilityOption {
    CompensableDva = 1,
    FundingSource = 2,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct EdEpisodeInput<'a> {
    pub code: &'a str, // UDG or AECC code
    pub classification_option: EdClassificationOption,
    pub eligibility_option: EdEligibilityOption,
    pub compensable_status: Option<u8>,
    pub dva_status: Option<u8>,
    pub funding_source: Option<u8>,
}

#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub struct EdAdjustmentFactors {
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct EdReferenceRow<'a> {
    pub code: &'a str,
    pub price_weight: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct EdEpisodeOutput {
    pub error_code: u8,
    pub w01: f64,
    pub gwau: f64,
    pub nwau: f64,
}

fn round_to(value: f64, decimals: i32) -> f64 {
    let factor = 10f64.powi(decimals);
    (value * factor).round() / factor
}

/// Calculate ED NWAU using IEEE 754 floating-point arithmetic.
pub fn calculate_ed(
    input: EdEpisodeInput<'_>,
    reference: Option<EdReferenceRow<'_>>,
    adjustments: EdAdjustmentFactors,
    inscope_funding_sources: &[u8],
) -> EdEpisodeOutput {
    let Some(ref_row) = reference else {
        return EdEpisodeOutput {
            error_code: 3,
            w01: 0.0,
            gwau: 0.0,
            nwau: 0.0,
        };
    };

    let w01 = ref_row.price_weight;
    let gwau = match input.classification_option {
        EdClassificationOption::UdgMapped | EdClassificationOption::UdgDirect => {
            round_to(w01 * (1.0 + adjustments.treatment_remoteness_adjustment), 6)
        }
        EdClassificationOption::AeccDirect => round_to(
            w01 * (1.0 + adjustments.indigenous_adjustment + adjustments.remoteness_adjustment)
                * (1.0 + adjustments.treatment_remoteness_adjustment),
            8,
        ),
    };

    let error_code = match input.eligibility_option {
        EdEligibilityOption::CompensableDva => {
            let (Some(comp), Some(dva)) = (input.compensable_status, input.dva_status) else {
                return EdEpisodeOutput {
                    error_code: 3,
                    w01,
                    gwau,
                    nwau: 0.0,
                };
            };
            let in_scope = (comp == 2 || comp == 9) && (dva == 2 || dva == 9);
            if !in_scope {
                2
            } else {
                0
            }
        }
        EdEligibilityOption::FundingSource => {
            let Some(fund) = input.funding_source else {
                return EdEpisodeOutput {
                    error_code: 2,
                    w01,
                    gwau,
                    nwau: 0.0,
                };
            };
            if !inscope_funding_sources.contains(&fund) {
                2
            } else {
                0
            }
        }
    };

    let nwau = if error_code > 0 {
        0.0
    } else {
        round_to(gwau, 8)
    };

    EdEpisodeOutput {
        error_code,
        w01,
        gwau,
        nwau,
    }
}

// ============================================================================
// 128-bit Exact Fixed-Point Decimal Arithmetic Engine (rust_decimal)
// ============================================================================

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EdEpisodeInputDecimal<'a> {
    pub code: &'a str,
    pub classification_option: EdClassificationOption,
    pub eligibility_option: EdEligibilityOption,
    pub compensable_status: Option<u8>,
    pub dva_status: Option<u8>,
    pub funding_source: Option<u8>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct EdAdjustmentFactorsDecimal {
    pub indigenous_adjustment: Decimal,
    pub remoteness_adjustment: Decimal,
    pub treatment_remoteness_adjustment: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EdReferenceRowDecimal<'a> {
    pub code: &'a str,
    pub price_weight: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EdEpisodeOutputDecimal {
    pub error_code: u8,
    pub w01: Decimal,
    pub gwau: Decimal,
    pub nwau: Decimal,
    pub total_funding: Decimal,
}

/// Calculate ED NWAU with 128-bit exact fixed-point decimal arithmetic.
pub fn calculate_ed_decimal(
    input: EdEpisodeInputDecimal<'_>,
    reference: Option<EdReferenceRowDecimal<'_>>,
    adjustments: EdAdjustmentFactorsDecimal,
    inscope_funding_sources: &[u8],
    nep_rate: Option<Decimal>,
) -> EdEpisodeOutputDecimal {
    let Some(ref_row) = reference else {
        return EdEpisodeOutputDecimal {
            error_code: 3,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    };

    let w01 = ref_row.price_weight;
    let gwau = match input.classification_option {
        EdClassificationOption::UdgMapped | EdClassificationOption::UdgDirect => {
            (w01 * (Decimal::ONE + adjustments.treatment_remoteness_adjustment)).round_dp(6)
        }
        EdClassificationOption::AeccDirect => (w01
            * (Decimal::ONE
                + adjustments.indigenous_adjustment
                + adjustments.remoteness_adjustment)
            * (Decimal::ONE + adjustments.treatment_remoteness_adjustment))
            .round_dp(8),
    };

    let error_code = match input.eligibility_option {
        EdEligibilityOption::CompensableDva => {
            let (Some(comp), Some(dva)) = (input.compensable_status, input.dva_status) else {
                return EdEpisodeOutputDecimal {
                    error_code: 3,
                    w01,
                    gwau,
                    nwau: Decimal::ZERO,
                    total_funding: Decimal::ZERO,
                };
            };
            let in_scope = (comp == 2 || comp == 9) && (dva == 2 || dva == 9);
            if !in_scope {
                2
            } else {
                0
            }
        }
        EdEligibilityOption::FundingSource => {
            let Some(fund) = input.funding_source else {
                return EdEpisodeOutputDecimal {
                    error_code: 2,
                    w01,
                    gwau,
                    nwau: Decimal::ZERO,
                    total_funding: Decimal::ZERO,
                };
            };
            if !inscope_funding_sources.contains(&fund) {
                2
            } else {
                0
            }
        }
    };

    let nwau = if error_code > 0 {
        Decimal::ZERO
    } else {
        gwau.round_dp(8)
    };

    let total_funding = match nep_rate {
        Some(rate) => (nwau * rate).round_dp(2),
        None => Decimal::ZERO,
    };

    EdEpisodeOutputDecimal {
        error_code,
        w01,
        gwau,
        nwau,
        total_funding,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::str::FromStr;

    #[test]
    fn test_ed_aecc_basic_pricing() {
        let input = EdEpisodeInput {
            code: "E0110A",
            classification_option: EdClassificationOption::AeccDirect,
            eligibility_option: EdEligibilityOption::FundingSource,
            compensable_status: None,
            dva_status: None,
            funding_source: Some(1),
        };
        let ref_row = EdReferenceRow {
            code: "E0110A",
            price_weight: 0.2837,
        };
        let adj = EdAdjustmentFactors::default();
        let inscope = [1, 2, 8];

        let out = calculate_ed(input, Some(ref_row), adj, &inscope);
        assert_eq!(out.error_code, 0);
        assert_eq!(out.w01, 0.2837);
        assert_eq!(out.nwau, 0.2837);
    }

    #[test]
    fn test_ed_decimal_exact_no_drift() {
        let input = EdEpisodeInputDecimal {
            code: "E0110A",
            classification_option: EdClassificationOption::AeccDirect,
            eligibility_option: EdEligibilityOption::FundingSource,
            compensable_status: None,
            dva_status: None,
            funding_source: Some(1),
        };
        let ref_row = EdReferenceRowDecimal {
            code: "E0110A",
            price_weight: Decimal::from_str("0.2837").unwrap(),
        };
        let adj = EdAdjustmentFactorsDecimal::default();
        let inscope = [1, 2, 8];
        let nep_rate = Some(Decimal::from_str("6500.00").unwrap());

        let out = calculate_ed_decimal(input, Some(ref_row), adj, &inscope, nep_rate);
        assert_eq!(out.error_code, 0);
        assert_eq!(out.w01, Decimal::from_str("0.2837").unwrap());
        assert_eq!(out.nwau, Decimal::from_str("0.2837").unwrap());
        // 0.2837 * 6500 = 1844.05
        assert_eq!(out.total_funding, Decimal::from_str("1844.05").unwrap());
    }

    #[test]
    fn test_ed_eligibility_exclusion() {
        let input = EdEpisodeInput {
            code: "E0110A",
            classification_option: EdClassificationOption::AeccDirect,
            eligibility_option: EdEligibilityOption::FundingSource,
            compensable_status: None,
            dva_status: None,
            funding_source: Some(5), // Out of scope funding source
        };
        let ref_row = EdReferenceRow {
            code: "E0110A",
            price_weight: 0.2837,
        };
        let adj = EdAdjustmentFactors::default();
        let inscope = [1, 2, 8];

        let out = calculate_ed(input, Some(ref_row), adj, &inscope);
        assert_eq!(out.error_code, 2);
        assert_eq!(out.nwau, 0.0);
    }
}
