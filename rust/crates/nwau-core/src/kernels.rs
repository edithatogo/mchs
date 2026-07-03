//! Formula kernel trait and implementations.
//!
//! A `Kernel` maps an episode input row and a reference row to an output.
//! Each calculator version implements this trait.

use crate::diagnostics::{Diagnostic, DiagnosticLevel};
use crate::types::{AdjustmentFactors, EpisodeOutput, EpisodeRow, ReferenceRow};

/// The formula kernel trait. Every calculator version provides an
/// implementation that maps (episode, reference, adjustments) → output.
pub trait Kernel {
    /// A human-readable label for this kernel version.
    fn label(&self) -> &'static str;

    /// Run the calculation for a single episode.
    fn calculate(
        &self,
        episode: &EpisodeRow,
        reference: &ReferenceRow,
        adjustments: &AdjustmentFactors,
    ) -> EpisodeOutput;

    /// Return the well-known calculator ID for this kernel.
    fn calculator_id(&self) -> crate::types::CalculatorId {
        crate::types::CalculatorId(self.label().to_string())
    }
}

/// The acute 2025 kernel implementation.
#[derive(Debug, Clone, Copy)]
pub struct Acute2025Kernel;

impl Acute2025Kernel {
    /// Construct a new acute 2025 kernel.
    pub fn new() -> Self {
        Self
    }
}

impl Default for Acute2025Kernel {
    fn default() -> Self {
        Self::new()
    }
}

impl Kernel for Acute2025Kernel {
    fn label(&self) -> &'static str {
        "acute-2025"
    }

    fn calculate(
        &self,
        episode: &EpisodeRow,
        reference: &ReferenceRow,
        adjustments: &AdjustmentFactors,
    ) -> EpisodeOutput {
        let validation = crate::acute::AcuteValidationState::valid();
        let input = crate::acute::AcuteEpisodeInput {
            drg: &episode.drg,
            los: episode.los,
            icu_hours: episode.icu_hours,
            icu_other: episode.icu_other,
            pat_sameday_flag: episode.flags.same_day,
            pat_private_flag: episode.flags.private_patient,
            pat_covid_flag: episode.flags.covid,
            eligible_paed_flag: episode.flags.eligible_paediatric,
            validation,
        };
        let acute_ref = reference.to_acute_ref();
        let acute_adj: crate::acute::AcuteAdjustmentFactors = (*adjustments).into();
        let acute_out = crate::acute::calculate_acute_2025(input, acute_ref, acute_adj);
        acute_out.into()
    }
}

/// The only DRG accepted by the bounded sub-acute canary path.
pub const SUBACUTE_CANARY_DRG: &str = "SUBACUTE-CANARY";

/// Error code used when sub-acute input is outside the canary boundary.
pub const SUBACUTE_UNSUPPORTED_ERROR_CODE: u8 = 90;

/// The sub-acute kernel boundary classification.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SubAcuteBoundary {
    /// Synthetic canary input that exercises a bounded sub-acute calculation.
    Canary,
    /// Real or incomplete sub-acute input that must not be promoted yet.
    Unsupported,
}

/// A conservative sub-acute kernel with an explicit synthetic canary boundary.
#[derive(Debug, Clone, Copy)]
pub struct SubAcuteKernel;

impl SubAcuteKernel {
    /// Construct a new sub-acute kernel.
    pub fn new() -> Self {
        Self
    }

    /// Classify whether the row is inside the bounded canary slice.
    pub fn boundary(
        &self,
        episode: &EpisodeRow,
        reference: &ReferenceRow,
        adjustments: &AdjustmentFactors,
    ) -> SubAcuteBoundary {
        if is_subacute_canary(episode, reference, adjustments) {
            SubAcuteBoundary::Canary
        } else {
            SubAcuteBoundary::Unsupported
        }
    }

    /// Return a diagnostic describing the sub-acute promotion boundary.
    pub fn diagnostic(
        &self,
        episode: &EpisodeRow,
        reference: &ReferenceRow,
        adjustments: &AdjustmentFactors,
    ) -> Diagnostic {
        let message = match self.boundary(episode, reference, adjustments) {
            SubAcuteBoundary::Canary => {
                "sub-acute canary calculation is bounded to synthetic fixture rows"
            }
            SubAcuteBoundary::Unsupported => {
                "sub-acute kernel is not promoted for non-canary activity"
            }
        };
        let level = match self.boundary(episode, reference, adjustments) {
            SubAcuteBoundary::Canary => DiagnosticLevel::Warning,
            SubAcuteBoundary::Unsupported => DiagnosticLevel::Error,
        };

        Diagnostic {
            level,
            message: message.into(),
            drg: Some(episode.drg.clone()),
            episode_id: episode.episode_id.clone(),
        }
    }
}

impl Default for SubAcuteKernel {
    fn default() -> Self {
        Self::new()
    }
}

impl Kernel for SubAcuteKernel {
    fn label(&self) -> &'static str {
        "sub-acute"
    }

    fn calculate(
        &self,
        episode: &EpisodeRow,
        reference: &ReferenceRow,
        adjustments: &AdjustmentFactors,
    ) -> EpisodeOutput {
        if !matches!(
            self.boundary(episode, reference, adjustments),
            SubAcuteBoundary::Canary
        ) {
            return EpisodeOutput::error(SUBACUTE_UNSUPPORTED_ERROR_CODE);
        }

        EpisodeOutput {
            error_code: 0,
            separation_category: Some(3),
            eligible_icu_hours: 0.0,
            los_icu_removed: episode.los,
            w01: reference.inlier_weight,
            w02: reference.inlier_weight,
            w03: reference.inlier_weight,
            w04: reference.inlier_weight,
            gwau: reference.inlier_weight,
            private_service_deduction: 0.0,
            private_accommodation_deduction: 0.0,
            nwau: reference.inlier_weight,
        }
    }
}

fn is_subacute_canary(
    episode: &EpisodeRow,
    reference: &ReferenceRow,
    adjustments: &AdjustmentFactors,
) -> bool {
    episode.drg == SUBACUTE_CANARY_DRG
        && reference.drg == SUBACUTE_CANARY_DRG
        && episode.los.is_finite()
        && episode.los > 0.0
        && episode.los >= reference.inlier_lower_bound
        && episode.los <= reference.inlier_upper_bound
        && episode.icu_hours == 0.0
        && episode.icu_other == 0.0
        && episode.flags == crate::types::EpisodeFlags::default()
        && reference.inlier_lower_bound.is_finite()
        && reference.inlier_upper_bound.is_finite()
        && reference.inlier_lower_bound > 0.0
        && reference.inlier_upper_bound >= reference.inlier_lower_bound
        && reference.inlier_weight.is_finite()
        && reference.inlier_weight >= 0.0
        && *adjustments == AdjustmentFactors::default()
}

/// A registry mapping calculator labels to boxed kernel implementations.
pub struct KernelRegistry {
    kernels: Vec<Box<dyn Kernel + Send + Sync>>,
}

impl KernelRegistry {
    /// Create a new empty registry.
    pub fn new() -> Self {
        Self {
            kernels: Vec::new(),
        }
    }

    /// Register a kernel.
    pub fn register(&mut self, kernel: Box<dyn Kernel + Send + Sync>) {
        self.kernels.push(kernel);
    }

    /// Look up a kernel by label.
    pub fn get(&self, label: &str) -> Option<&dyn Kernel> {
        self.kernels
            .iter()
            .find(|k| k.label() == label)
            .map(|b| &**b as &dyn Kernel)
    }

    /// Return all registered labels.
    pub fn labels(&self) -> Vec<&'static str> {
        self.kernels.iter().map(|k| k.label()).collect()
    }

    /// Register the default built-in kernels.
    pub fn with_defaults(mut self) -> Self {
        self.register(Box::new(Acute2025Kernel::new()));
        self.register(Box::new(SubAcuteKernel::new()));
        self
    }
}

impl Default for KernelRegistry {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::types::EpisodeFlags;

    #[test]
    fn acute_kernel_label() {
        let kernel = Acute2025Kernel::new();
        assert_eq!(kernel.label(), "acute-2025");
    }

    #[test]
    fn acute_kernel_calculates_nwau() {
        let kernel = Acute2025Kernel::new();
        let episode = EpisodeRow {
            drg: "801A".into(),
            los: 10.0,
            icu_hours: 0.0,
            icu_other: 0.0,
            flags: EpisodeFlags::default(),
            episode_id: None,
        };
        let reference = ReferenceRow {
            drg: "801A".into(),
            inlier_lower_bound: 7.0,
            inlier_upper_bound: 72.0,
            paediatric_multiplier: 1.35,
            same_day_list_flag: false,
            bundled_icu_flag: false,
            same_day_base_weight: 0.9527,
            same_day_per_diem: 1.1849,
            inlier_weight: 9.2472,
            long_stay_per_diem: 0.26,
            private_service_adjustment: 0.0,
        };
        let adjustments = AdjustmentFactors::default();
        let output = kernel.calculate(&episode, &reference, &adjustments);
        assert_eq!(output.error_code, 0);
        assert!((output.nwau - 9.2472).abs() < 1e-4);
    }

    #[test]
    fn registry_lookup() {
        let registry = KernelRegistry::new().with_defaults();
        assert!(registry.get("acute-2025").is_some());
        assert!(registry.get("sub-acute").is_some());
        assert!(registry.get("unknown").is_none());
        let labels = registry.labels();
        assert!(labels.contains(&"acute-2025"));
    }
}
