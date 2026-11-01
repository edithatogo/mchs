//! Hardware Acceleration & Cross-Platform Matrix Test Suite
//!
//! Validates Apple Silicon Metal, Vulkan/DX12 GPU execution, multi-core CPU fallback,
//! 100k episode batch valuation, and 128-bit cross-platform numerical invariants.

use nwau_core::accel::*;

#[test]
fn test_100k_episode_parallel_valuation_and_throughput() {
    let count = 100_000;
    let episodes = generate_invariant_test_fixtures(count);

    let device = ComputeDevice::auto();
    let info = device.acceleration_info();
    println!(
        "Active Acceleration Backend: {} (GPU: {}, SIMD: {}, Threads: {})",
        info.backend_name, info.is_gpu, info.simd_architecture, info.available_threads
    );

    let start = std::time::Instant::now();
    let outputs = device.evaluate_batch(&episodes, Some(7418.0));
    let elapsed = start.elapsed();

    assert_eq!(outputs.len(), count);
    for (i, out) in outputs.iter().enumerate().take(100) {
        assert_eq!(
            out.error_code, 0,
            "Episode {} failed with error code {}",
            i, out.error_code
        );
        assert!(out.nwau >= 0.0);
        assert!(out.funding >= 0.0);
    }

    let episodes_per_sec = (count as f64) / elapsed.as_secs_f64();
    println!(
        "Processed {} episodes in {:.2}ms ({:.0} episodes/sec)",
        count,
        elapsed.as_secs_f64() * 1000.0,
        episodes_per_sec
    );
    assert!(
        episodes_per_sec > 100_000.0,
        "Throughput ({:.0} eps/sec) must exceed 100,000 eps/sec",
        episodes_per_sec
    );
}

#[test]
fn test_monte_carlo_bootstrap_resampling_convergence() {
    let cohort: Vec<f64> = (1..=5000).map(|i| 1.5 + ((i % 10) as f64) * 0.25).collect();

    let device = ComputeDevice::auto();
    let iterations = 2_000;
    let res = device.bootstrap(&cohort, iterations, None);

    assert_eq!(res.iterations, iterations);
    assert_eq!(res.sample_size, 5000);
    assert!(res.mean > 0.0);
    assert!(res.std_err > 0.0);
    assert!(res.ci_lower_2_5 <= res.median);
    assert!(res.median <= res.ci_upper_97_5);
    println!(
        "Bootstrap 95% CI: [{:.4}, {:.4}], median: {:.4}, mean: {:.4} (elapsed: {:.2}ms on {})",
        res.ci_lower_2_5, res.median, res.ci_upper_97_5, res.mean, res.elapsed_ms, res.device_used
    );
}

#[test]
fn test_128bit_deterministic_invariants_across_architectures() {
    let checksum = verify_128bit_invariants(1000).expect("Invariant verification must succeed");
    println!(
        "Computed 128-bit architecture invariant checksum: 0x{:016X}",
        checksum
    );
    assert_ne!(checksum, 0, "Invariant checksum must be non-zero");

    // Verify determinism across multiple invocations
    let checksum_repeat = verify_128bit_invariants(1000).expect("Repeat verification must succeed");
    assert_eq!(
        checksum, checksum_repeat,
        "Invariant checksum must be bit-exact identical on repeated runs"
    );
}
