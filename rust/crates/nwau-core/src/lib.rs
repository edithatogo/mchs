//! Core acute 2025 Rust kernel.
//!
//! The formula layer is intentionally pure: reference row resolution, input
//! validation, and runtime adapters stay outside this crate's calculation
//! functions.

pub mod acute;
pub mod cli;
pub mod diagnostics;
pub mod ed;
pub mod file_io;
pub mod kernels;
pub mod manifest;
pub mod mental_health;
pub mod outpatients;
pub mod provenance;
pub mod registries;
pub mod subacute;
pub mod types;

pub use acute::{
    acute_error_code, calculate_acute_2025, calculate_acute_2026, calculate_acute_decimal,
    AcuteAdjustmentFactors, AcuteAdjustmentFactorsDecimal, AcuteEpisodeInput,
    AcuteEpisodeInputDecimal, AcuteEpisodeOutput, AcuteEpisodeOutputDecimal, AcuteReferenceRow,
    AcuteReferenceRowDecimal, AcuteValidationState, SeparationCategory,
};

pub use ed::{
    calculate_ed, calculate_ed_decimal, EdAdjustmentFactors, EdAdjustmentFactorsDecimal,
    EdClassificationOption, EdEligibilityOption, EdEpisodeInput, EdEpisodeInputDecimal,
    EdEpisodeOutput, EdEpisodeOutputDecimal, EdReferenceRow, EdReferenceRowDecimal,
};

pub use mental_health::{
    calculate_mh, calculate_mh_decimal, MhAdjustmentFactors, MhAdjustmentFactorsDecimal,
    MhAdmittedReferenceRow, MhAdmittedReferenceRowDecimal, MhCommunityReferenceRow,
    MhCommunityReferenceRowDecimal, MhEpisodeInput, MhEpisodeInputDecimal, MhEpisodeOutput,
    MhEpisodeOutputDecimal, MhPpsaOption, MhSeparationCategory, MhSubstream,
};

pub use outpatients::{
    calculate_outpatients, calculate_outpatients_decimal, is_multiprovider_exempt_clinic,
    OutpatientAdjustmentFactors, OutpatientAdjustmentFactorsDecimal, OutpatientDataType,
    OutpatientEpisodeInput, OutpatientEpisodeInputDecimal, OutpatientEpisodeOutput,
    OutpatientEpisodeOutputDecimal, OutpatientReferenceRow, OutpatientReferenceRowDecimal,
};

pub use subacute::{
    calculate_subacute, calculate_subacute_decimal, is_allowable_paediatric_ansnap,
    validate_subacute_episode, SubacuteAdjustmentFactors, SubacuteAdjustmentFactorsDecimal,
    SubacuteEpisodeInput, SubacuteEpisodeInputDecimal, SubacuteEpisodeOutput,
    SubacuteEpisodeOutputDecimal, SubacutePpsaOption, SubacuteReferenceRow,
    SubacuteReferenceRowDecimal, SubacuteSeparationCategory,
};

pub use cli::Cli;
pub use diagnostics::{Diagnostic, DiagnosticCollector, DiagnosticLevel, NwauError};
#[cfg(feature = "arrow-parquet")]
pub use file_io::{outputs_to_record_batch, write_output_parquet};
pub use file_io::{read_episode_csv, read_reference_csv, write_output_csv};
pub use kernels::{Acute2025Kernel, Acute2026Kernel, Kernel, KernelRegistry, SubAcuteKernel};
pub use manifest::Manifest;
pub use provenance::Provenance;
pub use registries::{DrgEntry, DrgRegistry, SeparationModeEntry, SeparationModeRegistry};
pub use types::{
    AdjustmentFactors, CalculatorId, EpisodeFlags, EpisodeOutput, EpisodeRow, PricingYear,
    ReferenceRow, Stream,
};

/// Return the kernel label used by the acute 2025 proof of concept.
pub fn kernel_label() -> &'static str {
    "acute 2025"
}

/// Return the kernel label used by the acute 2026 NEP26 engine.
pub fn kernel_label_2026() -> &'static str {
    "acute 2026"
}
