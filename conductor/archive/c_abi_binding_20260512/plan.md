# Plan: C ABI Binding

## Phase 1: ABI Contract and Boundary Design [checkpoint: archived]
- [x] Task: Define the conservative ABI contract for versioning, ownership, and errors.
    - [x] Lock append-only POD structs, borrowed views, and runtime version queries.
    - [x] Document Arrow C Data Interface usage and the file-based Arrow boundary.
    - [x] Document unsupported Python-specific behavior and deferred features.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: ABI Contract and Boundary Design' (Protocol in workflow.md)

## Phase 2: Preview Implementation and Fixture Parity [checkpoint: archived]
- [x] Task: Implement a minimal C ABI entry point for one validated calculator.
    - [x] Add a committed header and Rust workspace crate for ABI compatibility checks.
    - [x] Keep shared golden fixture parity as the gate before any readiness claim.
    - [x] Delegate valid scalar acute 2025 pointer-shaped calls to `nwau-core` and fail closed on invalid pointers.
    - [x] Add repository tests for the preview C ABI surface, memory ownership, error semantics, Arrow boundary, and publication posture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Preview Implementation and Fixture Parity' (Protocol in workflow.md)

## Phase 3: Archive Repair [checkpoint: repaired]
- [x] Task: Repair archive metadata and plan evidence.
    - [x] Restore `metadata.json` archive-policy fields for completion policy, support scope, archive evidence, and explicit gap register.
    - [x] Restore `plan.md` checkpoint markers so the archived plan remains auditable after migration.
    - [x] Preserve the public claim boundary: this is private preview implementation and contract definition, not a production-ready ABI promise.
- [x] Task: Conductor review checkpoint for Archive Repair.
    - [x] Confirm focused tests cover repaired metadata and plan evidence.
    - [x] Confirm the C ABI wrapper delegates calculator work to `nwau-core` rather than duplicating formula logic.
