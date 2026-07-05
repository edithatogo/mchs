# Plan: Jurisdiction Price Source Index

## Phase 1: Source Index Schema [checkpoint: archived]
- [x] Task: Define source index fields.
    - [x] Add jurisdiction, year, source, licence, checksum, units, and status.
    - [x] Add extraction notes and blocked-source handling.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Source Index Schema' (Protocol in workflow.md)

## Phase 2: Jurisdiction Rows [checkpoint: archived]
- [x] Task: Add public-safe source-index rows.
    - [x] Add NSW, VIC, QLD, WA, SA, TAS, ACT, and NT rows.
    - [x] Mark unavailable or restricted sources explicitly.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Jurisdiction Rows' (Protocol in workflow.md)

## Phase 3: Validation [checkpoint: archived]
- [x] Task: Add source-index tests.
    - [x] Prevent price values without provenance.
    - [x] Prevent unknown source status from appearing as supported.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation' (Protocol in workflow.md)

## Phase 4: Runtime Source Index API [checkpoint: pending]
- [x] Task: Add a machine-readable jurisdiction source-index API.
    - [x] Add public-safe metadata or explicit blocked rows for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT.
    - [x] Preserve source title, URL/path, checksum, licence, redistribution, unit, stream, status, and extraction notes.
    - [x] Do not commit jurisdiction price values in source-index rows.
- [x] Task: Add fail-closed source-index validation.
    - [x] Missing jurisdiction/year source rows raise a clear source-index error.
    - [x] Coverage validation requires every state and territory to have a public-safe or blocked row.
- [x] Task: Add archive and runtime evidence tests.
    - [x] Evidence: `nwau_py/jurisdiction_price_sources.py`.
    - [x] Evidence: `tests/test_jurisdiction_price_sources.py`.
    - [x] Evidence: `tests/test_jurisdiction_price_source_index_archive_track.py`.
    - [x] Evidence: `conductor/archive/jurisdiction_price_source_index_20260513/metadata.json`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Runtime Source Index API' (Protocol in workflow.md)
