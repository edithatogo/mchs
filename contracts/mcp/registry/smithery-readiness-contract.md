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
- Smithery accepted local stdio MCPB releases for `edithatogo/mchs`; deployment ID `200f2fd3-86c4-4122-b3bf-98abe5aa62f1` and MCPB SHA256 `de353472d4a88848a9cb69fe1376f3d22deca97c72ca264d49eba1f09c056456` are recorded.
- Public registry backend propagation is verified through unauthenticated public API and cache-bypassed registry requests returning release `355669d7-72a9-441e-87de-4682260335cc` with all six MCHS tools. Smithery search indexing and hosted runtime URL resolution remain unresolved/not claimed for the stdio bundle, so search/runtime completion must not be overclaimed. The public HTTPS deliverables below still apply to URL-based Smithery publication and hosted scanner workflows.

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

- A Smithery stdio MCPB listing exists and public listing/runtime propagation is
  verified, or a public HTTPS Streamable HTTP endpoint exists and can be
  scanned, with any cache/propagation delay recorded explicitly.
- Smithery scan or static server-card metadata exposes the MCHS MCP capabilities
  accurately.
- Authentication behavior is explicit and Smithery-compatible.
- No formula logic is implemented in the HTTP adapter.
- No Smithery publication is claimed until a Smithery listing or submission
  record exists.

## 2026-05-26 Connection Smoke Update

A temporary Smithery connection smoke test passed for the published
`edithatogo/mchs` stdio bundle when the local command used the project `uv`
environment. Tool listing returned all six MCHS tools and a read-only
`mchs.list_calculators` call succeeded. The temporary connection was removed
after the test. This narrows Smithery readiness risk to the plain CDN-cached
registry URL and the CLI-reported `run.tools` runtime URL; it no longer indicates
a bundle/tool-schema execution failure.

## 2026-05-26 Public Discovery Closure

Unauthenticated public discovery is verified through
`https://api.smithery.ai/servers/edithatogo/mchs`, which returns latest release
`355669d7-72a9-441e-87de-4682260335cc` and all six MCHS tools. The public Smithery page also exposes the tool
names. The legacy `registry.smithery.ai` endpoint and the CLI-reported
`run.tools` URL remain stale, but they are no longer treated as blocking for the
stdio MCPB publication path because public API discovery, page discovery, and
CLI connection smoke all passed.
