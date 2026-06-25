# Plan: C ABI Binding

## Phase 1: ABI Contract and Boundary Design
- [x] Task: Define the conservative ABI contract for versioning, ownership, and errors.
    - [x] Lock append-only POD structs, borrowed views, and runtime version queries.
    - [x] Document Arrow C Data Interface usage and the file-based Arrow boundary.
    - [x] Document unsupported Python-specific behavior and deferred features.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: ABI Contract and Boundary Design' (Protocol in workflow.md)

## Phase 2: Preview Implementation and Fixture Parity
- [x] Task: Implement a minimal C ABI entry point for one validated calculator.
    - [x] Add a committed header and Rust workspace crate for ABI compatibility checks.
    - [x] Keep shared golden fixture parity as the gate before any readiness claim.
    - [x] Delegate valid scalar acute 2025 pointer-shaped calls to `nwau-core` and fail closed on invalid pointers.
    - [x] Add repository tests for the preview C ABI surface, memory ownership, error semantics, Arrow boundary, and publication posture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Preview Implementation and Fixture Parity' (Protocol in workflow.md)
