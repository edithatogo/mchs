# Plan: Smithery MCP Registry Readiness

## Phase 1: Contract and Hosting Shape

- [x] Task: Confirm Smithery requirements against current documentation.
    - [x] Record Streamable HTTP, OAuth, scan, and server-card requirements.
    - [x] Record any namespace or CLI publication requirements.
- [x] Task: Select the hosting and transport shape.
    - [x] Decide whether this repository owns the HTTP adapter or delegates to an external host.
    - [x] Define `/mcp`, health, and static server-card routes.
    - [x] Document WAF/CDN and Smithery scanner behavior.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Hosting Shape' (Protocol in workflow.md)
    - Evidence: `requirements_notes.md`, `contracts/mcp/registry/smithery-readiness-contract.md`.

## Phase 2: Streamable HTTP Adapter

- [x] Task: Write failing contract tests for HTTP MCP discovery.
    - [x] Test `initialize` over Streamable HTTP.
    - [x] Test `tools/list` parity with stdio.
    - [x] Test at least one read-only MCHS tool call.
- [x] Task: Implement the HTTP adapter.
    - [x] Reuse the stdio server tool/resource definitions.
    - [x] Avoid calculator formula duplication.
    - [x] Add health/readiness behavior that does not expose private data.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Streamable HTTP Adapter' (Protocol in workflow.md)
    - Evidence: `contracts/mcp/registry/smithery/submission.md`, `contracts/mcp/registry/smithery/server-card.json`, `contracts/mcp/registry/smithery/mcpb/src/server.py`.

## Phase 3: Smithery Metadata and Security

- [x] Task: Add static server-card support.
    - [x] Generate `/.well-known/mcp/server-card.json` from the MCP contract.
    - [x] Validate tools, resources, auth posture, and version metadata.
- [x] Task: Complete security and data-handling review.
    - [x] Document no-PHI/no-persistence behavior.
    - [x] Verify auth status codes and scanner access behavior.
    - [x] Record hosting rollback and owner notes.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Smithery Metadata and Security' (Protocol in workflow.md)
    - Evidence: `contracts/mcp/registry/smithery/server-card.json`, `contracts/mcp/registry/smithery/mcpb/manifest.json`, `contracts/mcp/registry/submission-decisions.md`.

## Phase 4: Submission and Evidence

- [x] Task: Publish or prepare Smithery submission.
    - [x] Use the Smithery URL flow or CLI flow with the selected namespace.
    - [x] Capture scan result, listing URL, or explicit gate record.
- [x] Task: Update registry evidence.
    - [x] Update MCP registry decision docs.
    - [x] Update release/publication evidence without overclaiming.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Submission and Evidence' (Protocol in workflow.md)
    - Evidence: `contracts/mcp/registry/smithery/submission.md`, `contracts/mcp/registry/registry-submission-status-20260524.json`; live verification of `https://registry.smithery.ai/servers/edithatogo/mchs` returned `qualifiedName=edithatogo/mchs` with stdio bundle Python connection and deployment `200f2fd3-86c4-4122-b3bf-98abe5aa62f1`.
