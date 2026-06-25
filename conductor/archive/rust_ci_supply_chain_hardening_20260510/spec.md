# Specification: Rust CI, Pre-Commit, and Supply-Chain Hardening

## Overview

Align repository quality gates with the Rust-core roadmap so future Rust work cannot bypass formatting, linting, tests, security checks, provenance, or release controls.

## Current State

- Python CI exists with Ruff, ty, pytest, coverage, and Codecov.
- Docs-site CI exists for Starlight/Astro.
- The repository default branch is `master`, while one CI workflow currently triggers push checks on `main`.
- Pre-commit still treats mypy as an active hook even though the project tech stack records ty as the active type gate.
- No Rust CI, Rust pre-commit, Rust advisory, or Rust release automation exists.

## Requirements

- Fix default-branch CI drift.
- Align pre-commit with the documented Python quality gate.
- Add Rust checks once the workspace exists: `cargo fmt --check`, `cargo clippy`, and `cargo test`.
- Evaluate `cargo nextest` for faster Rust test execution.
- Add Rust supply-chain checks such as `cargo audit` or `cargo deny`.
- Keep dependency automation reviewable through Renovate.
- Plan release provenance, SBOM, signing, and `cargo-dist` only when Rust artifacts exist.

## Acceptance Criteria

- CI branch triggers match the actual repository default branch or intentionally support both `main` and `master`.
- Pre-commit configuration no longer contradicts `tech-stack.md`.
- Rust gates are documented before Rust implementation lands and implemented once a workspace exists.
- Supply-chain controls cover Python, Node/docs-site, and Rust ecosystems.
- GitHub Actions are required to pass before push/merge workflows claim readiness.

## Out of Scope

- Publishing Rust artifacts before a Rust crate exists.
- Removing transitional Python files without a separate migration decision.
