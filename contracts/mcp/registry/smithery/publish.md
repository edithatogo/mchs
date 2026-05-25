# Smithery Publication Runbook

Status: published as stdio MCPB release `2a0fd6ee-fe03-4c28-9ad0-b4665c71adc9` on 2026-05-25.

## Endpoint

The Smithery-ready adapter runs the existing MCHS MCP JSON-RPC dispatcher over
HTTP:

```bash
mchs-mcp-http --host 0.0.0.0 --port 8765
```

Routes:

- `POST /mcp`: Streamable HTTP JSON-RPC endpoint.
- `GET /healthz`: public readiness probe with no private data.
- `GET /.well-known/mcp/server-card.json`: static server-card metadata for
  Smithery scanner fallback.

## Publication Evidence

Smithery accepted a local stdio MCPB bundle after authentication for namespace
`edithatogo`.

```text
Release ID: 2a0fd6ee-fe03-4c28-9ad0-b4665c71adc9
MCP URL: https://mchs--edithatogo.run.tools
Server Page: https://smithery.ai/servers/edithatogo/mchs
Bundle SHA-256: `bfb8a18041fdc7a601165ecef3f2dfe15280450777dd732b05516b4b88c3a38d`
Evidence: `contracts/mcp/registry/smithery/accepted-release-20260525.json`
```

The published bundle uses the Python MCPB runtime shape and explicit tool
`inputSchema` metadata for all six tools. The Streamable HTTP adapter remains
available for a future public HTTPS deployment, but Smithery publication is no
longer blocked on hosting.

As of 2026-05-25T23:28:00+10:00, Smithery accepted the refreshed MCPB release, but the unauthenticated public registry API still returned a Cloudflare-cached prior deployment. Do not claim public registry API propagation until a later observation shows deployment `2a0fd6ee-fe03-4c28-9ad0-b4665c71adc9` or equivalent refreshed metadata.
