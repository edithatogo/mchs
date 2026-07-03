# Rust MCP Core Migration Specification

## Overview

Migrate the MCP stdio server's core calculation and validation behaviour to the shared Rust calculator core while preserving the published MCP tool contract. The MCP layer may remain a Python transport shim during transition, but promoted calculation behaviour must be delegated to Rust-backed execution rather than duplicated in the MCP adapter.

## Functional Requirements

- Inventory current MCP tools, resources, schemas, registry metadata, diagnostics, and examples.
- Define the dispatcher boundary from MCP requests to canonical schemas, Rust core calls, and MCP JSON responses.
- Preserve existing tool names, resource identifiers, schema shapes, error semantics, and registry-facing metadata unless a later contract update explicitly approves a change.
- Add tests proving Rust-backed MCP outputs match CLI outputs and canonical fixtures for promoted calculators and pricing years.
- Fail closed when a caller requests a calculator, pricing year, or output mode that is not Rust validated.
- Keep registry and documentation claims limited to validated stdio behaviour; do not claim Docker, hosted HTTP, or search-index readiness without separate evidence.
- Reuse the CLI migration's runtime-selection policy where practical so MCP and CLI do not diverge.

## Non-Functional Requirements

- The MCP layer must not contain independent formula logic.
- MCP tests must be non-interactive and suitable for CI.
- Error responses should remain useful to language-model clients while preserving machine-readable status fields.

## Acceptance Criteria

- A committed MCP inventory maps every current tool/resource to Rust-backed, Python-only, or unsupported status.
- Rust-backed MCP execution passes parity against CLI and canonical fixtures for the promoted surface.
- CI includes a non-interactive MCP conformance command.
- Registry and support-status documentation truthfully describe the runtime path and any remaining Python shim.
- No MCP documentation claims full Rust migration until unsupported tools and years are explicitly accounted for.

## Out of Scope

- Publishing a new MCP registry release.
- Adding hosted HTTP, OAuth, Docker catalog, or Smithery runtime behaviour unless covered by already-existing registry readiness tracks.
- Removing the Python transport shim before parity and release evidence support doing so.
- Changing MCP tool names or response schemas for convenience.
