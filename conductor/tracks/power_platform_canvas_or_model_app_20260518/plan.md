# Plan: Power Platform App Surface

## Phase 1: App UX Contract

- [ ] Task: Define app type and screens
    - [ ] Choose canvas or model-driven app based on NSW account constraints
    - [ ] Define calculator selection, input validation, results, diagnostics, and evidence screens
    - [ ] Define synthetic demo data only
- [ ] Task: Define accessibility and governance requirements
    - [ ] Record WCAG and Microsoft accessibility checks
    - [ ] Avoid patient-level data storage
    - [ ] Surface provenance and support status to users
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: App UX Contract' (Protocol in workflow.md)

## Phase 2: App Implementation

- [ ] Task: Create app assets
    - [ ] Add app package/source representation to the unpacked solution
    - [ ] Bind all actions to custom connector operations
    - [ ] Use environment variables for endpoints and feature gates
- [ ] Task: Validate no-formula app boundary
    - [ ] Scan app expressions for forbidden formula constants and calculation logic
    - [ ] Add screenshot or export evidence
    - [ ] Record manual verification requirements if tooling cannot inspect binary app assets
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: App Implementation' (Protocol in workflow.md)
