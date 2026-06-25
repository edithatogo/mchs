# Plan: Classification Input Validation

## Phase 1: Matrix and Schema Design [checkpoint: 111f776]
- [x] Task: Create a year-by-year classification compatibility matrix.
    - [x] Include AR-DRG, AECC, UDG, Tier 2, AMHCC, and known transition years.
    - [x] Identify licensed/non-redistributable inputs.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Matrix and Schema Design' (Protocol in workflow.md)

## Phase 2: Validator Tests
- [x] Task: Write validation tests for stream-specific required fields and version mismatches.
    - [x] Cover valid, missing, invalid, and incompatible version cases.
    - [x] Include CLI-facing diagnostics where applicable.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Validator Tests' (Protocol in workflow.md)

## Phase 3: Validator Implementation and Docs
- [x] Task: Implement strict classification-aware validation and documentation. [f2193a3]
    - [x] Add Pydantic or equivalent schema models at module boundaries.
    - [x] Update docs with preparation guidance for activity datasets.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validator Implementation and Docs' (Protocol in workflow.md)
