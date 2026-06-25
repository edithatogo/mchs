# Specification: Calculator Core Abstraction and Validation Models

## Goal

Define strict calculator-core boundaries that consume the public contract layer and keep computation separate from adapter concerns.

## Current State

- The track is active and should read as implementation guidance, not as a future-state wishlist.
- The public API contract layer is the upstream gate for this work.
- The current focus is on contract tests, contract-backed parameter models, and reference-bundle boundaries rather than adapter expansion.
- The next adapter step is a shared helper that keeps CLI and library entry points aligned to the same contract surface.

## Requirements

- Calculator orchestration must be separate from deterministic formula logic.
- Parameter models and input/output schemas must be explicit, validated, and aligned to the public API contract.
- Reference data resolution must be deterministic, traceable, bundle-based, and owned by a dedicated `reference_data` helper boundary rather than ad hoc calculator code.
- CLI, web, Python API, and C# adapters must not embed calculator-specific hidden assumptions or direct source lookup behavior.
- CLI and library entry points should share adapter helpers where practical so parity remains obvious and testable.
- The core must expose a narrow contract-oriented boundary for prepared inputs, compute execution, and structured outputs.
- The public API contract layer is the dependency gate for downstream adapter work and should remain the source of truth for contract shape.

## Acceptance Criteria

- A small calculator path demonstrates the target abstraction shape.
- Strict validation boundaries are documented and tested.
- Existing pandas behavior remains protected by regression tests.
- The track explicitly depends on the public API contract gate before downstream adapter work expands.
- Reference-bundle selection and contract-backed error shapes are documented conservatively.
- The calculator core should consume resolved reference-bundle helpers instead of inlining source lookup logic.
