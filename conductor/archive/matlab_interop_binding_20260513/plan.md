# Plan: MATLAB Interoperability

## Phase 1: Strategy and Contract
- [x] Task: Define MATLAB file, CLI/service, and C ABI interop strategy.
    - [x] Select initial reproducible analytics boundary.
    - [x] Define toolbox and platform gating constraints.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Strategy and Contract' (Protocol in workflow.md)

## Phase 2: Examples and Validation
- [x] Task: Add MATLAB examples and shared-fixture validation.
    - [x] Validate diagnostics and provenance against the shared contract.
    - [x] Document numerical analytics workflow patterns.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Examples and Validation' (Protocol in workflow.md)

## Phase 3: Thin Adapter Boundary
- [x] Task: Replace documentation-only MATLAB status with concrete file/CLI boundary helpers.
    - [x] Add file existence, CSV/Parquet import, required-column validation, diagnostics, and provenance.
    - [x] Add external CLI invocation wrapper that captures stdout, exit status, output-file checks, diagnostics, and provenance.
    - [x] Keep toolbox publication, service, and C ABI MEX paths deferred behind owner, parity, and toolchain gates.
