# Plan: Rust Core Continuation

## Phase 1: Rust Core Baseline and Promotion Matrix

- [x] Task: Audit current Rust and binding state.
    - [x] Inspect `rust/crates/nwau-core`, `rust/crates/nwau-py`, and `rust/crates/nwau-c-abi`.
    - [x] Inspect Python bridge and opt-in runtime behavior.
    - [x] Inspect CLI/file, canonical contract, support-status, and release evidence docs.
- [x] Task: Build a stream promotion matrix.
    - [x] List acute, ED, admitted mental health, community mental health, subacute, outpatient, adjustment, HAC, AHR, state/local pricing, and classification-adjacent surfaces.
    - [x] Assign each stream a state: blocked, documentation-only, canary, opt-in, release-candidate, GA, or not-ready.
    - [x] Name required fixtures, source evidence, validation commands, and owner for each stream.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Rust Core Baseline and Promotion Matrix' (Protocol in workflow.md)
    - Evidence: `docs/roadmaps/rust-core-promotion-matrix.md`, `tests/test_rust_core_ga_roadmap.py`.

## Phase 2: Red Phase Parity Gates

- [x] Task: Select the next Rust stream or bounded slice for promotion.
    - [x] Prefer a stream with available source fixtures and low ambiguity.
    - [x] Record why higher-risk streams are deferred if applicable.
- [x] Task: Write failing Rust and Python parity tests.
    - [x] Add Rust unit or integration tests for kernel output.
    - [x] Add Python binding tests for opt-in behavior and fallback behavior.
    - [x] Add CLI/file or C ABI tests when the promoted contract crosses those surfaces.
- [x] Task: Confirm the tests fail for the expected missing implementation or unsupported-state reason.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Red Phase Parity Gates' (Protocol in workflow.md)
    - Evidence: `rust/crates/nwau-core/tests/phase2_promotion_gate.rs`, `tests/test_rust_parity/test_phase2_promotion_gate.py`, `docs/release-evidence-rust-continuation.md`.

## Phase 3: Rust Implementation and Binding Promotion

- [x] Task: Implement the selected Rust kernel behavior.
    - [x] Use canonical input/output schemas and provenance diagnostics.
    - [x] Consume validated parameter or reference-data bundles.
    - [x] Avoid duplicating formulas in adapters.
- [x] Task: Update Python binding behavior.
    - [x] Keep Python fallback behavior stable.
    - [x] Enable Rust opt-in or default behavior only for streams with passing parity.
    - [x] Emit diagnostics when Rust is unavailable or unsupported for a stream.
- [x] Task: Update CLI/file and C ABI surfaces as needed.
    - [x] Ensure promoted surfaces call shared Rust logic.
    - [x] Preserve error and diagnostic contract compatibility.
- [x] Task: Run targeted Rust, Python, and contract tests until green.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Rust Implementation and Binding Promotion' (Protocol in workflow.md)
    - Evidence: `rust/crates/nwau-core/src/kernels.rs`, `rust/crates/nwau-core/tests/phase2_promotion_gate.rs`, `tests/test_rust_parity/test_phase2_promotion_gate.py`, `tests/test_rust_parity/test_python_parity.py`.

## Phase 4: Support Status, Docs, and Release Evidence

- [x] Task: Update support-status documentation and README claims.
    - [x] Record stream state and validation evidence.
    - [x] Distinguish Python-validated, Rust-canary, Rust-opt-in, release-candidate, and GA behavior.
    - [x] Keep deferred adapter claims conservative.
- [x] Task: Update release evidence.
    - [x] Record test commands and outputs.
    - [x] Record fixture provenance and coverage gaps.
    - [x] Record package or registry publication blockers separately from implementation readiness.
- [x] Task: Run final validation.
    - [x] Run Rust formatting, linting, and tests.
    - [x] Run targeted Python parity tests.
    - [x] Run stub detector to ensure Rust progress did not create new scaffold completion claims.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Support Status, Docs, and Release Evidence' (Protocol in workflow.md)
    - Evidence: `docs/roadmaps/rust-core-continuation.md`, `docs/roadmaps/rust-core-promotion-matrix.md`, `docs/release-evidence-rust-continuation.md`, `README.md`, final validation commands recorded in this task handoff.
