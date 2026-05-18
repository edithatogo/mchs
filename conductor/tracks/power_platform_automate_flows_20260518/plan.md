# Plan: Power Automate Orchestration Flows

## Phase 1: Flow Design

- [ ] Task: Define required flows
    - [ ] Interactive validation flow
    - [ ] Calculation request flow
    - [ ] Evidence export flow
    - [ ] Deployment smoke-test flow
- [ ] Task: Define trigger and output contracts
    - [ ] Use manual or app-triggered flows for interactive paths
    - [ ] Use scheduled or file-triggered flows only for synthetic demo paths
    - [ ] Standardize diagnostics and correlation ID logging
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Flow Design' (Protocol in workflow.md)

## Phase 2: Flow Implementation

- [ ] Task: Add flow assets to solution source
    - [ ] Bind flows to custom connector connection reference
    - [ ] Use environment variables for endpoint and fixture gate
    - [ ] Avoid hard-coded secrets or real-data examples
- [ ] Task: Validate flow behavior
    - [ ] Run solution checker where available
    - [ ] Run smoke flow in target environment when credentials exist
    - [ ] Record blocked environment notes separately from code readiness
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Flow Implementation' (Protocol in workflow.md)
