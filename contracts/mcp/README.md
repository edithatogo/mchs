# MCHS MCP Contract

This directory defines the Model Context Protocol (MCP) surface contract for the Micro-Costing Health Services (MCHS) system. MCP enables AI assistants to discover and interact with micro-costing calculators, run calculations, and retrieve evidence.

## Documents

| File | Description |
|---|---|
| `tools.md` | MCP tool definitions for calculator operations |
| `resources.md` | MCP resource definitions for schemas, support status, and evidence |
| `examples/` | Pass, fail, and unsupported request/response examples |
| `registry/server.json` | Published public registry metadata for the stdio MCP server |
| `registry/submission-decisions.md` | Registry submission decisions and publication evidence |

## Design Principles

- All tool input/output shapes conform to the canonical JSON Schemas in `contracts/canonical/`.
- Tools are idempotent where possible.
- Resources are read-only and represent static or semi-static data.
- No formula logic is exposed — tools delegate to the canonical calculation engine.

## Registry Publication Targets

This directory is the MCP contract and registry evidence for the published
stdio MCP server. The runnable server artifact is the `mchs-mcp` console script
included in `nwau-py` beginning with version `0.2.2`.

When a server exists, use this registry order:

| Target | Use when | Status for MCHS |
| --- | --- | --- |
| Official MCP Registry (`registry.modelcontextprotocol.io`) | Public server metadata is ready and points to a public package, container, or remote endpoint. This is the canonical MCP metadata registry. | Published as `io.github.edithatogo/mchs` version `0.2.2`. |
| Docker MCP Registry / Docker MCP Catalog | The server has a Docker deployment path and should be discoverable through Docker Desktop and Docker Hub tooling. | Submitted to Docker MCP Registry in PR `https://github.com/docker/mcp-registry/pull/3595`; catalog publication remains unclaimed until merge or visible listing evidence exists. |
| Glama | The server is open source or publicly reachable and should be indexed, inspected, and tested through a public discovery layer. | Eligible through official MCP Registry indexing; no separate authenticated submission is recorded. |
| Smithery | The server exposes Streamable HTTP with OAuth where required, or ships a local MCPB bundle for stdio distribution. | Readiness implementation exists through `mchs-mcp-http` and `contracts/mcp/registry/smithery/`; submission remains unclaimed until public HTTPS hosting and Smithery scan/listing evidence exist. |

Private or restricted healthcare deployments should use a private registry or
internal catalog instead of the public official MCP Registry.

## Local Stdio Server

The first runnable server shape is stdio. It can be launched without Docker:

```bash
uv run mchs-mcp
```

MCP client configuration:

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

The server exposes the contracted tools and resources while preserving the
boundary that formula logic belongs in the canonical runtime, not the MCP
adapter.

## Streamable HTTP Adapter for Smithery

The Smithery-ready transport adapter wraps the same MCP JSON-RPC dispatcher over
HTTP:

```bash
mchs-mcp-http --host 0.0.0.0 --port 8765
```

Routes:

| Route | Purpose |
| --- | --- |
| `POST /mcp` | Streamable HTTP JSON-RPC endpoint for MCP clients and Smithery URL publication. |
| `GET /healthz` | Public readiness probe with no private healthcare data. |
| `GET /.well-known/mcp/server-card.json` | Static server-card metadata for Smithery scanner fallback. |

Smithery publication must not be claimed until this adapter is reachable through
public HTTPS and Smithery scan/listing evidence is recorded.

## Docker MCP Registry Candidate

The Docker-ready local server path is represented by:

- `Dockerfile`
- `.dockerignore`
- `scripts/smoke_mcp_container.py`
- `contracts/mcp/registry/docker/server.yaml`
- `contracts/mcp/registry/docker/tools.json`
- `contracts/mcp/registry/docker/readme.md`

Docker MCP Registry metadata validation passed and PR
`https://github.com/docker/mcp-registry/pull/3595` is open. Docker MCP Catalog
publication must not be claimed until merge or visible listing evidence is
recorded.
