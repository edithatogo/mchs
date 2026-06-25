# Plan: FFI Safety Review

## Phase 1: ABI Audit
- [x] Task: Audit exported C ABI functions.
    - [x] Identify unsafe pointer reads.
    - [x] Identify unchecked UTF-8 and length assumptions.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: ABI Audit' (Protocol in workflow.md)

## Phase 2: Safety Fixes
- [x] Task: Apply FFI safety hardening.
    - [x] Use checked UTF-8 conversion.
    - [x] Add invalid argument status handling.
    - [x] Document ownership and lifetime rules.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Safety Fixes' (Protocol in workflow.md)

## Phase 3: Validation
- [x] Task: Add and run ABI tests.
    - [x] Test null inputs.
    - [x] Test invalid UTF-8.
    - [x] Test valid calls.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation' (Protocol in workflow.md)
