# Plan: AR-DRG Version Parity Fixtures

## Phase 1: Fixture Schema
- [x] Task: Define AR-DRG parity fixture schema and provenance fields.
    - [x] Include metadata for expected AR-DRG and NWAU-relevant parity scope without proprietary payloads.
    - [x] Define synthetic versus local licensed fixture handling.
    - [x] Evidence surfaces: `spec.md` contract and caveats, `metadata.json`, and the fixture schema or manifest template.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Fixture Schema' (Protocol in workflow.md)

## Phase 2: Fixture Validation
- [x] Task: Add fixture loader and compatibility tests.
    - [x] Reject incompatible pricing-year, coding-set, AR-DRG, or grouper versions.
    - [x] Support precomputed and external-grouper workflows.
    - [x] Evidence surfaces: loader tests, compatibility failure diagnostics, and any synthetic-safe fixture examples.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Fixture Validation' (Protocol in workflow.md)

## Phase 3: Documentation
- [x] Task: Document AR-DRG fixture creation and validation workflow.
    - [x] Explain how fixtures prove grouping and downstream NWAU behavior.
    - [x] Add safe synthetic workflow notes and local-only licensed fixture handling.
    - [x] Explain admitted acute NWAU checks and version-specific grouping expectations.
    - [x] State that proprietary grouper outputs and licensed code tables are not committed.
    - [x] Evidence surfaces: docs for synthetic fixtures, local-only licensed fixture references, and caveat language.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)

## Caveat Checks
- [x] Task: Verify the track never claims to commit, mirror, or redistribute licensed AR-DRG products or grouper bundles.
- [x] Task: Verify synthetic fixtures remain illustrative and safe for repository use.
- [x] Task: Verify local licensed fixtures are treated as user-supplied artifacts with path placeholders only.
