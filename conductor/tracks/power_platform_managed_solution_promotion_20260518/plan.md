# Plan: Power Platform Managed Solution Promotion

## Phase 1: Promotion Model

- [ ] Task: Define environment chain
    - [ ] Record dev/test/prod or NSW-specific equivalent
    - [ ] Define who approves each promotion
    - [ ] Define managed/unmanaged boundaries
- [ ] Task: Define versioning and rollback
    - [ ] Map solution version to package version
    - [ ] Define upgrade vs update behavior
    - [ ] Define rollback/export evidence procedure
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Promotion Model' (Protocol in workflow.md)

## Phase 2: Promotion Execution

- [ ] Task: Promote managed artifact
    - [ ] Run solution checker before promotion
    - [ ] Import managed solution to downstream environment
    - [ ] Record approvals and import outputs
- [ ] Task: Validate downstream behavior
    - [ ] Run app smoke checks
    - [ ] Run flow smoke checks
    - [ ] Verify no unmanaged edits were required downstream
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Promotion Execution' (Protocol in workflow.md)
