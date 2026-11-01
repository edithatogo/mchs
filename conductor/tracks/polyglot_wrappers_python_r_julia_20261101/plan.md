# Implementation Plan: Polyglot Wrappers

## Phase 1: Python Inversion & pyo3-polars Plugin [checkpoint: fe1bbcf]
- [x] Task: Implement `#[polars_expr]` functions in `rust/crates/nwau-py/src/lib.rs` for all 5 streams. a68cee6
- [x] Task: Refactor `nwau_py/calculators/` to invoke Rust expressions by default. 4e5cc79
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Python Inversion' (Protocol in workflow.md) fe1bbcf

## Phase 2: Julia In-Process Binding [checkpoint: 6298a26]
- [x] Task: Implement Julia `ccall` wrapper in `julia-binding/src/NationalWeightedActivityUnitWrapper.jl`. 36a21c0
- [x] Task: Implement memory-mapped Arrow batch valuation for Julia DataFrames. 6974cc6
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Julia Binding' (Protocol in workflow.md) 6298a26

## Phase 3: R In-Process Binding & Cross-Language Parity [checkpoint: ea269a4]
- [x] Task: Wire `r-binding/src/` to call `libnwau_c_abi`. fde1c78
- [x] Task: Run multi-language differential parity test suite across Rust, Python, R, and Julia. 6c14224
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: R Binding & Parity' (Protocol in workflow.md) ea269a4
