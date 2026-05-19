# Plan: Power Platform Operational Evidence and Governance

## Phase 1: Evidence Bundle

- [x] Task: Create deployment evidence bundle
    - [x] Record solution artifact hash and version
    - [x] Record environment import outputs
    - [x] Record connector/app/flow identifiers as pending runtime values
- [x] Task: Create runtime smoke evidence
    - [x] Record synthetic request/response trace template
    - [x] Record diagnostics and provenance output template
    - [x] Record support status and known limitations
- [x] Task: Create platform and visual test evidence contract
    - [x] Record PAC solution visibility evidence
    - [x] Register custom connector in NSW `dylan`
    - [x] Generate canvas `.msapp` artifact from registered connector
    - [x] Record real Power App visual review blocker
    - [x] Record real app and flow smoke blockers
    - [x] Record visual optimization checklist
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Evidence Bundle' (Protocol in workflow.md)

## Phase 2: Operational Governance

- [x] Task: Define monitoring and alerting
    - [x] Track connector failures and flow run failures
    - [x] Track service-boundary health
    - [x] Define support escalation path
- [x] Task: Define privacy and DLP evidence
    - [x] Record data handling classification
    - [x] Record DLP policy compatibility evidence template
    - [x] Record no patient-level committed data evidence
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Operational Governance' (Protocol in workflow.md)

## External Blocker

- [~] Task: Complete NSW tenant deployment evidence once credentials and target environment details are available.
    - [x] Provide target environment URL and ID.
    - [x] Authenticate `pac` against the NSW tenant.
    - [x] Import managed solution and record output.
    - [x] Register custom connector and record connector ID.
    - [x] Generate canvas app artifact from custom connector.
    - [x] Publish/import generated canvas app into the NSW tenant.
    - [x] View the real Power App in the NSW tenant.
    - [x] Optimize and evidence visual function in the NSW tenant.
    - [ ] Run app, connector, and flow smoke tests.
