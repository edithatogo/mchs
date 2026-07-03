//! Core acute 2025 Rust kernel.
//!
//! The formula layer is intentionally pure: reference row resolution, input
//! validation, and runtime adapters stay outside this crate's calculation
//! functions.

pub mod acute;
pub mod cli;
pub mod diagnostics;
pub mod file_io;
pub mod kernels;
pub mod manifest;
pub mod provenance;
pub mod registries;
pub mod types;

pub use acute::{
    acute_error_code, calculate_acute_2025, AcuteAdjustmentFactors, AcuteEpisodeInput,
    AcuteEpisodeOutput, AcuteReferenceRow, AcuteValidationState, SeparationCategory,
};

pub use cli::Cli;
pub use diagnostics::{Diagnostic, DiagnosticCollector, DiagnosticLevel, NwauError};
#[cfg(feature = "arrow-parquet")]
pub use file_io::{outputs_to_record_batch, write_output_parquet};
pub use file_io::{read_episode_csv, read_reference_csv, write_output_csv};
pub use kernels::{Acute2025Kernel, Kernel, KernelRegistry, SubAcuteKernel};
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
