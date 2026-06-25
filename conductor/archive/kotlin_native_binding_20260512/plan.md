# Plan: Kotlin/Native Binding

## Phase 1: Strategy Selection
- [x] Task: Compare C ABI, service, and Arrow/Parquet file interop for native Kotlin users.
    - [x] Select an initial strategy that avoids a JVM runtime dependency.
    - [x] Define Kotlin/Native API, memory ownership, and C ABI considerations.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Strategy Selection' (Protocol in workflow.md)

## Phase 2: Prototype and Validation
- [x] Task: Add Kotlin/Native prototype and shared-fixture tests.
    - [x] Validate outputs against golden fixtures.
    - [x] Document native, service, and file-contract deployment patterns.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Prototype and Validation' (Protocol in workflow.md)
