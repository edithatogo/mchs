# Plan: Outer Wrapper Retirement Migration

## Phase 1: Inventory

- [x] Task: Capture outer wrapper state.
    - [x] Record tracked gitlinks, tracked generated logs, untracked source slices, and ignored local files.
    - [x] Compare outer wrapper paths with canonical repo paths.
    - [x] Identify unique Power Platform, script, test, and evidence files.
- [x] Task: Create migration manifest.
    - [x] Assign each path a disposition: migrate, archive, delete, ignore, retain external, or duplicate.
    - [x] Require evidence checksums for files that are archived or migrated.
- [x] Task: Conductor - User Manual Verification 'Inventory' (Protocol in workflow.md)

## Phase 2: Preservation and Retirement [checkpoint: a659bd4]

- [x] Task: Preserve source slices. [6ca7d06]
    - [x] Move or copy approved unique source artifacts into canonical paths.
    - [x] Add tests or documentation references for migrated artifacts.
    - [x] Confirm no canonical file is overwritten without review.
- [x] Task: Retire wrapper-only artifacts. [8e680f9]
    - [x] Remove generated logs and browser state from source control when approved.
    - [x] Resolve the unmanaged gitlink by retiring the wrapper or adding valid superproject metadata.
    - [x] Record any user-owned cleanup that cannot be automated.
- [x] Task: Conductor - User Manual Verification 'Preservation and Retirement' (Protocol in workflow.md) [684e5c9]

## Phase 3: Validation

- [x] Task: Validate migration results. [7e66349]
    - [x] Run topology validator against canonical repo.
    - [x] Run topology validator against the outer wrapper with explicit `--outer-root`.
    - [x] Run focused tests for migrated source artifacts.
- [x] Task: Record residual gates. [a7e662c]
    - [x] Separate local cleanup from external registry or account blockers.
    - [x] Update support docs only for migrated, validated artifacts.
- [ ] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md)
