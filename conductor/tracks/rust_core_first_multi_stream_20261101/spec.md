# Specification: Rust-Core First Multi-Stream Engine

## Objective
Promote `nwau-core` from an Acute-canary implementation to the sole canonical calculation engine across all national hospital funding streams:
1. Admitted Acute (AR-DRG 12.0)
2. Emergency Department (AECC and UDG)
3. Admitted Mental Health (AMHCC)
4. Non-Admitted Outpatients (Tier 2 Clinics)
5. Subacute and Non-Acute Care (AN-SNAP v5.0)

## Requirements
1. **Canonical Formula Doctrine:**
   - Every formula rule, parameter model, boundary test, and adjustment calculation must live in `rust/crates/nwau-core/src/`.
   - External languages (Python, R, Julia) must never re-implement or fork formula logic.
2. **Exact Fixed-Point Arithmetic:**
   - All arithmetic must use `rust_decimal::Decimal` (128-bit fixed point) with deterministic rounding modes matching IHACPA specifications.
   - Accumulator drift across 100,000+ episode batches must remain strictly 0.00000000.
3. **Stream Modularization:**
   - Implement `rust/crates/nwau-core/src/ed.rs`
   - Implement `rust/crates/nwau-core/src/mental_health.rs`
   - Implement `rust/crates/nwau-core/src/outpatients.rs`
   - Implement `rust/crates/nwau-core/src/subacute.rs`
4. **Zero-Overhead Memory Footprint:**
   - Peak RSS under 100 MB when processing 100,000 episodes.
   - Streaming Arrow IPC RecordBatch evaluation without full-batch materialization.
