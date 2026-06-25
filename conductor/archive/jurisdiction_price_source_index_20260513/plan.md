# Plan: Jurisdiction Price Source Index

## Phase 1: Source Index Schema
- [x] Task: Define source index fields.
    - [x] Add jurisdiction, year, source, licence, checksum, units, and status.
    - [x] Add extraction notes and blocked-source handling.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Source Index Schema' (Protocol in workflow.md)

## Phase 2: Jurisdiction Rows
- [x] Task: Add public-safe source-index rows.
    - [x] Add NSW, VIC, QLD, WA, SA, TAS, ACT, and NT rows.
    - [x] Mark unavailable or restricted sources explicitly.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Jurisdiction Rows' (Protocol in workflow.md)

## Phase 3: Validation
- [x] Task: Add source-index tests.
    - [x] Prevent price values without provenance.
    - [x] Prevent unknown source status from appearing as supported.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation' (Protocol in workflow.md)
