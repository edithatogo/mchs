# Plan: Power Platform Custom Connector

## Phase 1: Connector Definition

- [ ] Task: Generate OpenAPI and connector metadata
    - [ ] Define operations for list calculators, get schema, validate input, calculate, explain result, and get evidence
    - [ ] Mark optional parameters correctly
    - [ ] Include clear non-endorsement and data-safety descriptions
- [ ] Task: Define connector policy and security
    - [ ] Map authentication scheme to the service boundary
    - [ ] Define host/base URL environment variable binding
    - [ ] Avoid hard-coded secrets or tenant IDs
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Connector Definition' (Protocol in workflow.md)

## Phase 2: Connector Packaging

- [ ] Task: Create unpacked connector source files
    - [ ] Add API properties and connection parameter assets
    - [ ] Add icon and publisher metadata placeholders
    - [ ] Add connector README and local import instructions
- [ ] Task: Validate connector importability
    - [ ] Run `pac connector` or solution import validation where available
    - [ ] Record blocked credential/environment notes explicitly
    - [ ] Add connector contract tests
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Connector Packaging' (Protocol in workflow.md)
