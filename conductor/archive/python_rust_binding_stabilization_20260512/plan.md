# Plan: Python Rust Binding Stabilization

## Phase 1: Binding Contract
- [x] Task: Define the Python-to-Rust calculator boundary and fallback policy.
    - [x] Document batch input/output schema and error mapping.
    - [x] Mark validated and experimental calculators explicitly.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Binding Contract' (Protocol in workflow.md)

## Phase 2: Packaging and Tests
- [x] Task: Add cross-platform maturin wheel build and parity tests.
    - [x] Reuse golden fixtures for Python and Rust-backed paths.
    - [x] Keep extension import failures diagnosable.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Packaging and Tests' (Protocol in workflow.md)
