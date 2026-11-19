# Execution plan: shared microcosting and valuation

Only documented design work is completed here. All runtime acceptance leaves
remain pending. Provider-owned work is linked rather than duplicated.

## P0 — evidence and ownership

- [x] P0.1 Inspect workforce, genomics, MCHS and maintained CareOps source boundaries.
- [x] P0.2 Record Rust/Python/R/Julia, source-data and ontology responsibilities.
- [x] P0.3 Record standard/optional-premium Power Platform routes and source-qualified
  Petri-net/BPMN candidate dependencies.
- [x] P0.4 Specify newborn-screening object/batch/denominator semantics and frontier
  experiments without claiming runtime or clinical qualification.
- [ ] P0.5 Freeze executable capability inventory and independently calculated
  workforce/genomics/MCHS fixtures; isolate demonstration PSA/VOI outputs.
- [ ] P0.6 Review the fixture evidence and settle the supported first release scope.

## P1 — contract and standalone core

- [ ] P1.1 Specify resource-use versus weighted-activity types and schema versions.
- [ ] P1.2 Specify valuation basis, perspective, unit quotation, source/effective/
  knowledge dates and correction/retraction contracts.
- [ ] P1.3 Specify decimal/rational transport, overflow, rounding and allocation
  residual rules; include nonterminating-hour and sub-cent cases.
- [ ] P1.4 Map MCHS and reimbursement-atlas records without changing their meanings.
- [ ] P1.5 Implement minimal Rust types, quote application and component/pool ledger.
- [ ] P1.6 Verify independent arithmetic, unit/date failures and allocation conservation.

## P2 — two consumers and Python delivery

- [ ] P2.1 Workforce owner extracts common primitives while preserving condition rules.
- [ ] P2.2 Repair workforce import namespace; qualify runtime support rather than
  loosening version metadata without testing language/dependency compatibility.
- [ ] P2.3 Genomics owner maps one workflow into resource recipes and preserves
  historical workbook/source comparisons with complete calculation-status reporting.
- [ ] P2.4 Use one dated workforce release in that genomic workflow; prove no loaded
  labour/component duplication and no batch-cost duplication.
- [ ] P2.5 Package PyO3/maturin wheels and thin Polars/Arrow convenience APIs.
- [ ] P2.6 Test native and independently installed Python consumers against the same
  reference cases; establish the independently versioned core/repository boundary.

## P3 — MCHS, sources and operational surface

- [ ] P3.1 MCHS owner implements explicit activity/tariff adapter and parallel views;
  qualify official sources separately from synthetic state/local fixtures.
- [ ] P3.2 Integrate reimbursement-atlas through a versioned source-pack adapter.
- [ ] P3.3 CareOps owner reproduces its bounded existing contract using the common core.
- [ ] P3.4 Deliver CLI/file exchange plus standard SharePoint request/result schema.
- [ ] P3.5 Qualify manual operation, then optional worker idempotency, claiming,
  incomplete-output handling and scoped authorised access.
- [ ] P3.6 Verify actual standard-app/environment entitlement and target behaviour
  before deployment; premium/API and local WASM remain separate optional leaves.

## P4 — newborn screening and reporting

- [ ] P4.1 Implement versioned pathway/resource recipes with infant, specimen,
  batch, assay, result, repeat and confirmation identities.
- [ ] P4.2 Add synthetic shared-batch, repeat, capacity-step and denominator cases.
- [ ] P4.3 Qualify a real programme pack with source-specific workflow and rates.
- [ ] P4.4 Consume UOGTO costing/reporting profiles and standards_check source IDs;
  emit evidence-linked coverage including explicit unresolved/not-applicable status.
- [ ] P4.5 Verify independent costing and diagnostic-reporting cases; separate
  reporting completeness from correct methods and empirical validity.

## P5 — R, Julia and optional browser/API

The R branch can proceed after the shared Rust contract and core are qualified;
it does not depend on P5.1. The C ABI is a dependency of the Julia branch. Existing
MCHS wrapper-track choices do not impose a C ABI requirement on Dapane's R wrapper.

- [ ] P5.1 Define/implement versioned C ABI, ownership, free/error/panic contracts.
- [ ] P5.2 Qualify a thin extendr wrapper calling the Rust core directly, with
  rextendr packaging, host lifetime/thread checks and exact numeric transport;
  use a C ABI only if the R owner independently selects that route.
- [ ] P5.3 Qualify Julia direct C calls and native artifact/JLL packaging.
- [ ] P5.4 Run independently installed platform consumers and exact roundtrip cases.
- [ ] P5.5 Qualify optional authenticated HTTP/custom-connector surface, including
  actual service, connector/flow/environment entitlements and operating costs.
- [ ] P5.6 Experiment with client-only bundled WASM/PCF under supported host/CSP;
  promote only after native/browser parity and environment acceptance.

## P6 — uncertainty and process integration

- [ ] P6.1 Evaluate the actual model over correlated parameter draws; preserve
  strategy, draw, replication, perspective and subgroup identity.
- [ ] P6.2 Consume Voiage's qualified paired-outcome/VOP/VOH contract; no local VOI estimator.
- [ ] P6.3 Qualify observed XES/OCEL records and a bounded Petri-net/PNML profile.
- [ ] P6.4 Qualify BPMN 2.0 subset/conversion with explicit unsupported-element diagnostics.
- [ ] P6.5 Integrate Kairos usage when provider Track 114 delivers its contract.
- [ ] P6.6 Test exclusive/parallel paths, rework, cancellation, censored intervals,
  transfer semantics and shared-batch allocation against independent models.

## P7 — research and consolidation

- [ ] P7.1 Benchmark incremental revaluation versus full recomputation and controlled
  missing-cost/double-counting detection versus conventional analysis.
- [ ] P7.2 Add Innovate adoption/capacity and optional Paignia strategic pricing cases.
- [ ] P7.3 Evaluate multi-perspective/subgroup measurement priorities with Voiage.
- [ ] P7.4 Conduct independent/multi-site transportability and usability studies;
  update a dated comparator review before frontier claims.
- [ ] P7.5 Review unique history, rights, successor and recovery before each optional
  archive action; retain scholarly projects and source-provider responsibilities.
- [ ] P7.6 Publish only qualified capabilities, artifacts and reproducible evidence.

## Design verification — 8 November 2026

Track JSON, required maturity fields, new relative links and whitespace checks
passed. Ruff 0.17.3 passed across an isolated materialization of all tracked
Python sources and applicable configuration. The current sparse checkout was
not used as evidence of whole-source coverage. Fourteen unrelated, pre-existing
track links target absent directories and remain outside this change.

No runtime tests, native builds, binding installations or tenant deployments
were run for this documentation change. Runtime tasks above remain pending.
The sourced reporting catalogue is proposed in
[standards_check PR 65](https://github.com/edithatogo/standards_check/pull/65).
