# Expert Panel Remediation

## Purpose

Convert the simulated expert-panel findings into actionable Conductor
priorities. Maps each high-priority recommendation to an existing track,
documents missing dependency and gate notes, and records any remaining gaps
that need new tracks.

## Source Documents

- `docs/reviews/20260512-expert-panel/synthesis.md`
- `docs/reviews/20260512-expert-panel/deliberation-and-prioritisation.md`

## Priority-to-Track Mapping

### Priority 0: Governance and claim control

| Recommendation | Owner Track | Status |
|---|---|---|
| Backfill roadmap governance metadata | `roadmap_portfolio_governance_backfill_20260512` | In progress |
| Apply governance checklist to every active track | `roadmap_portfolio_governance_backfill_20260512` | In progress |
| Fix stale workflow paths, repo names, claims | `roadmap_portfolio_governance_backfill_20260512` | In progress |

### Priority 1: Executable contracts and schemas

| Recommendation | Owner Track | Status |
|---|---|---|
| Reference Data Manifest Schema | `reference_data_manifest_schema_20260512` | Complete |
| Formula and Parameter Bundle Pipeline | `formula_parameter_bundle_pipeline_20260512` | Complete |
| Coding-Set Version Registry | `coding_set_version_registry_20260512` | Complete |
| Export JSON Schema / contract artifacts | `contract_schema_export_20260512` | In progress |

### Priority 2: Validation gates and parity evidence

| Recommendation | Owner Track | Status |
|---|---|---|
| Pricing-Year Validation Gates | `pricing_year_validation_gates_20260512` | Complete |
| SAS/Excel parity as required evidence | `pricing_year_validation_gates_20260512` | Complete |
| Fixture evidence records and gap exceptions | `pricing_year_validation_gates_20260512` | Complete |
| Funding-calculator validate-year | `pricing_year_validation_gates_20260512` | Complete |

### Priority 3: Source discovery and restricted asset controls

| Recommendation | Owner Track | Status |
|---|---|---|
| IHACPA Source Scanner | `ihacpa_source_scanner_20260512` | Complete |
| ICD-10-AM/ACHI/ACS Licensed Product Workflow | `icd_achi_acs_license_workflow_20260512` | Complete |
| Restricted artifact denylist/conventions | `icd_achi_acs_license_workflow_20260512` | Complete |
| Source hashes, retrieval dates, gap records | `ihacpa_source_scanner_20260512` | Complete |

### Priority 4: One complete stream/year canary

| Recommendation | Owner Track | Status |
|---|---|---|
| Select one stream/year | `end_to_end_validated_canary_20260512` | In progress |
| Archive/extract SAS/Excel sources | `end_to_end_validated_canary_20260512` | In progress |
| Formula bundle and manifest | `end_to_end_validated_canary_20260512` | In progress |
| Validate source/output parity | `end_to_end_validated_canary_20260512` | In progress |
| Python baseline + Rust canary | `end_to_end_validated_canary_20260512` | In progress |
| CLI/Arrow output | `end_to_end_validated_canary_20260512` | In progress |
| Starlight docs page | `end_to_end_validated_canary_20260512` | In progress |

### Priority 5: Rust core promotion

| Recommendation | Owner Track | Status |
|---|---|---|
| Polyglot Rust Core Roadmap | `polyglot_rust_core_roadmap_20260512` | Complete |
| Python Rust Binding Stabilization | `python_rust_binding_stabilization_20260512` | Complete |
| Shared cross-binding conformance tests | `python_rust_binding_stabilization_20260512` | Complete |

### Priority 6: Classification and grouper capabilities

| Recommendation | Owner Track | Status |
|---|---|---|
| AR-DRG registry and grouper interfaces | `ar_drg_icd_mapping_registry_20260512`, `ar_drg_grouper_integration_20260512` | Complete |
| Emergency UDG/AECC registry and mapping | `emergency_udg_aecc_transition_registry_20260512`, `emergency_code_mapping_pipeline_20260512` | Complete |
| Parity fixtures and licensed local-tool workflows | `ar_drg_version_parity_fixtures_20260512`, `emergency_classification_parity_fixtures_20260512` | Complete |

### Priority 7: Public documentation

| Recommendation | Owner Track | Status |
|---|---|---|
| Validation-status and appropriate-use docs | `public_appropriate_use_docs_20260512` | In progress |
| Pricing-year/classification compatibility matrices | `public_appropriate_use_docs_20260512` | In progress |
| Source and licensing caveats | `public_appropriate_use_docs_20260512` | In progress |
| Release evidence pages | `release_evidence_automation_20260512` | In progress |

### Priority 8: Costing-study support

| Recommendation | Owner Track | Status |
|---|---|---|
| Cost bucket registry | `cost_bucket_registry_20260512` | Roadmap only |
| Public NHCDC aggregate ingestion | `nhcdc_cost_report_ingestion_20260512` | Roadmap only |
| AHPCS concept models | `ahpcs_costing_process_model_20260512` | Roadmap only |
| Synthetic costing-study tutorials | `cost_bucket_analytics_tutorials_20260512`, `costing_study_tutorials_20260512` | Tutorials complete; analytics roadmap only |

### Priority 9: Polyglot bindings and apps

| Recommendation | Owner Track | Status |
|---|---|---|
| CLI/file interop | `cli_file_interop_binding_20260512` | Complete |
| C ABI | `c_abi_binding_20260512` | Complete |
| R and Julia | `r_binding_20260512`, `julia_binding_20260512` | Complete |
| C#/.NET and Go | `csharp_dotnet_binding_20260512`, `go_binding_20260512` | Complete |
| TypeScript/WASM and web demos | `typescript_wasm_binding_20260512` | Complete |
| Java/JVM and SQL/DuckDB | `java_jvm_binding_20260512`, `duckdb_sql_binding_20260512` | In progress / roadmap only |
| SAS interoperability | `sas_interop_binding_20260512` | Roadmap only |
| Power Platform managed solution | `power_platform_binding_20260512` | Roadmap only |

### Priority 10: Publication expansion

| Recommendation | Owner Track | Status |
|---|---|---|
| PyPI (primary) | `docs_release_publication_readiness_20260510` | Complete |
| conda-forge staged-recipes | (no track) | Gap: needs new track |
| Rust crates | (no track) | Gap: future-only when core stable |
| npm/WASM, NuGet, Go, JVM, R, Julia artifacts | (no track per registry) | Gap: needs publication expansion track |
| Power Platform managed solution | `power_platform_binding_20260512` | Roadmap only |

## Missing Dependency and Gate Notes

### Shared-contract dependencies required for binding tracks

| Binding Track | Missing Dependency | Action |
|---|---|---|
| Java/JVM Binding | Explicit dependency on `contract_schema_export_20260512` | Added in metadata.json |
| SQL/DuckDB Integration | Explicit dependency on `contract_schema_export_20260512` | Add when track is started |
| SAS Interoperability | Explicit dependency on `contract_schema_export_20260512` | Add when track is started |
| Power Platform Binding | Explicit dependency on `csharp_power_platform_engine_20260504` and `contract_schema_export_20260512` | Add when track is started |

### SAS/Excel parity dependencies for validation tracks

| Validation Track | Missing Dependency | Action |
|---|---|---|
| Pricing-Year Validation Gates | SAS/Excel parity gates | Already present |
| Classification Input Validation | SAS parity requirement for admitted classifications | Add explicit note |

### Restricted asset dependencies for classifier tracks

| Classifier Track | Missing Dependency | Action |
|---|---|---|
| AR-DRG Grouper Integration | Restricted licensed product workflow | Already depends on licensed handling |
| Emergency Grouper Integration | Restricted licensed product workflow | Already depends on licensed handling |

## Chair's Credibility-First Remediation Checklist

Ordered per the chair's final decision:

1. [x] **Governance:** Roadmap portfolio governance backfill.
2. [x] **Contracts:** Reference data manifests, formula bundles, coding registries, schema exports.
3. [x] **Validation:** Pricing-year gates, SAS/Excel parity, fixture evidence.
4. [x] **Source/licensing:** IHACPA scanner, licensed product workflow, gap records.
5. [ ] **One full canary:** Acute 2025 end-to-end lifecycle (`end_to_end_validated_canary_20260512`).
6. [ ] **Rust core promotion:** Polyglot roadmap, binding stabilization, conformance tests.
7. [x] **Classifier/grouper support:** AR-DRG, emergency registries, mappings, groupers, parity fixtures.
8. [ ] **Documentation:** Appropriate-use docs, validation status, licensing caveats (`public_appropriate_use_docs_20260512`).
9. [ ] **Costing tutorials:** Cost bucket registry, NHCDC ingestion, AHPCS model, analytics tutorials.
10. [ ] **Bindings and apps:** Remaining language bindings per priority ordering.
11. [ ] **Publication expansion:** conda-forge, crates, npm, NuGet, Go, JVM, R, Julia, Power Platform.

## Remaining Gaps Requiring New Tracks

| Gap | Priority | Suggested Track |
|---|---|---|
| conda-forge staged-recipes submission | Publication | `conda_forge_submission_<date>` |
| Rust crate publication workflow | Publication | `rust_crate_publication_<date>` |
| Multi-registry publication coordination | Publication | `publication_expansion_coordination_<date>` |
| Broad cross-binding conformance test suite | Binding | `cross_binding_conformance_<date>` |

