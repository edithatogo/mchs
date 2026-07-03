# Plan: strict quality gates

## Phase 1: Restore Evidence

- [x] Restore the missing track directory referenced by `conductor/tracks.md`.
- [x] Add the strict-quality-gates contract under `contracts/quality-gates/`.
- [x] Keep stale standalone workflow files out of the slice; current `pr-ci.yml`,
  `slow-validation.yml`, `slow-validation-reusable.yml`, CodeQL, release, and
  registry workflows remain the source of truth.

## Phase 2: Make Claims Executable

- [x] Add regression coverage that verifies contract evidence paths exist.
- [x] Verify strict workflow commands for formatting, linting, docstrings,
  typing, Python security, Rust security, Rust linting, tests, wheels, coverage,
  CodeQL, dependency review, property checks, mutation checks, and profiling.
- [x] Expand Renovate managers so dependency automation covers all public package
  managers represented in the contract.

## Phase 3: Validation

- [x] Run the strict-quality contract tests and adjacent registry/tooling tests.
- [x] Run formatting, linting, type, and security checks needed for CI.
- [ ] Commit, push, open a PR, and wait for GitHub Actions to pass before moving
  to the next cleanup slice.
