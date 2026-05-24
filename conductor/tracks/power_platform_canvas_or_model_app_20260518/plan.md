# Plan: Power Platform App Surface

## Phase 1: App UX Contract

- [x] Task: Define app type and screens
    - [x] Choose canvas or model-driven app based on NSW account constraints
    - [x] Define calculator selection, input validation, results, diagnostics, and evidence screens
    - [x] Define synthetic demo data only
- [x] Task: Define accessibility and governance requirements
    - [x] Record WCAG and Microsoft accessibility checks
    - [x] Avoid patient-level data storage
    - [x] Surface provenance and support status to users
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: App UX Contract' (Protocol in workflow.md)

## Phase 2: App Implementation

- [x] Task: Create app assets
    - [x] Add app package/source representation to the unpacked solution
    - [x] Bind all actions to custom connector operations
    - [x] Use environment variables for endpoints and feature gates
- [x] Task: Validate no-formula app boundary
    - [x] Scan app expressions for forbidden formula constants and calculation logic
    - [x] Add screenshot or export evidence
    - [x] Record manual verification requirements if tooling cannot inspect binary app assets
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: App Implementation' (Protocol in workflow.md)
