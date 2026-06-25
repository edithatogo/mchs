# Public Calculator API Contract

## Purpose

This document defines the versioned public calculator contract that downstream
adapters must treat as the source of truth for the declared support surface.
It is intentionally narrow and documents the current acute calculator surface first.

The contract is runtime-neutral and batch-first. Formula logic belongs in the
calculator core, not in adapters.

Scope conformance is bounded; this contract does not claim exhaustive runtime or
business-outcome coverage across all surfaces or versions.

## Contract Versioning

- Contract version: `1.0`
- Calculator identifiers are stable, lower-case names such as `acute`.
- Pricing years use the four-digit IHACPA label form, for example `2025`.
- Explicitly supported runtimes and deployment surfaces are defined in release notes
  and track metadata.

## Acute Contract

### Required Inputs

- `DRG`
- `LOS`
- `ICU_HOURS`
- `ICU_OTHER`
- `PAT_SAMEDAY_FLAG`
- `PAT_PRIVATE_FLAG`

### Required Outputs

- `NWAU25` for pricing year `2025`

### Validation Status

- The acute contract is validated against the shared contract tests in
  `tests/test_contracts.py` for declared support cases.
- The acute input contract rejects missing required fields, blank column names,
  duplicate column names, and unsupported calculator identifiers.
- Pricing-year validation accepts supported four-digit labels only.
- The contract is not claimed to prove every possible runtime result or every
  external business outcome outside the declared test envelope.

### Validation Gaps

- Runtime paths, locale/hosting combinations, and downstream consumers not
  listed in validated release artifacts are outside the proven scope and must be
  treated as explicit gaps.

## Error Model

Contract violations should surface structured, explainable errors:

- Missing or invalid contract values raise `ValueError`-style validation errors
  during contract construction.
- Missing input or output columns raise `ContractValidationError` with explicit
  messages naming the violated boundary.

## Adapter Mapping

- The CLI and Python API should both use the same calculator contract and runtime
  helper boundary for supported runtimes.
- Adapters may parse inputs, validate the contract, select the requested year, and
  format outputs.
- Adapters must not embed calculator math or source-bundle lookup behavior.
- The same contract should be consumable by Rust, Python, C#, web, Power
  Platform, R, Julia, Go, and TypeScript surfaces without changing the core
  schema.

## Generation Readiness

The contract shape is suitable for later OpenAPI or client model generation
because it exposes explicit schema versions, supported identifiers, required
columns, and structured validation errors.
