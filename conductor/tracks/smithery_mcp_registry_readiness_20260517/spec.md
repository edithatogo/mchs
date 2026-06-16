# Specification: Smithery MCP Registry Readiness

## Overview

Prepare MCHS for Smithery publication without overclaiming the current stdio
release. Smithery can publish a local stdio MCPB bundle or a public URL-based
MCP server using Streamable HTTP, with OAuth support if authentication is
required. This track records the completed stdio-bundle publication and keeps
hosted Streamable HTTP publication as an optional/future gate while preserving
the existing rule that the MCP adapter must not duplicate calculator formula
logic.

## Functional Requirements

- Package a local stdio MCPB bundle or implement/configure a Streamable HTTP
  MCP adapter for the existing MCHS MCP tools and resources.
- For the hosted HTTP path, serve a public HTTPS `/mcp` endpoint suitable for
  Smithery URL publishing.
- Provide `/.well-known/mcp/server-card.json` as static metadata for Smithery
  bundle/hosted publication evidence.
- Define authentication behavior explicitly; unauthenticated protected endpoints
  must return `401`, not `403`, when OAuth discovery is expected.
- Record the Smithery namespace, endpoint URL, submission method, scan result,
  and listing URL when publication is attempted.

## Non-Functional Requirements

- No PHI, patient-level records, confidential costing submissions, or private
  archives may be stored by the hosted service.
- The HTTP adapter must delegate to the canonical runtime and existing MCP
  contract.
- The endpoint must be deployable and rollbackable with documented operational
  ownership.
- WAF/CDN configuration must not block Smithery scanning or must be bypassed by
  the static server card.

## Acceptance Criteria

- `contracts/mcp/registry/smithery-readiness-contract.md` is met.
- Stdio bundle evidence or Streamable HTTP smoke tests cover discovery and at
  least one read-only MCHS capability for the claimed publication path.
- Static server-card metadata is generated and validated against the tool and
  resource contract.
- Smithery publication evidence exists, or an explicit external gate record is
  recorded without claiming publication.

## Out of Scope

- Docker MCP Registry submission.
- Production clinical hosting.
- Expanding calculator validation claims beyond existing support evidence.
