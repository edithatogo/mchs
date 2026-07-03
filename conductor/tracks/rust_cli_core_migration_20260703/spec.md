# Rust CLI Core Migration Specification

## Overview

Migrate the core command line calculation and validation path to the shared Rust calculator core. The existing `funding-calculator` user experience, file contracts, diagnostics, and exit semantics must remain stable while Rust coverage is promoted calculator by calculator.

The CLI may keep a Python launcher or compatibility shim during transition, but formula and calculation behaviour for promoted surfaces must come from the Rust core rather than duplicated Python logic.

## Functional Requirements

- Inventory every public CLI command, option, input mode, output mode, and documented file contract that is currently supported.
- Add an explicit Rust-backed execution path for supported calculators behind a feature flag, environment variable, or command option before any default switch.
- Preserve existing CLI command names, option spelling, schema names, file formats, exit codes, and user-facing diagnostics unless a later compatibility note explicitly approves a breaking change.
- Compare Rust-backed CLI results against canonical Python/reference fixtures for every promoted calculator, pricing year, and output format.
- Fail closed for calculators, pricing years, or output modes that are not yet Rust validated; do not silently fall back when the caller has explicitly requested Rust execution.
- Keep Python fallback available until the promotion-evidence track proves that Rust-backed CLI execution is ready to become the default.
- Update runtime support-status documentation so users can distinguish Python-default, Rust-opt-in, and Rust-default behaviour.

## Non-Functional Requirements

- Rust and Python compatibility code must share contracts and fixture data rather than maintaining independent formula copies.
- Validation output must be reproducible in CI and suitable for release evidence.
- The migration must not weaken existing type, lint, coverage, or supply-chain gates.

## Acceptance Criteria

- A committed CLI inventory identifies all current public commands and options and maps them to Rust-backed, Python-only, or unsupported statuses.
- Rust-backed CLI execution passes golden-fixture parity for the promoted calculator/year set.
- CI includes a non-interactive Rust-backed CLI conformance command.
- Documentation states the runtime selection mechanism, current support matrix, and rollback path.
- No README, docs, or registry text claims Rust is the default CLI engine until promotion evidence exists.

## Out of Scope

- Removing the Python package or public Python API.
- Porting every historical calculator year in one step without fixture-backed validation.
- Changing public file schema names or output contracts for convenience.
- MCP transport migration, except where shared Rust dispatcher work is reused by the MCP track.
