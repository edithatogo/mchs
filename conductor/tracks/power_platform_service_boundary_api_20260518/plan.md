# Plan: Power Platform Service Boundary API

## Phase 1: API Contract Freeze

- [x] Task: Map Power Platform request and response schemas
    - [x] Use public calculator contract fields
    - [x] Include diagnostics, provenance, support status, and correlation IDs
    - [x] Reject patient-level example payloads in committed assets
- [x] Task: Define authentication and authorization boundary
    - [x] Choose API key, Entra ID, managed identity, or gateway auth
    - [x] Document NSW tenant requirements
    - [x] Define audit-safe logging fields
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: API Contract Freeze' (Protocol in workflow.md)

## Phase 2: Service Implementation

- [x] Task: Implement or select deployable service host
    - [x] Expose `/healthz`, schema, validate, calculate, and evidence endpoints
    - [x] Delegate formula behavior to canonical runtime only
    - [x] Return Power Platform-friendly error objects
- [x] Task: Add service validation
    - [x] Add synthetic contract tests
    - [x] Add OpenAPI schema validation
    - [x] Add no-formula-duplication checks
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Service Implementation' (Protocol in workflow.md)
