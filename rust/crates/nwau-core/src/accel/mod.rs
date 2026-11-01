//! Cross-platform hardware acceleration and high-throughput compute kernels.
//!
//! Provides native Metal shader compute on Apple Silicon ARM64, Vulkan on Linux,
//! DirectX 12 on Windows, alongside multi-threaded Rayon CPU execution and
//! bit-exact 128-bit decimal invariant validation.

pub mod cpu;
pub mod device;
#[cfg(feature = "hardware-accel")]
pub mod gpu;
pub mod invariants;
pub mod types;

pub use cpu::{bootstrap_cpu, evaluate_batch_cpu, evaluate_batch_decimal_exact, DEFAULT_NEP};
pub use device::ComputeDevice;
pub use invariants::{
    compute_invariant_checksum, generate_invariant_test_fixtures, verify_128bit_invariants,
    GOLDEN_128BIT_INVARIANT_CHECKSUM,
};
pub use types::{AccelerationInfo, BootstrapResult, EpisodeGpuInput, EpisodeGpuOutput};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cpu_batch_evaluation() {
        let episodes = generate_invariant_test_fixtures(100);
        let outputs = evaluate_batch_cpu(&episodes, DEFAULT_NEP);
        assert_eq!(outputs.len(), 100);
        for out in outputs {
            assert_eq!(out.error_code, 0);
            assert!(out.nwau >= 0.0);
            assert!(out.funding >= 0.0);
        }
    }

    #[test]
    fn test_cpu_bootstrap_distribution() {
        let values: Vec<f64> = (1..=1000).map(|v| v as f64).collect();
        let res = bootstrap_cpu(&values, 200, None);
        assert_eq!(res.iterations, 200);
        assert_eq!(res.sample_size, 1000);
        assert!((res.mean - 500.5).abs() < 25.0);
        assert!(res.ci_lower_2_5 < res.median);
        assert!(res.median < res.ci_upper_97_5);
    }

    #[test]
    fn test_device_auto_selection() {
        let device = ComputeDevice::auto();
        let info = device.acceleration_info();
        assert!(!info.backend_name.is_empty());
        assert!(!info.simd_architecture.is_empty());

        let episodes = generate_invariant_test_fixtures(50);
        let outputs = device.evaluate_batch(&episodes, None);
        assert_eq!(outputs.len(), 50);
    }
}
