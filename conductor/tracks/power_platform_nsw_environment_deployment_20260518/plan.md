# Plan: Power Platform NSW Environment Deployment

## Phase 1: Environment Readiness

- [ ] Task: Confirm target NSW environment
    - [ ] Record environment URL, environment ID, tenant ID policy, and DLP constraints
    - [ ] Confirm `pac auth list` can target the environment
    - [ ] Confirm permissions for solution import and connector connection creation
- [ ] Task: Configure environment-specific settings
    - [ ] Set service endpoint environment variable
    - [ ] Set authentication/connection reference
    - [ ] Set synthetic-only or production fixture gate
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Environment Readiness' (Protocol in workflow.md)

## Phase 2: Deployment and Smoke

- [ ] Task: Import managed solution
    - [ ] Run managed solution import through `pac solution import` or approved pipeline
    - [ ] Publish customizations where required
    - [ ] Record import job output and solution version
- [ ] Task: Run post-deployment smoke tests
    - [ ] Invoke health/check flow
    - [ ] Open app and run synthetic validation scenario
    - [ ] Verify connector calls and diagnostics output
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Deployment and Smoke' (Protocol in workflow.md)

## External Blocker

- [ ] Task: Complete NSW tenant deployment evidence once credentials and target environment details are available.
    - [ ] Provide target environment URL and ID.
    - [ ] Authenticate `pac` against the NSW tenant.
    - [ ] Import managed solution and record output.
    - [ ] Run app, connector, and flow smoke tests.
