# Smithery Publication Runbook

Status: published as stdio MCPB release `73c5a62b-a82a-49bd-be46-7f26dca1ae12` on 2026-05-24.

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
Release ID: 73c5a62b-a82a-49bd-be46-7f26dca1ae12
MCP URL: https://mchs--edithatogo.run.tools
Server Page: https://smithery.ai/servers/edithatogo/mchs
```

The published bundle uses the Python MCPB runtime shape and explicit tool
`inputSchema` metadata for all six tools. The Streamable HTTP adapter remains
available for a future public HTTPS deployment, but Smithery publication is no
longer blocked on hosting.
