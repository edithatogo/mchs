# Smithery MCP Registry Readiness Contract

Date created: 2026-05-17

## Purpose

Define the required product, runtime, security, and evidence conditions before
MCHS can be submitted to Smithery. Smithery URL publishing requires a public
HTTPS MCP server using Streamable HTTP, with OAuth support when authentication is
required.

## Current State

- `mchs-mcp` is published as a stdio MCP server through `nwau-py`.
- `mchs-mcp-http` provides a Streamable HTTP adapter over the same JSON-RPC
  dispatcher.
- Static scanner fallback metadata is available at
  `/.well-known/mcp/server-card.json` when the HTTP adapter is hosted.
- No public HTTPS endpoint or Smithery listing is currently claimed.

## Smithery Requirements Interpreted for MCHS

- The server must expose a public HTTPS MCP endpoint, expected path `/mcp`,
  using Streamable HTTP transport.
- If the public endpoint requires authentication, it must implement OAuth in a
  way Smithery can discover and complete. Unauthenticated scans must return
  `401 Unauthorized`, not `403 Forbidden`, when OAuth is required.
- Smithery scanning must discover tools, resources, prompts, and server metadata,
  or the hosted service must expose a static server card at
  `/.well-known/mcp/server-card.json`.
- WAF/CDN rules must not block Smithery scanner traffic. If a WAF is used,
  requests with user agent `SmitheryBot/1.0 (+https://smithery.ai)` must be
  allowed or the static server card must be available.
- Session configuration, if any, must be represented as JSON Schema and must not
  expose secrets or healthcare data.

## Required Implementation Deliverables

- A hosted Streamable HTTP adapter that wraps the existing `mchs-mcp` tool and
  resource contract without duplicating formula logic.
- A health and readiness route that proves the deployment is live without
  exposing patient-level data or secrets.
- A static server card at `/.well-known/mcp/server-card.json` containing server
  name, version, authentication posture, tool definitions, resource definitions,
  and no private healthcare content.
- Deployment documentation that names the hosting platform, public endpoint,
  auth behavior, WAF/CDN handling, and rollback procedure.
- Smithery publication instructions using either the Smithery UI URL flow or CLI
  equivalent: `smithery mcp publish "https://<host>/mcp" -n <namespace>`.

## Required Validation Evidence

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

- A public HTTPS Streamable HTTP endpoint exists and can be scanned.
- Smithery scan or static server-card metadata exposes the MCHS MCP capabilities
  accurately.
- Authentication behavior is explicit and Smithery-compatible.
- No formula logic is implemented in the HTTP adapter.
- No Smithery publication is claimed until a Smithery listing or submission
  record exists.
