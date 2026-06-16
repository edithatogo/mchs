# Smithery MCP Registry Readiness Contract

Date created: 2026-05-17

## Purpose

Define the required product, runtime, security, and evidence conditions for
MCHS Smithery publication. The first accepted Smithery release is a local stdio
MCPB bundle; hosted URL publishing remains a separate optional future path that
requires a public HTTPS MCP server using Streamable HTTP, with OAuth support
when authentication is required.

## Current State

- `mchs-mcp` is published as a stdio MCP server through `nwau-py`.
- Official MCP Registry publication is complete for `io.github.edithatogo/mchs`
  version `0.2.2`.
- Smithery accepted the stdio MCPB release for `edithatogo/mchs` on
  2026-05-24 with deployment ID `200f2fd3-86c4-4122-b3bf-98abe5aa62f1`.
- No public hosted Streamable HTTP endpoint exists for the MCHS MCP server;
  hosted Streamable HTTP publication remains optional/future and is not claimed.

## Smithery Requirements Interpreted for MCHS

- The server must expose a public HTTPS MCP endpoint, expected path such as
  `/mcp`, using Streamable HTTP transport.
- If the public endpoint requires authentication, it must implement OAuth in a
  way Smithery can discover and complete. Unauthenticated scans must return
  `401 Unauthorized`, not `403 Forbidden`, when OAuth is required.
- Smithery scanning must be able to discover tools, resources, prompts, and
  server metadata, or the hosted service must expose a static server card at
  `/.well-known/mcp/server-card.json`.
- WAF/CDN rules must not block Smithery scanner traffic. If a WAF is used,
  requests with user agent `SmitheryBot/1.0 (+https://smithery.ai)` must be
  allowed or the static server card must be available.
- Session configuration, if any, must be represented as JSON Schema and must not
  expose secrets or healthcare data.

## Required Implementation Deliverables for Hosted HTTP

- A hosted Streamable HTTP adapter that wraps the existing `mchs-mcp` tool and
  resource contract without duplicating formula logic.
- A health and readiness route that proves the deployment is live without
  exposing patient-level data or secrets.
- A static server card at `/.well-known/mcp/server-card.json` containing:
  server name, version, authentication posture, tool definitions, resource
  definitions, and no private healthcare content.
- Deployment documentation that names the hosting platform, public endpoint,
  auth behavior, WAF/CDN handling, and rollback procedure.
- Smithery publication instructions using either the Smithery UI URL flow or
  CLI equivalent:
  `smithery mcp publish "https://<host>/mcp" -n <namespace>`.

## Required Validation Evidence for Hosted HTTP

- Contract tests proving the Streamable HTTP endpoint exposes the same MCP tools
  and resources as the stdio server.
- Smoke evidence for `initialize`, `tools/list`, and at least one read-only tool
  over Streamable HTTP.
- Static server-card validation against the published tool/resource contract.
- Security review evidence that the hosted service does not accept or persist
  patient-level data beyond the minimum request lifecycle required to answer the
  MCP call.
- Publication evidence containing the Smithery URL, namespace, submission date,
  scan result, and any manual metadata used.

## Acceptance Criteria

- Smithery stdio-bundle publication may be claimed only when the registry API,
  status URL, bundle path, and bundle checksum are recorded.
- Hosted HTTP publication may be claimed only when a public HTTPS Streamable
  HTTP endpoint exists and can be scanned.
- Smithery scan, bundle metadata, or static server-card metadata exposes the
  MCHS MCP capabilities accurately for the claimed publication path.
- Authentication behavior is explicit and Smithery-compatible for any hosted
  endpoint.
- No formula logic is implemented in the HTTP adapter or MCPB launcher.
- No Smithery publication is claimed until a Smithery listing or submission
  record exists.

## Out of Scope

- Multi-tenant healthcare hosting for production clinical workloads.
- Storing PHI, patient-level records, or institutional costing submissions.
- Replacing the official MCP Registry as the canonical registry of record.
