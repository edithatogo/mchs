# Docker MCP Registry Readiness Contract

Date created: 2026-05-17

## Purpose

Define the required runtime, image, metadata, security, and submission evidence
before MCHS can be submitted to the Docker MCP Registry and Docker MCP Catalog.

## Current State

- `mchs-mcp` is published through `nwau-py` as a local stdio server.
- `Dockerfile` provides a containerized stdio runtime candidate.
- `contracts/mcp/registry/docker/` contains candidate Docker Registry metadata.
- No Docker MCP Registry PR, Docker Catalog listing, or Docker Hub `mcp` image is
  currently claimed.

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

- A Dockerfile that installs the repository checkout and runs `mchs-mcp` as the
  default command.
- A minimal runtime image with no bundled private healthcare data, no test
  archives, and no unnecessary build tooling in the final layer.
- Container smoke tests proving the image can start and respond to MCP
  `initialize` and `tools/list` over stdio.
- A Docker MCP Registry candidate entry under the expected upstream shape:
  `servers/mchs/server.yaml`.
- A `tools.json` file for Docker Registry fallback if the automated Docker build
  cannot list tools without configuration.
- A `readme.md` or documentation link suitable for the Docker Registry PR.
- Submission documentation for the Docker Registry PR, including category, tags,
  title, description, source project URL, pinned commit, and config behavior.
- The candidate `about.source.commit` value must be replaced with the exact
  submission commit before opening the upstream Docker MCP Registry PR.

## Required Validation Evidence

- Docker build succeeds from a clean checkout.
- Containerized stdio smoke test succeeds for `initialize` and `tools/list`.
- Generated or hand-authored Docker Registry `server.yaml` validates in the
  Docker MCP Registry repository using `task validate -- --name mchs` or current
  equivalent.
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
- The Docker MCP Registry PR is opened or an explicit blocker is recorded.
- No Docker MCP Catalog or Docker Hub `mcp` namespace publication is claimed
  until Docker review/merge evidence exists.
