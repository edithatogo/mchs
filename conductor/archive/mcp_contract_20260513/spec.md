# Specification: MCP Contract

## Overview

Define a Rust-backed MCP server contract for agent-facing calculator use. MCP is
an adapter over canonical schemas and the domain API; it must not become a
separate calculator contract.

## Requirements

- Define tools: `mchs.list_calculators`, `mchs.get_schema`,
  `mchs.validate_input`, `mchs.calculate`, `mchs.explain_result`, and
  `mchs.get_evidence`.
- Define resources for schemas, support status, evidence bundles, and public
  documentation links.
- Reuse canonical request, response, diagnostics, errors, and provenance.
- Include pass, fail, unsupported, and evidence examples.

## Acceptance Criteria

- MCP tool schemas are generated from or checked against canonical schemas.
- MCP resources do not contain formula logic.
- Agent-facing examples are documented and validated.
