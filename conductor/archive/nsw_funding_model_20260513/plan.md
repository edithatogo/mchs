# Plan: NSW Funding Model

## Phase 1: NSW Source Inventory [checkpoint: archived]
- [x] Task: Identify NSW State Price sources by year.
    - [x] Capture LHD/SHN service agreement notes.
    - [x] Capture DNR costing basis where public.
    - [x] Capture source terminology and caveats.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: NSW Source Inventory' (Protocol in workflow.md)

## Phase 2: NSW Model Schema [checkpoint: archived]
- [x] Task: Define NSW funding model fields.
    - [x] Add state price, financial year, NWAU/HWAU version, district/network scope, adjustments, exclusions, and provenance.
    - [x] Add blocked/unknown state for unavailable years.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: NSW Model Schema' (Protocol in workflow.md)

## Phase 3: NSW Valuation Fixtures [checkpoint: archived]
- [x] Task: Add public-safe fixtures and tests.
    - [x] Add NSW State Price valuation fixture.
    - [x] Add missing-year fail-closed fixture.
    - [x] Add parallel valuation fixture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: NSW Valuation Fixtures' (Protocol in workflow.md)

## Phase 4: Runtime NSW Funding Registry [checkpoint: b51a134]
- [x] Task: Add a public-source NSW funding registry API.
    - [x] Add public-source NSW State Price fixtures for 2025 and 2026.
    - [x] Preserve source term, source URL, retrieved date, checksum, licence, scope, adjustments, exclusions, and provenance.
    - [x] Map NSW NWAU source terminology to the generic HWAU abstraction.
- [x] Task: Add fail-closed missing-year handling.
    - [x] Missing NSW financial years raise a clear registry error.
    - [x] The registry does not infer values for unregistered years.
- [x] Task: Add parallel valuation helper coverage.
    - [x] Parallel NSW/national valuation helper uses the NSW fixture and the national efficient price.
    - [x] Evidence: `nwau_py/nsw_funding_model.py`.
    - [x] Evidence: `tests/test_nsw_funding_model.py`.
    - [x] Evidence: `tests/test_nsw_funding_model_archive_track.py`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Runtime NSW Funding Registry' (Protocol in workflow.md)
