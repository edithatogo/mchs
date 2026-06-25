# Specification: Rust Core GA

## Overview

Make Rust Core GA the immediate project priority. The project should move from
Python-first with a future Rust target to a stream-by-stream Rust default model,
while Python remains the baseline reference and fallback until each stream has
complete parity evidence.

Scala/Spark, Swift, Stata, and MATLAB tracks are valid future consumers, but
they remain deferred until each has an accountable audience, owner, and
surface-specific evidence case.

## Functional Requirements

- Define a full Rust Core GA roadmap from governance freeze through public GA.
- Make calculator contracts, source manifests, formula bundles, coding-set
  registries, diagnostics, and provenance versioned inputs to the core.
- Require Rust implementation to be the single source of formula execution for
  promoted streams.
- Require parity validation against Python and SAS/Excel/source artefacts where
  available.
- Require more than 90 percent coverage for GA streams over Rust core and
  validation-critical adapters.
- Require minimum GA surfaces: Rust crate, CLI/file contract, Python binding,
  C ABI, and Arrow/Parquet interchange.
- Keep language-specific adapters thin and blocked from formula logic.
- Make release evidence, security posture, documentation, tags, packages, and
  homepage claims agree before GA.

## Non-Functional Requirements

- CI/CD must be strict for formatting, linting, tests, coverage, security, and
  release reproducibility.
- Docs must remain Starlight-based and conservative about support status.
- Release artefacts must include provenance and evidence bundles.
- Unsupported streams must be marked as unavailable, blocked, canary, opt-in, or
  release-candidate rather than inferred as supported.

## Acceptance Criteria

- `docs/roadmaps/rust-core-ga.md` exists and defines all GA phases, gates, and
  deferred tracks.
- `docs/roadmaps/polyglot-rust-core.md` identifies Rust Core GA as the immediate
  priority.
- `docs/roadmaps/polyglot-rust-core-architecture.md` aligns its promotion model
  with the GA roadmap.
- `conductor/tracks.md` includes `Rust Core GA` as an incomplete immediate
  priority track.
- Scala/Spark, Swift, Stata, and MATLAB tracks are marked as deferred behind
  their audience, owner, and evidence gates.

## Out of Scope

- Implementing the Rust core itself in this roadmap track.
- Publishing a GA release without evidence.
- Building deferred language adapters before the required core surfaces are
  release-candidate ready.
