# Plan: Jurisdiction Funding Model Registry

## Phase 1: State and Territory Source Inventory [checkpoint: archived]
- [x] Task: Source public evidence for all jurisdictions.
    - [x] NSW State Price and LHD/SHN service agreement notes.
    - [x] VIC national model transition, WIES history, VCDC/VicABC sources.
    - [x] QLD Efficient Price, QWAU, and Queensland ABF modifications.
    - [x] WA state-specific ABF adjustments and allocation price references.
    - [x] SA State Efficient Price and NEP-equivalent cost per NWAU sources.
    - [x] TAS service plan activity/funding schedules.
    - [x] ACT applicable price and ABF service funding agreement.
    - [x] NT service plan price per WAU and block funding schedules.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: State and Territory Source Inventory' (Protocol in workflow.md)

## Phase 2: Registry Schema [checkpoint: archived]
- [x] Task: Define jurisdiction model schema.
    - [x] Add jurisdiction, financial year, source unit, mapped HWAU unit, price, adjustment, stream applicability, source status, and provenance.
    - [x] Add blocked-source handling for missing or restricted data.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Registry Schema' (Protocol in workflow.md)

## Phase 3: Validation and Parallel Use [checkpoint: archived]
- [x] Task: Add jurisdiction fixtures and tests.
    - [x] Add public-safe source-status fixtures for all jurisdictions.
    - [x] Add valuation selection tests.
    - [x] Add fail-closed tests for unavailable jurisdiction/year combinations.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation and Parallel Use' (Protocol in workflow.md)

## Phase 4: Runtime Jurisdiction Registry [checkpoint: pending]
- [x] Task: Add a runtime jurisdiction funding-model registry.
    - [x] Add explicit rows for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT.
    - [x] Preserve source term, source unit, mapped unit, source URL, checksum, status, and provenance.
    - [x] Keep blocked or public-metadata rows explicit rather than inferring missing coverage.
- [x] Task: Add parallel jurisdiction valuation helpers.
    - [x] Select priced rows for NSW, VIC, and QLD where the registry carries a price.
    - [x] Keep WA, SA, TAS, ACT, and NT rows explicit even when no redistributable price is recorded.
    - [x] Evidence: `nwau_py/jurisdiction_funding_model_registry.py`.
    - [x] Evidence: `tests/test_jurisdiction_funding_model_registry.py`.
    - [x] Evidence: `tests/test_jurisdiction_funding_model_registry_archive_track.py`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Runtime Jurisdiction Registry' (Protocol in workflow.md)
