# Rust CLI/MCP Promotion Evidence Specification

## Overview

Create the promotion gate for moving Rust-backed CLI and MCP execution from opt-in or transitional status to the default runtime. This track does not port new formula logic; it proves whether the Rust-backed surfaces are ready, records any remaining gaps, and updates release/support documentation accordingly.

## Functional Requirements

- Build a cross-surface promotion matrix covering calculators, pricing years, CLI commands, MCP tools, input formats, output formats, diagnostics, and fallback behaviour.
- Define minimum evidence required before Rust-backed CLI or MCP execution can become the default.
- Add or wire CI jobs that run Rust tests, Python compatibility tests, CLI parity tests, and MCP parity tests together.
- Produce a fail-closed promotion report that separates validated Rust-default surfaces from opt-in, Python-only, and unsupported surfaces.
- Document runtime selection, rollback, and support status for users and maintainers.
- Ensure release notes, README, registry docs, and project-board status remain aligned with the evidence.

## Non-Functional Requirements

- Promotion evidence must be reproducible from committed commands and committed fixtures.
- Claims must use the project's validation vocabulary and avoid blanket completion wording.
- The default-runtime decision must be reversible without removing user-facing CLI or MCP contracts.

## Acceptance Criteria

- A committed promotion matrix shows exactly which CLI and MCP surfaces are Rust-default, Rust-opt-in, Python-only, or unsupported.
- CI includes a release-grade command or workflow that fails when Rust, Python, CLI, or MCP parity regresses.
- Release/support documentation states the default runtime decision and rollback path.
- Any remaining Python runtime dependency is explicitly described as a compatibility, transport, or unported-calculator dependency.
- The track closes only after CLI and MCP migration evidence has been reviewed and no unsupported surface is hidden by broad completion language.

## Out of Scope

- Porting additional calculators or years not already validated by the CLI and MCP migration tracks.
- Publishing new package versions or registry releases.
- Removing Python APIs, package metadata, or compatibility shims.
- Making claims about non-CLI/MCP adapters such as Power Platform, R, Julia, or web demos.
