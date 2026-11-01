//! Admitted Mental Health and Community Mental Health (AMHCC) kernel.
//!
//! Implements the funding formulas specified in IHACPA NEP determinations:
//! - Admitted Mental Health: Phase-based pricing with Short Stay Outlier (SSO),
//!   Inlier, and Long Stay Outlier (LSO) tiers.
//! - Community Mental Health: Service contact pricing with patient and non-patient
//!   contact weights.
//! - Adjustments: Specialist paediatric, Indigenous, remoteness, treatment remoteness,
//!   and private patient service / accommodation deductions.

use rust_decimal::Decimal;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MhSubstream {
    Admitted,
    Community,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MhPpsaOption {
    National = 1,
    StateLevel = 2,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MhSeparationCategory {
    ShortStayOutlier = 2,
    Inlier = 3,
    LongStayOutlier = 4,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MhEpisodeInput<'a> {
    pub amhcc: &'a str,
    pub los: f64,
    pub pat_sameday_flag: bool,
    pub pat_private_flag: bool,
    pub state: u8,
    // Community service contacts (hours/units)
    pub sc_pat_pub: f64,
    pub sc_nopat_pub: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MhAdjustmentFactors {
    pub specialist_paediatric_multiplier: f64, // default 1.0
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub private_serv_rate_national: f64,
    pub private_serv_rate_state: f64,
    pub private_accomm_sameday: f64,
    pub private_accomm_overnight: f64,
}

impl Default for MhAdjustmentFactors {
    fn default() -> Self {
        Self {
            specialist_paediatric_multiplier: 1.0,
            indigenous_adjustment: 0.0,
            remoteness_adjustment: 0.0,
            treatment_remoteness_adjustment: 0.0,
            private_serv_rate_national: 0.0,
            private_serv_rate_state: 0.0,
            private_accomm_sameday: 0.0,
            private_accomm_overnight: 0.0,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MhAdmittedReferenceRow<'a> {
    pub amhcc: &'a str,
    pub price_cat: u8, // 0: per-diem only, 1: tiered (SSO/Inlier/LSO)
    pub inlier_lower_bound: f64,
    pub inlier_upper_bound: f64,
    pub sso_base_weight: f64,
    pub sso_per_diem: f64,
    pub inlier_weight: f64,
    pub lso_per_diem: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MhCommunityReferenceRow<'a> {
    pub amhcc: &'a str,
    pub sc_pat_price_weight: f64,
    pub sc_nopat_price_weight: f64,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct MhEpisodeOutput {
    pub error_code: u8,
    pub substream: MhSubstream,
    pub separation_category: Option<MhSeparationCategory>,
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

/// Calculate Mental Health NWAU using IEEE 754 floating-point arithmetic.
pub fn calculate_mh(
    input: MhEpisodeInput<'_>,
    adm_reference: Option<MhAdmittedReferenceRow<'_>>,
    cmty_reference: Option<MhCommunityReferenceRow<'_>>,
    adjustments: MhAdjustmentFactors,
    ppsa_option: MhPpsaOption,
) -> MhEpisodeOutput {
    let is_admitted = input.amhcc.starts_with('1');
    let substream = if is_admitted {
        MhSubstream::Admitted
    } else {
        MhSubstream::Community
    };

    let specpaed = if adjustments.specialist_paediatric_multiplier >= 1.0 {
        adjustments.specialist_paediatric_multiplier
    } else {
        1.0
    };

    if is_admitted {
        let Some(ref_row) = adm_reference else {
            return MhEpisodeOutput {
                error_code: 3,
                substream,
                separation_category: None,
                w01: 0.0,
                gwau: 0.0,
                private_service_deduction: 0.0,
                private_accommodation_deduction: 0.0,
                nwau: 0.0,
            };
        };

        let sep_cat = if input.los < ref_row.inlier_lower_bound {
            MhSeparationCategory::ShortStayOutlier
        } else if input.los <= ref_row.inlier_upper_bound {
            MhSeparationCategory::Inlier
        } else {
            MhSeparationCategory::LongStayOutlier
        };

        let w01_raw = if ref_row.price_cat == 0 {
            ref_row.sso_base_weight + input.los * ref_row.lso_per_diem
        } else {
            match sep_cat {
                MhSeparationCategory::ShortStayOutlier => {
                    ref_row.sso_base_weight + input.los * ref_row.sso_per_diem
                }
                MhSeparationCategory::Inlier => ref_row.inlier_weight,
                MhSeparationCategory::LongStayOutlier => {
                    ref_row.inlier_weight
                        + (input.los - ref_row.inlier_upper_bound) * ref_row.lso_per_diem
                }
            }
        };
        let w01 = round_to(w01_raw, 4);

        let gwau = w01
            * specpaed
            * (1.0 + adjustments.indigenous_adjustment + adjustments.remoteness_adjustment)
            * (1.0 + adjustments.treatment_remoteness_adjustment);

        let (priv_service_deduction, priv_accomm_deduction) = if input.pat_private_flag {
            let priv_serv_rate = match ppsa_option {
                MhPpsaOption::National => adjustments.private_serv_rate_national,
                MhPpsaOption::StateLevel => adjustments.private_serv_rate_state,
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

        MhEpisodeOutput {
            error_code: 0,
            substream,
            separation_category: Some(sep_cat),
            w01,
            gwau,
            private_service_deduction: priv_service_deduction,
            private_accommodation_deduction: priv_accomm_deduction,
            nwau,
        }
    } else {
        let Some(ref_row) = cmty_reference else {
            return MhEpisodeOutput {
                error_code: 3,
                substream,
                separation_category: None,
                w01: 0.0,
                gwau: 0.0,
                private_service_deduction: 0.0,
                private_accommodation_deduction: 0.0,
                nwau: 0.0,
            };
        };

        let w01_raw = (input.sc_pat_pub * ref_row.sc_pat_price_weight
            + input.sc_nopat_pub * ref_row.sc_nopat_price_weight)
            .max(0.0);
        let w01 = round_to(w01_raw, 4);

        let gwau = w01
            * specpaed
            * (1.0 + adjustments.indigenous_adjustment + adjustments.remoteness_adjustment)
            * (1.0 + adjustments.treatment_remoteness_adjustment);

        MhEpisodeOutput {
            error_code: 0,
            substream,
            separation_category: None,
            w01,
            gwau,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau: gwau,
        }
    }
}

// ============================================================================
// 128-bit Exact Fixed-Point Decimal Arithmetic Engine (rust_decimal)
// ============================================================================

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MhEpisodeInputDecimal<'a> {
    pub amhcc: &'a str,
    pub los: Decimal,
    pub pat_sameday_flag: bool,
    pub pat_private_flag: bool,
    pub state: u8,
    pub sc_pat_pub: Decimal,
    pub sc_nopat_pub: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MhAdjustmentFactorsDecimal {
    pub specialist_paediatric_multiplier: Decimal,
    pub indigenous_adjustment: Decimal,
    pub remoteness_adjustment: Decimal,
    pub treatment_remoteness_adjustment: Decimal,
    pub private_serv_rate_national: Decimal,
    pub private_serv_rate_state: Decimal,
    pub private_accomm_sameday: Decimal,
    pub private_accomm_overnight: Decimal,
}

impl Default for MhAdjustmentFactorsDecimal {
    fn default() -> Self {
        Self {
            specialist_paediatric_multiplier: Decimal::ONE,
            indigenous_adjustment: Decimal::ZERO,
            remoteness_adjustment: Decimal::ZERO,
            treatment_remoteness_adjustment: Decimal::ZERO,
            private_serv_rate_national: Decimal::ZERO,
            private_serv_rate_state: Decimal::ZERO,
            private_accomm_sameday: Decimal::ZERO,
            private_accomm_overnight: Decimal::ZERO,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MhAdmittedReferenceRowDecimal<'a> {
    pub amhcc: &'a str,
    pub price_cat: u8,
    pub inlier_lower_bound: Decimal,
    pub inlier_upper_bound: Decimal,
    pub sso_base_weight: Decimal,
    pub sso_per_diem: Decimal,
    pub inlier_weight: Decimal,
    pub lso_per_diem: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MhCommunityReferenceRowDecimal<'a> {
    pub amhcc: &'a str,
    pub sc_pat_price_weight: Decimal,
    pub sc_nopat_price_weight: Decimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct MhEpisodeOutputDecimal {
    pub error_code: u8,
    pub substream: MhSubstream,
    pub separation_category: Option<MhSeparationCategory>,
    pub w01: Decimal,
    pub gwau: Decimal,
    pub private_service_deduction: Decimal,
    pub private_accommodation_deduction: Decimal,
    pub nwau: Decimal,
    pub total_funding: Decimal,
}

/// Calculate Mental Health NWAU with 128-bit exact fixed-point decimal arithmetic.
pub fn calculate_mh_decimal(
    input: MhEpisodeInputDecimal<'_>,
    adm_reference: Option<MhAdmittedReferenceRowDecimal<'_>>,
    cmty_reference: Option<MhCommunityReferenceRowDecimal<'_>>,
    adjustments: MhAdjustmentFactorsDecimal,
    ppsa_option: MhPpsaOption,
    nep_rate: Option<Decimal>,
) -> MhEpisodeOutputDecimal {
    let is_admitted = input.amhcc.starts_with('1');
    let substream = if is_admitted {
        MhSubstream::Admitted
    } else {
        MhSubstream::Community
    };

    let specpaed = if adjustments.specialist_paediatric_multiplier > Decimal::ZERO {
        adjustments.specialist_paediatric_multiplier
    } else {
        Decimal::ONE
    };

    if is_admitted {
        let Some(ref_row) = adm_reference else {
            return MhEpisodeOutputDecimal {
                error_code: 3,
                substream,
                separation_category: None,
                w01: Decimal::ZERO,
                gwau: Decimal::ZERO,
                private_service_deduction: Decimal::ZERO,
                private_accommodation_deduction: Decimal::ZERO,
                nwau: Decimal::ZERO,
                total_funding: Decimal::ZERO,
            };
        };

        let sep_cat = if input.los < ref_row.inlier_lower_bound {
            MhSeparationCategory::ShortStayOutlier
        } else if input.los <= ref_row.inlier_upper_bound {
            MhSeparationCategory::Inlier
        } else {
            MhSeparationCategory::LongStayOutlier
        };

        let w01_raw = if ref_row.price_cat == 0 {
            ref_row.sso_base_weight + input.los * ref_row.lso_per_diem
        } else {
            match sep_cat {
                MhSeparationCategory::ShortStayOutlier => {
                    ref_row.sso_base_weight + input.los * ref_row.sso_per_diem
                }
                MhSeparationCategory::Inlier => ref_row.inlier_weight,
                MhSeparationCategory::LongStayOutlier => {
                    ref_row.inlier_weight
                        + (input.los - ref_row.inlier_upper_bound) * ref_row.lso_per_diem
                }
            }
        };
        let w01 = w01_raw.round_dp(4);

        let gwau = w01
            * specpaed
            * (Decimal::ONE
                + adjustments.indigenous_adjustment
                + adjustments.remoteness_adjustment)
            * (Decimal::ONE + adjustments.treatment_remoteness_adjustment);

        let (priv_service_deduction, priv_accomm_deduction) = if input.pat_private_flag {
            let priv_serv_rate = match ppsa_option {
                MhPpsaOption::National => adjustments.private_serv_rate_national,
                MhPpsaOption::StateLevel => adjustments.private_serv_rate_state,
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

        MhEpisodeOutputDecimal {
            error_code: 0,
            substream,
            separation_category: Some(sep_cat),
            w01,
            gwau,
            private_service_deduction: priv_service_deduction,
            private_accommodation_deduction: priv_accomm_deduction,
            nwau,
            total_funding,
        }
    } else {
        let Some(ref_row) = cmty_reference else {
            return MhEpisodeOutputDecimal {
                error_code: 3,
                substream,
                separation_category: None,
                w01: Decimal::ZERO,
                gwau: Decimal::ZERO,
                private_service_deduction: Decimal::ZERO,
                private_accommodation_deduction: Decimal::ZERO,
                nwau: Decimal::ZERO,
                total_funding: Decimal::ZERO,
            };
        };

        let w01_raw = (input.sc_pat_pub * ref_row.sc_pat_price_weight
            + input.sc_nopat_pub * ref_row.sc_nopat_price_weight)
            .max(Decimal::ZERO);
        let w01 = w01_raw.round_dp(4);

        let gwau = w01
            * specpaed
            * (Decimal::ONE
                + adjustments.indigenous_adjustment
                + adjustments.remoteness_adjustment)
            * (Decimal::ONE + adjustments.treatment_remoteness_adjustment);

        let total_funding = match nep_rate {
            Some(rate) => (gwau * rate).round_dp(2),
            None => Decimal::ZERO,
        };

        MhEpisodeOutputDecimal {
            error_code: 0,
            substream,
            separation_category: None,
            w01,
            gwau,
            private_service_deduction: Decimal::ZERO,
            private_accommodation_deduction: Decimal::ZERO,
            nwau: gwau,
            total_funding,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::str::FromStr;

    #[test]
    fn test_mh_admitted_inlier() {
        let input = MhEpisodeInput {
            amhcc: "1001",
            los: 4.0,
            pat_sameday_flag: false,
            pat_private_flag: false,
            state: 1,
            sc_pat_pub: 0.0,
            sc_nopat_pub: 0.0,
        };
        let ref_row = MhAdmittedReferenceRow {
            amhcc: "1001",
            price_cat: 1,
            inlier_lower_bound: 3.0,
            inlier_upper_bound: 5.0,
            sso_base_weight: 1.0,
            sso_per_diem: 0.2,
            inlier_weight: 1.5,
            lso_per_diem: 0.3,
        };
        let adj = MhAdjustmentFactors::default();

        let out = calculate_mh(input, Some(ref_row), None, adj, MhPpsaOption::National);
        assert_eq!(out.error_code, 0);
        assert_eq!(out.substream, MhSubstream::Admitted);
        assert_eq!(out.separation_category, Some(MhSeparationCategory::Inlier));
        assert_eq!(out.w01, 1.5);
        assert_eq!(out.nwau, 1.5);
    }

    #[test]
    fn test_mh_admitted_lso() {
        let input = MhEpisodeInput {
            amhcc: "1001",
            los: 7.0, // 2 days over inlier_ub of 5.0
            pat_sameday_flag: false,
            pat_private_flag: false,
            state: 1,
            sc_pat_pub: 0.0,
            sc_nopat_pub: 0.0,
        };
        let ref_row = MhAdmittedReferenceRow {
            amhcc: "1001",
            price_cat: 1,
            inlier_lower_bound: 3.0,
            inlier_upper_bound: 5.0,
            sso_base_weight: 1.0,
            sso_per_diem: 0.2,
            inlier_weight: 1.5,
            lso_per_diem: 0.3,
        };
        let adj = MhAdjustmentFactors::default();

        let out = calculate_mh(input, Some(ref_row), None, adj, MhPpsaOption::National);
        assert_eq!(out.error_code, 0);
        assert_eq!(
            out.separation_category,
            Some(MhSeparationCategory::LongStayOutlier)
        );
        // 1.5 + (7.0 - 5.0) * 0.3 = 1.5 + 0.6 = 2.1
        assert_eq!(out.w01, 2.1);
        assert_eq!(out.nwau, 2.1);
    }

    #[test]
    fn test_mh_decimal_exact_inlier() {
        let input = MhEpisodeInputDecimal {
            amhcc: "1001",
            los: Decimal::from(4),
            pat_sameday_flag: false,
            pat_private_flag: false,
            state: 1,
            sc_pat_pub: Decimal::ZERO,
            sc_nopat_pub: Decimal::ZERO,
        };
        let ref_row = MhAdmittedReferenceRowDecimal {
            amhcc: "1001",
            price_cat: 1,
            inlier_lower_bound: Decimal::from(3),
            inlier_upper_bound: Decimal::from(5),
            sso_base_weight: Decimal::ONE,
            sso_per_diem: Decimal::from_str("0.2").unwrap(),
            inlier_weight: Decimal::from_str("1.5").unwrap(),
            lso_per_diem: Decimal::from_str("0.3").unwrap(),
        };
        let adj = MhAdjustmentFactorsDecimal::default();
        let nep_rate = Some(Decimal::from(6000));

        let out = calculate_mh_decimal(
            input,
            Some(ref_row),
            None,
            adj,
            MhPpsaOption::National,
            nep_rate,
        );
        assert_eq!(out.error_code, 0);
        assert_eq!(out.w01, Decimal::from_str("1.5000").unwrap());
        assert_eq!(out.nwau, Decimal::from_str("1.5000").unwrap());
        assert_eq!(out.total_funding, Decimal::from(9000));
    }
}
