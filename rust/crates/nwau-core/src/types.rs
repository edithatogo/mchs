//! Core calculator types — identifiers, streams, pricing years, and episode
//! metadata used across all formula kernels.

use serde::{Deserialize, Serialize};
use std::fmt;

/// A typed NWAU calculator identifier (e.g. "acute-2025").
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct CalculatorId(pub String);

impl CalculatorId {
    /// The built-in acute 2025 calculator.
    pub const ACUTE_2025: &'static str = "acute-2025";
    /// Reserved identifier for a future sub-acute calculator.
    pub const SUB_ACUTE: &'static str = "sub-acute";
    /// Reserved identifier for a future non-admitted calculator.
    pub const NON_ADMITTED: &'static str = "non-admitted";
    /// Reserved identifier for a future emergency department calculator.
    pub const EMERGENCY: &'static str = "emergency";

    /// Return true when `self` matches an implemented calculator ID.
    pub fn is_implemented(&self) -> bool {
        matches!(self.0.as_str(), Self::ACUTE_2025)
    }

    /// Return true when `self` matches a reserved calculator ID.
    pub fn is_reserved(&self) -> bool {
        matches!(
            self.0.as_str(),
            Self::SUB_ACUTE | Self::NON_ADMITTED | Self::EMERGENCY
        )
    }
}

impl fmt::Display for CalculatorId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

/// A pricing year (financial year label such as "2025").
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct PricingYear(pub u16);

impl PricingYear {
    /// The pricing year for the 2025 proof of concept.
    pub const CURRENT: PricingYear = PricingYear(2025);

    /// Return the two-digit suffix (e.g. 25 for 2025).
    pub fn suffix(&self) -> u16 {
        self.0 % 100
    }
}

impl fmt::Display for PricingYear {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// Care stream classification.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Stream {
    /// Acute admitted care.
    Acute,
    /// Sub-acute (rehabilitation, palliative, etc.).
    SubAcute,
    /// Non-admitted care.
    NonAdmitted,
    /// Emergency department care.
    Emergency,
    /// Community mental health care.
    CommunityMentalHealth,
}

impl Stream {
    /// Return the canonical string label used in configuration files.
    pub fn label(&self) -> &'static str {
        match self {
            Stream::Acute => "acute",
            Stream::SubAcute => "sub-acute",
            Stream::NonAdmitted => "non-admitted",
            Stream::Emergency => "emergency",
            Stream::CommunityMentalHealth => "community-mental-health",
        }
    }
}

impl fmt::Display for Stream {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.label())
    }
}
/// Episode-level classification flags.
#[derive(Debug, Clone, Copy, PartialEq, Default, Serialize, Deserialize)]
pub struct EpisodeFlags {
    /// Same-day separation.
    pub same_day: bool,
    /// Private patient flag.
    pub private_patient: bool,
    /// COVID-19 flagged episode.
    pub covid: bool,
    /// Eligible for paediatric adjustment.
    pub eligible_paediatric: bool,
    /// Indigenous status flag.
    pub indigenous: bool,
    /// Remoteness area code (1–5 or 0 for unknown).
    pub remoteness_code: u8,
}

/// A single episode input row with DRG, length of stay, ICU hours, and flags.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct EpisodeRow {
    /// Diagnostic Related Group code.
    pub drg: String,
    /// Length of stay in days.
    pub los: f64,
    /// ICU hours.
    pub icu_hours: f64,
    /// Other ICU-like hours (e.g. HDU/CCU).
    pub icu_other: f64,
    /// Episode-level classification flags.
    pub flags: EpisodeFlags,
    /// Optional episode identifier for provenance tracking.
    pub episode_id: Option<String>,
}

/// A reference row lookup entry for a single DRG.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct ReferenceRow {
    /// DRG code.
    pub drg: String,
    /// Inlier lower bound (days).
    pub inlier_lower_bound: f64,
    /// Inlier upper bound (days).
    pub inlier_upper_bound: f64,
    /// Paediatric multiplier.
    pub paediatric_multiplier: f64,
    /// Whether the DRG is on the same-day list.
    pub same_day_list_flag: bool,
    /// Whether ICU hours are bundled.
    pub bundled_icu_flag: bool,
    /// Same-day base weight.
    pub same_day_base_weight: f64,
    /// Same-day per-diem rate.
    pub same_day_per_diem: f64,
    /// Inlier weight.
    pub inlier_weight: f64,
    /// Long-stay per-diem rate.
    pub long_stay_per_diem: f64,
    /// Private service adjustment factor.
    pub private_service_adjustment: f64,
}

impl ReferenceRow {
    /// Convert to the acute module's reference row type.
    pub fn to_acute_ref(&self) -> crate::acute::AcuteReferenceRow<'_> {
        crate::acute::AcuteReferenceRow {
            drg: &self.drg,
            inlier_lower_bound: self.inlier_lower_bound,
            inlier_upper_bound: self.inlier_upper_bound,
            paediatric_multiplier: self.paediatric_multiplier,
            same_day_list_flag: self.same_day_list_flag,
            bundled_icu_flag: self.bundled_icu_flag,
            same_day_base_weight: self.same_day_base_weight,
            same_day_per_diem: self.same_day_per_diem,
            inlier_weight: self.inlier_weight,
            long_stay_per_diem: self.long_stay_per_diem,
            private_service_adjustment: self.private_service_adjustment,
        }
    }
}

/// Adjustment factors applicable to a single episode or batch.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct AdjustmentFactors {
    /// ICU hourly rate.
    pub icu_rate: f64,
    /// COVID adjustment (additive fraction).
    pub covid_adjustment: f64,
    /// Indigenous adjustment (additive fraction).
    pub indigenous_adjustment: f64,
    /// Remoteness adjustment (additive fraction).
    pub remoteness_adjustment: f64,
    /// Treatment remoteness adjustment (multiplicative).
    pub treatment_remoteness_adjustment: f64,
    /// Radiotherapy adjustment (additive fraction).
    pub radiotherapy_adjustment: f64,
    /// Dialysis adjustment (additive fraction).
    pub dialysis_adjustment: f64,
    /// Private accommodation deduction for same-day episodes.
    pub private_accommodation_same_day: f64,
    /// Private accommodation deduction per day for overnight episodes.
    pub private_accommodation_overnight: f64,
}

impl Default for AdjustmentFactors {
    fn default() -> Self {
        Self {
            icu_rate: 0.0,
            covid_adjustment: 0.0,
            indigenous_adjustment: 0.0,
            remoteness_adjustment: 0.0,
            treatment_remoteness_adjustment: 0.0,
            radiotherapy_adjustment: 0.0,
            dialysis_adjustment: 0.0,
            private_accommodation_same_day: 0.0,
            private_accommodation_overnight: 0.0,
        }
    }
}

impl From<AdjustmentFactors> for crate::acute::AcuteAdjustmentFactors {
    fn from(f: AdjustmentFactors) -> Self {
        crate::acute::AcuteAdjustmentFactors {
            icu_rate: f.icu_rate,
            covid_adjustment: f.covid_adjustment,
            indigenous_adjustment: f.indigenous_adjustment,
            remoteness_adjustment: f.remoteness_adjustment,
            treatment_remoteness_adjustment: f.treatment_remoteness_adjustment,
            radiotherapy_adjustment: f.radiotherapy_adjustment,
            dialysis_adjustment: f.dialysis_adjustment,
            private_accommodation_same_day: f.private_accommodation_same_day,
            private_accommodation_overnight: f.private_accommodation_overnight,
        }
    }
}

/// The primary output of a single episode calculation.
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct EpisodeOutput {
    /// Error code (0 = ok).
    pub error_code: u8,
    /// Separation category.
    pub separation_category: Option<u8>,
    /// Eligible ICU hours after adjustments.
    pub eligible_icu_hours: f64,
    /// LOS with ICU hours removed.
    pub los_icu_removed: f64,
    /// W01: base weight.
    pub w01: f64,
    /// W02: after paediatric adjustment.
    pub w02: f64,
    /// W03: after patient adjustments.
    pub w03: f64,
    /// W04: after COVID adjustment.
    pub w04: f64,
    /// GWaU: gross weighted activity unit.
    pub gwau: f64,
    /// Private service deduction.
    pub private_service_deduction: f64,
    /// Private accommodation deduction.
    pub private_accommodation_deduction: f64,
    /// NWAU: net weighted activity unit.
    pub nwau: f64,
}

impl EpisodeOutput {
    /// Create a zeroed output for error cases.
    pub fn error(error_code: u8) -> Self {
        Self {
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
            nwau: 0.0,
        }
    }
}

impl From<crate::acute::AcuteEpisodeOutput> for EpisodeOutput {
    fn from(o: crate::acute::AcuteEpisodeOutput) -> Self {
        Self {
            error_code: o.error_code,
            separation_category: o.separation_category.map(|s| s as u8),
            eligible_icu_hours: o.eligible_icu_hours,
            los_icu_removed: o.los_icu_removed,
            w01: o.w01,
            w02: o.w02,
            w03: o.w03,
            w04: o.w04,
            gwau: o.gwau,
            private_service_deduction: o.private_service_deduction,
            private_accommodation_deduction: o.private_accommodation_deduction,
            nwau: o.nwau25,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn calculator_id_support_state() {
        assert!(CalculatorId("acute-2025".into()).is_implemented());
        assert!(!CalculatorId("sub-acute".into()).is_implemented());
        assert!(CalculatorId("sub-acute".into()).is_reserved());
        assert!(!CalculatorId("custom".into()).is_reserved());
    }

    #[test]
    fn pricing_year_suffix() {
        assert_eq!(PricingYear(2025).suffix(), 25);
        assert_eq!(PricingYear(2026).suffix(), 26);
    }

    #[test]
    fn stream_labels() {
        assert_eq!(Stream::Acute.label(), "acute");
        assert_eq!(
            Stream::CommunityMentalHealth.label(),
            "community-mental-health"
        );
    }

    #[test]
    fn episode_output_from_acute() {
        let acute_out = crate::acute::AcuteEpisodeOutput {
            error_code: 0,
            separation_category: Some(crate::acute::SeparationCategory::Inlier),
            eligible_icu_hours: 10.0,
            los_icu_removed: 5.0,
            w01: 1.0,
            w02: 1.2,
            w03: 1.5,
            w04: 1.5,
            gwau: 2.0,
            private_service_deduction: 0.1,
            private_accommodation_deduction: 0.05,
            nwau25: 1.85,
        };
        let out: EpisodeOutput = acute_out.into();
        assert_eq!(out.nwau, 1.85);
        assert_eq!(out.error_code, 0);
    }
}
