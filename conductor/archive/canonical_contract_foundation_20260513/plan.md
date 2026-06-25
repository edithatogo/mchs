# Plan: Canonical Contract Foundation

This track fans out to 4 surface contracts in parallel (depth-2 subagents).
The canonical schemas are the dependency that all surface tracks require.

## Phase 1: Schema Inventory [sequential — must complete first]
- [x] Task: Inventory existing calculator, manifest, evidence, diagnostics, and provenance schemas.
    - [x] Identify canonical and derived schemas.
    - [x] Identify missing pass and fail fixtures.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Schema Inventory' (Protocol in workflow.md)

## Phase 2: Canonical Schema Set + Surface Fan-Out [depth-2 parallel]
- [x] Task: Implement versioned JSON Schema contracts.
    - [x] Add calculator request and response schemas.
    - [x] Add diagnostics, errors, provenance, support-status, and evidence schemas.
    - [x] Add derivation notes for OpenAPI and Arrow/Parquet.
- [x] Task (parallel subagents): Define surface contracts from canonical schemas.
    - [x] Subagent B2: CLI/File contract — commands, exit codes, manifests, examples.
    - [x] Subagent B3: HTTP API OpenAPI 3.1 — endpoints, sync/async, examples.
    - [x] Subagent B4: MCP contract — tools, resources, examples.
    - [x] Subagent B5: OpenAI tool adapter — tool definitions, examples, boundary docs.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Canonical Schema Set and Surface Fan-Out' (Protocol in workflow.md)

## Phase 3: Contract Validation
- [x] Task: Add schema validation tests.
    - [x] Add pass fixtures.
    - [x] Add fail-closed fixtures.
    - [x] Assert adapters cannot redefine formula logic.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Contract Validation' (Protocol in workflow.md)
