# Plan: HTTP API Contract

## Phase 1: Resource Model
- [x] Task: Define API resources and endpoint semantics.
    - [x] Include calculators, schemas, validation, calculations, jobs, results, and evidence.
    - [x] Define sync and async execution behavior.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Resource Model' (Protocol in workflow.md)

## Phase 2: OpenAPI Contract
- [x] Task: Implement OpenAPI 3.1 specification.
    - [x] Reference canonical schemas.
    - [x] Add examples for pass, fail, and unsupported requests.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: OpenAPI Contract' (Protocol in workflow.md)

## Phase 3: Contract Tests
- [x] Task: Validate OpenAPI and examples in CI.
    - [x] Assert error and provenance consistency.
    - [x] Assert unsupported streams fail closed.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Contract Tests' (Protocol in workflow.md)
