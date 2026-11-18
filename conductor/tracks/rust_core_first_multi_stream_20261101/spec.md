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

## Serde suitability across NWAU native contracts (18 November 2026)

`rust/crates/nwau-core/Cargo.toml` already declares `serde` derive, `serde_json`, `csv`, `chrono`/`uuid` Serde features and `rust_decimal` with Serde; optional Arrow/Parquet and GPU/bytemuck have distinct responsibilities. The canonical calculation engine must retain **exact decimal** arithmetic and source version, whereas Serde handles only representation at JSON/CSV metadata boundaries. No dependency can be replaced solely with Serde.

Next integration-owner work, after frozen multi-stream input/output fixtures and without reopening completed historical tracks:
- [ ] Inventory stable NWAU source manifest, CLI/wire DTOs and public C/Python binding projections. Prefer existing Serde-typed structures for stable JSON exchange; preserve extension/unknown fields where required.
- [ ] Verify exact decimal scale, rounding and missingness across JSON, CSV and Arrow/Parquet; never convert Decimal to f64 silently or serialize secrets/patient data in receipts.
- [ ] Preserve columnar I/O, algorithms, pricing-year and classification-source evidence and independent published reference oracles. No Serde roundtrip is a clinical or funding-formula validation.
- [ ] Admit a replacement only with identified handwritten duplicate codec, measurable code reduction, full published source provenance and exact-head locked Cargo, cross-language, GPU-optional and numerical acceptance. Otherwise record no-go; this section itself changes no implementation or release state.
