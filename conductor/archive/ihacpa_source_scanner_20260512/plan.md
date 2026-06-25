# Plan: IHACPA Source Scanner

## Phase 1: Command Contract
- [x] Task: Define source scanner command contract and source categories.
    - [x] Specify dry-run output and review workflow.
    - [x] Define gap-record handling for Box-hosted or inaccessible artifacts.
    - [x] Align command docs and fixtures with `funding-calculator sources ...`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Command Contract' (Protocol in workflow.md)

## Phase 2: Scanner Implementation
- [x] Task: Implement source discovery and draft-manifest generation.
    - [x] Add parser tests using saved HTML or synthetic source fixtures.
    - [x] Add retrieval metadata handling through discovery manifests and explicit unchanged-source fixtures.
    - [x] Add CLI dry-run coverage for scan and add-year flows.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Scanner Implementation' (Protocol in workflow.md)

## Phase 3: Docs and CI Safety
- [x] Task: Document scanner use and add non-network CI checks.
    - [x] Ensure CI validates parser fixtures without depending on live IHACPA availability.
    - [x] Explain manual review before committing source changes.
    - [x] Document conservative validation wording and publication boundaries.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Docs and CI Safety' (Protocol in workflow.md)
