# Plan: Pricing-Year Diff Tooling

## Phase 1: Diff Model
- [x] Task: Define comparison categories and output formats.
    - [x] Include constants, weights, adjustments, coding sets, sources, and validation statuses.
    - [x] Define markdown and JSON outputs.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Diff Model' (Protocol in workflow.md)

## Phase 2: Command Implementation
- [x] Task: Implement `funding-calculator diff-year <from-year> <to-year>` with tests.
    - [x] Add summary handling for large table changes.
    - [x] Add fixture cases for changed, unchanged, missing, and new values.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Command Implementation' (Protocol in workflow.md)

## Phase 3: Release Integration
- [x] Task: Document use of year diffs in release and validation workflows.
    - [x] Add examples for 2025-26 to 2026-27 changes.
    - [x] Link diff output to release note preparation.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Release Integration' (Protocol in workflow.md)
