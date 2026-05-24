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

Prepared locally. Public Docker MCP Catalog publication is not claimed until the
Docker MCP Registry PR is opened, reviewed, and merged.
