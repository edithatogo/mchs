# Specification: Package Surface Ownership Registry

## Overview

Create a machine-readable registry of every package, binding, app, documentation,
and external registry surface. The registry prevents package sprawl by requiring
each surface to declare its local path, manifest, owner track, support status,
release target, CI gate, generated-artifact policy, and external gate status.

## Functional Requirements

- Cover Python, Rust, docs, R, Julia, Go, .NET, Swift, JVM, WASM/npm,
  VS Code, Power Platform, Stata, MATLAB, conda, CRAN, Maven, Conan, and vcpkg.
- Distinguish implemented package roots from contract-only, registry-only, and
  planned external surfaces.
- Require every in-tree package manifest to be represented exactly once.
- Require release-target and evidence-boundary fields for every surface.
- Validate that local manifest paths exist for implemented surfaces.
- Block public support claims when a surface has no evidence boundary.

## Non-Functional Requirements

- Use the existing support status vocabulary.
- Keep registry data concise enough for CI validation.
- Do not convert planned surfaces into support claims.

## Acceptance Criteria

- `package-surfaces.schema.json` defines the required machine contract.
- `package-surfaces.json` includes all required surfaces and all discovered
  manifest roots.
- The topology validator fails if a package manifest is missing from the
  registry.
- Tests verify the required surface set and key ownership fields.

## Out of Scope

- Publishing package registry releases.
- Generating package manifests for planned surfaces.
- Moving package source directories.
