---
title: Polyglot Rust core roadmap
slug: 2026/governance/polyglot-rust-core-roadmap
---

Python remains the validated public runtime while the project moves toward a
shared Rust calculator core with thin bindings. This page is a roadmap and
contract summary; it is not a claim that Rust is already the default runtime.

Rust canary and foundation evidence is recorded for the scoped migration
surfaces, but it does not promote Rust to the default public runtime. Further
language-adapter expansion remains gated by named audience, accountable owner,
contract tests, parity fixtures, packaging posture, and release evidence.
Scala/Spark, Swift, Stata, and MATLAB remain deferred until those
surface-specific criteria are recorded.

## Target architecture

The intended end state is one Rust calculator core exposed through thin
surfaces for Python, Rust, R, Julia, C#/.NET, Go, TypeScript/WASM, Java/JVM,
C ABI, SQL/DuckDB, SAS interoperability, CLI/file workflows, web demos, and
Power Platform orchestration.

Formula logic must stay single-sourced. Bindings, apps, notebooks, SQL
extensions, and low-code assets may translate inputs and present outputs, but
they must not duplicate calculator math.

## Promotion lifecycle

Each calculator stream advances independently:

1. Python baseline.
2. Rust canary.
3. Rust opt-in.
4. Rust default.

Rust default requires fixture parity, packaging evidence, documentation, and
binding contracts for that stream. Evidence from one stream does not promote
another stream.

## Contract surfaces

The roadmap contract is versioned at
`contracts/polyglot-rust-core-roadmap/polyglot-rust-core-roadmap.contract.json`.

It covers:

* Arrow-compatible batch input and output.
* Machine-readable diagnostics.
* Provenance and checksum fields.
* Validation status semantics.
* Binding conformance expectations.
* ABI boundary expectations.
* Synthetic fixture gates.

## Packaging and release surfaces

The package roadmap distinguishes current, preview, private, release-candidate,
and general-availability states. Python is the current validated public
runtime. Rust crates, C ABI, TypeScript/WASM, SQL/DuckDB, CLI/file, R, Julia,
NuGet/C#, Go, JVM, SAS interop, web demos, and Power Platform managed
solutions each need their own release gate before public support claims.

## Related source material

* [Rust core architecture](./rust-core-architecture/)
* [Public calculator contract](./public-calculator-contract/)
* [Validation vocabulary](./validation-vocabulary/)
* [Release policy](./release-policy/)
* [Supply-chain controls](./supply-chain-controls/)

## Non-overclaiming rule

Public docs should say "Python baseline" unless a stream has explicit Rust
parity evidence. Public docs should say "Rust canary" or "Rust opt-in" only
when the stream has the matching validation record. Public docs should say
"Rust default" only after parity, packaging, fallback, and release evidence are
complete for that stream.
