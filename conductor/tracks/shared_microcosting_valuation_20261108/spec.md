# Specification: Dapane shared microcosting and valuation

## Problem and outcome

Workforce, genomics, hospital funding and operational costing duplicate data and
valuation mechanics while representing different economic meanings. Establish an
independent Rust core and composable domain contracts without erasing their roles.
Support Python first, R and Julia later; expose results through a Power App using
a standard-connector baseline, optional premium service and candidate browser lane.

## Scope

- Shared typed quantities, resource use and separate weighted activity, exact
  valuation, explicit allocation and reconciled component ledgers.
- Versioned sources, quotations, methods, effective/knowledge dates, perspectives,
  uncertainty/heterogeneity identities and reproducible run bundles.
- Workforce and genomics as first consumers; early MCHS mapping; newborn screening
  as next composed service model.
- Optional UOGTO reporting semantics sourced from standards_check; external
  tariff data from reimbursement-atlas; process adapters using qualified Rust4PM
  and optional PM4Py rather than duplicated engines.
- Existing Kairos, Voiage, Innovate and Paignia responsibilities and provider pins.

## Non-goals for this change

This planning change publishes no Rust package, language binding, Power App,
clinical programme, accepted workforce release or live price catalogue. It does
not archive repositories, change public calculation APIs or qualify methods by
copying legacy outputs. UOGTO semantic implementation is separately owned and
cannot be described as a completed runtime integration.

## Interfaces and constraints

The [architecture](../../../docs/roadmaps/dapane-framework.md) defines the target
contracts and ownership. Keep a small standalone Rust core; language wrappers,
IO, ontology validation, process models and service transports remain optional.
No compulsory pandas/xarray representation enters the new framework. Migration
adapters may retain historical inputs with explicit status until their existing
models are reproduced and repaired under separate decisions.

The R wrapper can use extendr against the core without waiting for the Julia C
ABI. Wrappers adapt host objects and packaging; all numerical rules remain in
the shared implementation. The [Power Platform boundary](../../power-platform-boundary.md)
defines the manual bundle baseline and separately qualified optional transports.

Select supported units and exact decimal/rational transport before FFI. Preserve
MCHS pricing editions separately from economic price year. Cost, tariff, funding
and actual-payment outputs cannot be silently added or substituted.

## Acceptance criteria

1. Two independent domain consumers use one shared numerical implementation.
2. Shared batch/pool and loaded-component examples conserve costs without duplication.
3. Missing rates, unsupported rule interactions and incompatible units fail explicitly.
4. Date segmentation and aggregation preserve exact results under declared policies.
5. Installed Python artifacts match native fixtures; later R/Julia use the same oracle.
6. A newborn-screening model preserves infant/specimen/batch/test relationships and
   labels all invented examples as synthetic.
7. A standard Power App route has no hidden premium connector/HTTP/gateway dependency;
   target environment/user entitlement is separately checked at deployment.
8. Source/profile mappings distinguish reporting, methods, appraisal and prototypes;
   SHACL validation is not represented as empirical or methodological validity.
9. Process adapters expose supported semantics and pass branching, parallelism,
   repeat, cancellation and shared-batch cases before support is advertised.
10. Every released capability names exact artifacts, methods, data versions,
    limitations and observed validation evidence.

## Migration and rollback

Keep old entry points as explicit adapters during qualification. Run candidate
results beside independent reference examples, separating extraction differences
from scientific corrections. Consumers pin qualified versions and can restore
their previous qualified adapter. Archive only after a successor and preservation
record exist; no blanket consolidation is authorised by an archive recommendation.

## Planning assumptions

Dapane is a working name, not a reserved registry identity. Interpret the process
request as Petri nets/BPMN 2.0. Coding-agent delivery should use small executable
leaves and one coherent review at numerical/schema/release boundaries. Initial
two-domain demonstrator estimate: 2–4 weeks with usable fixtures and timely domain
decisions; source interpretation and external validation have separate readiness.
