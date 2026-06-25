# Plan: NHCDC Cost Report Ingestion

## Phase 1: Source Inventory
- [x] Task: Inventory public NHCDC reports, appendices, and data request specifications by year.
    - [x] Capture URLs, file types, checksums, publication dates, and table categories.
    - [x] Record missing or changed formats as explicit gaps.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Source Inventory' (Protocol in workflow.md)
  [checkpoint: 3b77ab5]

## Phase 2: Parser and Normalization
- [x] Task: Add parser fixtures and normalized output schema for public NHCDC tables.
    - [x] Use safe sample workbooks or fixture slices.
    - [x] Preserve table-level provenance.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Parser and Normalization' (Protocol in workflow.md)
  [checkpoint: 3b77ab5]

## Phase 3: Documentation and Examples
- [x] Task: Document public NHCDC table ingestion and interpretation limits.
    - [x] Link cost bucket registry and costing-study tutorials.
    - [x] Explain aggregate public data versus confidential patient-level submissions.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation and Examples' (Protocol in workflow.md)
  [checkpoint: 3b77ab5]
