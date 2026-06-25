# Specification: Rust Core Architecture and Calculator Abstraction

## Overview

Define the target architecture for a Rust-first calculator core before any implementation work. The architecture must separate formulae, parameters, schemas, reference data, provenance, validation status, and delivery adapters so future language surfaces do not duplicate calculation logic.

## Current State

- The current validated implementation is Python-first and still uses pandas broadly.
- Arrow/Parquet bundles, public API contracts, golden fixtures, Starlight docs, GitHub Pages demo boundaries, and Power Platform boundaries already exist.
- No Rust workspace, Rust core crate, binding crate, or stable cross-language ABI currently exists.
- Existing C# and Power Platform material is architecture guidance, not an implemented engine.

## Requirements

- Treat Rust as the intended future calculation source of truth only after fixture parity is proven.
- Keep Python as the production and validation baseline during migration.
- Use Arrow-compatible batch input and output as the primary kernel contract.
- Allow scalar formula functions only for unit testing, formula clarity, and internal composition.
- Define boundaries for formula kernels, parameter models, input/output schemas, reference data loading, provenance, validation metadata, and adapters.
- Update existing architecture documents so Rust becomes the intended core while Power Platform remains orchestration only.
- Preserve source traceability to SAS, Excel, compiled/Python reference files, and committed fixtures.
- Include a promotion policy for moving a calculator from Python-default to Rust-backed behavior.

## Acceptance Criteria

- A Rust-core architecture ADR is added.
- `conductor/tech-stack.md` records Rust as the intended core target and distinguishes it from current Python implementation state.
- Public API, C# architecture, Power Platform boundary, and web architecture docs align with the Rust-core direction.
- The architecture explicitly forbids duplicated formula logic in language adapters.
- The migration policy requires golden fixture parity before Rust-backed paths become default.

## Out of Scope

- Implementing Rust code.
- Replacing any Python calculator behavior.
- Implementing language bindings, Streamlit, GitHub Pages WASM, or Power Platform artifacts.
