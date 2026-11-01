//! Types for hardware-accelerated batch valuation and Monte Carlo bootstrap resampling.

use bytemuck::{Pod, Zeroable};
use serde::{Deserialize, Serialize};

/// High-density C-compatible episode representation for SIMD and GPU storage buffers.
#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq, Pod, Zeroable, Serialize, Deserialize)]
pub struct EpisodeGpuInput {
    /// Patient length of stay in fractional or whole days.
    pub los: f32,
    /// ICU hours spent in eligible intensive care.
    pub icu_hours: f32,
    /// ICU weight per hour for eligible ICU stays.
    pub icu_rate: f32,
    /// Base inlier price weight.
    pub base_weight: f32,
    /// Lower inlier length-of-stay threshold.
    pub inlier_lower: f32,
    /// Upper inlier length-of-stay threshold (long-stay outlier cutoff).
    pub inlier_upper: f32,
    /// Short-stay per diem multiplier.
    pub short_stay_per_diem: f32,
    /// Long-stay per diem multiplier.
    pub long_stay_per_diem: f32,
    /// Combined co-payment/adjustment factor (indigenous, remoteness, etc.).
    pub adjustment_factor: f32,
    /// Private patient service/accommodation deduction.
    pub private_deduction: f32,
    /// Same-day status flag (1 = same day, 0 = overnight).
    pub same_day_flag: u32,
    /// 32-bit alignment padding for standard WGSL uniform alignment.
    pub _pad: u32,
}

impl Default for EpisodeGpuInput {
    fn default() -> Self {
        Self {
            los: 1.0,
            icu_hours: 0.0,
            icu_rate: 0.0,
            base_weight: 1.0,
            inlier_lower: 1.0,
            inlier_upper: 10.0,
            short_stay_per_diem: 0.5,
            long_stay_per_diem: 0.1,
            adjustment_factor: 1.0,
            private_deduction: 0.0,
            same_day_flag: 0,
            _pad: 0,
        }
    }
}

/// High-density C-compatible output representation populated by GPU compute shaders or CPU SIMD.
#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq, Pod, Zeroable, Serialize, Deserialize)]
pub struct EpisodeGpuOutput {
    /// Resulting National Weighted Activity Unit (NWAU).
    pub nwau: f32,
    /// Total calculated funding in AUD based on NEP.
    pub funding: f32,
    /// Execution error code (0 = success).
    pub error_code: u32,
    /// 32-bit alignment padding.
    pub _pad: u32,
}

impl Default for EpisodeGpuOutput {
    fn default() -> Self {
        Self {
            nwau: 0.0,
            funding: 0.0,
            error_code: 0,
            _pad: 0,
        }
    }
}

/// Statistics and empirical confidence intervals resulting from Monte Carlo bootstrap resampling.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BootstrapResult {
    /// Sample mean of total NWAU or metric across bootstrap iterations.
    pub mean: f64,
    /// Standard error (standard deviation of the bootstrap distribution).
    pub std_err: f64,
    /// Empirical 2.5% percentile (lower bound of 95% confidence interval).
    pub ci_lower_2_5: f64,
    /// Median (50th percentile) of the bootstrap distribution.
    pub median: f64,
    /// Empirical 97.5% percentile (upper bound of 95% confidence interval).
    pub ci_upper_97_5: f64,
    /// Number of Monte Carlo resample iterations performed.
    pub iterations: usize,
    /// Size of the original episode cohort.
    pub sample_size: usize,
    /// The compute device / execution backend used.
    pub device_used: String,
    /// Elapsed computation time in milliseconds.
    pub elapsed_ms: f64,
}

/// Diagnostic metadata identifying the active hardware acceleration platform.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccelerationInfo {
    /// Name of the active backend ("Apple Silicon Metal", "Rayon Multi-Core CPU", "Vulkan", "DirectX 12").
    pub backend_name: String,
    /// Whether hardware acceleration is running via native GPU shaders.
    pub is_gpu: bool,
    /// CPU SIMD architecture detected (e.g., "ARM NEON", "x86_64 AVX2", "Portable Fallback").
    pub simd_architecture: String,
    /// Number of available CPU physical/logical threads.
    pub available_threads: usize,
    /// Device adapter description if GPU initialized.
    pub device_description: Option<String>,
}
