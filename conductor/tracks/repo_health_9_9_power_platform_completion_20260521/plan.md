# Plan: Repo Health 9.9 Power Platform Completion

## Phase 1: Page and Function Coverage

- [x] Task: Source-control all current Power App screens
    - [x] Commit home screen source
    - [x] Commit Health screen source
    - [x] Commit ListCalculators screen source
    - [x] Commit GetCalculatorSchema screen source
    - [x] Commit ValidateInput screen source
    - [x] Commit Calculate screen source
    - [x] Commit GetEvidence screen source
- [x] Task: Create page/function coverage contract
    - [x] Map every connector operation to a screen
    - [x] Mark generated operation pages as incomplete until UX and runtime smoke evidence exist
    - [x] Preserve orchestration-only formula boundary
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Page and Function Coverage' (Protocol in workflow.md)

## Phase 2: Repo Health 9.9 Gate

- [x] Task: Create 9.9 repo-health contract
    - [x] Define required gates for operation pages, service boundary smoke, flow smoke, DLP, GitHub live gates, and subrepo ownership
    - [x] Keep current score at 9.5 until gates pass
    - [x] Add validators and tests for truthful claim boundaries
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Repo Health 9.9 Gate' (Protocol in workflow.md)

## External Blockers

- [ ] Task: Complete generated operation page redesigns with loading, success, validation-error, connector-error, trace ID, keyboard, and responsive evidence.
- [ ] Task: Configure production service-boundary endpoint and connection reference values.
- [ ] Task: Execute live app connector smoke for Health, ListCalculators, GetCalculatorSchema, ValidateInput, Calculate, and GetEvidence.
- [ ] Task: Add and execute real Power Automate flow smoke.
- [ ] Task: Capture NSW DLP, monitoring, and connector policy evidence.
- [ ] Task: Run official GitHub Power Platform live gate with repository secrets.
- [ ] Task: Provision standalone Power Platform subrepo remote or record explicit waiver.
