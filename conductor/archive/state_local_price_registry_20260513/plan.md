# Plan: State and Local Price Registry

## Phase 1: Source Discovery
- [x] Task: Inventory national and state price sources over time.
    - [x] Identify NEP sources.
    - [x] Identify state-specific or jurisdictional price sources.
    - [x] Identify public versus local-only/licensed sources.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Source Discovery' (Protocol in workflow.md) [checkpoint: archived]

## Phase 2: Registry Schema
- [x] Task: Define versioned price schedule schema.
    - [x] Add jurisdiction, year, effective period, currency, unit, and provenance.
    - [x] Add local price and discounted price rule models.
    - [x] Add blocked/missing source status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Registry Schema' (Protocol in workflow.md) [checkpoint: archived]

## Phase 3: Validation Fixtures
- [x] Task: Add synthetic and public-safe fixtures.
    - [x] Add national price fixture.
    - [x] Add state/local price fixture.
    - [x] Add discounted price fixture.
    - [x] Add unavailable-source fail fixture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation Fixtures' (Protocol in workflow.md) [checkpoint: archived]

## Phase 4: Runtime Registry API
- [x] Task: Implement a runtime PriceRegistry API for national, state, local, discounted, missing, and blocked schedule behavior.
- [x] Task: Source national rows from shared NEP pricing constants and keep state/local/discounted rows explicitly local-only synthetic fixtures.
- [x] Task: Add fail-closed tests for missing and blocked schedules.
- [x] Task: Repair metadata.json with completion policy, archive evidence, partially resolved runtime gap, and explicit source gap.
- [x] Task: Update conductor/tracks.md so the archived track is marked complete instead of in progress.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Runtime Registry API' (Protocol in workflow.md) [checkpoint: repaired]
    - Evidence: `conductor/archive/state_local_price_registry_20260513/metadata.json`, `nwau_py/price_registry.py`, `tests/test_price_registry.py`, and `tests/test_state_local_price_registry_archive_track.py`.
