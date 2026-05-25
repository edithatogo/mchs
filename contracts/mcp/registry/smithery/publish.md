# Smithery Publication Runbook

Status: accepted as stdio MCPB release
`9eb5d712-5258-4d91-8eff-a0245bd40826` on 2026-05-26. A later
cache-bypassed registry probe returned release
`4824a436-6bb3-4fe7-bcd4-671d956924db` with all six tools, while the plain
CDN-cached registry URL and Smithery runtime URL still required caution.

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
- `4824a436-6bb3-4fe7-bcd4-671d956924db`

After release `4824a436-6bb3-4fe7-bcd4-671d956924db`, a cache-bypassed
registry request returned bundle URL
`bc30c556-4078-4961-9d71-077bf535225f/4824a436-6bb3-4fe7-bcd4-671d956924db/server.mcpb`
and all six tools. Remaining unresolved surfaces are the plain CDN-cached
registry endpoint and `https://mchs--edithatogo.run.tools`, which still returned
`404` with `x-smithery-error: server_not_found`.

## Connection Smoke Evidence

On 2026-05-26T01:06:00+10:00, a temporary Smithery connection
`mchs-ci-smoke` was created in namespace `edithatogo` using the published
`edithatogo/mchs` bundle. The first attempt exposed a local shell issue: the
machine default conda Python had a mismatched `pydantic` / `pydantic_core`
install. Retrying with the project `uv` environment first on `PATH` initialized
successfully.

Successful smoke evidence:

- `smithery tool list mchs-ci-smoke --namespace edithatogo --flat --limit 100`
  returned all six MCHS tools.
- `smithery tool call mchs-ci-smoke mchs.list_calculators '{"year":"2026"}'
  --namespace edithatogo --json` succeeded with the expected empty list payload
  for that year.
- The temporary connection `mchs-ci-smoke` was removed after the smoke test.

This confirms Smithery can connect to and execute the stdio bundle through the
CLI when the local Python environment is healthy. It does not close the separate
plain CDN cache or `https://mchs--edithatogo.run.tools` runtime URL issue.
