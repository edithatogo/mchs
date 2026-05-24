# MCP Registry Submission Decisions

Date: 2026-05-17

## Current Artifact

The first runnable MCP artifact is a stdio server launched with `mchs-mcp`.
Docker is not required.

## Registry Decisions

| Registry | Decision | Evidence |
| --- | --- | --- |
| Official MCP Registry | Published. | `mcp-publisher` published `io.github.edithatogo/mchs` version `0.2.2` on 2026-05-17; registry search API returns active/latest metadata for `io.github.edithatogo/mchs`; `nwau-py 0.2.2` is visible on PyPI. |
| Glama | Eligible through official-registry indexing; no separate authenticated submission completed from this environment. | Glama documentation states it is a superset of the official MCP Registry. Direct Glama API verification was blocked by its edge protection from this environment. |
| Smithery | Prepared; submission pending authenticated Smithery publication. | `mchs-mcp-http`, static server-card metadata, and MCPB manifest candidate exist. A live Smithery listing is not claimed until a public HTTPS endpoint or MCPB bundle is submitted through an authenticated Smithery account. |
| Docker MCP Registry | Prepared; upstream PR pending. | Dockerfile and Docker MCP Registry candidate files exist under `contracts/mcp/registry/docker/`. Docker Catalog publication is not claimed until the upstream Docker MCP Registry PR is opened, reviewed, and merged. |

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

## Secondary Registry Submission Preparation

- Smithery preparation: `contracts/mcp/registry/smithery/submission.md`.
- Docker MCP Registry preparation:
  `contracts/mcp/registry/docker/submission.md`.
- Secondary registry listing publication requires authenticated external
  submission and registry review.
