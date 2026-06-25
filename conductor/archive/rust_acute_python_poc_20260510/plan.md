# Plan: Rust Acute 2025 Proof of Concept with Python Bindings

## Phase 1: Rust Workspace and Kernel Contract [checkpoint: a6b3fc4]

- [x] Task: Write failing tests for Rust workspace expectations [d0ddb5d]
    - [x] Verify the Rust workspace files exist
    - [x] Verify Rust package metadata names the acute 2025 proof of concept
    - [x] Verify Python packaging can locate the binding scaffold
- [x] Task: Scaffold the Rust workspace [6df096a]
    - [x] Add core and Python binding crates with explicit responsibilities
    - [x] Add formatting, linting, and test entry points
    - [x] Document how the workspace maps to the architecture ADR
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Rust Workspace and Kernel Contract' (Protocol in workflow.md) [a6b3fc4]

## Phase 2: Acute 2025 Formula Kernel [checkpoint: d4ce021]

- [x] Task: Write Rust formula tests [63b3348]
    - [x] Cover acute 2025 fixture rows and edge cases from the existing Python tests
    - [x] Cover parameter validation and numeric precision expectations
    - [x] Cover source-provenance metadata attached to formula behavior
- [x] Task: Implement the acute 2025 Rust kernel [d4ce021]
    - [x] Keep formula functions deterministic and free of hidden global state [d4ce021]
    - [x] Keep reference data access separate from formula execution [d4ce021]
    - [x] Preserve traceability to SAS and Python reference behavior [d4ce021]
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Acute 2025 Formula Kernel' (Protocol in workflow.md) [d4ce021]

## Phase 3: Python Binding and Adapter [checkpoint: 731db86]

- [x] Task: Write Python binding tests [731db86]
    - [x] Verify Python can call the Rust-backed acute path [731db86]
    - [x] Verify the binding preserves input and output schema names [731db86]
    - [x] Verify the binding remains opt-in and does not replace default Python execution [731db86]
- [x] Task: Implement the Python binding adapter [731db86]
    - [x] Add PyO3/maturin build integration [731db86]
    - [x] Expose an explicit Rust-backed acute 2025 entry point [731db86]
    - [x] Add CLI or API opt-in wiring without changing current defaults [731db86]
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Python Binding and Adapter' (Protocol in workflow.md) [731db86]

## Phase 4: Parity, Performance, and Canary Documentation [checkpoint: 9bb72b4]

- [x] Task: Write parity and canary tests [9bb72b4]
    - [x] Compare Rust-backed outputs against acute 2025 golden fixtures [9bb72b4]
    - [x] Compare Rust-backed and Python-default outputs on the same fixture pack [9bb72b4]
    - [x] Verify failure reports include fixture provenance and tolerance [9bb72b4]
- [x] Task: Document Rust proof-of-concept status [9bb72b4]
    - [x] Record validation evidence and known limitations [9bb72b4]
    - [x] Record performance measurements without making unsupported claims [9bb72b4]
    - [x] Document rollback and non-default runtime behavior [9bb72b4]
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Parity, Performance, and Canary Documentation' (Protocol in workflow.md) [9bb72b4]
