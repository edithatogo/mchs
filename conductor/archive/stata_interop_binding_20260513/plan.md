# Plan: Stata Interoperability

## Phase 1: Strategy and Contract
- [x] Task: Define Stata file, CLI, and service interop strategy.
    - [x] Select initial reproducible costing-study boundary.
    - [x] Define DTA/CSV/Parquet and package gating constraints.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Strategy and Contract' (Protocol in workflow.md)

## Phase 2: Examples and Validation
- [x] Task: Add Stata examples and shared-fixture validation.
    - [x] Validate diagnostics and provenance against the shared contract.
    - [x] Document health-economics workflow patterns.
- [x] Task: Promote legacy status wording to bounded file/CLI adapter.
    - [x] Add `mchs import`, `mchs run`, and `mchs validate` commands without calculator logic.
    - [x] Keep package publication deferred behind owner and CLI/file stability gates.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Examples and Validation' (Protocol in workflow.md)
