# Smithery Publication Runbook

Status: accepted as stdio MCPB release
`9eb5d712-5258-4d91-8eff-a0245bd40826` on 2026-05-26, with public
registry/runtime propagation still unresolved.

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
Release ID: 9eb5d712-5258-4d91-8eff-a0245bd40826
MCP URL: https://mchs--edithatogo.run.tools
Server Page: https://smithery.ai/servers/edithatogo/mchs
```

The published bundle uses the Python MCPB runtime shape and explicit tool
`inputSchema` metadata for all six tools. The Streamable HTTP adapter remains
available for a future public HTTPS deployment, but Smithery publication is no
longer blocked on hosting.

Bundle SHA-256:
`bfb8a18041fdc7a601165ecef3f2dfe15280450777dd732b05516b4b88c3a38d`

Evidence:
`contracts/mcp/registry/smithery/accepted-release-20260526.json`

As of 2026-05-26T00:32:00+10:00, Smithery accepted a republished MCPB
release, but the unauthenticated public registry API still returned a
Cloudflare-cached prior bundle with zero tools and the Smithery MCP URL returned
`404` with `x-smithery-error: server_not_found`. Do not claim public registry
API propagation or runtime URL readiness until a later observation shows
release `9eb5d712-5258-4d91-8eff-a0245bd40826` or equivalent refreshed
metadata and a resolvable runtime surface. External tracking issue:
`https://github.com/edithatogo/mchs/issues/151`.

Additional authenticated republish attempts on 2026-05-26 were also accepted:

- `54be0e8b-a018-4fb1-b76f-3b89ff3e6ccd`
- `06472680-7f3b-4a68-a56c-ed5a909e06be`

Post-republish probes still showed unresolved public surfaces: the plain
registry endpoint remained cached to an older zero-tool bundle, CLI search did
not return `edithatogo/mchs`, and `https://mchs--edithatogo.run.tools` still
returned `404` with `x-smithery-error: server_not_found`.
