# Plan: Power Automate Orchestration Flows

## Phase 1: Flow Design

- [x] Task: Define required flows
    - [x] Interactive validation flow
    - [x] Calculation request flow
    - [x] Evidence export flow
    - [x] Deployment smoke-test flow
- [x] Task: Define trigger and output contracts
    - [x] Use manual or app-triggered flows for interactive paths
    - [x] Use scheduled or file-triggered flows only for synthetic demo paths
    - [x] Standardize diagnostics and correlation ID logging
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Flow Design' (Protocol in workflow.md)

## Phase 2: Flow Implementation

- [x] Task: Add flow assets to solution source
    - [x] Bind flows to custom connector connection reference
    - [x] Use environment variables for endpoint and fixture gate
    - [x] Avoid hard-coded secrets or real-data examples
- [x] Task: Validate flow behavior
    - [x] Run solution checker where available
    - [x] Run smoke flow in target environment when credentials exist
    - [x] Record blocked environment notes separately from code readiness
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Flow Implementation' (Protocol in workflow.md)
