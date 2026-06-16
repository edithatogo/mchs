# Docker MCP Registry Submission

Date prepared: 2026-05-24

## Candidate files

- `contracts/mcp/registry/docker/servers/mchs/server.yaml`
- `contracts/mcp/registry/docker/servers/mchs/tools.json`
- `contracts/mcp/registry/docker/servers/mchs/readme.md`

## Intended upstream PR placement

Copy the candidate directory to the Docker MCP Registry repository as:

```text
servers/mchs/
```

## Submission command sequence

```bash
git clone https://github.com/docker/mcp-registry.git
cp -R contracts/mcp/registry/docker/servers/mchs mcp-registry/servers/mchs
cd mcp-registry
task validate -- --name mchs
task build -- --tools mchs
```

Open a pull request against `docker/mcp-registry` with the validation output.

## Current status

Submitted to the upstream Docker MCP Registry.

- Active PR: https://github.com/docker/mcp-registry/pull/3799
- State observed on 2026-05-24: open, mergeable, review required.
- Superseded duplicate PR closed: https://github.com/docker/mcp-registry/pull/3595

Public Docker MCP Catalog or Docker Hub `mcp/mchs` publication is not claimed
until the upstream PR is reviewed, merged, and propagated by Docker.


## Latest local upstream validation

On 2026-05-24, the active candidate was copied into a fresh clone of
`docker/mcp-registry` and validated with:

```bash
go run ./cmd/validate --name mchs
```

Observed result:

```text
✅ Name is valid
✅ Directory is valid
✅ Title is valid
✅ YAML formatting is valid
✅ Commit is pinned
✅ Secrets are valid
✅ Config env is valid
✅ License is valid
✅ Icon is valid
✅ Remote validation skipped (not a remote server)
✅ OAuth dynamic configuration is valid
```

## Latest live observation

On 2026-06-16, PR https://github.com/docker/mcp-registry/pull/3799 remained open, not draft, `mergeable=MERGEABLE`, with `mergeStateStatus=BLOCKED`, `reviewDecision=REVIEW_REQUIRED`, no configured status checks, and no maintainer review. The branch had already been refreshed against current `docker/mcp-registry@main`, and a clean temporary checkout validation passed with `go run ./cmd/validate --name mchs`. Docker Catalog publication remains unclaimed until maintainer review, merge, and propagation complete.
