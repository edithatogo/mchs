//! Non-Admitted Outpatients (Tier 2 Clinics) kernel.
//!
//! Implements the funding formulas specified in IHACPA NEP determinations:
//! - Tier 2 clinic price weight lookup.
//! - Multiprovider clinic adjustments (for qualified clinics).
//! - Paediatric clinic adjustments.
//! - Indigenous, patient remoteness, and treatment remoteness adjustments.
//! - Both episode/event-level (data_type 1) and aggregate/count-level (data_type 2) models.

use rust_decimal::Decimal;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutpatientDataType {
    EventLevel = 1,
    AggregateCount = 2,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct OutpatientEpisodeInput<'a> {
    pub clinic_code: &'a str,
    pub data_type: OutpatientDataType,
    pub multiprovider_flag: bool,
    pub eligible_paediatric_flag: bool,
    pub inscope_flag: bool,
    // Event counts (for AggregateCount)
    pub group_event_count: f64,
    pub indiv_event_count: f64,
    pub multidisciplinary_event_count: f64,
}

#[derive(Debug, Clone, Copy, PartialEq, Default)]
pub struct OutpatientAdjustmentFactors {
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub multiprovider_adjustment: f64,
    pub paediatric_adjustment: f64, // Multiplier (default 1.0)
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct OutpatientReferenceRow<'a> {
    pub clinic_code: &'a str,
    pub price_weight: f64,
    pub paediatric_adjustment: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct OutpatientEpisodeOutput {
    pub error_code: u8,
    pub w01: f64,
    pub gwau: f64,
    pub nwau: f64,
}

fn round_to(value: f64, decimals: i32) -> f64 {
    let factor = 10f64.powi(decimals);
    (value * factor).round() / factor
}

/// Clinics excluded from multiprovider adjustment: 20.48, 20.56, 40.62.
pub fn is_multiprovider_exempt_clinic(clinic: &str) -> bool {
    clinic == "20.48" || clinic == "20.56" || clinic == "40.62"
}

/// Calculate Outpatient NWAU using IEEE 754 floating-point arithmetic.
pub fn calculate_outpatients(
    input: OutpatientEpisodeInput<'_>,
    reference: Option<OutpatientReferenceRow<'_>>,
    adjustments: OutpatientAdjustmentFactors,
) -> OutpatientEpisodeOutput {
    let Some(ref_row) = reference else {
        return OutpatientEpisodeOutput {
            error_code: 3,
            w01: 0.0,
            gwau: 0.0,
            nwau: 0.0,
        };
    };

    let w01 = ref_row.price_weight;
    if w01 == 0.0 {
        return OutpatientEpisodeOutput {
            error_code: 1,
            w01: 0.0,
            gwau: 0.0,
            nwau: 0.0,
        };
    }

    if !input.inscope_flag {
        return OutpatientEpisodeOutput {
            error_code: 2,
            w01,
            gwau: 0.0,
            nwau: 0.0,
        };
    }

    let multiprov_applies =
        input.multiprovider_flag && !is_multiprovider_exempt_clinic(input.clinic_code);
    let multiprov_val = if multiprov_applies {
        adjustments.multiprovider_adjustment
    } else {
        0.0
    };

    let paed_factor = if input.eligible_paediatric_flag {
        if ref_row.paediatric_adjustment > 0.0 {
            ref_row.paediatric_adjustment
        } else if adjustments.paediatric_adjustment > 0.0 {
            adjustments.paediatric_adjustment
        } else {
            1.0
        }
    } else {
        1.0
    };

    let gwau = match input.data_type {
        OutpatientDataType::EventLevel => {
            let base = 1.0
                + adjustments.indigenous_adjustment
                + adjustments.remoteness_adjustment
                + multiprov_val;
            let treat = 1.0 + adjustments.treatment_remoteness_adjustment;
            w01 * paed_factor * base * treat
        }
        OutpatientDataType::AggregateCount => {
            let treat = 1.0 + adjustments.treatment_remoteness_adjustment;
            let base_count = input.group_event_count + input.indiv_event_count;
            let total_count = base_count + input.multidisciplinary_event_count;
            if multiprov_applies {
                w01 * (1.0 + multiprov_val) * treat * total_count
            } else {
                w01 * treat * base_count
            }
        }
    };

    let nwau = round_to(gwau, 8);

    OutpatientEpisodeOutput {
        error_code: 0,
        w01,
        gwau,
        nwau,
    }
}

// ============================================================================
// 128-bit Exact Fixed-Point Decimal Arithmetic Engine (rust_decimal)
// ============================================================================

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OutpatientEpisodeInputDecimal<'a> {
    pub clinic_code: &'a str,
    pub data_type: OutpatientDataType,
    pub multiprovider_flag: bool,
    pub eligible_paediatric_flag: bool,
    pub inscope_flag: bool,
    pub group_event_count: Decimal,
    pub indiv_event_count: Decimal,
    pub multidisciplinary_event_count: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OutpatientAdjustmentFactorsDecimal {
    pub indigenous_adjustment: Decimal,
    pub remoteness_adjustment: Decimal,
    pub treatment_remoteness_adjustment: Decimal,
    pub multiprovider_adjustment: Decimal,
    pub paediatric_adjustment: Decimal,
}

impl Default for OutpatientAdjustmentFactorsDecimal {
    fn default() -> Self {
        Self {
            indigenous_adjustment: Decimal::ZERO,
            remoteness_adjustment: Decimal::ZERO,
            treatment_remoteness_adjustment: Decimal::ZERO,
            multiprovider_adjustment: Decimal::ZERO,
            paediatric_adjustment: Decimal::ONE,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OutpatientReferenceRowDecimal<'a> {
    pub clinic_code: &'a str,
    pub price_weight: Decimal,
    pub paediatric_adjustment: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OutpatientEpisodeOutputDecimal {
    pub error_code: u8,
    pub w01: Decimal,
    pub gwau: Decimal,
    pub nwau: Decimal,
    pub total_funding: Decimal,
}

/// Calculate Outpatient NWAU with 128-bit exact fixed-point decimal arithmetic.
pub fn calculate_outpatients_decimal(
    input: OutpatientEpisodeInputDecimal<'_>,
    reference: Option<OutpatientReferenceRowDecimal<'_>>,
    adjustments: OutpatientAdjustmentFactorsDecimal,
    nep_rate: Option<Decimal>,
) -> OutpatientEpisodeOutputDecimal {
    let Some(ref_row) = reference else {
        return OutpatientEpisodeOutputDecimal {
            error_code: 3,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    };

    let w01 = ref_row.price_weight;
    if w01 == Decimal::ZERO {
        return OutpatientEpisodeOutputDecimal {
            error_code: 1,
            w01: Decimal::ZERO,
            gwau: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    }

    if !input.inscope_flag {
        return OutpatientEpisodeOutputDecimal {
            error_code: 2,
            w01,
            gwau: Decimal::ZERO,
            nwau: Decimal::ZERO,
            total_funding: Decimal::ZERO,
        };
    }

    let multiprov_applies =
        input.multiprovider_flag && !is_multiprovider_exempt_clinic(input.clinic_code);
    let multiprov_val = if multiprov_applies {
        adjustments.multiprovider_adjustment
    } else {
        Decimal::ZERO
    };

    let paed_factor = if input.eligible_paediatric_flag {
        if ref_row.paediatric_adjustment > Decimal::ZERO {
            ref_row.paediatric_adjustment
        } else if adjustments.paediatric_adjustment > Decimal::ZERO {
            adjustments.paediatric_adjustment
        } else {
            Decimal::ONE
        }
    } else {
        Decimal::ONE
    };

    let gwau = match input.data_type {
        OutpatientDataType::EventLevel => {
            let base = Decimal::ONE
                + adjustments.indigenous_adjustment
                + adjustments.remoteness_adjustment
                + multiprov_val;
            let treat = Decimal::ONE + adjustments.treatment_remoteness_adjustment;
            w01 * paed_factor * base * treat
        }
        OutpatientDataType::AggregateCount => {
            let treat = Decimal::ONE + adjustments.treatment_remoteness_adjustment;
            let base_count = input.group_event_count + input.indiv_event_count;
            let total_count = base_count + input.multidisciplinary_event_count;
            if multiprov_applies {
                w01 * (Decimal::ONE + multiprov_val) * treat * total_count
            } else {
                w01 * treat * base_count
            }
        }
    };

    let nwau = gwau.round_dp(8);
    let total_funding = match nep_rate {
        Some(rate) => (nwau * rate).round_dp(2),
        None => Decimal::ZERO,
    };

    OutpatientEpisodeOutputDecimal {
        error_code: 0,
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
    fn test_outpatients_event_level_basic() {
        let input = OutpatientEpisodeInput {
            clinic_code: "10.01",
            data_type: OutpatientDataType::EventLevel,
            multiprovider_flag: false,
            eligible_paediatric_flag: false,
            inscope_flag: true,
            group_event_count: 0.0,
            indiv_event_count: 0.0,
            multidisciplinary_event_count: 0.0,
        };
        let ref_row = OutpatientReferenceRow {
            clinic_code: "10.01",
            price_weight: 0.1742,
            paediatric_adjustment: 1.0,
        };
        let adj = OutpatientAdjustmentFactors::default();

        let out = calculate_outpatients(input, Some(ref_row), adj);
        assert_eq!(out.error_code, 0);
        assert_eq!(out.w01, 0.1742);
        assert_eq!(out.nwau, 0.1742);
    }

    #[test]
    fn test_outpatients_multiprovider_adjustment() {
        let input = OutpatientEpisodeInput {
            clinic_code: "10.01",
            data_type: OutpatientDataType::EventLevel,
            multiprovider_flag: true,
            eligible_paediatric_flag: false,
            inscope_flag: true,
            group_event_count: 0.0,
            indiv_event_count: 0.0,
            multidisciplinary_event_count: 0.0,
        };
        let ref_row = OutpatientReferenceRow {
            clinic_code: "10.01",
            price_weight: 0.2000,
            paediatric_adjustment: 1.0,
        };
        let adj = OutpatientAdjustmentFactors {
            multiprovider_adjustment: 0.35,
            ..Default::default()
        };

        let out = calculate_outpatients(input, Some(ref_row), adj);
        assert_eq!(out.error_code, 0);
        // 0.2000 * (1 + 0.35) = 0.27
        assert_eq!(out.nwau, 0.27);
    }

    #[test]
    fn test_outpatients_decimal_exact() {
        let input = OutpatientEpisodeInputDecimal {
            clinic_code: "10.01",
            data_type: OutpatientDataType::EventLevel,
            multiprovider_flag: true,
            eligible_paediatric_flag: false,
            inscope_flag: true,
            group_event_count: Decimal::ZERO,
            indiv_event_count: Decimal::ZERO,
            multidisciplinary_event_count: Decimal::ZERO,
        };
        let ref_row = OutpatientReferenceRowDecimal {
            clinic_code: "10.01",
            price_weight: Decimal::from_str("0.2000").unwrap(),
            paediatric_adjustment: Decimal::ONE,
        };
        let adj = OutpatientAdjustmentFactorsDecimal {
            multiprovider_adjustment: Decimal::from_str("0.35").unwrap(),
            ..Default::default()
        };
        let nep_rate = Some(Decimal::from(6000));

        let out = calculate_outpatients_decimal(input, Some(ref_row), adj, nep_rate);
        assert_eq!(out.error_code, 0);
        assert_eq!(out.nwau, Decimal::from_str("0.27000000").unwrap());
        assert_eq!(out.total_funding, Decimal::from(1620));
    }
}
