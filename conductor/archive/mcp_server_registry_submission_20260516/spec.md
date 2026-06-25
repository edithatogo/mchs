# Specification: MCP Server Readiness and Registry Submission

## Overview

Turn the completed MCP contract into a runnable, evidence-backed MCP server and
submit its metadata to appropriate MCP registries. The first supported runtime
is a local stdio server over the existing validated Python package. Docker is
optional and out of the initial submission path.

## Requirements

- Implement a thin MCP server that delegates to the current canonical Python
  runtime and contract schemas rather than duplicating formula logic.
- Expose the contracted MCP tools:
  `mchs.list_calculators`, `mchs.get_schema`, `mchs.validate_input`,
  `mchs.calculate`, `mchs.explain_result`, and `mchs.get_evidence`.
- Provide a local stdio entry point suitable for MCP clients.
- Add install and configuration documentation for local MCP client use.
- Add server metadata for public discovery, including name, version,
  description, package/install source, capabilities, support scope, license,
  security notes, and known limitations.
- Validate the server with contract-backed tests and at least one MCP client or
  protocol-level smoke test.
- Submit metadata to the official MCP Registry once a public installable server
  artifact exists.
- Submit or list with secondary discovery targets only when their requirements
  are met:
  - Glama for public open-source indexing and inspection.
  - Smithery if the server has Streamable HTTP or an MCPB bundle.
  - Docker MCP Registry only if a containerized distribution is intentionally
    added later.

## Acceptance Criteria

- A user can run the MCP server locally without Docker.
- The server exposes all contracted tools and resources with schema-compatible
  inputs and outputs.
- Tests prove no formula logic lives in the MCP server layer.
- Registry metadata points to a real public package, repository, or endpoint.
- Official MCP Registry submission is prepared and either completed or blocked
  by an explicit external-review/credential note.
- Glama and Smithery decisions are recorded with evidence.
- Docker is not required for the first MCP release.

## Out of Scope

- Docker-first distribution.
- Private healthcare deployments or private MCP registry operation.
- Hosted multi-tenant Streamable HTTP service unless added by a later track.
- Expanding validation claims beyond the currently supported calculator,
  runtime, and fixture scope.
