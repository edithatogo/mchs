# Specification: Docker MCP Registry Readiness

## Overview

Prepare MCHS for Docker MCP Registry and Docker MCP Catalog submission. The
current MCP server is stdio-first through PyPI, so this track creates the
containerized distribution and Docker Registry metadata required before Docker
publication can be claimed.

## Functional Requirements

- Add a reproducible Docker deployment path for `mchs-mcp`.
- Keep the final runtime image minimal and free of private healthcare data,
  source archives, tests, and unnecessary build tooling.
- Add container smoke tests for MCP `initialize` and `tools/list` over stdio.
- Prepare Docker MCP Registry submission files for the local server path:
  `server.yaml`, optional `tools.json`, and documentation/readme content.
- Validate the submission in a fork/checkout of `docker/mcp-registry` using its
  current validation commands.
- Record the Docker Registry PR URL or explicit gate record.

## Non-Functional Requirements

- Prefer the Docker-built image path so Docker can provide signatures,
  provenance, SBOMs, and automatic updates.
- Do not require secrets for server discovery or metadata calls.
- Do not claim Docker Catalog publication until Docker review/merge evidence
  exists.
- Preserve the canonical calculator runtime boundary and avoid formula logic in
  container wrappers.

## Acceptance Criteria

- `contracts/mcp/registry/docker-mcp-registry-readiness-contract.md` is met.
- Docker build succeeds from a clean checkout.
- Container smoke tests prove MCP discovery works.
- Docker MCP Registry candidate files validate in Docker's registry tooling.
- A Docker MCP Registry PR or documented gate record exists.

## Out of Scope

- Smithery publication.
- Production healthcare hosting.
- Self-provided Docker Hub publication unless the Docker-built path is rejected
  or explicitly changed by a later decision.
