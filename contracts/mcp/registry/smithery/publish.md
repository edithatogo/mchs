# Smithery Publication Runbook

Status: accepted as stdio MCPB release
`9eb5d712-5258-4d91-8eff-a0245bd40826` on 2026-05-26. The latest accepted
republish is `355669d7-72a9-441e-87de-4682260335cc`; unauthenticated public API
and cache-bypassed registry probes return that release with all six tools.
Search indexing remains stale and the hosted runtime URL is not claimed because
the Smithery listing is a stdio bundle (`remote=false`, `deploymentUrl=null`). Public metadata was refreshed on 2026-05-26 so the direct Smithery API record now has display name `MCHS`, an MCHS/NWAU description, homepage `https://github.com/edithatogo/mchs`, and license `MIT`. Upstream tracking: `https://github.com/smithery-ai/cli/issues/780`.

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
- `355669d7-72a9-441e-87de-4682260335cc`

After release `355669d7-72a9-441e-87de-4682260335cc`, the public API and a
cache-bypassed registry request returned bundle URL
`bc30c556-4078-4961-9d71-077bf535225f/355669d7-72a9-441e-87de-4682260335cc/server.mcpb`
and all six tools. Remaining unresolved surfaces are Smithery search indexing
and `https://mchs--edithatogo.run.tools`, which still returned `404` with
`x-smithery-error: server_not_found`; that runtime URL is expected to remain
unavailable for stdio bundle publication unless a hosted remote deployment is
configured.

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

## Public Discovery Closure

On 2026-05-26T01:41+10:00, unauthenticated public discovery was verified through
`https://api.smithery.ai/servers/edithatogo/mchs`. The response returned latest
release `355669d7-72a9-441e-87de-4682260335cc`, the refreshed MCPB bundle URL,
and all six MCHS tool schemas. The public Smithery page
`https://smithery.ai/servers/edithatogo/mchs` also included all six tool names.

The older `https://registry.smithery.ai/servers/edithatogo/mchs` path remained
Cloudflare-cached to the old zero-tool bundle, and the CLI-reported
`https://mchs--edithatogo.run.tools` URL still returned `404` with
`x-smithery-error: server_not_found`. Those surfaces are retained as stale
legacy/runtime observations, but they no longer block stdio bundle publication
or Smithery discovery because the public API, public page, and CLI connection
smoke all passed.

## Refreshed CLI Connection Smoke

On 2026-05-26, Smithery authentication was rechecked for organization
`org_01KNBP45KXPA0END8FASDT0PV1` and namespace `edithatogo`. A fresh
connection smoke using the default published command first exposed a local
machine issue: the shell resolved `python` to a conda interpreter with a
mismatched `pydantic` / `pydantic_core` install. The same Smithery connection
succeeded when the server was launched through the project environment:

```bash
smithery mcp add --id mchs-ci-smoke --namespace edithatogo --force -- uv run python -m nwau_py.mcp_server
smithery tool list mchs-ci-smoke --namespace edithatogo --flat --limit 100
smithery tool call mchs-ci-smoke mchs.list_calculators '{"year":"2026"}' --namespace edithatogo
```

The tool list returned all six MCHS tools, and the tool call succeeded with the
expected empty calculator list payload for 2026. `smithery mcp search mchs
--json` still returned unrelated results and did not include `edithatogo/mchs`,
so search indexing remains the only Smithery discovery caveat. Public API
discovery and direct CLI connection smoke remain the authoritative publication
evidence for the stdio bundle.

## Metadata Refresh

On 2026-05-26T02:42:54+10:00, the Smithery server metadata was updated through
`PATCH https://api.smithery.ai/servers/edithatogo%2Fmchs`. The direct server API
record now returns:

- Display name: `MCHS`
- Description: `Model Context Protocol server for MCHS/NWAU calculator discovery, schema lookup, request validation, calculation delegation, result explanation, and registry evidence.`
- Homepage: `https://github.com/edithatogo/mchs`
- License: `MIT`

This addresses the empty-description metadata defect on the direct listing.
`smithery mcp search mchs --json` still did not return `edithatogo/mchs`
immediately after the metadata refresh, so search indexing remains an upstream
or asynchronous Smithery surface rather than a local publication defect.
