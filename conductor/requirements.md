# Requirements Specification

Agent coordination note: this file is the requirements authority for Codex, Cline, Kanban, and delegated subagents working in this repository. Do not replace it with implementation stubs or optimistic status claims; update it when requirements change and cross-reference affected tracks.

## Purpose

This file defines the MoSCoW requirements for the `mchs`/`microcosting-healthservices` library and its Conductor delivery system. Requirements here are binding for tracks, contracts, CI/CD, documentation, release readiness, and delegated-agent work.

## MoSCoW Requirements

### Must Have

| ID | Requirement | Acceptance evidence | Owning tracks |
| --- | --- | --- | --- |
| MUST-001 | Rust must become the single source of calculator logic for GA while preserving Python as a stable public consumer during migration. | Rust core contracts, parity tests, Python binding tests, release evidence bundle. | `rust_core_ga_20260513`, `rust_core_ga_post_cline_review_20260513` |
| MUST-002 | Public contracts must be explicit, versioned, documented, and machine-validated before surfaces claim support. | JSON Schema/OpenAPI/MCP/CLI-file schemas, schema tests, compatibility tests, docs references. | `canonical_contract_foundation_20260513`, `contract_enforcement_harness_20260513` |
| MUST-003 | Calculator, manifest, pricing-year, classification, valuation, and evidence schemas must fail closed on unknown, unsupported, or unvalidated data. | Negative tests, validation diagnostics, support-status matrix, docs caveats. | `support_status_matrix_20260513`, `pricing_year_validation_gates_20260512` |
| MUST-004 | CI/CD must enforce strict formatting, linting, typing, documentation, security, coverage, provenance, and release gates. | Required GitHub Actions, branch protection documentation, coverage >=90%, security workflows, SBOM/attestations. | `strict_quality_gates_20260513`, `release_workflow_validation_20260513` |
| MUST-005 | Test coverage must be at least 90% for supported Python and Rust core paths, with stronger parity requirements for calculator logic. | Coverage reports, Codecov status, cargo llvm-cov or equivalent, pytest coverage, parity fixtures. | `strict_quality_gates_20260513`, `release_evidence_bundle_20260513` |
| MUST-006 | Pricing-year validation must compare against SAS and Excel formulae where official sources exist, or record explicit gap evidence where they do not. | Source manifest entries, parity reports, gap records, validation ladder status. | `end_to_end_validated_canary_20260512`, `release_evidence_bundle_20260513` |
| MUST-007 | Documentation must be built with Starlight/Astro and distinguish current support, planned support, blocked support, and no-new-development surfaces. | Starlight pages, support matrix, tutorials, versioned contracts, Pages workflow. | `docs_sota_starlight_completion_20260513` |
| MUST-008 | GitHub repository setup must be production-grade: labels, milestones, branch protections, environments, security settings, releases, tags, package metadata, homepage, and publishing evidence. | GitHub audit report, repo settings checklist, release/tag evidence, package registry evidence. | `github_repo_sota_setup_20260513` |
| MUST-009 | Delegated agents must receive granular, bounded, multi-level tasks with explicit contracts, owned files, review requirements, validation evidence, and handoff requirements. | Track plans with subagent work packages, handoff logs, review records. | `multilevel_agent_execution_20260513` |
| MUST-010 | No task or track may be marked complete because stubs, scaffolds, TODOs, or docs-only placeholders exist. | No-stub audit, completeness gates, implementation evidence, tests exercising real behavior. | `no_stub_completion_enforcement_20260513` |
| MUST-011 | Every phase must automatically run `conductor-review`, apply high-confidence fixes, rerun narrow validation, checkpoint, and continue unless blocked. | Plan checkpoint records, git notes, review reports, validation commands. | `multilevel_agent_execution_20260513`, `conductor_requirements_design_authority_20260513` |
| MUST-012 | Every track completion must publish or record release/push evidence when it affects public repository state, packages, documentation, or contracts. | Commit SHA, remote push evidence, CI status, release evidence bundle. | `release_evidence_bundle_20260513`, `github_repo_sota_setup_20260513` |
| MUST-013 | Public clinical dataset examples must be access- and license-assessed before implementation, keep raw patient-level files and disclosure-risk outputs local-only, and fail closed when Australian classification provenance is missing. | Dataset assessment, source/license manifest, local-cache policy, safe-output policy, raw-data commit guards, fail-closed tests, provenance report. | `public_clinical_dataset_worked_example_20260704` |

### Should Have

| ID | Requirement | Acceptance evidence | Owning tracks |
| --- | --- | --- | --- |
| SHOULD-001 | Contracts should be generated from shared typed models where practical rather than manually duplicated. | Schema generation command, generated artifacts, drift tests. | `contract_enforcement_harness_20260513` |
| SHOULD-002 | CLI, file, API, MCP, OpenAI tool adapter, Python, R, Julia, C#, TypeScript/WASM, and Stata surfaces should reuse Rust core contracts and parity fixtures. | Cross-surface conformance tests and docs. | `cli_file_contracts_20260513`, `http_api_contract_20260513`, `mcp_contract_20260513`, `openai_tool_adapter_20260513` |
| SHOULD-003 | Recursive SOTA audits should periodically compare this repository against high-quality scientific/data-engineering OSS projects and create remediation tracks. | Audit report, updated requirements/design/workflow, remediation tracks. | `recursive_sota_contract_audit_20260513` |
| SHOULD-004 | Release evidence should include SBOMs, checksums, provenance attestations, signed tags where available, dependency review, and security scan outcomes. | Release artifacts and workflow logs. | `release_workflow_validation_20260513` |
| SHOULD-005 | Tutorials should cover costing studies, HWAU valuation, jurisdiction/local pricing overlays, synthetic examples, and policy caveats. | Versioned docs pages and runnable notebooks/examples. | `costing_study_tutorials_20260512`, `parallel_valuation_outputs_20260513` |
| SHOULD-006 | Worked examples should demonstrate advanced existing features when useful: provenance reports, data-quality summaries, disclosure-risk summaries, support-status outputs, Python API execution, CLI/file interop, MCP boundary validation, API/OpenAI contract documentation, scenario/sensitivity comparisons, and classification provenance diagnostics. | MIMIC-IV Demo tutorial outputs, machine-readable reports, docs screenshots or command transcripts, validation tests, surface conformance evidence, scenario report. | `public_clinical_dataset_worked_example_20260704` |

### Could Have

| ID | Requirement | Acceptance evidence | Owning tracks |
| --- | --- | --- | --- |
| COULD-001 | Additional deferred bindings may remain visible as roadmap context without active development. | Deferred status records and no-new-development docs. | `deferred_surface_cleanup_20260513` |
| COULD-002 | Optional web demos may use TypeScript/WASM for synthetic-data-only interactive documentation. | WASM demo contract and privacy boundary docs. | `typescript_wasm_binding_20260512`, `github_pages_api_architecture_20260513` |
| COULD-003 | External service deployment recipes may be added after local contracts and release evidence are stable. | Deployment docs and threat model. | Future track only |
| COULD-004 | Additional public dataset examples or reusable example harnesses may be added as separate tracks after suitability evidence shows a distinct access, classification, data model, surface-conformance, disclosure-risk, scenario-reporting, or workflow value. | Follow-up GitHub issues, dataset suitability records, separate Conductor tracks for ED, FHIR/MEDS, downloader/cache, surface conformance, disclosure-risk, scenario-reporting, or registry work. | `public_clinical_dataset_worked_example_20260704` |

### Won't Have for Current GA

| ID | Requirement | Reason | Owning tracks |
| --- | --- | --- | --- |
| WONT-001 | No JVM-based Kotlin or Java dependency for core delivery. | User preference and lower value for current audiences. | `audience_language_strategy_20260513` |
| WONT-002 | No SQL/DuckDB active surface for current GA. | User explicitly deprioritised it. | `deferred_surface_cleanup_20260513` |
| WONT-003 | No Scala/Spark, Swift, MATLAB, or Go active implementation before Rust Core GA unless a new evidence-backed owner appears. | Avoid language sprawl and scaffold-only work. | `deferred_surface_cleanup_20260513` |
| WONT-004 | No reimplementation or redistribution of proprietary licensed groupers/classification tables. | Licensing and correctness boundaries. | `icd_achi_acs_license_workflow_20260512`, `ar_drg_grouper_integration_20260512` |
| WONT-005 | No raw public patient-level dataset files or disclosure-risk derived outputs in git, and no treatment of MIMIC US DRG, ICD-9-CM, ICD-10-CM, or ICD-10-PCS fields as validated Australian AR-DRG, ICD-10-AM, ACHI, or ACS equivalents. | Raw-data guard tests, safe-output checks, docs caveats, fail-closed classification diagnostics. | `public_clinical_dataset_worked_example_20260704` |

## Completion Semantics

A requirement is not satisfied until the repository contains implementation, tests or validation evidence, documentation, and release or publication evidence when applicable. Stubs, TODOs, empty adapters, mocked-only paths, or roadmap statements are evidence of intent only.
