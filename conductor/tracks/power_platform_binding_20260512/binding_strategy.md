# Binding Strategy: Power Platform Binding

## Decision

Publish Power Platform as a managed solution / custom connector consumer of
the shared calculator contract. Power Platform apps, flows, and connectors
call the shared-core through a service API or CLI/file boundary and never
contain calculator formula logic.

This follows the boundary rules in
`conductor/power-platform-boundary.md` and reuses the contract and
orchestration patterns established by the C# engine and CLI/file interop
tracks.

## Rationale

- Power Platform is an orchestration and presentation layer. Calculator
  formula logic belongs in the shared Rust core, not in Power Fx,
  Dataverse plugins, or canvas app expressions.
- The shared service API or CLI/file boundary gives a single integration
  point for managed connectors, Power Automate flows, and model-driven apps.
- ALM (Application Lifecycle Management) through `pac` CLI and managed
  solutions keeps Power Platform assets declarative and source-controlled.
- The existing Power Platform boundary document
  (`conductor/power-platform-boundary.md`) already defines the integration
  shape and separation rules.

## Contract shape

### Integration modes

| Mode                 | Consumer               | Transport          | Notes                         |
|----------------------|------------------------|--------------------|-------------------------------|
| Custom Connector     | Canvas/model-driven app| HTTP / REST API    | Primary interactive mode      |
| Power Automate Flow  | Automated workflow     | HTTP / REST API    | Batch or event-driven         |
| Service API          | Azure Function / App   | HTTPS              | Secured execution boundary    |
| CLI/file boundary    | File drop or process   | Parquet / CSV      | Offline or bulk handoff       |

### Request/response schema

The custom connector request and response schema mirrors the public
calculator contract (`conductor/public-api-contract.md`) and adds only
transport metadata:

- `contract_version` — pinned calculator contract version
- `calculator_id` — public calculator identifier
- `pricing_year` — target IHACPA pricing year
- `input` — structured input payload matching the contract schema
- `fixture_gate` — declared synthetic-only or local-only gate
- `correlation_id` — traceable caller identifier

The source-controlled contract artifacts are
`contracts/power-platform/power-platform-binding.contract.json` and
`contracts/power-platform/custom-connector.openapi.yaml`.
Power Platform uses `listMchsCalculatorCapabilities` for selector discovery,
`validateMchsCalculatorInput` for pre-submit checks, and `runMchsCalculation`
for calculation delegation.

Response fields from the calculator contract are surfaced as structured
outputs for workflow apps: success/fail status, computed values,
diagnostics, and provenance.

### ALM requirements

- Power Platform solution assets are packaged as managed solutions using
  `pac solution pack` and tracked in source control under
  `power-platform/`.
- Environment variables and connection references are declared in the
  solution and configured per environment.
- Solution checker (`pac solution check`) must pass before solution import.
- ALM promotions flow from dev → test → prod with `pac solution upgrade`.

## Supported calculators

Power Platform discovers calculator/year coverage through
`listMchsCalculatorCapabilities` and
`contracts/power-platform/calculator-capability-matrix.json`. source-available
coverage from 2013 through 2026 is visible for selection context, while submit
actions remain disabled until the selected state is implemented or helper.
Historical variant surfaces remain discoverable without being runnable app
logic.

## Limitations

- Power Platform does not execute calculator logic. All calculation happens
  in the service boundary or through pre-computed file handoff.
- Real-data workflows must remain behind a secured service boundary that
  enforces authentication, authorization, and audit logging.
- Power Fx, Dataverse plugins, and canvas-app expressions must not contain
  formula constants, pricing-year mappings, or classification rules.
- Power BI datasets and reports must consume pre-computed results, not
  recalculate within DAX or Power Query.

## Versioning

- The Power Platform connector and solution version pin to the shared
  calculator contract version.
- ALM package versions follow the shared-core release versioning policy.
- Breaking contract changes trigger a new connector version and solution
  upgrade.

## Diagnostics and provenance

- Diagnostics from the service boundary (validation warnings, calculator
  errors, fixture gate states) are surfaced as structured connector outputs.
- Power Automate flows log correlation IDs and results for auditability.
- Power BI reports consuming pre-computed data declare the
  `contract_version` and `pricing_year` as dataset metadata.

## Privacy and synthetic examples

- All committed Power Platform example manifests and test data are
  synthetic.
- Real IHACPA pricing data or patient-level extracts never enter Power
  Platform example assets.
- The `fixture_gate` field distinguishes synthetic examples from
  local-only real data.

## When to use Power Platform vs. other bindings

Use Power Platform when:
- the consumer needs a low-code canvas or model-driven app interface
- the workflow requires Power Automate event-driven orchestration
- institutional consumers are restricted to managed Microsoft solutions

Prefer CLI/file interop or native bindings when:
- the integration is batch-only and does not need a UI
- the consumer needs in-process or sub-second calculator calls
- the deployment target is not a Microsoft tenant

## Readiness bar

- Local contract artifacts and validation tests are source-controlled, including
  `tests/test_power_platform_binding_track.py`.
- The managed solution publication path is documented, but runtime execution is
  not claimed until tenant connector configuration and app-player smoke evidence
  are captured.
- There is no tenant-exported managed solution zip in source control; managed
  solution export/import remains an external tenant gate.
- Do not claim Power Platform integration as production-ready until the shared
  service API is stable, the custom connector points at a real service endpoint,
  and solution checker passes for the managed solution.
