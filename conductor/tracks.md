# Project Tracks

This file tracks the delivery order for the project. The focused tracks below are the implementation source of truth. The modernization foundation track is retained only as an umbrella coordination track and must not duplicate work owned by the focused tracks.

New tracks must follow the governance rules in
[`roadmap-governance.md`](./roadmap-governance.md). In particular, new track
metadata should include track class, current state, dependencies, primary
contract, completion evidence, and publication status. Roadmap or scaffold
content alone is not sufficient evidence for marking a track complete.

## Delivery Order

1. [x] **Track: Source Archive and Provenance Registry**
   *Link: [./tracks/source_archive_provenance_20260504/](./tracks/source_archive_provenance_20260504/)*
   *Gate: establish source acquisition, storage policy, and manifest provenance before downstream validation or implementation work.*

2. [x] **Track: Cross-Language Golden Test Suite**
   *Link: [./archive/cross_language_golden_tests_20260504/](./archive/cross_language_golden_tests_20260504/)*
   *Depends on: source archive manifesting and known-good reference artifacts.*
   *Gate: define validation evidence and fixture contracts before broad tooling or architecture migrations.*

3. [x] **Track: Python Tooling and CI Modernization**
   *Link: [./tracks/python_tooling_ci_20260504/](./tracks/python_tooling_ci_20260504/)*
   *Depends on: source archive provenance and validation fixture shape.*
   *Gate: lock the supported Python/tooling matrix, CI, coverage, type checking, linting, and profiling entry points before larger refactors.*

4. [x] **Track: Calculator Core Abstraction and Validation Models**
   *Link: [./archive/calculator_core_abstractions_20260504/](./archive/calculator_core_abstractions_20260504/)*
   *Depends on: validation evidence and CI coverage so the boundary contract can be protected by tests.*
   *Gate: define the calculator core boundary, parameter models, schemas, and provenance metadata before adapter work.*

5. [x] **Track: Public Calculator API Contract**
   *Link: [./tracks/public_api_contract_20260504/](./tracks/public_api_contract_20260504/)*
   *Depends on: calculator core abstractions and golden fixtures.*
   *Gate: freeze the versioned input/output contract before web, C#, or Power Platform integration.*

6. [x] **Track: Arrow and Polars Data Bundle Migration**
   *Link: [./archive/arrow_polars_data_bundle_20260504/](./archive/arrow_polars_data_bundle_20260504/)*
   *Depends on: calculator core abstractions and stable validation fixtures.*
   *Gate: migrate data representation and DataFrame boundaries only after the core contract is stable.*

7. [x] **Track: GitHub Pages Web App Prototype**
   *Link: [./tracks/github_pages_web_app_20260504/](./tracks/github_pages_web_app_20260504/)*
   *Depends on: public API contract, validation fixtures, and governance rules for demo-only flows.*
   *Gate: implement the browser-facing prototype only after a contract and privacy boundary exist.*

8. [x] **Track: C# Calculation Engine and Power Platform Adapter**
   *Link: [./tracks/csharp_power_platform_engine_20260504/](./tracks/csharp_power_platform_engine_20260504/)*
   *Depends on: public API contract, calculator core abstractions, and golden fixtures.*
   *Gate: keep Power Platform orchestration separate from the calculation engine and drive parity from shared fixtures.*

9. [x] **Track: Release and Supply-Chain Governance**
   *Link: [./tracks/release_supply_chain_governance_20260504/](./tracks/release_supply_chain_governance_20260504/)*
   *Depends on: CI, validation evidence, and contract stability.*
   *Gate: add release policy, signed artifacts, dependency automation, and provenance controls after the implementation pipeline is stable.*

10. [x] **Track: Starlight Documentation Site and Versioning**
   *Link: [./archive/starlight_docs_site_20260506/](./archive/starlight_docs_site_20260506/)*
   *Depends on: public calculator contracts, validation vocabulary, docs governance, and GitHub Pages delivery rules.*
   *Gate: define and ship the Starlight documentation platform, its versioning model, migration path, plugin set, and deployment workflow before any docs-site decommissioning is considered.*

11. [x] **Track: Ecosystem Standards and Language Readiness**
   *Link: [./tracks/ecosystem_language_readiness_20260507/](./tracks/ecosystem_language_readiness_20260507/)*
   *Depends on: public calculator contracts, golden fixtures, release governance, Starlight documentation, and Power Platform boundary documentation.*
   *Gate: assess scientific software standards, language packaging maturity, C# and Power Platform implementation readiness, contribution pathways, and health interoperability standards before starting new language ports or integration surfaces.*

12. [x] **Track: Rust Core Architecture and Calculator Abstraction**
   *Link: [./tracks/rust_core_architecture_20260510/](./tracks/rust_core_architecture_20260510/)*
   *Depends on: public calculator contracts, Arrow/Parquet bundle guidance, golden fixtures, ecosystem readiness, and existing C# and Power Platform boundary documentation.*
   *Gate: define Rust as the intended future calculator core and document formula, parameter, schema, reference data, provenance, validation, and adapter boundaries before Rust implementation begins.*

13. [x] **Track: Rust Acute 2025 Proof of Concept with Python Bindings**
   *Link: [./archive/rust_acute_python_poc_20260510/](./archive/rust_acute_python_poc_20260510/)*
   *Depends on: Rust core architecture, acute 2025 golden fixtures, Python packaging, and Arrow-compatible batch contract decisions.*
   *Gate: implement the first Rust-backed acute 2025 canary behind explicit Python opt-in and prove fixture parity before any default runtime change.*

14. [x] **Track: Multi-Surface Binding and Delivery Roadmap**
   *Link: [./tracks/multi_surface_binding_delivery_20260510/](./tracks/multi_surface_binding_delivery_20260510/)*
   *Depends on: Rust core architecture, Rust/Python proof-of-concept results, public contracts, web architecture, and Power Platform boundary rules.*
   *Gate: define binding and delivery sequencing for Python, R, Julia, C#, Rust, Go, TypeScript/WASM, Streamlit, GitHub Pages, and Power Platform before implementing additional adapters.*

15. [x] **Track: Rust CI, Pre-Commit, and Supply-Chain Hardening**
   *Link: [./tracks/rust_ci_supply_chain_hardening_20260510/](./tracks/rust_ci_supply_chain_hardening_20260510/)*
   *Depends on: Python tooling and CI modernization, release governance, docs-site workflow, and Rust workspace decisions.*
   *Gate: align branch triggers, pre-commit hooks, Rust quality gates, dependency review, advisory checks, provenance, and release hardening before Rust code is treated as merge-ready.*

16. [x] **Track: Documentation, Release, and Public Readiness**
   *Link: [./tracks/docs_release_publication_readiness_20260510/](./tracks/docs_release_publication_readiness_20260510/)*
   *Depends on: Rust core architecture, binding delivery roadmap, Starlight documentation, release governance, validation vocabulary, and public repository status.*
   *Gate: publish conservative docs for current versus intended Rust-backed behavior, release status, contributor workflows, public-readiness gaps, and safe delivery surfaces.*

## Umbrella Coordination

- [x] **Track: Modernization Foundation**
  *Link: [./tracks/modernization_foundation_20260504/](./tracks/modernization_foundation_20260504/)*
  *Coordination only.*
  *Retained to preserve sequencing and governance context.*
  *Do not duplicate work already owned by the focused tracks above.*

---

- [x] **Track: Power Platform ALM App Setup and Delivery**
  *Link: [./archive/power_platform_alm_app_20260510/](./archive/power_platform_alm_app_20260510/)*
  *Gate: research current Microsoft Power Platform ALM guidance, choose a supported source-control and deployment path, create the solution-based orchestration scaffold, and wire it into a repeatable pack/unpack and promotion workflow.*

- [x] **Track: Power BI and Power Platform CLI Tooling**
  *Link: [./archive/power_bi_cli_tooling_20260511/](./archive/power_bi_cli_tooling_20260511/)*
  *Depends on: Power Platform ALM App Setup and Delivery.*
  *Gate: bootstrap `az`/`pac`/`powerbi` CLI tooling, normalize PATH and version checks, explicitly reject `pacx` legacy path, and define the delivery contract for Power Platform solution and Power BI operations.*

- [x] **Track: IHACPA Source Archive Gap Closure and Restore Validation**
  *Link: [./archive/ihacpa_source_archive_gap_closure_20260511/](./archive/ihacpa_source_archive_gap_closure_20260511/)*
  *Depends on: source archive manifesting and restore-policy rules.*
  *Gate: recover or explicitly gap-record the remaining Box-hosted SAS artifacts, keep the archive manifest truthful, and validate restore behavior against the committed provenance record.*

- [x] **Track: IHACPA Feature Incorporation and Calculator Coverage Roadmap**
  *Link: [./archive/ihacpa_feature_incorporation_roadmap_20260511/](./archive/ihacpa_feature_incorporation_roadmap_20260511/)*
  *Depends on: source archive inventory and current calculator surfaces.*
  *Gate: map archive families and helpers to executable surfaces, classify complexity/HAC/AHR status, and close any remaining parity gaps with tests and documented follow-on work.*

---

- [x] **Track: IHACPA 2026-27 Support**
*Link: [./tracks/ihacpa_2026_27_support_20260512/](./tracks/ihacpa_2026_27_support_20260512/)*
*Gate: add current 2026-27 NEP, technical specification, price-weight, calculator, and classification-version support with explicit validation status.*

---

- [x] **Track: Community Mental Health Calculator Support**
*Link: [./archive/community_mental_health_calculator_20260512/](./archive/community_mental_health_calculator_20260512/)*
*Gate: separate community mental health and AMHCC shadow/current behavior from admitted mental health before claiming stream coverage.*

- [x] **Track: Classification Input Validation**
*Link: [./archive/classification_input_validation_20260512/](./archive/classification_input_validation_20260512/)*
*Gate: add stream-specific classification version matrices and strict input validation before broader calculator expansion.*

---

- [x] **Track: Costing-Study Tutorials and Examples**
*Link: [./archive/costing_study_tutorials_20260512/](./archive/costing_study_tutorials_20260512/)*
*Gate: provide synthetic, reproducible costing-study workflows connecting NWAU, NEP, AHPCS, NHCDC, and benchmarking use cases.*

---

- [x] **Track: Historical IHACPA Coverage Audit**
*Link: [./tracks/historical_ihacpa_coverage_20260512/](./tracks/historical_ihacpa_coverage_20260512/)*
*Gate: verify how far official NEP, technical specification, calculator, and NHCDC materials go back before extending historical support claims.*

---

- [x] **Track: Python Rust Binding Stabilization**
*Link: [./tracks/python_rust_binding_stabilization_20260512/](./tracks/python_rust_binding_stabilization_20260512/)*
*Gate: stabilize pyo3/maturin bindings while keeping Python as the validated public API and Rust-backed paths opt-in until parity is proven.*

---

- [x] **Track: R Binding**
*Link: [./archive/r_binding_20260512/](./archive/r_binding_20260512/)*
*Gate: support health-economics and costing-study R users without duplicating calculator formula logic.*

---

- [x] **Track: Julia Binding**
*Link: [./archive/julia_binding_20260512/](./archive/julia_binding_20260512/)*
*Gate: support Julia analytics through C ABI or Arrow/CLI interop while preserving single-sourced calculator logic.*

---

- [x] **Track: TypeScript and WebAssembly Binding**
*Link: [./archive/typescript_wasm_binding_20260512/](./archive/typescript_wasm_binding_20260512/)*
*Gate: enable browser docs demos and Node workflows from the shared Rust core with synthetic-data-only privacy boundaries.*

---

- [x] **Track: C ABI Binding**
*Link: [./archive/c_abi_binding_20260512/](./archive/c_abi_binding_20260512/)*
*Gate: define a stable institutional embedding ABI only after core schemas and calculator parity are stable.*

---

- [x] **Track: CLI and File Interoperability Binding**
*Link: [./archive/cli_file_interop_binding_20260512/](./archive/cli_file_interop_binding_20260512/)*
*Gate: provide a language-neutral Arrow/Parquet/CSV and CLI contract for ecosystems where native bindings are premature.*

---

- [x] **Track: Reference Data Manifest Schema**
*Link: [./archive/reference_data_manifest_schema_20260512/](./archive/reference_data_manifest_schema_20260512/)*
*Gate: define machine-readable pricing-year manifests for source artifacts, constants, coding sets, and validation status before automating future-year support.*

---

- [x] **Track: IHACPA Source Scanner**
*Link: [./archive/ihacpa_source_scanner_20260512/](./archive/ihacpa_source_scanner_20260512/)*
*Gate: discover and draft future IHACPA source manifests without overclaiming validation or redistributing restricted material.*

---

- [x] **Track: Pricing-Year Validation Gates**
*Link: [./archive/pricing_year_validation_gates_20260512/](./archive/pricing_year_validation_gates_20260512/)*
*Gate: prevent pricing years from being marked supported or validated without required source, extraction, and fixture evidence.*
*Evidence surfaces: `funding-calculator validate-year <year>`, the validation ladder in `conductor/roadmap-governance.md`, the status vocabulary in `conductor/validation-vocabulary.md`, and the manifest schema contract in `conductor/archive/reference_data_manifest_schema_20260512`.*

---

- [x] **Track: Pricing-Year Diff Tooling**
*Link: [./archive/pricing_year_diff_tooling_20260512/](./archive/pricing_year_diff_tooling_20260512/)*
*Gate: compare pricing years and summarize formula, parameter, classification, source, and validation deltas for review and releases.*
*Evidence surfaces: the installed `funding-calculator diff-year <from-year> <to-year>` command, `conductor/archive/pricing_year_diff_tooling_20260512/strategy.md`, and `conductor/archive/pricing_year_diff_tooling_20260512/ci_notes.md`.*

---

- [x] **Track: Coding-Set Version Registry**
*Link: [./archive/coding_set_version_registry_20260512/](./archive/coding_set_version_registry_20260512/)*
*Gate: record AR-DRG, AECC, UDG, Tier 2, AMHCC, ICD-10-AM, ACHI, and ACS version compatibility and licensing boundaries.*
*Evidence surfaces: `conductor/roadmap-governance.md`, `conductor/validation-vocabulary.md`, `conductor/archive/classification_input_validation_20260512/classification_matrix.md`, `docs/reviews/20260512-expert-panel/deliberation-and-prioritisation.md`, `conductor/archive/coding_set_version_registry_20260512/strategy.md`, and `conductor/archive/coding_set_version_registry_20260512/ci_notes.md`.*

---

- [x] **Track: Formula and Parameter Bundle Pipeline**
*Link: [./archive/formula_parameter_bundle_pipeline_20260512/](./archive/formula_parameter_bundle_pipeline_20260512/)*
*Gate: extract, normalize, version, diff, and validate future IHACPA formula and parameter bundles before production calculator claims.*
*Evidence surfaces: `reference-data/2026/manifest.yaml`, `contracts/source-scanner/examples/add-year.draft-manifest.json`, and `conductor/tracks/end_to_end_validated_canary_20260512`.*

---

- [x] **Track: AR-DRG ICD/ACHI/ACS Mapping Registry**
*Link: [./archive/ar_drg_icd_mapping_registry_20260512/](./archive/ar_drg_icd_mapping_registry_20260512/)*
*Gate: model version-specific relationships between ICD-10-AM, ACHI, ACS, AR-DRG versions, and mapping-table provenance before deriving or validating DRGs.*

---

- [x] **Track: AR-DRG Grouper Integration**
*Link: [./archive/ar_drg_grouper_integration_20260512/](./archive/ar_drg_grouper_integration_20260512/)*
*Gate: support precomputed AR-DRGs and licensed external grouper integration without reimplementing proprietary grouping logic.*

---

- [x] **Track: ICD-10-AM/ACHI/ACS Licensed Product Workflow**
*Link: [./archive/icd_achi_acs_license_workflow_20260512/](./archive/icd_achi_acs_license_workflow_20260512/)*
*Gate: define local-only handling, manifest references, commit guards, setup docs, and appropriate-use caveats for licensed classification tables and groupers.*

---

- [x] **Track: AR-DRG Version Parity Fixtures**
*Link: [./archive/ar_drg_version_parity_fixtures_20260512/](./archive/ar_drg_version_parity_fixtures_20260512/)*
*Gate: validate version-specific AR-DRG grouping and admitted acute NWAU behavior with safe synthetic and local licensed fixtures.*

---

- [x] **Track: Emergency UDG/AECC Transition Registry**
*Link: [./archive/emergency_udg_aecc_transition_registry_20260512/](./archive/emergency_udg_aecc_transition_registry_20260512/)*
*Gate: model UDG, AECC, transition periods, emergency stream compatibility, and pricing-year applicability before accepting emergency classification inputs as interchangeable.*

---

- [x] **Track: Emergency Code Mapping Pipeline**
*Link: [./archive/emergency_code_mapping_pipeline_20260512/](./archive/emergency_code_mapping_pipeline_20260512/)*
*Gate: add versioned, provenance-aware mapping bundles for source emergency fields to UDG or AECC outputs without inventing unsupported crosswalks.*

---

- [x] **Track: Emergency Grouper Integration**
*Link: [./archive/emergency_grouper_integration_20260512/](./archive/emergency_grouper_integration_20260512/)*
*Gate: support precomputed and externally derived UDG/AECC outputs through a validated classifier interface and local tool/service integration.*

---

- [x] **Track: Emergency Classification Parity Fixtures**
*Link: [./archive/emergency_classification_parity_fixtures_20260512/](./archive/emergency_classification_parity_fixtures_20260512/)*
*Gate: validate UDG/AECC parity fixtures only after the emergency transition registry, mapping pipeline, and grouper integration are in place, and keep synthetic and local-only licensed fixtures separate from redistributed content.*

---

- [x] **Track: Abstraction Doctrine Enforcement**
*Link: [./archive/abstraction_doctrine_enforcement_20260512/](./archive/abstraction_doctrine_enforcement_20260512/)*
*Gate: make formula, parameter, registry, classifier, binding, app, and documentation boundaries explicit and enforceable before implementing more surfaces.*

---

- [x] **Track: Polyglot Rust Core Roadmap**
*Link: [./archive/polyglot_rust_core_roadmap_20260512/](./archive/polyglot_rust_core_roadmap_20260512/)*
*Gate: coordinate the transition from Python-first package to shared Rust calculator core with thin Python, R, Julia, TypeScript/WASM, C ABI, CLI/file, web, and Power Platform consumers.*

---

- [x] **Track: Rust Core GA**
*Link: [./tracks/rust_core_ga_20260513/](./tracks/rust_core_ga_20260513/)*
*Gate: Immediate priority. Promote the Rust calculator core to release-candidate and GA through versioned contracts, parity evidence, required delivery surfaces, strict CI/CD, security, and release automation before expanding lower-priority adapters.*

---

- [x] **Track: Canonical Contract Foundation**
*Link: [./archive/canonical_contract_foundation_20260513/](./archive/canonical_contract_foundation_20260513/)*
*Gate: Immediate priority after Rust Core GA planning. Define canonical JSON Schema/OpenAPI-compatible domain contracts for calculator requests, responses, diagnostics, errors, provenance, support status, and evidence before adding more surfaces.*

---

- [x] **Track: Support Status Matrix**
*Link: [./archive/support_status_matrix_20260513/](./archive/support_status_matrix_20260513/)*
*Gate: Define machine-readable support statuses for stream, year, jurisdiction, surface, runtime, and language claims before public docs or release metadata can mark support as complete.*

---

- [x] **Track: CLI/File Contracts**
*Link: [./archive/cli_file_contracts_20260513/](./archive/cli_file_contracts_20260513/)*
*Gate: Define stable CLI commands, exit codes, stdin/stdout/stderr behavior, JSON manifests, Arrow/Parquet batch files, diagnostics, and provenance before promoting Rust execution surfaces.*

---

- [x] **Track: HTTP API Contract**
*Link: [./tracks/http_api_contract_20260513/](./tracks/http_api_contract_20260513/)*
*Gate: Define a domain OpenAPI 3.1 contract for calculators, schemas, validation, calculations, async jobs, results, and evidence without pretending the calculator is an LLM endpoint.*

---

- [x] **Track: MCP Contract**
*Link: [./tracks/mcp_contract_20260513/](./tracks/mcp_contract_20260513/)*
*Gate: Expose calculator tools and resources for agents through MCP over canonical schemas, preserving diagnostics and provenance without creating a separate formula contract.*

---

- [x] **Track: OpenAI Tool Adapter**
*Link: [./tracks/openai_tool_adapter_20260513/](./tracks/openai_tool_adapter_20260513/)*
*Gate: Provide OpenAI-compatible tool definitions over the API/MCP contracts while keeping the domain API canonical and avoiding LLM endpoint emulation.*

---

- [x] **Track: Audience Language Strategy**
*Link: [./archive/audience_language_strategy_20260513/](./archive/audience_language_strategy_20260513/)*
*Gate: Prioritize language support around researchers and enterprise engineers, require audience/owner/evidence before new bindings, and prevent language sprawl before Rust Core GA.*

---

- [x] **Track: HWAU Terminology Migration**
*Link: [./tracks/hwau_terminology_migration_20260513/](./tracks/hwau_terminology_migration_20260513/)*
*Gate: Use HWAU as the generic healthcare weighted activity unit abstraction while preserving NWAU as Australian source terminology and compatibility alias.*

---

- [x] **Track: State and Local Price Registry**
*Link: [./tracks/state_local_price_registry_20260513/](./tracks/state_local_price_registry_20260513/)*
*Gate: Source and version national, state, local, and discounted HWAU price schedules over time with provenance, licence status, and fail-closed support metadata.*

---

- [x] **Track: Jurisdiction Price Source Index**
*Link: [./tracks/jurisdiction_price_source_index_20260513/](./tracks/jurisdiction_price_source_index_20260513/)*
*Gate: Build a source index for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT before extracting or committing jurisdiction price values.*

---

- [x] **Track: NSW Funding Model**
*Link: [./tracks/nsw_funding_model_20260513/](./tracks/nsw_funding_model_20260513/)*
*Gate: Model NSW State Price per NWAU/HWAU, LHD/SHN service agreement notes, adjustments, blocked years, and provenance before applying NSW-specific valuations.*

---

- [x] **Track: Jurisdiction Funding Model Registry**
*Link: [./tracks/jurisdiction_funding_model_registry_20260513/](./tracks/jurisdiction_funding_model_registry_20260513/)*
*Gate: Cover NSW, VIC, QLD, WA, SA, TAS, ACT, and NT funding model sources with jurisdiction-specific terminology, provenance, support status, and blocked-source handling.*

---

- [x] **Track: Parallel Valuation Outputs**
*Link: [./tracks/parallel_valuation_outputs_20260513/](./tracks/parallel_valuation_outputs_20260513/)*
*Gate: Produce HWAU-only, national, state, local, and discounted valuation outputs in parallel from the same normalized activity result across CLI/file, API, MCP, and OpenAI adapter surfaces.*

---

- [x] **Track: Rust Crate Boundaries and HWAU Rename**
*Link: [./tracks/rust_crate_boundary_rename_20260513/](./tracks/rust_crate_boundary_rename_20260513/)*
*Gate: Plan crate boundaries and NWAU-to-HWAU migration with compatibility aliases before renaming active Rust implementation paths.*

---

- [x] **Track: GitHub Pages API Architecture**
*Link: [./tracks/github_pages_api_architecture_20260513/](./tracks/github_pages_api_architecture_20260513/)*
*Gate: Document that GitHub Pages hosts docs/static WASM demos only, while API-backed demos require an external or local backend.*

---

- [x] **Track: Release Evidence Bundle**
*Link: [./tracks/release_evidence_bundle_20260513/](./tracks/release_evidence_bundle_20260513/)*
*Gate: Define required release evidence bundles before any stream, jurisdiction, or surface can be promoted to release-candidate or GA.*

---

- [x] **Track: C#/.NET Binding**
*Link: [./archive/csharp_dotnet_binding_20260512/](./archive/csharp_dotnet_binding_20260512/)*
*Gate: expose institutional .NET integration through C ABI, service, or CLI/file contracts without duplicating formula logic.*

---

- [x] **Track: Go Binding**
*Link: [./archive/go_binding_20260512/](./archive/go_binding_20260512/)*
*Gate: support Go services and data pipelines through shared-core or file/service contracts without formula duplication.*

---

- [x] **Track: Kotlin/Native Binding**
*Link: [./archive/kotlin_native_binding_20260512/](./archive/kotlin_native_binding_20260512/)*
*Gate: support native Kotlin consumers through C ABI, service, or Arrow/Parquet interop with shared fixture validation and no JVM runtime requirement.*

---

- [x] **Track: Scala/Spark Binding**
*Link: [./archive/scala_spark_binding_20260513/](./archive/scala_spark_binding_20260513/)*
*Gate: Design complete; implementation is now held at the audience/owner evidence gate. Proceed only when a named enterprise audience, accountable owner, and post-GA Scala/Spark evidence case are recorded.*

---

- [x] **Track: Swift Binding**
*Link: [./archive/swift_binding_20260513/](./archive/swift_binding_20260513/)*
*Gate: Design complete; implementation is now held at the audience/owner evidence gate. Proceed only when a named Apple-platform healthcare audience, accountable owner, and post-GA Swift evidence case are recorded.*

---

- [x] **Track: Stata Interoperability**
*Link: [./archive/stata_interop_binding_20260513/](./archive/stata_interop_binding_20260513/)*
*Gate: Design complete; implementation is now held at the audience/owner evidence gate and stable CLI/file contract readiness. Proceed only when a named health-economics owner and post-GA Stata evidence case are recorded.*

---

- [x] **Track: MATLAB Interoperability**
*Link: [./archive/matlab_interop_binding_20260513/](./archive/matlab_interop_binding_20260513/)*
*Gate: Design complete; implementation is now held at the audience/owner evidence gate. Proceed only when a named healthcare economics audience, accountable owner, and post-GA MATLAB evidence case are recorded.*

---

- [x] **Track: SQL and DuckDB Integration**
*Link: [./tracks/duckdb_sql_binding_20260512/](./tracks/duckdb_sql_binding_20260512/)*
*Gate: Historical/deprioritized. Do not develop SQL/DuckDB as an active surface; retain only as prior roadmap context unless a future evidence-backed audience emerges.*

---

- [x] **Track: SAS Interoperability**
*Link: [./archive/sas_interop_binding_20260512/](./archive/sas_interop_binding_20260512/)*
*Gate: support SAS reference comparison and import/export workflows without creating a separate SAS formula implementation.*

---

- [x] **Track: Power Platform Binding**
*Link: [./tracks/power_platform_binding_20260512/](./tracks/power_platform_binding_20260512/)*
*Gate: publish Power Platform orchestration as a managed solution/custom connector consumer of the shared calculator contract, never as a formula implementation.*

---

- [x] **Track: Cost Bucket Registry**
*Link: [./archive/cost_bucket_registry_20260512/](./archive/cost_bucket_registry_20260512/)*
*Gate: represent public IHACPA/NHCDC cost bucket definitions, mappings, caveats, and local overlay references without bundling confidential submissions.*

---

- [x] **Track: NHCDC Cost Report Ingestion**
*Link: [./tracks/nhcdc_cost_report_ingestion_20260512/](./tracks/nhcdc_cost_report_ingestion_20260512/)*
*Gate: ingest public NHCDC cost report appendices and data request specifications with provenance while distinguishing aggregate reports from patient-level costing data.*

---

- [x] **Track: AHPCS Costing Process Model**
*Link: [./archive/ahpcs_costing_process_model_20260512/](./archive/ahpcs_costing_process_model_20260512/)*
*Gate: model AHPCS costing-process concepts as validation aids for costing studies without claiming official compliance certification.*

---

- [x] **Track: Cost Bucket Analytics Tutorials**
*Link: [./archive/cost_bucket_analytics_tutorials_20260512/](./archive/cost_bucket_analytics_tutorials_20260512/)*
*Gate: publish synthetic and public-safe cost bucket tutorials for benchmarking, cost-versus-NWAU studies, and local mapping overlays.*

---

- [x] **Track: Roadmap Portfolio Governance Backfill**
*Link: [./tracks/roadmap_portfolio_governance_backfill_20260512/](./tracks/roadmap_portfolio_governance_backfill_20260512/)*
*Gate: backfill class, dependency, explicit contract, current-state, and completion-evidence metadata across the expanded Conductor roadmap before further broad implementation claims.*

---

- [x] **Track: Expert Panel Remediation**
*Link: [./tracks/expert_panel_remediation_20260512/](./tracks/expert_panel_remediation_20260512/)*
*Gate: convert simulated expert-panel findings into explicit track dependencies, gate notes, and remediation priorities before implementing lower-priority bindings or publication expansion.*

---

- [x] **Track: End-to-End Validated Canary**
*Link: [./tracks/end_to_end_validated_canary_20260512/](./tracks/end_to_end_validated_canary_20260512/)*
*Gate: prove one stream/year lifecycle from source archive through SAS/Excel parity, formula bundles, Rust canary, Python/CLI conformance, and Starlight documentation before scaling implementation claims.*

---

- [x] **Track: Public Appropriate-Use Documentation**
*Link: [./archive/public_appropriate_use_docs_20260512/](./archive/public_appropriate_use_docs_20260512/)*
*Gate: publish conservative docs for validation status, appropriate use, policy caveats, source licensing, and non-endorsement before broad promotion.*

---

- [x] **Track: Release Evidence Automation**
*Link: [./tracks/release_evidence_automation_20260512/](./tracks/release_evidence_automation_20260512/)*
*Gate: make release, package, tag, docs, workflow, and registry publication claims machine-checkable before expanding publication targets.*

---

- [x] **Track: Contract Schema Export**
*Link: [./archive/contract_schema_export_20260512/](./archive/contract_schema_export_20260512/)*
*Gate: export versioned schemas for calculator contracts, manifests, evidence, diagnostics, and provenance before implementing broad bindings.*

---

- [x] **Track: Rust Core GA Post-Cline Review**
*Link: [./tracks/rust_core_ga_post_cline_review_20260513/](./tracks/rust_core_ga_post_cline_review_20260513/)*
*Gate: Review Cline's Rust Core GA implementation after the active session finishes, verify evidence, and downgrade overclaims before merge.*

---

- [x] **Track: FFI Safety Review**
*Link: [./archive/ffi_safety_review_20260513/](./archive/ffi_safety_review_20260513/)*
*Gate: Harden FFI/C ABI pointer, UTF-8, length, ownership, and error-status behavior before merging ABI changes.*

---

- [x] **Track: Release Workflow Validation**
*Link: [./tracks/release_workflow_validation_20260513/](./tracks/release_workflow_validation_20260513/)*
*Gate: Validate Rust CI, coverage, security, and release workflows, including tag outputs, SBOM fallback, and evidence-bundle integration.*

---

- [x] **Track: Support Status Reconciliation**
*Link: [./archive/support_status_reconciliation_20260513/](./archive/support_status_reconciliation_20260513/)*
*Gate: Reconcile generated canonical support statuses with the governance support matrix before public support claims.*

---

- [x] **Track: Deferred Surface Cleanup**
*Link: [./tracks/deferred_surface_cleanup_20260513/](./tracks/deferred_surface_cleanup_20260513/)*
*Gate: Decide whether generated deferred-surface artefacts are retained, quarantined, or removed after Cline finishes.*

---

- [x] **Track: Conductor Requirements and Design Authority**
*Link: [./archive/conductor_requirements_design_authority_20260513/](./archive/conductor_requirements_design_authority_20260513/)*
*Gate: Maintain MoSCoW requirements, system design diagrams, and cross-references as the authority for all tracks, contracts, CI/CD, docs, and agent orchestration.*

---

- [x] **Track: Contract Enforcement Harness**
*Link: [./archive/contract_enforcement_harness_20260513/](./archive/contract_enforcement_harness_20260513/)*
*Gate: Turn canonical, CLI/file, API, MCP, OpenAI adapter, binding, and release contracts into generated or validated artifacts with drift checks and fail-closed tests.*

---

- [x] **Track: Strict Quality Gates**
*Link: [./tracks/strict_quality_gates_20260513/](./tracks/strict_quality_gates_20260513/)*
*Gate: Enforce SOTA formatting, linting, typing, docstring/docs, security, supply-chain, and >90% coverage gates before completion, release, or publication claims.*

---

- [x] **Track: Multi-Level Agent Execution**
*Link: [./tracks/multilevel_agent_execution_20260513/](./tracks/multilevel_agent_execution_20260513/)*
*Gate: Make tracks granular enough for multi-agent and nested-subagent execution with disjoint ownership, handoffs, conductor-review loops, commits, and push gates.*

---

- [x] **Track: GitHub Repository SOTA Setup**
*Link: [./tracks/github_repo_sota_setup_20260513/](./tracks/github_repo_sota_setup_20260513/)*
*Gate: Complete GitHub labels, milestones, branch protections, security settings, homepage, releases, tags, packages, Pages, and publication evidence.*

---

- [x] **Track: Starlight Documentation SOTA Completion**
*Link: [./tracks/docs_sota_starlight_completion_20260513/](./tracks/docs_sota_starlight_completion_20260513/)*
*Gate: Make the Starlight/Astro documentation comprehensive, versioned, tutorial-rich, support-status aware, and contract-linked.*

---

- [x] **Track: Recursive SOTA Contract Audit**
*Link: [./tracks/recursive_sota_contract_audit_20260513/](./tracks/recursive_sota_contract_audit_20260513/)*
*Gate: Periodically compare this repository to SOTA scientific/software projects, improve the project contract, and create implementation tracks for gaps.*

---

- [x] **Track: No-Stub Completion Enforcement**
*Link: [./tracks/no_stub_completion_enforcement_20260513/](./tracks/no_stub_completion_enforcement_20260513/)*
*Gate: Prevent roadmap, scaffold, fake, TODO, placeholder, or mocked-only work from being marked complete without real implementation and validation evidence.*

---

- [x] **Track: Track Archive Integrity**
*Link: [./tracks/track_archive_integrity_20260513/](./tracks/track_archive_integrity_20260513/)*
*Gate: Audit `[x]` tracks, archive only truly completed work, downgrade overclaimed tracks, and keep archive evidence truthful.*

---

- [x] **Track: MCP Server Readiness and Registry Submission**
*Link: [./tracks/mcp_server_registry_submission_20260516/](./tracks/mcp_server_registry_submission_20260516/)*
*Gate: Provide a runnable stdio-first MCP server, contract-backed validation, official MCP Registry metadata, and truthful secondary registry submission evidence without requiring Docker.*

---

- [x] **Track: Smithery MCP Registry Readiness**
*Link: [./tracks/smithery_mcp_registry_readiness_20260517/](./tracks/smithery_mcp_registry_readiness_20260517/)*
*Gate: do not claim Smithery publication until a public Streamable HTTP endpoint, static server card or scan evidence, and Smithery submission/listing evidence exist.*

---

- [x] **Track: Docker MCP Registry Readiness**
*Link: [./tracks/docker_mcp_registry_readiness_20260517/](./tracks/docker_mcp_registry_readiness_20260517/)*
*Gate: do not claim Docker MCP Catalog publication until a Dockerfile-backed container path, Docker Registry metadata, validation evidence, and Docker Registry PR or merge evidence exist.*

---

- [x] **Track: Python PyPI Registry Submission**
*Link: [./tracks/python_pypi_registry_submission_20260524/](./tracks/python_pypi_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `PyPI`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: Rust crates.io Registry Submission**
*Link: [./tracks/rust_crates_io_registry_submission_20260524/](./tracks/rust_crates_io_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `crates.io`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: TypeScript/WASM npm Registry Submission**
*Link: [./tracks/typescript_npm_registry_submission_20260524/](./tracks/typescript_npm_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `npm`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: .NET NuGet Registry Submission**
*Link: [./tracks/dotnet_nuget_registry_submission_20260524/](./tracks/dotnet_nuget_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `NuGet`, and capture immutable evidence before claiming publication.*

---

- [~] **Track: R CRAN Registry Submission**
*Link: [./tracks/r_cran_registry_submission_20260524/](./tracks/r_cran_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `CRAN`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: Julia General Registry Submission**
*Link: [./tracks/julia_general_registry_submission_20260524/](./tracks/julia_general_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `General registry`, and capture immutable evidence before claiming publication. Publication is verified by the merged General PR.*

---

- [x] **Track: Go Module Registry Submission**
*Link: [./tracks/go_module_registry_submission_20260524/](./tracks/go_module_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `Go module proxy/pkg.go.dev`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: Swift Package Index Submission**
*Link: [./tracks/swift_package_index_submission_20260524/](./tracks/swift_package_index_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `Swift Package Index`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: JVM Maven Central Registry Submission**
*Link: [./tracks/jvm_maven_central_registry_submission_20260524/](./tracks/jvm_maven_central_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `Maven Central`, and capture immutable evidence before claiming publication.*

---

- [~] **Track: conda-forge Feedstock Submission**
*Link: [./tracks/conda_forge_feedstock_submission_20260524/](./tracks/conda_forge_feedstock_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `conda-forge`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: Homebrew Formula Submission**
*Link: [./tracks/homebrew_formula_submission_20260524/](./tracks/homebrew_formula_submission_20260524/)*
*Gate: Personal tap publication is verified; Homebrew/core remains an optional upstream review gate.*

---

- [x] **Track: VS Code/Open VSX Extension Submission**
*Link: [./tracks/vscode_openvsx_registry_submission_20260524/](./tracks/vscode_openvsx_registry_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `Open VSX / Visual Studio Marketplace`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: MATLAB File Exchange Submission**
*Link: [./tracks/matlab_file_exchange_submission_20260524/](./tracks/matlab_file_exchange_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `MATLAB File Exchange`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: Stata SSC Submission**
*Link: [./tracks/stata_ssc_submission_20260524/](./tracks/stata_ssc_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `SSC / Stata package distribution`, and capture immutable evidence before claiming publication.*

---

- [~] **Track: C/C++ vcpkg and Conan Submission**
*Link: [./tracks/c_cpp_vcpkg_conan_submission_20260524/](./tracks/c_cpp_vcpkg_conan_submission_20260524/)*
*Gate: Discover existing publication, prepare package artifacts if absent, submit through `vcpkg / ConanCenter`, and capture immutable evidence before claiming publication.*

---

- [x] **Track: Scaffold and Stub Completion Backlog**
*Link: [./tracks/scaffold_stub_completion_backlog_20260524/](./tracks/scaffold_stub_completion_backlog_20260524/)*
*Gate: Bring scaffold-only, stub-only, complete-with-gaps, and overclaimed surfaces to validated completion or reclassify them truthfully with follow-on implementation tracks.*

---

- [x] **Track: Rust Core Continuation**
*Link: [./tracks/rust_core_continuation_20260524/](./tracks/rust_core_continuation_20260524/)*
*Gate: Continue stream-by-stream promotion from Python-first calculators to a validated Rust core with parity, binding, CLI/file, support-status, and release evidence before GA claims.*

---

- [ ] **Track: Repository Topology Authority**
*Link: [./tracks/repository_topology_authority_20260624/](./tracks/repository_topology_authority_20260624/)*
*Gate: Declare the canonical repo root, ban unmanaged nested repos and gitlinks, and define source, evidence, package, generated, and external-gate ownership.*

---

- [ ] **Track: Outer Wrapper Retirement Migration**
*Link: [./tracks/outer_wrapper_retirement_migration_20260624/](./tracks/outer_wrapper_retirement_migration_20260624/)*
*Gate: Inventory the transitional outer wrapper, preserve source and Power Platform evidence, and retire or formalize the broken gitlink wrapper without data loss.*

---

- [ ] **Track: Package Surface Ownership Registry**
*Link: [./tracks/package_surface_ownership_registry_20260624/](./tracks/package_surface_ownership_registry_20260624/)*
*Gate: Register every package, binding, app, docs, and registry surface with owner, manifest, CI gate, support state, release target, and evidence boundary.*

---

- [ ] **Track: Repository Topology CI Gate**
*Link: [./tracks/repository_topology_ci_gate_20260624/](./tracks/repository_topology_ci_gate_20260624/)*
*Gate: Fail closed on nested Git state, unmanaged gitlinks, missing package-surface ownership, tracked generated artifacts, and invalid wrapper assumptions.*

---

- [ ] **Track: Release Boundary Control Plane**
*Link: [./tracks/release_boundary_control_plane_20260624/](./tracks/release_boundary_control_plane_20260624/)*
*Gate: Map package surfaces to release workflows, version sources, registry evidence, support status, and external blocker classes before public claims change.*

---

- [ ] **Track: Generated Artifact Retention Policy**
*Link: [./tracks/generated_artifact_retention_policy_20260624/](./tracks/generated_artifact_retention_policy_20260624/)*
*Gate: Define which generated artifacts are ignored, release-attached, archived, or evidence-owned, and block accidental generated-output drift.*

---

- [ ] **Track: Worktree, Branch, and PR Hygiene**
*Link: [./tracks/worktree_branch_pr_hygiene_20260624/](./tracks/worktree_branch_pr_hygiene_20260624/)*
*Gate: Standardize clean temporary worktrees, minimal PR slices, branch naming, safe pushes, CI proof, and subagent handoff requirements.*

---

- [ ] **Track: Future Repo Split Playbook**
*Link: [./tracks/future_repo_split_playbook_20260624/](./tracks/future_repo_split_playbook_20260624/)*
*Gate: Define when a surface may leave the monorepo and how to extract it with history, registry continuity, CI proof, and rollback.*
