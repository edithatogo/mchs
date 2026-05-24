# Specification: Smithery MCP Registry Readiness

## Overview

Prepare MCHS for Smithery publication without overclaiming the current stdio
release. Smithery requires a public URL-based MCP server using Streamable HTTP,
with OAuth support if authentication is required. This track defines and builds
that readiness path while preserving the existing rule that the MCP adapter must
not duplicate calculator formula logic.

## Functional Requirements

- Implement or configure a Streamable HTTP MCP adapter for the existing MCHS MCP
  tools and resources.
- Serve a public HTTPS `/mcp` endpoint suitable for Smithery URL publishing.
- Provide `/.well-known/mcp/server-card.json` as a static metadata fallback for
  Smithery scanning.
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
- Streamable HTTP smoke tests cover `initialize`, `tools/list`, and one
  read-only MCHS tool.
- Static server-card metadata is generated and validated against the tool and
  resource contract.
- Smithery publication evidence exists, or an explicit external gate record is
  recorded without claiming publication.

## Out of Scope

- Docker MCP Registry submission.
- Production clinical hosting.
- Expanding calculator validation claims beyond existing support evidence.
