# MCP Registry Submission Decisions

Date created: 2026-05-17
Last updated: 2026-05-26

## Current Artifact

The first runnable MCP artifact is a stdio server launched with `mchs-mcp`.
Docker is not required.

## Registry Decisions

| Registry | Decision | Evidence |
| --- | --- | --- |
| Official MCP Registry | Published. | `mcp-publisher` published `io.github.edithatogo/mchs` version `0.2.2` on 2026-05-17; registry search API returns active/latest metadata for `io.github.edithatogo/mchs`; `nwau-py 0.2.2` is visible on PyPI. |
| Glama | Eligible through official-registry indexing; no separate authenticated submission completed from this environment. | Glama documentation states it is a superset of the official MCP Registry. Direct Glama API verification was blocked by its edge protection from this environment. |
| Smithery | Accepted stdio release; public API and metadata verified; search/runtime not claimed. | Smithery accepted stdio MCPB release `355669d7-72a9-441e-87de-4682260335cc` on 2026-05-26; unauthenticated public API and cache-bypassed registry discovery return all six tools, and direct listing metadata was refreshed with display name, description, homepage, and license. Search indexing and hosted `run.tools` runtime are not claimed for the stdio bundle, as recorded in `contracts/mcp/registry/smithery/accepted-release-20260526.json`. |
| Docker MCP Registry | Submitted by PR, not yet catalog-published. | `Dockerfile`, `scripts/smoke_mcp_container.py`, and `contracts/mcp/registry/docker/` provide the local containerized server candidate. Docker Registry metadata validation passed and PR `https://github.com/docker/mcp-registry/pull/3799` is open. Review feedback on `tools.json` was addressed in fork commit `f5fa706`. |

## Official MCP Registry Basis

Checked against the official MCP Registry documentation on 2026-05-17:

- The registry is still in preview, so release evidence must not overclaim
  permanent listing stability.
- PyPI packages use `"registryType": "pypi"` in `server.json`.
- Stdio package transports use `"transport": { "type": "stdio" }`.
- PyPI ownership verification requires the published package README to contain
  `mcp-name: $SERVER_NAME`; this project uses
  `mcp-name: io.github.edithatogo/mchs`.
- The GitHub namespace `io.github.edithatogo/mchs` is compatible with GitHub
  OIDC publication from the `edithatogo/mchs` repository.

## Release Execution

The concrete `v0.2.2` release sequence is recorded in
`contracts/mcp/registry/release-execution-v0.2.2.md`.

## Local Stdio Configuration

```json
{
  "mcpServers": {
    "mchs": {
      "command": "mchs-mcp",
      "args": []
    }
  }
}
```

For development from the repository checkout:

```bash
uv run mchs-mcp
```

## Publication Evidence

- GitHub release: `https://github.com/edithatogo/mchs/releases/tag/v0.2.2`
- PyPI package: `https://pypi.org/project/nwau-py/0.2.2/`
- Official MCP Registry search:
  `https://registry.modelcontextprotocol.io/v0/servers?search=io.github.edithatogo%2Fmchs`
- MCP Registry publish workflow:
  `https://github.com/edithatogo/mchs/actions/runs/25981730256`
- Smithery server page:
  `https://smithery.ai/servers/edithatogo/mchs`
- Smithery MCP URL:
  `https://mchs--edithatogo.run.tools`
- Docker MCP Registry PR:
  `https://github.com/docker/mcp-registry/pull/3799`

## Remaining Submission Blockers

- Smithery stdio release acceptance and public API/page discovery are complete
  for `edithatogo/mchs`. Do not claim search-index visibility or hosted
  `run.tools` runtime readiness unless Smithery later exposes those surfaces for
  this bundle. Upstream tracking: `https://github.com/smithery-ai/cli/issues/780`.
- Docker MCP Registry PR `https://github.com/docker/mcp-registry/pull/3799`
  must merge, or the catalog listing must be visible, before Docker MCP Catalog
  publication can be claimed.
