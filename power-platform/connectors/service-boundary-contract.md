# Service Boundary Contract

This document defines the request/response contract used by the Power Platform
orchestration layer for MCP-delegated execution.

Machine-readable contract artifacts:

- `contracts/power-platform/power-platform-binding.contract.json`
- `contracts/power-platform/custom-connector.openapi.yaml`
- `contracts/power-platform/calculator-capability-matrix.json`

## Request Fields

- `contract_version`
- `calculator_id`
- `pricing_year`
- `fixture_gate`
- `correlation_id`
- `input`

## Response Fields

- `status`
- `result_payload`
- `result` (compatibility alias of `result_payload`)
- `warnings`
- `trace_id`
- `diagnostics`
- `provenance`
- `correlation_id`

## Boundary Endpoints

- `GET /healthz`
- `GET /v1/calculators`
- `GET /v1/calculators/{calculator_id}`
- `GET /v1/schemas/{schema_name}`
- `POST /v1/validate`
- `POST /v1/calculations`
- `POST /calculators/run` (legacy orchestration alias)
- `GET /v1/evidence/{bundle_id}`
- `GET /.well-known/mcp/server-card.json`
- `GET /capabilities`
- `POST /validate`
- `POST /calculations`

## Capability Discovery

Power Platform selectors must call `listMchsCalculatorCapabilities` and render
calculator/year states from the source-available capability matrix instead of
hardcoding app formulas. Submit paths use `validateMchsCalculatorInput` before
`runMchsCalculation`.

## Rules

- Power Platform must send requests to the secured boundary only.
- Calculation logic stays outside Power Platform and is delegated to MCP/runtime handlers.
- The boundary must preserve traceability for auditing and validation.
- Authentication is enforced when the service boundary is configured with API key
  material in deployment.
