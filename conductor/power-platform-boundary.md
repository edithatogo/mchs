# Power Platform Boundary

## Purpose

Power Platform should orchestrate calculator workflows, not contain calculator
logic.

## Shared Microcosting Direction — 2026-11-08

The [shared microcosting track](./tracks/shared_microcosting_valuation_20261108/index.md)
and [Dapane roadmap](../docs/roadmaps/dapane-framework.md) add a standard-connector,
manual-bundle baseline alongside the existing optional service route. These are
delivery designs; this document establishes no deployed app, tenant configuration,
user entitlement or qualified browser runtime.

| Route | Calculation boundary | Qualification before use |
| --- | --- | --- |
| Standard baseline | Canvas app and standard SharePoint connector exchange versioned request/result bundles; an operator runs the shared CLI/core | Manual export/import, exact transport, run identity, incomplete-output handling and actual app/environment rights |
| Optional asynchronous worker | An independently operated, authorised worker consumes the same bundles and invokes the same core | Host cost, scoped access, job claiming, retries/idempotency, cancellation, audit and asynchronous turnaround |
| Optional premium API | Authenticated service exposed through an OpenAPI/custom connector or Azure-hosted handler | Service operation, API security and applicable connector, flow and environment entitlements |
| Candidate local component | A bundled Rust-to-WASM build of the same core in a PCF component | Target web/mobile host, CSP, dependency packaging, memory/lifecycle behaviour, parity and environment enablement |

The SharePoint connector's standard classification does not establish the rights
of a particular user or environment. Associated premium flows and Managed
Environments can introduce additional requirements. A worker or queue cannot be
used to remove licensing obligations for a service behind it. Host operation and
Microsoft licensing are separate deployment questions. The standard baseline
introduces no hidden custom connector, premium HTTP action, gateway or Dataverse
dependency.

Client-only PCF classification is distinct from technical qualification of a
Rust/WASM build. Direct external-service calls make a PCF component premium;
browser code must preserve the host security configuration and supported
authentication model. Retain manual/file operation if the candidate component
cannot meet the target host's constraints.

References: [SharePoint connector](https://learn.microsoft.com/en-us/connectors/sharepoint/),
[app licence designation](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/license-designation),
[Managed Environments](https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-licensing),
[licensing and multiplexing](https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/faqs),
[PCF overview](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview)
and [PCF limitations](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations).

## Boundary Rules

- Inputs should map to the public calculator contract.
- Outputs and errors should be structured for workflow apps.
- Calculation uses the shared Rust-backed core through a qualified delivery
  route. Power Platform formulas must not reproduce its calculation rules.
- The calculation contract and core remain independently buildable and releasable
  from Power Platform, including when a qualified build is packaged in PCF.
- Power Platform and optional Dataverse remain orchestration and storage layers.

## Integration Shape

- A Custom Connector or Azure Function can expose the optional service boundary.
- Standard SharePoint and manual CLI/file exchange use the same versioned
  contracts without requiring an interactive HTTP endpoint.
- The connector should consume contract identifiers and fixture identifiers.
- Real patient-level data remain subject to the existing secure-service and
  [data-governance](./data-governance.md) requirements. A manual demonstration or
  browser experiment does not establish approval for patient-level use; worker
  deployments also require the documented secure boundary.
- Power Platform should not duplicate formula logic or own pricing-year
  validation rules.

## Secure Delivery Contract References

- Existing MCHS solutions and reports consume the shared runtime-neutral
  contract in [`public-api-contract.md`](./public-api-contract.md). Dapane's
  generic resource/valuation bundles need their own qualified versioned contract;
  an MCHS adapter must not impose acute-specific fields on every costing domain.
- Command handlers, bundle manifests and connectors pass contract and run
  metadata explicitly. MCHS retains `contract_version`, `calculator_id` and
  `pricing_year`; its pricing edition remains distinct from economic price year.
  Preserve input/source lineage and include fixture identifiers for qualification
  runs, without inventing fixture identities for operational inputs.
- Power Platform must consume the versioned output contract rather than author
  calculator math or independent schema definitions in tables, flows or canvas logic.
- Data refresh and reporting invoke the qualified calculation route; they must
  not add a second implementation of the calculation rules.

## Delivery Surface Command Split

- Use `pac` for Power Platform lifecycle operations (environments, solution
  pack/unpack, checker, import/export, publish, ALM transitions).
- Use `powerbi` for reporting surface operations (workspace discovery, dataset or
  report import/export, and report operations).
- Keep both surfaces read-only with respect to calculation semantics: actual scoring
  uses the shared core through the qualified manual, worker, service or component route.

## Repository Artifacts and Boundaries

- Repository artifacts for Power Platform and Power BI should be represented as
  declarative files tracked in source control and deployable by CLI operations.
- Do not create separate calculation implementations in managed solution assets,
  Power BI reports or dataset expressions. A qualified PCF route may package the
  same versioned Rust/WASM core as a dependency; this remains a candidate until
  its host and contract checks pass.
