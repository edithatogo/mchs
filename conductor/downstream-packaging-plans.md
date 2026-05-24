# Downstream Packaging Plans

## Purpose

This document captures the packaging and release expectations for the
non-Python surfaces that sit on top of the Rust core.

## General Rules

- Packaging wrappers must not duplicate calculator formulas.
- Release readiness is claimable only after fixture-backed parity is recorded
  against the shared public contracts.
- Versioning should remain tied to the Rust core release, the public contract
  version, and the adapter package version so the surfaces cannot drift
  silently.
- If a surface is better served by a service boundary than by an ABI, prefer
  the service boundary.

## R

- Recommended evaluation path: `extendr`.
- Package shape: a thin wrapper over the Rust core, or a fixture-backed
  service client if native packaging becomes fragile.
- Release expectations: publish only after the Rust core and Python adapter are
  stable and the adapter tests confirm contract parity.

## Julia

- Recommended evaluation path: CLI/file wrapper first, with CSV as the
  executable prototype and Arrow as the target batch interchange format.
- Native package evaluation should include `jlrs` as an embedding option once
  the Rust core boundary is stable enough to justify direct runtime coupling.
- Deferred evaluation path: C ABI or `ccall` only after the Rust core contract
  is stable enough to expose versioned symbols.
- A Julia `ccall` wrapper remains the lower-level fallback when `jlrs` is not
  appropriate.
- Package shape: a thin wrapper over the shared calculator boundary with
  minimal Julia-side logic.
- Release expectations: keep Julia package versioning aligned with the Rust
  core and shared contract release. Do not claim General Registry readiness
  until fixture-backed parity runs through the package.

## C#

- Recommended evaluation path: stable ABI wrapper or secured service boundary.
- Package shape: a thin adapter or connector; never a separate calculator
  engine.
- Release expectations: package only after parity tests and the service or ABI
  contract are stable enough for repeatable releases.

## Go

- Recommended evaluation path: C ABI wrapper or secured service boundary.
- Package shape: a thin client or wrapper with explicit contract mapping.
- Release expectations: defer until the lower-risk adapter path is proven and
  the Rust core contract is stable.

## TypeScript and WASM

- Recommended evaluation path: browser docs demo first, with a hand-maintained
  TypeScript facade over generated low-level WASM glue.
- Package shape: wrapper-only adapter shell for the shared Rust/WASM artifact;
  TypeScript must not implement formulas or duplicate validation rules.
- Privacy expectations: committed examples and browser demos must use
  synthetic data only, with no telemetry, upload, PHI, secrets, or patient-level
  persistence.
- Release expectations: keep npm publication and browser calculator readiness
  deferred until the exposed calculators match shared golden fixtures through
  the WASM artifact and bundle-size checks are stable.

## Power Platform

- Recommended evaluation path: custom connector or service boundary.
- Package shape: managed solution or connector package that consumes the shared
  contract, not calculator logic.
- Release expectations: version the connector and solution independently, but
  only claim readiness when the secure service boundary is stable and privacy
  rules are enforced.

## Readiness Claims

- Implemented: the surface has a validated, test-backed adapter in the repo.
- Planned: the surface has a documented toolchain and packaging target.
- Deferred: the surface is intentionally not the next implementation step.
- Advisory: the surface is useful for orchestration or governance but does not
  own calculation logic.
