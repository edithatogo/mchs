# Audience and Language Strategy

The project should not try to support every language equally. The language
roadmap should be governed by two primary audiences and one rule: no adapter may
own formula logic.

Rust core foundation evidence is recorded. Rust remains canary/preview for
declared stream-year slices until release evidence closes; additional
language-adapter expansion is governed by audience, owner, contract, parity,
packaging, and release evidence criteria rather than by a broad GA claim.

## Primary audiences

### Researchers

Researchers need reproducibility, transparent evidence, and familiar analysis
workflows.

**Priority surfaces:**

| Surface | Rationale | Current Status |
|---------|-----------|----------------|
| Python | Validated public runtime; primary researcher delivery surface. | GA (current baseline) |
| R | Health-economics and biostatistics standard; local CLI/file wrapper exists. | Planned — requires owner and release evidence |
| CLI/file | Language-neutral batch execution for any analysis workflow. | Planned — immediate priority after GA |
| Arrow/Parquet | Interchange format for high-volume and cross-language data. | Planned — part of GA surface set |
| Quarto/Jupyter documentation | Reproducible research notebook output. | In progress — Starlight + generated references |
| Julia | Analytics and scientific computing community where existing binding work can be retained. | Canary — existing work retained, no new development until post-GA |

**Conditional surfaces:**

| Surface | Condition | Current Status |
|---------|-----------|----------------|
| SAS interoperability | Private/local reference comparison for licensed SAS users and legacy institutional datasets. | Private/no new development — no public adapter; retain existing SAS-read workflows only |
| Stata interoperability | Health-economics and econometric workflow demand. | Deferred until stable CLI/file contracts and named owner |
| MATLAB interoperability | Numerical and legacy analytics workflows. | Deferred until named owner and evidence case |

### Enterprise engineers

Enterprise engineers need stable contracts, deployment boundaries, and release
evidence.

**Priority surfaces:**

| Surface | Rationale | Current Status |
|---------|-----------|----------------|
| Rust crate | Intended future calculator core; required GA surface. | Planned — immediate priority |
| HTTP API | Service integration for enterprise deployment. | Planned — immediate priority after GA |
| Python binding | Current validated public runtime with Rust-backed opt-in path. | GA (baseline) + canary (Rust opt-in) |
| TypeScript/WASM | Browser or edge deployment for docs demos and lightweight computation. | Canary — opt-in adapter for synthetic demos only |
| C#/.NET | Power Platform and Microsoft enterprise integration. | Preview adapter — release deferred behind signed NuGet evidence |
| MCP and OpenAI tool adapters | Model Context Protocol tools for agentic workflows plus OpenAI-compatible tool definitions over canonical schemas. | Planned — MCP first, OpenAI adapter deferred behind MCP contract |
| CLI/file contracts | Stable batch execution commands, exit codes, manifests. | Planned — immediate priority after GA |
| C ABI | Institutional embedding for cross-language FFI. | Planned — required GA surface |
| Arrow/Parquet interchange | High-throughput batch I/O for all surfaces. | Planned — part of GA surface set |

**Conditional surfaces:**

| Surface | Condition | Current Status |
|---------|-----------|----------------|
| TypeScript/WASM for GitHub Pages demos | Browser-based delivery requires synthetic-data-only privacy boundaries. | Canary — opt-in, not default |
| Power Platform | Orchestration-only; service boundaries must be approved. | Deferred with source-controlled connector contract; tenant ALM gates remain |
| Power BI | Visualisation integration via shared service contracts. | Planned — deferred behind Power Platform |

## Deferred language surfaces

These tracks remain valid future consumers of the shared calculator core. Rust
Core GA is no longer the active blocker; implementation work should proceed
only after each surface has an accountable audience, owner, and evidence case.

| Language/Surface | Deferral Gate | Rationale | Dependencies |
|-----------------|---------------|-----------|--------------|
| Scala/Spark | Audience/owner evidence gate | Needs named enterprise audience and owner | Arrow/Parquet, service contract |
| Swift | Audience/owner evidence gate | Needs Apple-platform healthcare audience and owner | C ABI, service contract |
| Stata | Audience/owner evidence gate plus stable CLI/file contracts | Retain for health-economics with a named owner | CLI/file contracts |
| MATLAB | Audience/owner evidence gate | Needs healthcare economics audience and owner | C ABI, CLI/file, service contract |
| Go | No new development | Cross-compilation posture not validated; no named audience | Arrow/Parquet, CLI/file |
| Standalone C (non-ABI) | No new development | C ABI is the required GA surface; standalone C is not a separate delivery target | C ABI |
| SQL/DuckDB | Historical | Prior references retained for traceability; not an active surface | N/A |

## Promotion criteria

A language or surface can move forward only when it has:

1. **Named audience.** Who needs this surface? What workflows does it enable?
2. **Named owner or maintainer.** Who maintains contract tests, fixtures, docs,
   and releases?
3. **Thin-binding design.** No formula logic in the adapter; logic stays in the
   shared core.
4. **Contract tests against canonical schemas.** The surface must pass versioned
   contract tests.
5. **Parity fixtures.** Shared fixture packs verify output parity across surfaces.
6. **Documentation and examples.** Each surface has usage docs, examples, and
   known-limitations notes.
7. **Packaging and release evidence.** The package is published, signed, and
   provenance-tracked.
8. **Release evidence bundle.** Evidence exists for every dimension: stream, year,
   jurisdiction, surface, runtime.

No surface may claim GA status without completing all eight criteria. A surface
without a named audience and owner is `no_new_development` by default.

## Implementation sequencing

The immediate implementation sequence is:

1. **Rust core foundation** — Foundation evidence is recorded, but Rust remains
   canary/preview until stream-year parity and release evidence close. Keep the
   evidence gates active for any surface promotion.
2. **Canonical domain schemas** — JSON Schema contracts for calculator
   request/response, diagnostics, provenance, support status, evidence.
3. **CLI/file contracts** — Stable CLI commands, exit codes, manifests,
   Arrow/Parquet batch files.
4. **HTTP API contract** — OpenAPI 3.1 domain contract (not an LLM endpoint).
5. **MCP contract** — Calculator tools and resources for agentic workflows.
6. **OpenAI tool adapter** — OpenAI-compatible tool definitions over canonical
   schemas.
7. **HWAU terminology migration** — Generic healthcare weighted activity unit
   abstraction with NWAU alias.
8. **State and local pricing registry** — National, state, local, and discounted
   price schedules with provenance.
9. **Parallel valuation outputs** — HWAU-only, national, state, local, discounted
   outputs in parallel.
10. **Conditional language surfaces** — Only after Rust foundation evidence,
    stream-specific promotion evidence, and documented demand.

## Non-overclaiming rule

- Public docs must show the narrowest truthful support status.
- A stream without parity evidence is `blocked` or `planned`, not GA.
- A language without a named owner is `no_new_development`.
- Deferred tracks must be documented as deferred, not as active implementation
  targets.
- Any language surface that is not listed as a priority above is frozen until
  its audience, owner, parity, packaging, and release evidence are recorded.
