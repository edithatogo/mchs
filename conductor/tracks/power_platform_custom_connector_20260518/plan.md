# Plan: Power Platform Custom Connector

## Phase 1: Connector Definition

- [x] Task: Generate OpenAPI and connector metadata
    - [x] Define operations for list calculators, get schema, validate input, calculate, explain result, and get evidence
    - [x] Mark optional parameters correctly
    - [x] Include clear non-endorsement and data-safety descriptions
- [x] Task: Define connector policy and security
    - [x] Map authentication scheme to the service boundary
    - [x] Define host/base URL environment variable binding
    - [x] Avoid hard-coded secrets or tenant IDs
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Connector Definition' (Protocol in workflow.md)

## Phase 2: Connector Packaging

- [x] Task: Create unpacked connector source files
    - [x] Add API properties and connection parameter assets
    - [x] Add icon and publisher metadata placeholders
    - [x] Add connector README and local import instructions
- [x] Task: Validate connector importability
    - [x] Run `pac connector` or solution import validation where available
    - [x] Record blocked credential/environment notes explicitly
    - [x] Add connector contract tests
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Connector Packaging' (Protocol in workflow.md)
