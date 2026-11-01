//! 128-bit deterministic cross-platform invariant verification.
//!
//! Guarantees that numerical pricing calculations produce bit-exact identical
//! outputs across macOS ARM64, Ubuntu x64, Ubuntu ARM64, and Windows.

use super::cpu::evaluate_batch_decimal_exact;
use super::types::EpisodeGpuInput;
use rust_decimal::Decimal;

/// Golden invariant checksum for the 1,000 synthetic test episodes evaluated at 128-bit precision.
pub const GOLDEN_128BIT_INVARIANT_CHECKSUM: u64 = 0xED9A975B0552E7E0;

/// Generate deterministic synthetic fixture episodes covering edge cases:
/// inliers, boundaries, short-stay trimming, long-stay outliers, ICU hours, and co-payment deductions.
pub fn generate_invariant_test_fixtures(count: usize) -> Vec<EpisodeGpuInput> {
    let mut fixtures = Vec::with_capacity(count);
    for i in 0..count {
        let los = ((i % 50) as f32) * 0.5 + 0.25;
        let base_weight = 0.5 + ((i % 20) as f32) * 0.25;
        let inlier_lower = 1.0 + ((i % 5) as f32) * 0.5;
        let inlier_upper = inlier_lower + 5.0 + ((i % 10) as f32);
        let short_stay_per_diem = base_weight / inlier_lower;
        let long_stay_per_diem = (base_weight * 0.6) / (inlier_upper - inlier_lower + 1.0);
        let adjustment_factor = 1.0 + ((i % 4) as f32) * 0.05;
        let private_deduction = if i % 7 == 0 { 0.15 } else { 0.0 };
        let same_day_flag = if i % 13 == 0 { 1 } else { 0 };
        let icu_hours = if i % 6 == 0 { (i % 48) as f32 } else { 0.0 };
        let icu_rate = 0.035;

        fixtures.push(EpisodeGpuInput {
            los,
            icu_hours,
            icu_rate,
            base_weight,
            inlier_lower,
            inlier_upper,
            short_stay_per_diem,
            long_stay_per_diem,
            adjustment_factor,
            private_deduction,
            same_day_flag,
            _pad: 0,
        });
    }
    fixtures
}

/// Compute a 64-bit deterministic hash of the 128-bit decimal results.
pub fn compute_invariant_checksum(results: &[(Decimal, i64)]) -> u64 {
    let mut hasher_state: u64 = 0xCBF29CE484222325; // FNV-1a 64-bit offset basis
    for (nwau_dec, funding_cents) in results {
        // Hash the 16 bytes of the 128-bit decimal representation
        let dec_bytes = nwau_dec.serialize();
        for b in dec_bytes {
            hasher_state ^= b as u64;
            hasher_state = hasher_state.wrapping_mul(0x100000001B3);
        }
        // Hash the 8 bytes of the funding cents
        for b in funding_cents.to_le_bytes() {
            hasher_state ^= b as u64;
            hasher_state = hasher_state.wrapping_mul(0x100000001B3);
        }
    }
    hasher_state
}

/// Verify that 128-bit calculations on this architecture match the golden invariant hash.
pub fn verify_128bit_invariants(count: usize) -> Result<u64, String> {
    let fixtures = generate_invariant_test_fixtures(count);
    let results = evaluate_batch_decimal_exact(&fixtures, 741800);
    let checksum = compute_invariant_checksum(&results);

    // If validating standard 1,000 count, assert against golden hash
    if count == 1000 {
        if checksum != GOLDEN_128BIT_INVARIANT_CHECKSUM {
            return Err(format!(
                "128-bit architecture invariant drift detected! Expected 0x{:016X}, got 0x{:016X}",
                GOLDEN_128BIT_INVARIANT_CHECKSUM, checksum
            ));
        }
    }

    Ok(checksum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_invariant_determinism() {
        let f1 = generate_invariant_test_fixtures(100);
        let r1 = evaluate_batch_decimal_exact(&f1, 741800);
        let c1 = compute_invariant_checksum(&r1);

        let f2 = generate_invariant_test_fixtures(100);
        let r2 = evaluate_batch_decimal_exact(&f2, 741800);
        let c2 = compute_invariant_checksum(&r2);

        assert_eq!(c1, c2, "Invariant checksum must be perfectly deterministic");
        assert_ne!(c1, 0, "Checksum must not be trivial zero");
    }
}
