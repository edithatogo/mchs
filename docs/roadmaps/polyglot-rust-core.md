# Polyglot Rust Core Roadmap

This roadmap documents the current Python-first state, the intended Rust-core
target state, and the sequencing tracks that govern the transition.

## Immediate priority

Rust Core GA is now the immediate priority. See
[Rust Core GA](./rust-core-ga.md) for the execution roadmap from governance
freeze through release-candidate and GA promotion. Current open language
adapter tracks are deferred until the Rust core reaches release-candidate
status and the required Rust crate, CLI/file, Python binding, C ABI, and
Arrow/Parquet surfaces are stable.

## Current state

- Python remains the validated runtime path for published calculator behavior.
- Rust is an opt-in target, not the default runtime.
- Public documentation should describe implemented behavior and separate it
  from future work and validation evidence.

## Target state

- A shared Rust calculator core becomes the single source of formula logic.
- Thin bindings and adapters expose that core to Python, Rust, R, Julia,
  C#/.NET, Go, TypeScript/WASM, Kotlin/Native, C ABI, SQL/DuckDB, SAS interop,
  CLI/file workflows, web surfaces, and Power Platform orchestration.
- Additional FOSS-facing roadmap surfaces include Kotlin/Native, Scala/Spark,
  Swift, Stata, and MATLAB. These are contract/file/service consumers, not
  independent formula implementations.
- Python remains supported while parity evidence is incomplete.
- Rust becomes the default runtime only after fixture parity, packaging,
  documentation, and binding contracts are complete.

## Roadmap tracks

| Track family | Track link | Why it matters |
| --- | --- | --- |
| Binding | [Python Rust Binding Stabilization](../../conductor/tracks/python_rust_binding_stabilization_20260512/spec.md) | Defines the opt-in Python boundary over the Rust core and the fallback rules while parity is still in progress. |
| Abstraction | [Abstraction Doctrine Enforcement](../../conductor/archive/abstraction_doctrine_enforcement_20260512/spec.md) | Establishes the canonical kernel boundary so formulas, adapters, and docs stay aligned. |
| Source-manifest | [Reference Data Manifest Schema](../../conductor/archive/reference_data_manifest_schema_20260512/spec.md) | Defines the year-scoped manifest shape that records sources, gaps, provenance, and validation status. |
| Formula-bundle | [Formula and Parameter Bundle Pipeline](../../conductor/archive/formula_parameter_bundle_pipeline_20260512/spec.md) | Provides the extraction, versioning, and validation pipeline for formula and parameter bundles. |
| Validation-gate | [Pricing-Year Validation Gates](../../conductor/archive/pricing_year_validation_gates_20260512/spec.md) | Prevents unsupported support claims until the required source and fixture evidence exists. |
| GA | [Rust Core GA](../../conductor/tracks/rust_core_ga_20260513/spec.md) | Makes Rust GA the immediate priority, defers lower-priority adapters, and defines the evidence gates for release-candidate and GA promotion. |
| Contract | [Canonical Contract Foundation](../../conductor/archive/canonical_contract_foundation_20260513/spec.md) | Defines canonical schemas before CLI/file, API, MCP, OpenAI adapter, and language surfaces. |
| Contract | [Support Status Matrix](../../conductor/archive/support_status_matrix_20260513/spec.md) | Defines machine-readable statuses for streams, years, jurisdictions, surfaces, runtimes, and languages. |
| Contract | [CLI/File Contracts](../../conductor/archive/cli_file_contracts_20260513/spec.md) | Defines the stable batch and automation boundary for Rust Core GA. |
| Contract | [HTTP API Contract](../../conductor/tracks/http_api_contract_20260513/spec.md) | Defines the OpenAPI 3.1 domain API over canonical schemas. |
| Contract | [MCP Contract](../../conductor/tracks/mcp_contract_20260513/spec.md) | Defines a Rust-backed agent-facing MCP server with tools and resources over canonical schemas. |
| Adapter | [OpenAI Tool Adapter](../../conductor/tracks/openai_tool_adapter_20260513/spec.md) | Defines a thin OpenAI tool adapter without making the calculator an LLM endpoint. |
| Governance | [Audience Language Strategy](../../conductor/archive/audience_language_strategy_20260513/spec.md) | Prioritizes researcher and enterprise-engineer surfaces and blocks unsupported language sprawl. |
| Domain | [HWAU Terminology Migration](../../conductor/tracks/hwau_terminology_migration_20260513/spec.md) | Uses HWAU as the generic weighted activity unit concept while retaining NWAU as Australian source terminology. |
| Reference-data | [State and Local Price Registry](../../conductor/tracks/state_local_price_registry_20260513/spec.md) | Sources national, state, local, and discounted price schedules over time with provenance. |
| Reference-data | [Jurisdiction Price Source Index](../../conductor/tracks/jurisdiction_price_source_index_20260513/spec.md) | Indexes jurisdiction price sources before value extraction. |
| Reference-data | [NSW Funding Model](../../conductor/tracks/nsw_funding_model_20260513/spec.md) | Models NSW State Price per NWAU/HWAU, LHD/SHN applicability, adjustments, and provenance. |
| Reference-data | [Jurisdiction Funding Model Registry](../../conductor/tracks/jurisdiction_funding_model_registry_20260513/spec.md) | Covers Australian state and territory funding models, including ACT and NT, with source-status handling. |
| Output | [Parallel Valuation Outputs](../../conductor/tracks/parallel_valuation_outputs_20260513/spec.md) | Produces HWAU-only, national, state, local, and discounted valuations in parallel. |
| Architecture | [Rust Crate Boundaries and HWAU Rename](../../conductor/archive/rust_crate_boundary_rename_20260513/spec.md) | Plans crate boundaries and NWAU-to-HWAU migration without disrupting active Rust work. |
| Architecture | [GitHub Pages API Architecture](../../conductor/tracks/github_pages_api_architecture_20260513/spec.md) | Clarifies static docs/WASM versus external or local API hosting. |
| Release | [Release Evidence Bundle](../../conductor/tracks/release_evidence_bundle_20260513/spec.md) | Defines evidence required before release-candidate and GA support claims. |

## Sequencing guidance

1. Lock the abstraction boundary first so formulas stay single-sourced.
2. Make source manifests and formula bundles explicit before widening adapter
   coverage.
3. Stabilize the Python binding over the Rust core while Rust remains
   opt-in.
4. Keep validation gates conservative so docs never outrun the evidence.

## Documentation rule

This roadmap is a documentation integration artifact. It should be read as a
status and sequencing guide, not as proof that the Rust core or any downstream
binding is complete.
