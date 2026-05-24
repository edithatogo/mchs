# Plan: Power Platform Managed Solution Promotion

## Phase 1: Promotion Model

- [x] Task: Define environment chain
    - [x] Record dev/test/prod or NSW-specific equivalent
    - [x] Define who approves each promotion
    - [x] Define managed/unmanaged boundaries
- [x] Task: Define versioning and rollback
    - [x] Map solution version to package version
    - [x] Define upgrade vs update behavior
    - [x] Define rollback/export evidence procedure
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Promotion Model' (Protocol in workflow.md)

## Phase 2: Promotion Execution

- [x] Task: Promote managed artifact
    - [x] Run solution checker before promotion
    - [x] Import managed solution to downstream environment
    - [x] Record approvals and import outputs
- [x] Task: Validate downstream behavior
    - [x] Run app smoke checks
    - [x] Run flow smoke checks
    - [x] Verify no unmanaged edits were required downstream
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Promotion Execution' (Protocol in workflow.md)

## External Blocker

- [x] Task: Complete NSW tenant deployment evidence once credentials and target environment details are available.
    - [x] Provide target environment URL and ID.
    - [x] Authenticate `pac` against the NSW tenant.
    - [x] Import managed solution and record output.
    - [x] Run app, connector, and flow smoke tests.
