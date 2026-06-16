# Docker MCP Registry Readiness Contract

Date created: 2026-05-17

## Purpose

Define the required runtime, image, metadata, security, and submission evidence
for MCHS Docker MCP Registry submission and Docker MCP Catalog publication. The
current completed state is submission-ready/review-pending; Docker Catalog
publication is not claimed until Docker review, merge, and propagation complete.

## Current State

- `mchs-mcp` is published through `nwau-py` as a local stdio server.
- A Dockerfile-backed local container path exists in this repository.
- Docker MCP Registry PR `https://github.com/docker/mcp-registry/pull/3799`
  is open and review-pending.
- Docker Catalog publication is not claimed. Docker Hub `mcp/mchs`
  publication is also not claimed.

## Docker MCP Registry Requirements Interpreted for MCHS

Docker accepts two relevant submission shapes:

- Local containerized MCP server: source repository includes a Dockerfile,
  Docker can build the server image, and the registry PR adds a
  `servers/<name>/server.yaml` entry. Docker-built images are preferred because
  Docker can provide signatures, provenance, SBOMs, and automatic updates.
- Remote MCP server: a public HTTPS endpoint already exists and communicates via
  `streamable-http` or `sse`, with `server.yaml`, `tools.json`, and `readme.md`
  in the Docker MCP Registry PR.

For MCHS, the preferred first Docker path is the local containerized server
because the existing artifact is a local stdio MCP server.

## Required Implementation Deliverables

- A Dockerfile that installs the published package or repository checkout and
  runs `mchs-mcp` as the default command.
- A minimal runtime image with no bundled private healthcare data, no test
  archives, and no unnecessary build tooling in the final layer.
- Container smoke tests proving the image can start and respond to MCP
  `initialize` and `tools/list` over stdio.
- A Docker MCP Registry candidate entry under the expected upstream shape:
  `servers/mchs/server.yaml`.
- A `tools.json` file for Docker Registry fallback if the automated Docker build
  cannot list tools without configuration.
- A `readme.md` or documentation link suitable for the Docker Registry PR.
- Submission documentation for the Docker Registry PR, including category,
  tags, title, description, source project URL, pinned commit, and config
  behavior.

## Required Docker Metadata

The candidate `server.yaml` must include, at minimum:

- `name`: `mchs` or an agreed Docker-safe variant.
- `image`: Docker-built target such as `mcp/mchs` unless a self-provided image is
  intentionally chosen.
- `type`: `server` for the local containerized path.
- `meta.category`: a category appropriate for healthcare analytics, data, or
  developer tooling depending on Docker's accepted taxonomy.
- `meta.tags`: include `mcp`, `healthcare`, `analytics`, `nwau`, and
  `calculator` if accepted by Docker review.
- `about.title`: `MCHS NWAU Calculator MCP` or equivalent.
- `about.description`: a conservative description that avoids clinical or
  official-government endorsement claims.
- `about.source.project`: `https://github.com/edithatogo/mchs`.
- `about.source.commit`: the commit used for the submission.
- `config`: omit secrets and environment variables unless a future deployment
  adds real configuration knobs.

## Required Validation Evidence

- Docker build succeeds from a clean checkout.
- Containerized stdio smoke test succeeds for `initialize` and `tools/list`.
- Generated or hand-authored Docker Registry `server.yaml` validates in the
  Docker MCP Registry repository using its `task validate -- --name mchs`
  command or current equivalent.
- Docker Registry build/list-tools validation succeeds using
  `task build -- --tools mchs`, or `tools.json` is supplied with a documented
  reason.
- Pull request URL and review status are recorded before any Docker Catalog
  publication claim is made.

## Acceptance Criteria

- The repository has a reproducible Docker deployment path for `mchs-mcp`.
- The container does not require secrets for discovery or read-only metadata
  calls.
- Docker Registry submission files exist and are validated against Docker's
  current tooling.
- The Docker MCP Registry PR is opened or an explicit gate record is recorded.
- No Docker MCP Catalog or Docker Hub `mcp` namespace publication is claimed
  until Docker review/merge evidence exists.

## Out of Scope

- Production healthcare hosting.
- Self-provided image publication unless Docker-built submission is rejected or
  explicitly deprioritized.
- Bundling private source archives, PHI, or institutional costing data into the
  image.
