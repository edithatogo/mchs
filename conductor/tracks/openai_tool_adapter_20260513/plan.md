# Plan: OpenAI Tool Adapter

## Phase 1: Adapter Boundary
- [x] Task: Define OpenAI tool adapter scope.
    - [x] Document why the domain API remains canonical.
    - [x] Document why the calculator does not emulate an LLM endpoint.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Adapter Boundary' (Protocol in workflow.md)

## Phase 2: Tool Definitions
- [x] Task: Generate tool definitions from canonical schemas.
    - [x] Include calculate, validate, explain, list, schema, and evidence tools.
    - [x] Add examples for successful, unsupported, and invalid requests.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Tool Definitions' (Protocol in workflow.md)

## Phase 3: Validation and Docs
- [x] Task: Add adapter validation and documentation.
    - [x] Assert outputs preserve diagnostics and provenance.
    - [x] Add usage examples for agent workflows.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation and Docs' (Protocol in workflow.md)
