# Specification: strict quality gates

## Objective

Restore the missing backing artifacts for the `Strict Quality Gates` Conductor
entry and make the completion claim testable against the current repository
workflow topology.

## Contract

The track owns `contracts/quality-gates/strict-quality-gates.contract.json`.
That contract defines the required quality gate classes, workflow evidence,
dependency automation coverage, and public-surface artifacts that must exist
before repository-side completion or publication readiness can be claimed.

## Required Gates

- Python formatting, linting, docstring linting, type checking, security linting,
  Bandit, and pip-audit run in `.github/workflows/pr-ci.yml`.
- Python tests run across the supported Python matrix, with Rust extension build
  coverage where required by the workflow.
- Cross-platform maturin wheel build and Rust binding smoke checks run for Linux,
  macOS, and Windows.
- Rust formatting, cargo-audit, clippy with warnings denied, and cargo tests run
  in PR CI.
- Coverage is enforced at 90% through `--cov-fail-under=90`, and Codecov upload
  failures fail CI.
- Slow validation provides property, mutation, and profiling jobs through both
  the scheduled workflow and reusable PR-label workflow.
- CodeQL and dependency review remain active, with dependency-review severity
  configured in `.github/dependency-review-config.yml`.
- Renovate covers the public package managers represented in the repository:
  Python, GitHub Actions, Cargo, npm, Go modules, Gradle, NuGet, and Dockerfiles.

## Acceptance Criteria

- `conductor/tracks.md` links to this track directory.
- The strict-quality contract exists and lists only evidence paths present in
  the repository.
- The strict-quality test verifies the contract, current workflows, and
  dependency automation configuration.
- External registry states remain explicit external gates; the contract must not
  treat CRAN, SSC, Maven Central, Visual Studio Marketplace, Open VSX, or other
  third-party approvals as complete unless their evidence is present.
