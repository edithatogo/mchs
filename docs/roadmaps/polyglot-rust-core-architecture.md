# Polyglot Rust Core Architecture Roadmap

## Purpose

This roadmap defines the target architecture for the project’s polyglot Rust
core workstream. It is intentionally roadmap-only: the current validated
runtime remains Python-first, and this document does not claim that Rust is
implemented or default today.

The execution path to GA is defined in the
[Rust Core GA roadmap](./rust-core-ga.md). That roadmap is the immediate
priority and defers non-essential adapter expansion until the core reaches
release-candidate status.

The intended end state is a single Rust calculator core with thin delivery
surfaces for Python, Rust, R, Julia, C#/.NET, Go, TypeScript/WASM, Kotlin/Native, C
ABI, SQL/DuckDB, SAS interoperability, CLI/file workflows, web, and Power
Platform consumers.

## Architecture principles

- Formula logic is single-sourced in the Rust core.
- Bindings and adapters are thin translation layers only.
- All promotion claims must be backed by fixture evidence and release
  validation.
- Unsupported or partially validated streams stay opt-in or unavailable.
- Traceability to IHACPA source material must survive every promotion step.

## Current baseline

- Python remains the production and validation baseline.
- Rust is a future target, not the current source of truth.
- Each calculator stream must prove parity independently before promotion.

## Single-source formula doctrine

The core doctrine for this workstream is that each formula is defined once and
only once.

- The canonical formula implementation lives in the Rust core.
- Language-specific surfaces may marshal inputs, map outputs, and expose
  diagnostics, but they may not duplicate calculator logic.
- If a surface needs special handling, that handling belongs in the adapter
  boundary, source manifest, parameter bundle, or validation fixture, not in a
  second formula implementation.
- Scalar helpers may exist for tests, debugging, or internal composition, but
  they are not alternate business logic sources.

## Source and dependency model

The roadmap treats the following as ordered dependencies:

1. IHACPA source materials and governed reference artefacts.
2. Normalized source manifests that identify the authoritative inputs for each
   calculator stream.
3. Parameter bundles, coding-set registries, classifiers, groupers, and other
   declarative dependencies consumed by the core.
4. Golden fixtures, provenance records, and contract tests derived from those
   source materials.
5. The Rust calculator core, which consumes the normalized data and emits
   Arrow-compatible batch outputs, diagnostics, provenance, and validation
   status.
6. Thin delivery surfaces that consume the core or its CLI/file contract.

Adapters must not reach back into source logic that the core is meant to own.
They may only translate, route, package, or present data that is already
defined by the shared contract.

## Promotion lifecycle

Each calculator stream moves through the same promotion lifecycle:

1. Python baseline
2. Rust canary
3. Rust opt-in
4. Rust default

Promotion is stream-by-stream, not all-at-once. A stream can advance only when
its own evidence is complete.

### 1. Python baseline

The Python baseline is the current validated state.

Entry condition:

- The stream is already published and validated on the Python path.

Required evidence:

- Source traceability to the governed reference materials.
- Fixture pack coverage for the stream’s accepted inputs.
- Documented current behavior for inputs, outputs, diagnostics, and
  provenance.

Exit condition to Rust canary:

- A matching Rust contract exists for the stream’s declared inputs and outputs.
- The stream’s fixture pack has a Rust parity target.
- The adapter path can still fall back to Python.

### 2. Rust canary

The Rust canary is an opt-in experimental path used to prove the contract
before wider exposure.

Entry condition:

- The Rust core exposes the stream’s contract boundary.
- Arrow-compatible batch inputs and outputs are defined for the stream.
- The source manifest, parameter bundle, and fixture set are wired to the
  stream.

Required evidence:

- Canary runs demonstrate parity against the Python baseline for the agreed
  fixture set.
- Diagnostics and provenance match the contract.
- Fallback to Python remains available if the Rust path is missing or
  incomplete.

Exit condition to Rust opt-in:

- Fixture parity is validated for the stream's agreed canonical inputs.
- Release packaging exists for the chosen delivery surface.
- The stream’s validation record is stable enough for user-selected adoption.

### 3. Rust opt-in

Rust opt-in means the Rust path is available for intentional use, but it is not
yet the default runtime.

Entry condition:

- The stream has canary evidence and a releaseable delivery surface.
- Contract tests pass across the chosen bindings.
- The docs and release notes state the stream’s opt-in status clearly.

Required evidence:

- Full parity coverage for the stream’s supported canonical cases.
- No known divergence in formula logic, provenance, or diagnostics.
- Packaging and fallback behavior are reproducible for the supported matrix.

Exit condition to Rust default:

- The stream has passed the complete fixture matrix.
- The Rust delivery path is the preferred validated path.
- Rollback and fallback procedures are defined and tested for the stream.

### 4. Rust default

Rust default means the stream is routed to the Rust core by default while the
Python path remains the historical baseline and fallback reference.

Entry condition:

- All promotion evidence for the stream is complete.
- Binding and contract tests are stable across the supported matrix.
- The stream’s documentation, packaging, and validation records all agree on
  the default runtime.

Required evidence:

- No open parity gaps for the stream’s supported cases.
- Release and rollback evidence exists for the promoted delivery surface.
- Source traceability remains intact through every package and binding.

## Promotion gates by evidence type

| Evidence type | Must exist before canary | Must exist before opt-in | Must exist before default |
| --- | --- | --- | --- |
| Governed source manifest | Yes | Yes | Yes |
| Parameter bundles and registries | Yes | Yes | Yes |
| Fixture pack with expected outputs | Yes | Yes | Yes |
| Arrow-compatible batch contract | Yes | Yes | Yes |
| Diagnostics and provenance contract | Yes | Yes | Yes |
| Binding or delivery packaging | No | Yes | Yes |
| Contract tests across surfaces | No | Yes | Yes |
| Documented fallback path | Yes | Yes | Yes |
| Release evidence for the surfaced package | No | Yes | Yes |
| Complete parity record for supported cases | No | Yes | Yes |

## Binding and surface policy

- Python remains the validated public baseline until a stream is promoted.
- Rust is the target core, not a separate formula source.
- R, Julia, C#/.NET, Go, TypeScript/WASM, Kotlin/Native, C ABI, SQL/DuckDB, SAS,
  CLI/file, web, and Power Platform surfaces are downstream consumers of the
  shared contract.
- Kotlin/Native is the preferred authored Kotlin surface. Java/JVM support is
  not part of the initial Kotlin binding track.
- Scala/Spark, Swift, Stata, and MATLAB are future contract consumers where
  their communities justify the maintenance cost.
- A surface may be primary, thin, orchestration-only, or file/CLI mediated, but
  none of those categories may reintroduce duplicated formula logic.

## Roadmap guardrails

- Do not claim Rust default status without fixture parity evidence.
- Do not claim any binding is production-ready without its contract tests and
  packaging evidence.
- Do not treat canary evidence from one calculator stream as a proxy for all
  streams.
- Do not move a stream forward if source traceability is incomplete.
- Do not expand deferred language adapters before the Rust Core GA required
  surfaces are release-candidate ready.

## Roadmap statement

The intended direction is Python baseline to Rust canary to Rust opt-in to
Rust default, with every step gated by source traceability, fixture parity,
and contract evidence. That is the architecture target only; it does not
describe current implementation state.
