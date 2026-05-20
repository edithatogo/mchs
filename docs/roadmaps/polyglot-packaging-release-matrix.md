# Polyglot Rust Core Packaging and Release Matrix

Roadmap snapshot: 2026-05-12.

This document defines the packaging status and release gates for each public
surface that participates in the Polyglot Rust Core roadmap. It is packaging
only: it does not redefine calculator logic, binding contracts, or Rust-core
promotion rules.

## Release policy

Release progression uses four states:

1. `private` - internal-only, no public artifact promise.
2. `preview` - published or distributable, but opt-in and not yet supported as
   a default path.
3. `release-candidate` - promotion-ready, blocked only by final parity,
   packaging, or security checks.
4. `ga` - supported default packaging path for the surface.

Common release gates apply to every surface:

- Shared Rust core passes fixture parity against the validated Python baseline.
- Binding or adapter contract tests pass on the current release candidate.
- Provenance, versioning, and license metadata are emitted by the build.
- Release notes document the supported input/output shape, limitations, and
  upgrade path.
- CI covers the target runtime or host platform that will consume the artifact.

## Packaging matrix

| Surface | Artifact/package shape | Registry evidence state | Current status | Release gate to advance |
| --- | --- | --- | --- | --- |
| Python | Wheels and source distribution | Published on PyPI (`nwau-py`) | `ga` current validated public runtime | Keep as baseline until every promoted surface demonstrates parity against the same fixtures and diagnostics contract. |
| Rust | Crates (`nwau-core`, `nwau-c-abi`, `nwau-py`) | Unpublished; local crates exist, and two of three crates are explicitly `publish = false` | `preview` internal-first binding layer | Promote to `ga` only when the Rust core is the single source of formula logic, the public crate API is stable, and semver/release automation is in place. |
| R | Package wrapper over the shared core or file contract | Private / roadmap-only (no registry submission evidence) | `private` | Release when the wrapper is thin, R CI validates the same fixtures, and the package does not embed duplicate formula logic. |
| Julia | Package wrapper over the shared core or file contract | Private / roadmap-only (no registry submission evidence) | `private` | Release when Julia CI, artifact install checks, and parity fixtures pass without runtime-specific behavior drift. |
| NuGet / C# | .NET package and managed wrapper | Unpublished (no public NuGet evidence) | `preview` | Release when the .NET wrapper remains thin, binary compatibility is documented, and signed package publishing is repeatable. |
| Go | Go module, preferably thin wrapper over C ABI or CLI/file contract | Unpublished (no public module evidence) | `private` | Release when cross-compilation is stable, no duplicated business logic exists, and the module can be tested end-to-end in CI. |
| TypeScript / WASM | npm package plus WASM bundle | Private shell only; `wasm-binding/package.json` is `"private": true` and unpublished | `preview` | Release when browser and Node smoke tests pass, bundle size and loading behavior are controlled, and the WASM artifact remains deterministic. |
| Kotlin/Native | Native artifact over C ABI, service, or file contract | Private / roadmap-only (no registry submission evidence) | `private` | Release when the Kotlin adapter is thin, CI covers the supported native target range, and the packaging path is reproducible. |
| Scala / Spark | Spark package, Spark SQL integration, or lakehouse file/service adapter | Private / roadmap-only (no registry submission evidence) | `private` | Release when Spark fixtures pass, schema evolution is pinned, and no formula logic is implemented in Spark jobs. |
| Swift | Swift Package Manager package over C ABI, service, or file contract | Private / roadmap-only (no registry submission evidence) | `private` | Release when Apple-platform fixtures pass and native packaging does not create duplicated calculator behavior. |
| Stata | Stata ado/do examples or package over file, CLI, or service contract | Private / roadmap-only (no registry submission evidence) | `private` | Release when health-economics examples pass shared fixtures and remain boundary-only. |
| MATLAB | MATLAB scripts/toolbox over file, CLI, service, or C ABI contract | Private / roadmap-only (no registry submission evidence) | `private` | Release when numerical examples pass shared fixtures and no MATLAB formula implementation is introduced. |
| C ABI | Shared library plus stable headers | Unpublished local artifacts only | `preview` | Release when exported symbols are versioned, headers are frozen for the supported ABI window, and backward-compatibility tests pass. |
| SQL / DuckDB | Extension, SQL UDF package, or embedded integration | Unpublished local prototype | `preview` | Release when SQL fixtures round-trip through the same Rust core and explainability/diagnostics remain consistent with the host engine. |
| MCP server | Stdio MCP server entry point over the canonical MCP contract | Local stdio server implemented; official MCP Registry metadata and GitHub OIDC publication workflow prepared; registry publication waits for a package release that includes `mchs-mcp`; Docker/Smithery deferred | `preview` local-use surface | Publish metadata to the official MCP Registry after the package release includes `mchs-mcp`; consider Glama for public indexing, Smithery only after HTTP or MCPB packaging, and Docker MCP Registry only if containerized distribution is added. |
| SAS interop | File-based exchange assets, adapter scripts, or integration bundle | Private / roadmap-only (no registry submission evidence) | `private` | Release only if the interface stays boundary-only, the exchange contract is fixed, and the artifact can be validated without proprietary formula duplication. |
| CLI / file | CLI binary, batch file contract, and deterministic input/output formats | Published as Python CLI entrypoint; branded CLI package remains unpublished | `ga` for file contract; `preview` for branded CLI distribution | Move CLI distribution to `ga` only after exit codes, stdin/stdout contracts, and batch-file behavior are stable across fixtures. |
| Web demos | Static demo shell, documentation demo, or hosted sample app | Unpublished demo distribution only | `preview` | Release only as a demo surface that calls the shared artifact or file contract; do not embed a separate formula implementation. |
| Power Platform managed solutions | Managed solution, connectors, environment variables, and flow/app packaging | Private / roadmap-only (no public solution registry evidence) | `private` | Release when the managed solution boundary is explicit, the service contract is approved, and no formula logic lives inside apps, flows, or low-code expressions. |

Registry note: do not assert publication on any surface unless the target
registry page is explicitly linked in evidence. The current machine-readable
status for non-Python alternative formats is
`docs/roadmaps/release/alternative-format-publication-status-20260521.json`.

## Surface-specific notes

### Python

Python wheels remain the authoritative public runtime until Rust parity and
binding contracts are complete. Packaging should stay conservative: no
feature-specific divergence from the validated baseline, and no release that
cannot be reproduced from CI artifacts.

### Rust

Rust crates are the packaging form of the shared calculator core. They should
remain preview until the core API, diagnostics, and provenance surfaces are
stable enough to support semver and downstream consumption.

### R and Julia

R and Julia are thin consumers. Their release gate is not "can the package be
built" but "does the package stay thin, stay reproducible, and stay fixture-
equivalent to Python/Rust across supported inputs."

### NuGet, Go, and native adapters

These ecosystems should consume the shared core through the narrowest viable
boundary. Prefer a generated or adapter-based release over reimplementing the
formula layer in language-native code.

### TypeScript / WASM and web demos

TypeScript/WASM can ship as a reusable artifact once browser and Node behavior
is stable. Web demos are not a separate computation surface; they are a
presentation layer over the shared artifacts and should never become the
primary implementation.

### C ABI and SQL / DuckDB

C ABI is the compatibility floor for low-level integration. SQL/DuckDB should
be packaged as an integration surface that binds to the same core logic and
returns the same diagnostics and provenance metadata as other callers.

### SAS interop

SAS remains boundary-first and should stay private until the project has a
clear, supportable exchange format. Any public claim should be limited to the
interop artifact, not the business logic.

### CLI / file

The CLI and file contract are the simplest release path for deterministic batch
execution. They are also the fallback integration surface for consumers that do
not need language-native bindings.

### Power Platform

Power Platform is an orchestration surface, not a place to host the core
calculation logic. Managed solution packaging should only expose approved
connectors, environment configuration, and a secure path to the shared service
or file contract.

## Promotion rules

- No surface moves from `private` to `preview` unless the shared Rust core has
  passed the current fixture set and the surface-specific CI path is green.
- No surface moves from `preview` to `release-candidate` unless its artifact can
  be installed or executed without manual intervention in the target host.
- No surface moves to `ga` unless the artifact is supported, documented, and
  traceable to the same validated core release.
- If a surface cannot demonstrate thin-binding behavior, it stays `private`
  regardless of whether packaging exists.

## Release sequencing

Recommended order of promotion:

1. Python baseline remains stable.
2. Rust crate and CLI/file contract reach release-candidate together.
3. C ABI and TypeScript/WASM follow once the core ABI and diagnostics are
   stable.
4. R, Julia, NuGet/C#, Go, Kotlin/Native, and other adapters follow after the
   thin-wrapper contract is proven across fixture suites.
5. SQL/DuckDB, SAS interop, web demos, and Power Platform remain boundary-only
   until their host integration paths are approved.

## Acceptance checklist for this matrix

- Every listed surface has a documented artifact type and current status.
- Every listed surface has a concrete release gate.
- The matrix does not overclaim support for surfaces that remain private or
  preview.
- The matrix is consistent with the track spec and the Python-first validated
  runtime stance.
