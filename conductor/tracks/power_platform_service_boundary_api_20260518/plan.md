# Plan: Power Platform Service Boundary API

## Phase 1: API Contract Freeze

- [ ] Task: Map Power Platform request and response schemas
    - [ ] Use public calculator contract fields
    - [ ] Include diagnostics, provenance, support status, and correlation IDs
    - [ ] Reject patient-level example payloads in committed assets
- [ ] Task: Define authentication and authorization boundary
    - [ ] Choose API key, Entra ID, managed identity, or gateway auth
    - [ ] Document NSW tenant requirements
    - [ ] Define audit-safe logging fields
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: API Contract Freeze' (Protocol in workflow.md)

## Phase 2: Service Implementation

- [ ] Task: Implement or select deployable service host
    - [ ] Expose `/healthz`, schema, validate, calculate, and evidence endpoints
    - [ ] Delegate formula behavior to canonical runtime only
    - [ ] Return Power Platform-friendly error objects
- [ ] Task: Add service validation
    - [ ] Add synthetic contract tests
    - [ ] Add OpenAPI schema validation
    - [ ] Add no-formula-duplication checks
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Service Implementation' (Protocol in workflow.md)
