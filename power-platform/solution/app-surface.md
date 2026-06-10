# App Surface

## Responsibilities

- Collect user inputs.
- Orchestrate calls to the secure service boundary.
- Present structured results and validation messages.

## Non-Responsibilities

- Do not calculate the business result in the app layer.
- Do not duplicate formula logic.
- Do not store sensitive business rules inside forms, flows, or tables.

## Runtime Contract

- The app is a user-facing orchestration shell.
- The app consumes environment variables and connection references.
- The app must stay aligned with the service-boundary contract and the
  `contracts/power-platform` OpenAPI operation IDs:
  `listMchsCalculatorCapabilities`, `validateMchsCalculatorInput`, and
  `runMchsCalculation`.
- The app must call `listMchsCalculatorCapabilities` before rendering
  calculator and pricing-year selectors. It must render every calculator row
  against every pricing year returned by the capability matrix. It may enable
  only states declared as enabled in the contract and must display
  source-available, planned, blocked, shadow, and unavailable states without
  submitting them as calculations.
- The source-controlled capability window currently spans 2013 through 2026,
  matching the archived IHACPA source evidence horizon.
- Calculator rows may expose disabled `variant_surfaces` metadata for
  historical source substreams such as ED UDG, ED AECC, and emergency-service
  URG/ES. Variants do not create separate runnable operations.
- The source-controlled selector model lives in
  `power-platform/solution/app-surface.json`.
- The app must pass through `contract_version`, `calculator_id`,
  `pricing_year`, `fixture_gate`, and `correlation_id` with every request.
- The app may display `diagnostics`, `provenance`, `status`, and `result`
  fields returned by the shared service boundary.
