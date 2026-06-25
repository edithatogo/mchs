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

## Phase 2: Preservation and Retirement

- [ ] Task: Preserve source slices.
    - [ ] Move or copy approved unique source artifacts into canonical paths.
    - [ ] Add tests or documentation references for migrated artifacts.
    - [ ] Confirm no canonical file is overwritten without review.
- [ ] Task: Retire wrapper-only artifacts.
    - [ ] Remove generated logs and browser state from source control when approved.
    - [ ] Resolve the unmanaged gitlink by retiring the wrapper or adding valid superproject metadata.
    - [ ] Record any user-owned cleanup that cannot be automated.
- [ ] Task: Conductor - User Manual Verification 'Preservation and Retirement' (Protocol in workflow.md)

## Phase 3: Validation

- [ ] Task: Validate migration results.
    - [ ] Run topology validator against canonical repo.
    - [ ] Run topology validator against the outer wrapper with explicit `--outer-root`.
    - [ ] Run focused tests for migrated source artifacts.
- [ ] Task: Record residual gates.
    - [ ] Separate local cleanup from external registry or account blockers.
    - [ ] Update support docs only for migrated, validated artifacts.
- [ ] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md)
