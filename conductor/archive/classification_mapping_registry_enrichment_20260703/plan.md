# Plan: Classification Mapping Registry Enrichment

## Phase 1: Shared Classification Registry Contract
- [x] Task: Define the shared classification mapping data model and public metadata source of truth.
    - [x] Add failing tests for supported streams, required fields, and year/version bindings.
    - [x] Add failing tests for fail-closed compatibility checks on mismatched stream/year/classification combinations.
    - [x] Add failing tests that assert the registry stays public-metadata only for loadable fixtures.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Shared Classification Registry Contract' (Protocol in workflow.md)

## Phase 2: Local Hooks, CLI Exposure, and Docs
- [x] Task: Add local-only AR-DRG mapping hook placeholders and expose the registry through the CLI and library surface.
    - [x] Add failing tests for local-only hook validation and CLI listing/compatibility output.
    - [x] Implement the registry helpers and hook placeholders with fail-closed errors for unsupported or licensed-only paths.
    - [x] Export the new registry surface and update docs to describe the DRG derivation boundary.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Local Hooks, CLI Exposure, and Docs' (Protocol in workflow.md)
