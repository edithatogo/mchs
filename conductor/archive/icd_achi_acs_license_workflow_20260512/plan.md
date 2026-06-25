# Plan: ICD-10-AM/ACHI/ACS Licensed Product Workflow

## Phase 1: Contract and Boundary
- [x] Task: Define the licensed-product workflow contract and local-only boundary.
  - [x] Document public metadata versus restricted products.
  - [x] Add local-only path and manifest conventions.
  - [x] Evidence surfaces: `spec.md` contract section, `metadata.json`, and any referenced manifest template.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Boundary' (Protocol in workflow.md)

## Phase 2: Guards and Synthetic Fixtures
- [x] Task: Add repository guards and CI-safe synthetic fixtures.
  - [x] Prevent accidental commit of restricted tables/groupers.
  - [x] Test missing licensed asset diagnostics.
  - [x] Evidence surfaces: ignore/guard rules, missing-asset tests, and synthetic fixture files only.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Guards and Synthetic Fixtures' (Protocol in workflow.md)

## Phase 3: Local-Only User Documentation
- [x] Task: Document licensed-product setup for admitted acute grouping workflows.
  - [x] Explain local file references and environment variables.
  - [x] Clarify licensing responsibility and unsupported redistribution.
  - [x] Evidence surfaces: setup docs, caveat language, and local configuration examples.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Local-Only User Documentation' (Protocol in workflow.md)

## Caveat Checks
- [x] Task: Verify the track never claims to ship, mirror, or vendor restricted classification content.
- [x] Task: Verify completion evidence stays limited to docs, guards, and synthetic-safe tests.
- [x] Task: Verify all published references keep licensed assets local-only and user-supplied.
