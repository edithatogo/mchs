# Docker MCP Registry Requirements Notes

Date checked: 2026-05-24

Sources:

- Docker MCP Catalog: https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/
- Docker MCP Toolkit CLI: https://docs.docker.com/ai/mcp-catalog-and-toolkit/cli/
- Docker MCP Registry: https://github.com/docker/mcp-registry

## Confirmed requirements

- Docker's MCP catalog is container-first. Local catalog servers run as isolated Docker containers, and accepted registry entries appear in Docker Desktop MCP Toolkit, Docker MCP Catalog, and, for Docker-built images, Docker Hub's `mcp` namespace.
- Docker supports local container servers and remote servers. The first MCHS path remains local container submission because the current MCHS server is stdio-oriented and does not yet expose a public remote endpoint.
- Docker documents two contribution shapes:
  - Docker-built image: preferred path; Docker builds, signs, publishes, and maintains the image after PR approval.
  - Self-provided image: contributor provides the already-built image; this is simpler for owner-managed images but does not receive Docker's Docker-built provenance/SBOM/signing treatment.
- A local YAML server descriptor can identify a server by `name`, `title`, `type: server`, `image`, and `description`; registry PR content should align with the upstream `servers/<server>/server.yaml` convention.
- Docker Desktop 4.62 or later is the documented CLI/UI baseline for current MCP Toolkit flows.
- Validation evidence should include at least container startup, MCP `initialize`, MCP `tools/list`, and any Docker registry validation command that is current when the PR is prepared.

## MCHS submission decision

- Use a Docker-built image candidate unless the upstream registry requires a self-provided image for this package.
- Keep runtime configuration empty unless a future tool requires credentials. The MCHS server must remain synthetic/public-data only for registry demos.
- Candidate server identity:
  - Name: `mchs`
  - Title: `MCHS Health Services Microcosting`
  - Category: `data-analysis`
  - Tags: `healthcare`, `microcosting`, `pricing`, `python`, `mcp`
  - Description: `Synthetic-data-safe MCP tools for Australian health-services microcosting, NWAU pricing, and validation workflows.`

## Remaining gate

The Dockerfile-backed runtime, smoke tests, registry candidate files, upstream
validation output, and active PR evidence now exist. The remaining deferred gate
is Docker review, merge, and Docker Catalog/Docker Hub `mcp/mchs` propagation;
no catalog publication is claimed before that evidence exists.
