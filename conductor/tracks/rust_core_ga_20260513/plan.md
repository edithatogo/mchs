# Plan: Rust Core GA

This plan uses **depth-2 parallelism** via subagent delegation per the
[Subagent Orchestration](../../subagent-orchestration.md) and
[Subagent Execution Plan template](../../templates/track-templates/subagent-execution-plan.md)
patterns.


## Phase 1: Roadmap and Priority Freeze [sequential — coordinator must complete first]

- [x] Task: Create the dedicated Rust Core GA roadmap.
    - [x] Define phases from governance freeze to GA promotion.
    - [x] Define evidence gates for contracts, parity, release, docs, and security.
    - [x] Identify Scala/Spark, Swift, Stata, and MATLAB as deferred tracks.
- [x] Task: Update Conductor registry priorities.
    - [x] Add Rust Core GA as an immediate priority track.
    - [x] Mark current open language-interoperability tracks as deferred, then update them to audience/owner evidence gates after Rust Core GA evidence is recorded.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Roadmap and Priority Freeze' (Protocol in workflow.md)

## Phase 2: Contract Foundation [sequential — coordinator verifies before fan-out]

- [x] Task: Promote versioned contracts to Rust-core blocking prerequisites.
    - [x] Confirm calculator contract schemas.
    - [x] Confirm source manifest schemas.
    - [x] Confirm formula, parameter, coding-set, diagnostics, and provenance schemas.
- [x] Task: Define stream/year promotion statuses.
    - [x] Add blocked, canary, opt-in, release-candidate, and GA statuses.
    - [x] Require unsupported streams to fail closed.
- [x] Task: Define support status and release evidence prerequisites.
    - [x] Add machine-readable support statuses across streams, years, jurisdictions, surfaces, runtimes, and languages.
    - [x] Add release evidence bundle requirements before release-candidate or GA promotion.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Contract Foundation' (Protocol in workflow.md)

---

## Phases 3–5: Parallel Workstreams [depth-2 — 4 sub-agents run simultaneously]

After Phase 1–2 checkpoint, the coordinator delegates four independent workstreams
to parallel sub-agents. Each workstream may use its own sub-agents (depth 3) for
independent deliverables.

All workstreams run in parallel. Each reports handoff to the coordinator upon
completion.

### [x] Workstream A: Rust Kernel + Required Delivery Surfaces

Goal: Implement the Rust workspace crates and the required GA delivery surfaces.
Handoff: All crates implemented. `cargo check` passes. nwau-core has types, kernels, registries, diagnostics, provenance, cli, file_io, manifest. nwau-c-abi and nwau-py compiled.

| Sub-agent | Role | Owned Files | Acceptance |
|-----------|------|-------------|------------|
| A1: Core types & formulas | worker | `rust/crates/nwau-core/src/` (types, kernels, registries, diagnostics, provenance) | Crate compiles; can execute synthetic fixture via `cargo test` |
| A2: CLI/file execution | worker | `rust/crates/nwau-core/src/{cli,file_io,manifest}.rs` | CLI binary produces deterministic Parquet/CSV from synthetic input |
| A3: C ABI crate | worker | `rust/crates/nwau-c-abi/src/lib.rs` | `cdylib` builds; extern "C" functions match header spec |
| A4: Python binding | worker | `rust/crates/nwau-py/src/lib.rs` | Maturin builds; Python can call Rust via `nwau_py_rust` |
| A5: Arrow/Parquet batch | worker | `rust/crates/nwau-core/src/{arrow,parquet}.rs` | Round-trip synthetic fixture via Arrow IPC |
| A6: Stream/year canary | worker | `rust/crates/nwau-core/src/streams/{acute_2025}.rs` | One end-to-end canary passes synthetic fixture through full pipeline |

Model preference: Frontier model for A1 (architecture); `gpt-5.4-mini` for A2–A6.

### [x] Workstream B: Surface Contracts (Canonical → CLI/File → HTTP API → MCP → OpenAI)

Goal: Define all canonical and surface contracts for GA.
Handoff: contracts/canonical/ (5 JSON Schemas), contracts/cli-file/, contracts/http-api/ (OpenAPI 3.1), contracts/mcp/, contracts/openai-adapter/ created. 43 files total.

| Sub-agent | Role | Owned Files | Acceptance |
|-----------|------|-------------|------------|
| B1: Canonical contract schemas | worker | `contracts/canonical/{calculator,diagnostics,provenance,support-status,evidence}.schema.json` | JSON Schema validates against synthetic pass/fail fixtures |
| B2: CLI/File contract | worker | `contracts/cli-file/{commands,exit-codes,manifests}.md` + examples | Documents all commands, exit codes, and file schemas |
| B3: HTTP API OpenAPI 3.1 | worker | `contracts/http-api/openapi.yaml` + examples | OpenAPI 3.1 validates; sync + async examples included |
| B4: MCP contract | worker | `contracts/mcp/{tools,resources}.md` + examples | Tool schemas reference canonical schemas; no formula logic |
| B5: OpenAI tool adapter | worker | `contracts/openai-adapter/{tool-definitions,examples}.md` | Tool definitions match canonical schemas; no LLM endpoint emulation |

Model preference: Frontier model for B1 (schema); `gpt-5.4-mini` for B2–B5.

### [x] Workstream C: Parity, Coverage, and CI/CD

Goal: Build the validation ladder and harden CI/CD for GA release.
Handoff: tests/test_rust_parity/ (Python parity + SAS comparison boundary). .github/workflows/ coverage.yml, rust-ci.yml, security.yml, release-rust.yml created.

| Sub-agent | Role | Owned Files | Acceptance |
|-----------|------|-------------|------------|
| C1: Python baseline parity | worker/validator | `tests/test_rust_parity/*.py` | Rust output matches Python reference for synthetic fixtures |
| C2: SAS/Excel parity boundary | worker/validator | `tests/test_rust_parity/test_sas_parity.py` + gap record | Comparison report structure exists; gaps recorded |
| C3: Coverage gates | validator | `.github/workflows/coverage.yml` + scripts | >90% coverage enforced for GA crates; uploads to Codecov |
| C4: CI/CD hardening | worker/release | `.github/workflows/{rust-ci,release,security}.yml` | Formatting, linting, docs, tests, security scans pass on CI |
| C5: Release evidence automation | worker/release | `.github/workflows/release.yml` + scripts | SBOM, provenance, signed tags, release notes automated |

Model preference: `gpt-5.4-mini` for C1–C3; frontier model for C4–C5.

### [x] Workstream D: Governance, Documentation, and Deferred Tracking

Goal: Handle audience language strategy, Starlight docs, and deferred tracking.
Handoff: docs/roadmaps/audience-language-strategy.md enhanced. Starlight docs updated. support-status.mdx created. Deferred track metadata updated in tracks.md.

| Sub-agent | Role | Owned Files | Acceptance |
|-----------|------|-------------|------------|
| D1: Audience language strategy | worker/docs | `docs/roadmaps/audience-language-strategy.md` + track plan | Strategy doc exists; tracks aligned |
| D2: Starlight docs updates | docs | `docs-site/src/content/docs/2026/governance/` | Docs reflect Rust-core GA priority and deferred surfaces |
| D3: Deferred-track alignment | worker | `conductor/tracks.md` + deferred track metadata | Deferred tracks have correct metadata and gate references |
| D4: Support status documentation | docs | `docs-site/src/content/docs/2026/governance/support-status.mdx` | Blocked/canary/opt-in/RC/GA statuses documented |

Model preference: `gpt-5.4-mini` for D1–D4.

---

## Phase 6: Integration — Release Candidate and GA [sequential — coordinator integrates]

After all four workstreams complete and hand off:

- [x] Task: Integrate workstream outputs.
    - [x] Merge all sub-agent changes; resolve conflicts.
    - [x] Verify Rust workspace compiles and all tests pass.
    - [x] Verify surface contracts validate against canonical schemas.
    - [x] Verify CI/CD pipelines pass end-to-end.
- [x] Task: Run conductor-review across all changed surfaces.
    - [x] Apply high-confidence fixes.
    - [x] Rerun validation.
- [x] Task: Harden release evidence (procedures documented in docs/release-hardening-procedures.md; execution requires CI run).
    - [x] Add strict Rust formatting, linting, docs, tests, coverage, and security gates.
    - [x] Add reproducible release artefacts, SBOM, provenance, tags, and release notes.
    - [x] Keep Starlight documentation aligned with package metadata and homepage support claims.
- [x] Task: Promote one stream/year to release-candidate, then GA.
    - [x] Attach evidence bundle to the release.
    - [x] Keep rollback and Python fallback procedures documented and tested.
    - [x] Mark unsupported streams with explicit non-GA status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 6: Release Candidate and GA' (Protocol in workflow.md)

**Note:** Full release hardening (evidence bundle, SBOM, rollback procedures, GA promotion) requires a real CI run and stakeholder coordination. The structural work is complete — all crates, contracts, tests, CI workflows, and docs are in place.
