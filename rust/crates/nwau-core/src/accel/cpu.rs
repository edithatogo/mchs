//! Multi-threaded CPU execution engine with Rayon parallelization and SIMD-friendly vectorization.

use super::types::{BootstrapResult, EpisodeGpuInput, EpisodeGpuOutput};
use rayon::prelude::*;
use rust_decimal::Decimal;
use std::time::Instant;

/// National Efficient Price (NEP) reference constant in AUD (default $7,418.00).
pub const DEFAULT_NEP: f32 = 7418.0;

/// Evaluate a slice of episodes using multi-threaded Rayon execution.
pub fn evaluate_batch_cpu(episodes: &[EpisodeGpuInput], nep: f32) -> Vec<EpisodeGpuOutput> {
    episodes
        .par_iter()
        .map(|ep| evaluate_single_episode(ep, nep))
        .collect()
}

/// Compute a single episode valuation kernel.
#[inline(always)]
pub fn evaluate_single_episode(ep: &EpisodeGpuInput, nep: f32) -> EpisodeGpuOutput {
    if ep.base_weight <= 0.0 || ep.los < 0.0 {
        return EpisodeGpuOutput {
            nwau: 0.0,
            funding: 0.0,
            error_code: 1, // Invalid input code
            _pad: 0,
        };
    }

    let unadjusted_weight = if ep.same_day_flag != 0 {
        ep.base_weight
    } else if ep.los < ep.inlier_lower {
        ep.los * ep.short_stay_per_diem
    } else if ep.los <= ep.inlier_upper {
        ep.base_weight
    } else {
        ep.base_weight + (ep.los - ep.inlier_upper) * ep.long_stay_per_diem
    };

    let icu_weight = if ep.icu_hours > 0.0 && ep.icu_rate > 0.0 {
        ep.icu_hours * ep.icu_rate
    } else {
        0.0
    };

    let gross_nwau = (unadjusted_weight + icu_weight) * ep.adjustment_factor;
    let net_nwau = (gross_nwau - ep.private_deduction).max(0.0);
    let funding = net_nwau * nep;

    EpisodeGpuOutput {
        nwau: net_nwau,
        funding,
        error_code: 0,
        _pad: 0,
    }
}

/// Perform Monte Carlo bootstrap resampling over a population of NWAU values using CPU multi-threading.
pub fn bootstrap_cpu(
    values: &[f64],
    iterations: usize,
    sample_size: Option<usize>,
) -> BootstrapResult {
    let start = Instant::now();
    let n = values.len();
    assert!(n > 0, "Cannot bootstrap an empty slice of values");
    let k = sample_size.unwrap_or(n);

    // Parallel bootstrap iterations using XorShift64 PRNG per thread for maximum throughput
    let mut bootstrap_means: Vec<f64> = (0..iterations)
        .into_par_iter()
        .map(|iter_idx| {
            // Seed per iteration using splitmix64
            let mut state = (iter_idx as u64 + 1).wrapping_mul(0x9E3779B97F4A7C15);
            let mut sum = 0.0;
            for _ in 0..k {
                // Fast XorShift64
                state ^= state << 13;
                state ^= state >> 7;
                state ^= state << 17;
                let sample_idx = (state as usize) % n;
                sum += values[sample_idx];
            }
            sum / (k as f64)
        })
        .collect();

    // Sort to obtain empirical percentiles
    bootstrap_means.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));

    let count = bootstrap_means.len();
    let mean: f64 = bootstrap_means.iter().sum::<f64>() / (count as f64);
    let variance: f64 = bootstrap_means
        .iter()
        .map(|x| (x - mean).powi(2))
        .sum::<f64>()
        / (count as f64);
    let std_err = variance.sqrt();

    let idx_2_5 = ((count as f64) * 0.025).round() as usize;
    let idx_50 = count / 2;
    let idx_97_5 = ((count as f64) * 0.975).min((count - 1) as f64).round() as usize;

    let elapsed = start.elapsed().as_secs_f64() * 1000.0;

    BootstrapResult {
        mean,
        std_err,
        ci_lower_2_5: bootstrap_means[idx_2_5.min(count - 1)],
        median: bootstrap_means[idx_50.min(count - 1)],
        ci_upper_97_5: bootstrap_means[idx_97_5.min(count - 1)],
        iterations,
        sample_size: k,
        device_used: "Rayon Multi-Core CPU".to_string(),
        elapsed_ms: elapsed,
    }
}

/// Deterministic 128-bit decimal batch valuation guaranteeing bit-exact parity across all CPU platforms.
pub fn evaluate_batch_decimal_exact(
    episodes: &[EpisodeGpuInput],
    nep_cents: i64,
) -> Vec<(Decimal, i64)> {
    episodes
        .par_iter()
        .map(|ep| {
            let f_to_d = |v: f32| Decimal::from_f32_retain(v).unwrap_or(Decimal::ZERO);
            let los = f_to_d(ep.los);
            let base_weight = f_to_d(ep.base_weight);
            let inlier_lower = f_to_d(ep.inlier_lower);
            let inlier_upper = f_to_d(ep.inlier_upper);
            let short_stay_per_diem = f_to_d(ep.short_stay_per_diem);
            let long_stay_per_diem = f_to_d(ep.long_stay_per_diem);
            let adjustment_factor = f_to_d(ep.adjustment_factor);
            let private_deduction = f_to_d(ep.private_deduction);

            let unadjusted_weight = if ep.same_day_flag != 0 {
                base_weight
            } else if los < inlier_lower {
                los * short_stay_per_diem
            } else if los <= inlier_upper {
                base_weight
            } else {
                base_weight + (los - inlier_upper) * long_stay_per_diem
            };

            let gross = unadjusted_weight * adjustment_factor;
            let net = if gross > private_deduction {
                gross - private_deduction
            } else {
                Decimal::ZERO
            };

            let nep_dec = Decimal::from(nep_cents) / Decimal::from(100);
            let funding_cents = (net * nep_dec * Decimal::from(100)).round();
            let funding_i64 = funding_cents.to_string().parse::<i64>().unwrap_or(0);

            (net, funding_i64)
        })
        .collect()
}
