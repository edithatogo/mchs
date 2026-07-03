# Specification: Rust Acute 2025 Proof of Concept with Python Bindings

## Overview

Implement the first Rust calculator proof of concept for acute 2025 and expose it through Python bindings. The proof of concept must be opt-in until fixture parity and validation evidence justify promotion.

## Current State

- Acute 2025 has Python implementation, tests, and golden fixtures.
- The repository has Arrow/Parquet bundle conventions and manifest-driven fixture packs.
- There is no Rust workspace or Python binding package yet.

## Requirements

- Create a Rust workspace with clear crate ownership for core formulae, schemas, and Python bindings.
- Use PyO3/maturin for the Python binding path unless the architecture track records a better local decision first.
- Implement acute 2025 as the first Rust-backed kernel.
- Use Arrow-compatible batch input/output as the main kernel contract.
- Compare Rust output against existing acute 2025 golden fixtures.
- Keep Python calculators as the default path until Rust parity is explicitly validated.
- Expose any Rust-backed Python adapter behind an explicit opt-in API, CLI flag, or environment-gated path.
- Document parity status, limitations, and rollback behavior.

## Acceptance Criteria

- Rust workspace and Python binding scaffold exist.
- Rust unit tests cover formula-level acute 2025 behavior.
- Python tests can invoke the Rust-backed acute 2025 path.
- Golden fixture parity passes for the acute 2025 pilot fixture pack.
- Existing Python default behavior is unchanged unless explicitly opted in.
- CI includes the Rust and Python checks needed for this proof of concept.

## Out of Scope

- Porting every calculator.
- Making Rust the default runtime.
- Shipping non-Python bindings.
- Supporting real patient data in GitHub Pages.
