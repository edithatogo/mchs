# Dapane: shared microcosting and valuation framework

Status: proposed architecture and implementation roadmap, 8 November 2026.
This document does not claim a new package, binding, deployment or validated costing
model has been released. Dapane is the recommended working name; registry publication
and name reservation are separate future tasks.

## Purpose and scope

Create an independent Rust framework for resource microcosting, allocation and
explicit economic, accounting, cash, tariff and funding valuations. Python is the
first language binding; R and Julia follow through the same numerical implementation.
Domain packages remain independently useful and optional. A static costing study must
run without a simulator, game solver, ontology reasoner or Power Platform tenant.

MCHS coordinates the initial cross-repository plan because it already owns activity,
pricing and polyglot interfaces. It is not the permanent home of all domain models.
Prove an independent package boundary with workforce and genomics consumers before
publishing the new framework. Preserve existing APIs through explicit adapters.

## Ownership and existing work

| Owner | Continuing responsibility | Shared-framework relationship |
| --- | --- | --- |
| Dapane, proposed | Quantities, valuation policies, allocation arithmetic, result ledger, reproducibility and bindings | Independent Rust core |
| microcosting_healthworkforce | Conditions, employment scope, eligibility inputs, supported rule interactions and dated workforce sources | First valuation/quotation plugin; generic import namespace must be repaired |
| microcosting_genomics | Assay/workflow recipes, batching, repeat/failure assumptions and historical workbook interpretation | Resource-model plugin; existing demonstration analyses require separation |
| mchs | Classification-specific weighted activity, edition-specific equations and funding/pricing rules | Activity and tariff plugin; no automatic conversion of funding into resource cost |
| reimbursement-atlas | Schedule discovery, source editions, licences, parser outputs and cross-jurisdiction evidence | Optional tariff-data provider; reuse its registry rather than copy parsers |
| careops/modules/careops-costing | Workflow, assumption capture, review, presentation and reporting | Standard-connector/file consumer first; premium surfaces remain optional |
| Kairos and CareOps-Sim | Neutral resource execution and healthcare process models respectively | Optional usage producers; Kairos never depends on the valuation core |
| Innovate | Adoption, utilisation, substitution and competition mechanisms | Supplies trajectories; application orchestrates feedback with costs |
| Voiage | VOI, value of perspective and heterogeneity methods under their qualified contracts | Consumes aligned strategy/draw/perspective/subgroup results |
| Paignia | Supported game representation and solving | Optional strategic-pricing application dependency |
| UOGTO | Semantic definitions, reporting-profile mappings and explicit game/HTA bridges | Optional costing-valuation applied pack; no mandatory runtime reasoner |
| standards_check | Original checklist provenance and canonical source catalogue | Source owner for reporting instruments; ontology owns semantic reconciliation |
| rust4pm | Process-mining library/fork and interoperability work | Optional process adapter candidate; qualify upstream revision and supported subset |

Existing owners remain authoritative: workforce conditions/source tracks, MCHS Rust
and wrapper tracks, Kairos Track 114, Voiage simulation-outcome and perspective/
heterogeneity tracks, Innovate's native programme and Paignia T17. This plan adds
consumer boundaries; it does not mark their implementation complete or move their
dependency pins.

## Common data model

Keep physical resource use separate from classified/weighted activity. A unit must
retain its measurement system and edition: an NWAU, a specimen and a staff-hour are
not interchangeable. The public contracts should describe:

1. ResourceUse: source-qualified identity, activity/cost-object links, quantity/unit,
   instant or half-open interval, observation/assumption basis and correction identity.
2. ActivityMeasure: service/episode identity, classification system and version,
   measure quantity and source provenance.
3. UnitQuote and RateRelease: exact amount/denominator, currency, applicability,
   effective interval, knowledge/publication/retrieval dates and immutable release.
4. ValuationPolicy: perspective, valuation basis, horizon, price year, inflation/FX
   method, capital treatment, allocation, discounting and rounding policy.
5. ValuationLine: quantity, applied quotation or method, component and cost-pool
   identities, result, lineage, completeness and unsupported-capability diagnostics.
6. RunBundle: schema/method/engine/plugin/data versions, input and output digests,
   strategy, scenario, parameter-draw, replication, perspective and subgroup keys.

Use JSON manifests and schema-versioned Arrow/Parquet payloads as optional encodings.
Do not equate a successful schema check with truthful sources, correct methodology or
valid clinical/industrial interpretation. Preserve evidence, access/licensing and
validation status as independent axes. A synthetic rate is never promoted by calling
it public or locally licensed.

## Numerical and economic invariants

- Preserve decimal source values and exact rational exposure where required. A finite
  decimal implementation alone cannot reproduce every current workforce Fraction result.
- Define decimal-string/coefficient-scale and numerator/denominator transport before
  crossing Python, JSON, Arrow, R or Julia boundaries. Reject overflow, unsupported
  precision and accidental float coercion.
- State whether rounding occurs at line, pool, invoice or aggregate level; retain the
  unrounded value and reconcile allocated residuals. Bitwise identity is a bounded
  contract for exact paths, not a universal promise for every probabilistic backend.
- Separate acquisition expenditure, accounting allocation, economic opportunity cost,
  tariff/funding valuation and observed payment. Actual payments need observations or
  an explicitly labelled payment model.
- Fixed/variable and average/marginal classifications depend on horizon and scenario.
  Spare capacity does not automatically produce a cash saving.
- A resource-use identity is counted once. Loaded rates disclose included components.
  Purchase, depreciation and economic annualisation are alternative asset treatments.
- Allocated pool amounts plus explicit unallocated residuals reconcile to each pool.
- Split usage at relevant effective-rate boundaries. Keep historical-as-known and
  retrospectively-corrected analyses distinguishable; never select a newer pack silently.
- Stochastic evaluation accepts explicit indexed draws and correlations. It never
  substitutes random demonstration outcomes for unsupported model calculations.

## Rust packages and dependency policy

Use a small Rust workspace: core types/arithmetic, optional data IO, CLI, Python
binding, later C ABI and optional WASM. Domain plugins initially mean ordinary typed
packages or versioned file adapters. Do not introduce a native dynamic plugin ABI or
an arbitrary expression language before two consumers establish the need.

Reuse serde/serde_json, thiserror, a qualified date/time implementation, rust_decimal,
an established rational-number implementation where needed, and existing hashing and
schema tooling. Prefer Polars for the supported table interface; Arrow/Parquet is an
interchange boundary rather than a mandatory dependency of scalar arithmetic.

At implementation time, record exact tested versions, Rust MSRV, Python ABI and OS/
architecture targets in one compatibility matrix. Current stable releases are the
baseline; preview versions belong in isolated canary jobs. Do not synchronously
upgrade every sibling repository or silently widen workforce's selected Python pin.
Avoid copying MCHS's optional hardware-acceleration defaults into a small costing core.

Use deterministic CPU execution first. Benchmark real allocation/valuation workloads
before parallelism, GPU, distributed execution or differentiable kernels are supported.
Deterministic parallel reduction, chunk-boundary invariance and exact numeric transport
are acceptance requirements for each acceleration path. Whole-source and installed-
artifact tests must distinguish implementation, packaging and consumer qualification.

Supply-chain work should use existing portfolio controls: locked dependencies, scoped
permissions, immutable action pins, licence/advisory checks, SBOM and release provenance.
No extra approval board is needed for ordinary implementation. Real source rights,
method qualification and deployment remain separate named decisions.

## Python now; R and Julia later

| Surface | Implementation direction | Qualification |
| --- | --- | --- |
| Python | PyO3 + maturin; thin batch APIs and Polars/Arrow adapters | Installed wheels, error/ownership checks, shared fixture parity, no duplicated maths |
| R | Thin extendr wrapper calling the same Rust core; scaffold/package with rextendr | R GC/lifetime handling, main-thread API constraints, missing values, native package install |
| Julia | Direct `@ccall`/`ccall` through the versioned C ABI; BinaryBuilder/JLL artifacts when release-ready | GC preservation, ownership, platform artifact resolution and same fixtures |
| CLI/file | Stable JSON manifest plus optional Arrow/Parquet | Independent clean consumer and deterministic receipts |
| WASM | Optional build of the same bounded core | Browser memory, performance and package/host checks; no promised full Arrow stack |

The C ABI exposes opaque handles or owned result buffers, explicit lengths and error
codes, version negotiation, allocator/free symmetry and panic containment. Rust layouts
and unwinding must never cross that boundary. Native language objects stay in their
host wrappers. Zero-copy is permitted only where layout/lifetime/ownership is proven;
it is not an unconditional requirement for every type or binding.

The R wrapper can depend on the Rust core directly; delivery need not wait for the C
ABI. Keep extendr and PyO3 in their wrapper crates, outside the minimal core. Julia
consumes the separately qualified C ABI without requiring Python or R. No wrapper
introduces a second implementation of the economic or numerical rules.

## Power Platform surfaces

Keep the calculation in the shared Rust engine. The app handles inputs, run state,
comparison and explanation. Preserve prior premium work as an optional delivery lane.

| Lane | Shape | Conditions |
| --- | --- | --- |
| Standard baseline | Canvas app + standard SharePoint connector; requests/results in Lists and a document library; manual CLI/file run first | Users and environment must have applicable standard-app rights; no custom/HTTP connector is introduced |
| Optional asynchronous worker | An independently operated authorised Rust worker processes versioned request bundles and writes results | Separate host cost, identity, scoped access, job claiming, immutable inputs, retries/idempotency, cancellation and audit; asynchronous turnaround, not a promised instant API |
| Optional premium service | Custom connector/OpenAPI to authenticated Rust service or Azure-hosted container/custom handler | Actual premium connector/flow/environment entitlement and service operation are required |
| Later local interactive option | Candidate Rust-to-WASM build packaged in a PCF component | Prove canvas web/mobile host, CSP, bundled assets, memory and lifecycle behaviour; direct external-service calls make the component premium |

A standard connector alone does not establish non-premium entitlement: Microsoft
Managed Environments and an app-associated premium flow can impose additional rights.
Managed Environment requirements also cover users of standard apps. Do not treat a
displayed Standard badge as proof that an HTTP flow is covered. The independent worker
must not be a proxy for unlicensed premium services; a SharePoint queue does not remove
licensing obligations of any service behind it. No gateway, premium HTTP action,
Dataverse dependency or Copilot is hidden in the baseline. Actual tenant provisioning
and use rights are not established by this design.

Microsoft documents a standard classification for client-only PCF components in an
otherwise standard app. This does not establish Rust/WASM execution support in every
canvas host. PCF enablement requires environment administrator action and component
import/qualification. Bundle the component's dependencies, use supported app inputs
and outputs, and preserve the host's security configuration; canvas PCF custom
authentication is unsupported. The worker/file route remains available if the WASM
candidate cannot meet the target host's constraints.

For large results, store immutable files and only run IDs/status/summaries in Lists.
Use explicit errors and completeness; never expose a partial result as complete.
The UI never reimplements Rust financial rules in Power Fx.

## Newborn screening as the next domain model

Implement a screening pathway profile composed from shared resource recipes and
workforce quotations. It should cover conventional laboratory screening and optional
genomic routes without assuming that every programme uses the same tests or criteria.
Use a versioned jurisdiction/programme pack for scope and clinical assumptions.

Separate Infant, ScreeningEpisode, Specimen/Card, CollectionAttempt, Assay, Batch,
Result, Recall, ConfirmatoryEpisode and FollowUp. A specimen may serve many assays and
a batch many infants. Cost collection, transport, setup, controls and other shared work
once, with an explicit allocation policy and residual. Do not copy a batch total onto
each infant or each screened condition.

Model the following configurable pathway stages: information/consent; collection;
transport/accession; specimen quality; initial testing; insufficient sample or failed/
indeterminate test; repeat/reflex testing; result handling; recall and confirmation;
referral/communication; quality assurance, storage and programme overhead. Clinical
branch probabilities and timing are sourced inputs, not ontology defaults.

Distinguish cost per eligible birth, participating infant, valid screen, completed
pathway and confirmed diagnosis. Preserve denominator and observation-window identity.
Compare programme total, added condition/panel, alternative pathway and capacity-step
scenarios. Include setup/training, capital, ongoing QC, repeats, false-positive follow-up
and travel/family time when the selected perspective requires them. Lifetime outcomes
and cost-effectiveness belong to the linked health-economic model; a costing recipe
does not establish clinical benefit or programme eligibility.

Initial semantic fixture: two infants, two specimens, one shared batch, a separate
confirmation episode, distinct resource lines and a reconciled batch allocation.
Add repeat-collection and failed-assay variants during runtime qualification.
All numbers are invented for arithmetic tests; no patient record or clinical rate is
published. A subsequent real study needs scoped programme data and independent examples.

Use AGREEDT for diagnostic-test reporting coverage alongside general economic and
costing profiles. Australia's current programme sources separate screening and further
diagnostic testing; current policy material also identifies superseded parts of the
older national framework. Do not hard-code old nomination/decision pathways.

## Process models: Petri nets and BPMN 2.0

Interpret the requested process-model term as Petri nets. Reuse the user's rust4pm
work and established process-mining tools rather than implement another parser/miner.

Stage the adapter work:

1. Import observed event/resource records with stable activity and object identifiers.
2. Qualify XES and OCEL 2.0 adapters; retain infant/specimen/batch relationships.
3. Qualify a bounded Petri-net/PNML profile with explicit marking, transition firing,
   multiplicity, resource allocation and timing assumptions.
4. Import/export a named BPMN 2.0 subset, initially qualifying start/end events, tasks
   and selected exclusive/parallel gateways. Qualify inclusive gateways, loops,
   concurrency interactions, additional events and subprocesses separately before
   advertising them. Reject unsupported semantics rather than silently flattening them.
5. Attach resource recipes to executed activity instances; attach valuations separately.
6. Use Kairos for required simulated execution and PM tools for discovery/conformance.

rust4pm/process_mining is a native candidate under MIT/Apache-2.0; its documented API
volatility requires exact-pin qualification. Its advertised native capabilities include
XES, OCEL 2.0 and Petri nets/PNML, not a general BPMN execution engine. PM4Py is an
optional interoperability or comparison adapter under AGPL-3.0 or separate commercial
terms, and its documented BPMN support is itself limited. Do not silently embed it in
an Apache-only runtime or assume a subprocess resolves all licence obligations.
Neither a drawn BPMN diagram nor a PNML import proves an executable, timed or
economically valid model. Standards_check's checklist Petri nets represent reporting
workflows, not automatically patient/service resource models.

Qualification cases cover parallel activity, shared staff, batch setup, loops/rework,
cancelled and censored activities, transfer versus consumption and model-version drift.
Changing a price pack must not rerun or change resource execution. Where a price changes
behaviour or adoption, the application explicitly coordinates the feedback scenario.

## Reporting ontology and evidence

Add the optional UOGTO costing-valuation pack and sourced reporting profiles. Preserve
each instrument/version and its distinct role: reporting checklist, method reference,
appraisal instrument, sector costing standard or unvalidated protocol/prototype.
Standards_check retains source catalogue ownership. Mappings use verified item IDs
where available; source-level/domain mappings remain explicitly labelled.

Reconciliation means shared semantic domains and conditional profiles, not a claim
that all checklist items are equivalent or mandatory for every study. Reported,
partially reported, not reported, not assessed and not applicable remain distinguishable.
Not-applicable needs a rationale; reported needs evidence. Structural SHACL conformance
does not establish study quality, source truth or scientific correctness.

## Consolidation and archive decisions

| Repository | Disposition | Gate |
| --- | --- | --- |
| mchs; microcosting_healthworkforce; microcosting_genomics | Keep as specialist products/plugins | Migrate only shared mechanics; preserve public API and historical reproducibility |
| careops-costing; careops-costing-public | Already archived in inspected metadata | Continue in careops/modules/careops-costing; do not restart migration |
| hwcc | Conditional archive candidate | Reconcile unique rules/private evidence with maintained CareOps source, document successor and recovery |
| cobra-costing | Conditional archive candidate; root currently contains README/licence only | Review all branches/history and unique research intent before final archive |
| tutorial_microcosting_genomics | Keep scholarly identity; consolidate duplicated executable examples if useful | Preserve citations, history and manuscript assets before considering an archive |
| checklist_microcosting | Preserve methods research; candidate software consolidation into standards_check/UOGTO | Clearly retain synthetic/protocol status; preserve unique research before archive |
| voi_sequencing_costs | Keep as research consumer | Replace duplicate machinery through supported adapters; retain study artefacts |
| standards_check; reimbursement-atlas; rust4pm | Keep with their separate responsibilities | No replacement by duplicated checklist, tariff or process infrastructure |

No repository is archived by this planning change. Archival requires a concrete
successor, preserved history/licensing, unique-content review and a working migration.

## Beyond-frontier research programme

These are hypotheses to evaluate, not claims of novelty or validated capability:

- Evidence-linked executable costing: bind each valuation to source, method, quantity,
  uncertainty and reporting requirement; test error detection and reproducibility.
- Object-centric process costing: conserve shared resource/batch costs across many
  linked cases; compare against flattened event-log methods using controlled fixtures.
- Incremental revaluation: update a changed rate/source/model fragment and recompute
  only affected results; prove equivalence to complete recomputation before speed claims.
- Multi-perspective and heterogeneous valuation: retain correlated subgroup/perspective
  outputs, avoid adding transfers across perspectives, and delegate VOP/VOH/VOI methods
  to qualified Voiage capabilities rather than invent local estimators.
- Measurement planning: use Voiage to compare additional time-motion, utilisation,
  wastage or price evidence; distinguish epistemic uncertainty from population variation.
- Capacity and adoption feedback: combine Innovate trajectories and explicit resource
  thresholds; test average, incremental and opportunity-cost differences independently.
- Strategic pricing: use Paignia only for supported negotiation/competition games with
  source-qualified domain payoffs and observable decision assumptions.
- Privacy-preserving multi-site calibration: qualify aggregate or federated summaries,
  disclosure control and privacy/utility tradeoffs; avoid a universal central record store.

Pre-register benchmark questions and independent oracles. Measure numerical correctness,
missing-cost detection, reporting coverage, cross-language parity, reproducibility,
throughput/memory and real modelling effort. Synthetic studies establish controlled
behaviour; multi-site external data establish transportability. A frontier claim needs
a dated comparator review and evidence exceeding the strongest relevant baseline.

## Primary references and ecosystem records

- [Rust/Python packaging](https://pyo3.rs/main/getting-started) and [maturin](https://www.maturin.rs/).
- [Arrow C data interface](https://arrow.apache.org/docs/format/CDataInterface.html).
- [R extendr](https://extendr.rs/), [Julia C interface](https://docs.julialang.org/en/v1/manual/calling-c-and-fortran-code/) and [BinaryBuilder/JLL packaging](https://docs.binarybuilder.org/stable/).
- [Power Apps licence designation](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/license-designation) and [licensing FAQ](https://learn.microsoft.com/en-us/power-platform/admin/powerapps-licensing-faq).
- [PCF overview and licensing](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview).
- [Canvas PCF enablement](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps) and [PCF limitations](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations).
- [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepoint/), [Managed Environment licensing](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-licensing) and [Power Automate licensing/multiplexing](https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/faqs).
- [Azure Functions Rust/custom handlers](https://learn.microsoft.com/en-us/azure/azure-functions/functions-custom-handlers) and [selected SharePoint/Graph permissions](https://learn.microsoft.com/en-us/graph/permissions-selected-overview).
- [Australian NBS process](https://www.health.gov.au/our-work/newborn-bloodspot-screening/about) and [current scope/policy pathway](https://www.health.gov.au/our-work/newborn-bloodspot-screening/what-is-screened).
- [AGREEDT](https://doi.org/10.1177/0272989X18797590).
- [Rust4PM](https://github.com/edithatogo/rust4pm), [process_mining docs](https://docs.rs/process_mining/), [PM4Py](https://github.com/process-intelligence-solutions/pm4py) and [BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/).
- [PM4Py's documented BPMN subset](https://processintelligence.solutions/pm4py/examples/bpmn-support).
- [UOGTO](https://github.com/edithatogo/UOGTO), [standards_check](https://github.com/edithatogo/standards_check) and [reimbursement-atlas](https://github.com/edithatogo/reimbursement-atlas).

Source review date: 2026-11-08. Public pages and external package support must be
rechecked at the relevant implementation/release milestone.
