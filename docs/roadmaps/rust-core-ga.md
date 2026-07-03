# Rust Core GA Roadmap

This roadmap makes the Rust calculator core the immediate priority. Downstream
language and interoperability tracks are deferred until the core reaches a
validated release-candidate state.

## Goal

Promote Rust from future/preview target to the GA runtime for supported
calculator streams, with Python retained as the baseline reference and fallback
until each stream has complete parity evidence.

## Non-negotiable GA principles

- Rust owns formula execution for promoted streams.
- Python remains the reference baseline until a stream is promoted.
- Bindings, notebooks, apps, and language packages stay thin.
- Source manifests, formula bundles, coding-set registries, fixtures,
  diagnostics, and provenance are versioned inputs to the core.
- No stream becomes Rust-default without SAS/Excel/source parity evidence where
  those reference artefacts exist.
- No public package or documentation claim may outrun release evidence.

## Deprioritized work

The following tracks are valid future work but are not immediate priorities:

- Scala/Spark Binding
- Swift Binding
- Stata Interoperability
- MATLAB Interoperability

They should remain boundary-only roadmap items until the Rust core reaches
release-candidate status and the C ABI/CLI/file contracts are stable enough for
additional consumers.

## Phase 0: Governance freeze

Purpose: stop scope drift while the core is promoted.

Exit gates:

- Roadmap declares Rust Core GA as the immediate priority.
- Open language-interoperability tracks are explicitly deferred.
- Release claims distinguish `private`, `preview`, `release-candidate`, and
  `ga`.
- Documentation states that adapters cannot implement formula logic.

## Phase 1: Contract and data foundation

Purpose: make every core input explicit and versioned.

Deliverables:

- Versioned calculator contract schemas.
- Versioned source manifests for supported streams and pricing years.
- Versioned formula and parameter bundles.
- Versioned coding-set and classification registries.
- Arrow-compatible batch input/output schemas.
- Stable diagnostics, errors, and provenance schemas.

Exit gates:

- Schemas are exported and validated in CI.
- Fixture packs identify source artefacts, checksums, expected outputs, and
  licensing/redistribution status.
- Missing or unavailable source artefacts produce blocked status rather than
  inferred support.

## Phase 2: Rust kernel architecture

Purpose: implement the calculator core without duplicating language-specific
business logic.

Deliverables:

- Rust crate workspace for core types, formula kernels, registries,
  diagnostics, provenance, and CLI/file execution.
- Stream modules isolated behind stable traits.
- Decimal/money/weight precision policy.
- Deterministic error model.
- No patient-level data or proprietary reference tables committed.

Exit gates:

- Rust code path can execute synthetic fixtures for at least one end-to-end
  canary stream/year.
- Core APIs are thin enough for Python, CLI/file, C ABI, and WASM consumers.
- Bindings must not own formula logic.

## Phase 3: Parity and validation

Purpose: prove correctness stream by stream.

Validation hierarchy:

1. Source/schema conformance.
2. Golden synthetic fixtures.
3. SAS/Excel parity where public or locally licensed reference artefacts exist.
4. Python baseline parity.
5. Cross-surface parity for CLI/file and Python binding.
6. Regression and mutation tests for edge cases.

Exit gates:

- At least one representative stream/year completes the full evidence ladder.
- Every supported stream has a parity status: `blocked`, `canary`, `opt-in`,
  `release-candidate`, or `ga`.
- Coverage target for GA streams is greater than 90 percent over the Rust core
  and validation-critical adapters.

## Phase 4: Delivery surfaces required for GA

Purpose: expose the core through stable minimum surfaces before widening the
language matrix.

Required surfaces:

- Rust crate.
- CLI/file contract.
- Python binding with fallback controls.
- C ABI headers and ownership rules.
- Arrow/Parquet batch interchange.

Deferred surfaces:

- Scala/Spark.
- Swift.
- Go.
- MATLAB.
- SQL/DuckDB.
- Any additional language adapter not required for GA validation.

Exit gates:

- Required surfaces have contract tests and release artefacts.
- Fallback and rollback behavior is documented and tested.
- No deferred surface is needed for the first GA release.

## Phase 5: CI/CD, release, and security hardening

Purpose: make GA reproducible.

Deliverables:

- Rust formatting, linting, typing-equivalent checks, docs, and security scans.
- Cross-platform build matrix for supported targets.
- Coverage upload through the Codecov app.
- SBOM and provenance artefacts.
- Signed tags and release notes.
- Package publishing dry-run and production release workflow.
- Docs deployment with Starlight.

Exit gates:

- CI passes on protected main.
- Release artefacts are reproducible from CI.
- Security and dependency scans have no unresolved high-severity blockers.
- Documentation, package metadata, homepage, and release notes agree on support
  status.

## Phase 6: Release-candidate to GA promotion

Purpose: promote conservatively, with rollback.

Release-candidate gates:

- Rust path is opt-in for supported streams.
- Parity evidence is attached to the release.
- Python fallback remains available.
- Known limitations are documented.

GA gates:

- Rust path is default for promoted streams.
- No open parity gaps exist for supported cases.
- Rollback procedure is documented and tested.
- Public docs and package metadata state exact supported streams and years.
- A post-release monitoring and issue triage plan exists.

## Immediate implementation order

1. Create the Rust Core GA Conductor track.
2. Freeze language-adapter expansion behind the Rust Core GA track.
3. Define the audience language strategy for researchers and enterprise engineers.
4. Define the support status matrix.
5. Export and validate canonical contract schemas.
6. Define CLI/file contracts.
7. Define the HTTP API contract.
8. Define the MCP contract.
9. Define the OpenAI tool adapter as a thin integration layer.
10. Define the jurisdiction price source index.
11. Implement the Rust workspace and one representative stream/year canary.
12. Add parity validation against Python and available SAS/Excel artefacts.
13. Harden required delivery surfaces.
14. Attach release evidence bundles.
15. Promote one stream/year to release-candidate.
16. Promote to GA only after evidence and release automation pass.

## Parallel implementation lanes

The roadmap is intentionally parallelisable. Agents can work concurrently when
their write scopes and contracts are separated:

- Lane A: canonical schemas, support status, diagnostics, errors, and
  provenance.
- Lane B: Rust core crate, kernel traits, registries, CLI/file execution, and
  fixture execution.
- Lane C: CLI/file, HTTP API, MCP, and OpenAI adapter contracts generated from
  canonical schemas.
- Lane D: HWAU terminology, national/state/local price registries, NSW model,
  jurisdiction models, and parallel valuation outputs.
- Lane E: documentation, evidence bundles, release automation, CI/CD, and
  security gates.

No lane may redefine formula logic, bypass canonical schemas, or mark support
as complete without the required evidence gates.

## Definition of done

Rust Core GA is complete only when at least one declared calculator stream/year
is defaulting to Rust in a public release, the evidence bundle is attached to
that release, Starlight documentation is published, and unsupported streams are
clearly marked as unavailable, blocked, canary, or opt-in.
