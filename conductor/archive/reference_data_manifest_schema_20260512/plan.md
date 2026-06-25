# Plan: Reference Data Manifest Schema

## Phase 1: Schema Design
- [x] Task: Design the manifest schema and validation-status taxonomy.
    - [x] Include source artifacts, constants, weights, adjustments, coding sets, and validation status.
    - [x] Define explicit gap-record semantics.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Schema Design' (Protocol in workflow.md)

## Phase 2: Models and Fixtures
- [x] Task: Add typed manifest models and example fixtures.
    - [x] Add tests for valid, invalid, missing, and gap-record cases.
    - [x] Add pinned example manifests for pricing years `2026` and `2025`.
    - [x] Add tests for required gap-record fields, duplicate rejection, missing-vs-gap distinction, and actionable diagnostics.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Models and Fixtures' (Protocol in workflow.md)

## Phase 3: Documentation
- [x] Task: Document manifest authoring and schema evolution.
    - [x] Explain validation statuses and source provenance requirements.
    - [x] Link manifests to calculator support matrices.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)
