# Plan: Smithery MCP Registry Readiness

## Phase 1: Contract and Hosting Shape

- [x] Task: Confirm Smithery requirements against current documentation.
    - [x] Record Streamable HTTP, OAuth, scan, and server-card requirements.
    - [x] Record CLI publication requirements.
- [x] Task: Select the hosting and transport shape.
    - [x] Define this repository as owner of the HTTP adapter.
    - [x] Define `/mcp`, health, and static server-card routes.
    - [x] Document WAF/CDN and Smithery scanner behavior.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Hosting Shape' (Protocol in workflow.md)

## Phase 2: Streamable HTTP Adapter

- [x] Task: Write contract tests for HTTP MCP discovery.
    - [x] Test server-card tool parity.
    - [x] Test HTTP JSON-RPC dispatch parity with stdio handler.
- [x] Task: Implement the HTTP adapter.
    - [x] Reuse the stdio server tool/resource definitions.
    - [x] Avoid calculator formula duplication.
    - [x] Add health/readiness behavior that does not expose private data.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Streamable HTTP Adapter' (Protocol in workflow.md)

## Phase 3: Smithery Metadata and Security

- [x] Task: Add static server-card support.
    - [x] Generate `/.well-known/mcp/server-card.json` from the MCP contract at runtime.
    - [x] Validate tools, resources, auth posture, and version metadata in tests.
- [x] Task: Complete security and data-handling review.
    - [x] Document no-PHI/no-persistence behavior.
    - [x] Verify no auth is required for discovery metadata.
    - [x] Record hosting and publication runbook notes.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Smithery Metadata and Security' (Protocol in workflow.md)

## Phase 4: Submission and Evidence

- [x] Task: Prepare Smithery submission.
    - [x] Add Smithery URL flow command and selected namespace.
    - [x] Record that public HTTPS hosting is still required before submission.
- [x] Task: Update registry evidence.
    - [x] Update MCP registry decision docs.
    - [x] Update release/publication evidence without overclaiming.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Submission and Evidence' (Protocol in workflow.md)
