# Implementation Plan: Polyglot Wrappers

## Phase 1: Python Inversion & pyo3-polars Plugin
- [ ] Task: Implement `#[polars_expr]` functions in `rust/crates/nwau-py/src/lib.rs` for all 5 streams.
- [ ] Task: Refactor `nwau_py/calculators/` to invoke Rust expressions by default.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Python Inversion' (Protocol in workflow.md)

## Phase 2: Julia In-Process Binding
- [ ] Task: Implement Julia `ccall` wrapper in `julia-binding/src/NationalWeightedActivityUnitWrapper.jl`.
- [ ] Task: Implement memory-mapped Arrow batch valuation for Julia DataFrames.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Julia Binding' (Protocol in workflow.md)

## Phase 3: R In-Process Binding & Cross-Language Parity
- [ ] Task: Wire `r-binding/src/` to call `libnwau_c_abi`.
- [ ] Task: Run multi-language differential parity test suite across Rust, Python, R, and Julia.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: R Binding & Parity' (Protocol in workflow.md)
