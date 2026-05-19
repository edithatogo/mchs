# Plan: Power Platform NSW Environment Deployment

## Phase 1: Environment Readiness

- [x] Task: Confirm target NSW environment
    - [x] Record environment URL, environment ID, tenant ID policy, and DLP constraints
    - [x] Confirm `pac auth list` can target the environment
    - [x] Confirm permissions for solution import and connector connection creation
- [x] Task: Configure environment-specific settings
    - [x] Set service endpoint environment variable
    - [x] Set authentication/connection reference
    - [x] Set synthetic-only or production fixture gate
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Environment Readiness' (Protocol in workflow.md)

## Phase 2: Deployment and Smoke

- [x] Task: Import managed solution
    - [x] Run managed solution import through `pac solution import` or approved pipeline
    - [x] Publish customizations where required
    - [x] Record import job output and solution version
- [x] Task: Run post-deployment smoke tests
    - [x] Invoke health/check flow
    - [x] Open app and run synthetic validation scenario
    - [x] Verify connector calls and diagnostics output
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Deployment and Smoke' (Protocol in workflow.md)

## External Blocker

- [x] Task: Complete NSW tenant deployment evidence once credentials and target environment details are available.
    - [x] Provide target environment URL and ID.
    - [x] Authenticate `pac` against the NSW tenant.
    - [x] Import managed solution and record output.
    - [x] Run app, connector, and flow smoke tests.
