# Specification: Documentation, Release, and Public Readiness

## Overview

Make the Rust-core roadmap visible, conservative, and auditable in the public documentation and release process.

## Current State

- Starlight/Astro docs site exists.
- Governance docs are mirrored into the docs site.
- Validation language exists, but Rust-core status is not documented because the Rust roadmap is new.
- The repository is public.

## Requirements

- Add Starlight documentation for Rust-core architecture, migration status, binding roadmap, and safe delivery surfaces.
- Keep validation claims precise: current Python behavior remains validated only where supported by fixtures or source evidence.
- Add release guidance for future Rust crates, Python wheels, WASM packages, and language bindings.
- Ensure contributor docs describe how to run Python, docs, and future Rust checks.
- Verify public repo hygiene: license, citation expectations, security policy recommendations, contribution pathway, governance docs, and validation vocabulary.

## Acceptance Criteria

- Public docs explain current state versus intended Rust-core future state.
- Docs-site build and link checks pass.
- Release policy records how Rust and binding artifacts will be versioned and validated.
- Contributor guidance names the full local quality gate.
- Public-readiness gaps are either fixed or recorded in follow-on work.

## Out of Scope

- Publishing release artifacts.
- Claiming Rust parity before fixture evidence exists.
- Changing licensing without explicit project governance approval.
