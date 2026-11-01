# Implementation Plan: Julia Monorepo Consolidation

## Phase 1: Canonical Source Sync & Architecture
- [ ] Task: Audit parity between `julia-binding/` and GitHub `NationalWeightedActivityUnitWrapper.jl`.
- [ ] Task: Document the standalone registry sync pattern (`git subtree` or automated dispatch).
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Canonical Source Sync' (Protocol in workflow.md)

## Phase 2: Native C-ABI (`ccall`) Implementation
- [ ] Task: Implement dynamic library loader for `libnwau_c_abi` in `src/NationalWeightedActivityUnitWrapper.jl`.
- [ ] Task: Implement `ccall` wrapper functions for version verification and status diagnostics.
- [ ] Task: Implement acute admitted in-memory calculator calling `nwau-core`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Native C-ABI' (Protocol in workflow.md)

## Phase 3: Tabular Arrow Integration & Bleeding-Edge Tests
- [ ] Task: Integrate `Arrow.jl` for columnar episode batch streaming using Julia 1.11+ `Memory{T}` buffers.
- [ ] Task: Add test suite verifying differential parity against Python and Rust golden fixtures.
- [ ] Task: Run multi-platform tests across macOS ARM64 and Linux on Julia >= 1.11.
- [ ] Task: Prepare final sync commit to `edithatogo/NationalWeightedActivityUnitWrapper.jl` with archival banner and archive repository.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Tabular Arrow Integration & Tests' (Protocol in workflow.md)
