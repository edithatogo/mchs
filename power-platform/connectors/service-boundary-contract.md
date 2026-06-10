# Service Boundary Contract

This document defines the request/response contract used by the Power Platform
orchestration layer. The checked bundle lives in
[`../../contracts/power-platform/power-platform-binding.contract.json`](../../contracts/power-platform/power-platform-binding.contract.json),
with the custom connector boundary in
[`../../contracts/power-platform/custom-connector.openapi.yaml`](../../contracts/power-platform/custom-connector.openapi.yaml).

## Request Fields

- `contract_version`
- `calculator_id`
- `pricing_year`
- `fixture_gate`
- `correlation_id`
- `input`

## Response Fields

- `status`
- `result`
- `diagnostics`
- `provenance`
- `correlation_id`

## Connector Operations

- `listMchsCalculatorCapabilities` reads `/capabilities` and returns the
  calculator/pricing-year matrix used by app selectors.
- `validateMchsCalculatorInput` posts to `/validate` and returns diagnostics
  without executing a calculation.
- `runMchsCalculation` posts to `/calculations` and executes only inside the
  shared calculator service boundary.

Validation and calculation operations use the same request envelope so flows
and apps do not need to interpret calculator-specific schemas.

## Rules

- Power Platform must send requests to the secured boundary only.
- Power Platform must render calculator and pricing-year choices from the
  capability matrix instead of hardcoding a single calculator/year default.
- Power Platform must show the full calculator/year matrix, including disabled
  source-available years that have official source evidence but no runnable
  service parity claim yet.
- Calculation logic stays outside Power Platform.
- The boundary must preserve traceability for auditing and validation.
- Power Platform assets may map fields, generate correlation IDs, route errors,
  persist statuses, and display diagnostics.
- Power Platform assets must not own NWAU formula constants, pricing-year
  mappings, classification grouping rules, or source-bundle lookup rules.
