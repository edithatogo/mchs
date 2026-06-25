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
3. `release-candidate` - promotion-ready, pending only final parity,
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
| Rust | Crates (`nwau-core`, `nwau-c-abi`, `nwau-py`) | `nwau-core 0.1.0` is published and verified on crates.io; `nwau-c-abi` and `nwau-py` remain unpublished/private | `preview` internal-first binding layer | Promote to `ga` only when the Rust core is the single source of formula logic, the public crate API is stable, and semver/release automation is in place. |
| R | Package wrapper over the shared core or file contract | `nwauR 0.1.0` is prepared with `R CMD check` and package-local CRAN-style checks passing; no CRAN publication evidence | `private` | Release when the wrapper is thin, R CI validates the same fixtures, and CRAN submission/review is complete. |
| Julia | Package wrapper over the shared core or file contract | `NationalWeightedActivityUnitWrapper 0.1.0` is published and verified by merged Julia General PR #156254; superseded `NwauCore 0.1.0` General PR #156236 is preserved as historical evidence | `preview` | Keep Julia CI, artifact install checks, and parity fixtures passing before broader runtime support claims. |
| NuGet / C# | .NET package and managed CLI/file wrapper | `Mchs.Bindings.DotNet 0.1.0` is published and verified by NuGet flat-container API evidence | `preview` | Release when the .NET wrapper remains thin, binary compatibility is documented, and signed package publishing is repeatable. |
| Go | Go module with service and binding-file adapters | `github.com/edithatogo/mchs/bindings/go@v0.1.0` is published and verified through the Go module proxy/pkg.go.dev | `private` | Release when cross-compilation is stable, no duplicated business logic exists, and the module can be tested end-to-end in CI. |
| TypeScript / WASM | npm package plus adapter for WASM exports | `@edithatogo/mchs-wasm-binding 0.1.0` is published and verified on npm | `preview` | Release when browser and Node smoke tests pass, bundle size and loading behavior are controlled, and the WASM artifact remains deterministic. |
| Kotlin/Native | Native artifact over C ABI, service, or file contract; current local shape is a request validator | Private adapter code; no registry submission evidence | `private` | Release when the Kotlin adapter is thin, CI covers the supported native target range, and the packaging path is reproducible. |
| Scala / Spark | Spark package, Spark SQL integration, or lakehouse file/service adapter | Private transport-boundary adapters; no registry submission evidence | `private` | Release when Spark fixtures pass, schema evolution is pinned, and no formula logic is implemented in Spark jobs. |
| JVM / Maven Central | Kotlin/JVM binding jar over file/service boundary contracts | `io.github.edithatogo:mchs-jvm-bindings 0.1.0` is published and verified on Maven Central; Sonatype Central namespace `io.github.edithatogo` is verified; repo1 metadata exposes latest/release/version `0.1.0`; public JAR SHA-256 is `2f499b78d06317fd9bf2e343542b74043f163f127cd32db4651098f6ac6af49e`; Publisher API deployment `5fb01ae9-2609-4284-9427-5830e08bcbb5` validated and published | `preview` | Keep POM metadata, signing, checksum, and Central Portal publication evidence reproducible before any later JVM release. |
| Swift | Swift Package Manager package over C ABI, service, or file contract | Swift Package Index publication is verified for `MCHSBind 0.1.0` by merged PackageList PR #13999 and public SPI page evidence | `preview` | Keep Apple-platform fixtures and compatibility-build evidence separate from publication, and do not duplicate calculator behavior. |
| Stata | Stata ado/do examples or package over file, CLI, or service contract | SSC/RePEc publication is verified for package `mchs`; local Stata runtime execution is not claimed | `preview` | Release stronger support only when health-economics examples pass shared fixtures in a Stata runtime and remain boundary-only. |
| MATLAB | MATLAB scripts/toolbox over file, CLI, service, or C ABI contract | MATLAB File Exchange publication is verified for add-on `184067`; local MATLAB/Octave runtime execution is not claimed | `preview` | Release stronger support only when numerical examples pass shared fixtures in a MATLAB/Octave runtime and no MATLAB formula implementation is introduced. |
| C ABI | Shared library plus stable headers | `nwau-c-abi` passes Cargo package verification, Conan create, and disposable vcpkg overlay install locally; vcpkg PR #51965 was closed unmerged because vcpkg does not currently support Rust library ports; ConanCenter PR #30262 remains open | `preview` | Release when exported symbols are versioned, headers are frozen for the supported ABI window, ConanCenter review passes, vcpkg policy support exists or that registry is explicitly deferred, and backward-compatibility tests pass. |
| SQL / DuckDB | Extension, SQL UDF package, or embedded integration | Unpublished local prototype | `preview` | Release when SQL fixtures round-trip through the same Rust core and explainability/diagnostics remain consistent with the host engine. |
| MCP server | Stdio MCP server entry point over the canonical MCP contract | Official MCP Registry publication is verified for `io.github.edithatogo/mchs 0.2.2`; Docker/Smithery remain separate MCP registry gates | `preview` local-use surface | Keep official MCP metadata aligned with package releases; consider Glama for public indexing, Smithery only after HTTP or MCPB packaging, and Docker MCP Registry only if containerized distribution is added. |
| SAS interop | File-based exchange assets, adapter scripts, or integration bundle | Private / roadmap-only (no registry submission evidence) | `private` | Release only if the interface stays boundary-only, the exchange contract is fixed, and the artifact can be validated without proprietary formula duplication. |
| CLI / file | CLI binary, batch file contract, and deterministic input/output formats | Published as Python CLI entrypoint; branded CLI package remains unpublished | `ga` for file contract; `preview` for branded CLI distribution | Move CLI distribution to `ga` only after exit codes, stdin/stdout contracts, and batch-file behavior are stable across fixtures. |
| Web demos | Static demo shell, documentation demo, or hosted sample app | Unpublished demo distribution only | `preview` | Release only as a demo surface that calls the shared artifact or file contract; do not embed a separate formula implementation. |
| Power Platform managed solutions | Managed solution, connectors, environment variables, and flow/app packaging | Private / roadmap-only (no public solution registry evidence) | `private` | Release when the managed solution boundary is explicit, the service contract is approved, and no formula logic lives inside apps, flows, or low-code expressions. |

Registry note: do not assert publication on any surface unless the target registry page is explicitly linked in evidence.

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
