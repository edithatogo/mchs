# Specification: Rust Core Continuation

## Overview

This track keeps the Rust core transition moving beyond roadmap and canary
state. Python remains the validated public baseline until each calculator
stream has Rust parity evidence, but the project should keep implementing the
shared Rust kernel and promoting streams through canary, opt-in,
release-candidate, and GA states.

The track also prevents deferred adapter work from pulling formula logic away
from the Rust core. Language bindings and platform integrations must consume
the shared contracts rather than implementing their own calculator behavior.

## Functional Requirements

- Audit the current Rust workspace, Python binding, CLI/file contracts, C ABI,
  support status, and release evidence against the Rust Core GA roadmap.
- Define the next stream-by-stream promotion order for Rust implementation.
- Write parity tests before promoting any Rust calculator behavior.
- Implement Rust kernel logic for the selected stream or streams using
  validated parameter bundles, reference data, provenance, diagnostics, and
  canonical schemas.
- Keep Python as the reference fallback until Rust output matches trusted
  Python and source-derived fixtures.
- Promote Python binding behavior only after opt-in canary tests pass and
  support status is updated.
- Ensure CLI/file, C ABI, MCP, HTTP/API, and future language adapters call the
  Rust core or declared service/file contracts instead of duplicating formulas.
- Capture release evidence before any stream is described as GA.

## Non-Functional Requirements

- Rust code must pass `cargo fmt`, `cargo clippy`, `cargo test`, and targeted
  parity tests before promotion.
- Python compatibility tests must continue to pass for supported versions.
- Coverage expectations from the workflow remain in force for promoted Rust and
  validation-critical adapter paths.
- Unsupported streams must stay explicit: blocked, canary, opt-in,
  release-candidate, complete-with-gaps, or not-ready.

## Acceptance Criteria

- A current Rust-core promotion matrix exists and names each stream's state,
  evidence, owner, and next action.
- At least one currently non-GA Rust stream has failing parity tests written
  first, implementation completed, and passing parity evidence recorded, or the
  track records why no stream can be promoted yet.
- Python binding behavior remains backward-compatible and uses Rust only where
  support status permits it.
- CLI/file and C ABI surfaces prove they consume shared Rust contracts for
  promoted streams.
- Docs and README claims agree with the actual Rust support state.
- Deferred language adapters remain thin and cannot claim completion through
  documentation-only or unvalidated formula behavior.

## Out of Scope

- Reimplementing proprietary groupers or restricted licensed classification
  assets.
- Publishing crates, npm packages, NuGet packages, CRAN packages, or other
  registries before implementation and release evidence exists.
- Advancing low-priority adapters ahead of Rust parity and core promotion.
