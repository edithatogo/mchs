# Specification: Smithery MCP Registry Readiness

## Overview

Prepare MCHS for Smithery publication without overclaiming the current stdio
release. Smithery requires a public URL-based MCP server using Streamable HTTP,
with OAuth support if authentication is required. This track implements the
repository-side readiness path while preserving the existing rule that the MCP
adapter must not duplicate calculator formula logic.

## Functional Requirements

- Implement a Streamable HTTP MCP adapter for the existing MCHS MCP tools and
  resources.
- Provide a `POST /mcp` endpoint suitable for public HTTPS hosting and Smithery
  URL publishing.
- Provide `/.well-known/mcp/server-card.json` as static metadata fallback for
  Smithery scanning.
- Define authentication behavior explicitly; the current public discovery shape
  requires no authentication for metadata calls.
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

- `contracts/mcp/registry/smithery-readiness-contract.md` is met for repository
  readiness.
- Streamable HTTP dispatcher covers `initialize`, `tools/list`, and read-only
  MCHS tool discovery through the shared MCP handler.
- Static server-card metadata is generated from the tool and resource contract.
- Smithery publication evidence exists, or an explicit external blocker is
  recorded without claiming publication.

## Out of Scope

- Docker MCP Registry submission.
- Production clinical hosting.
- Expanding calculator validation claims beyond existing support evidence.
