# Power Platform Service Boundary (Power-app orchestration boundary)

This service slice exposes a hardened HTTP boundary for Power Platform and other
orchestration surfaces. The implementation intentionally delegates calculation
requests to existing MCP handlers in `nwau_py.mcp_server` and does not execute
pricing formulas directly.

## Boundaries

- `GET /healthz` exposes runtime readiness.
- `GET /.well-known/mcp/server-card.json` exposes MCP metadata fallback.
- `GET /v1/calculators` lists calculators supported by MCP.
- `GET /v1/calculators/{calculator_id}` reads one calculator definition.
- `GET /v1/schemas/{schema_name}` reads canonical schemas through MCP resources.
- `POST /v1/validate` validates request payloads against the MCP boundary.
- `POST /v1/calculations` validates then delegates to MCP calculation handler.
- `GET /v1/evidence/{bundle_id}` returns evidence from MCP.
- `POST /calculators/run` provides a connector-compatible legacy alias for the
  flow contract.

## Security contract

- If `MCHS_SERVICE_BOUNDARY_API_KEY` is set, requests must include
  `x-mchs-api-key` with the same value.
- If unset, requests are accepted without authentication in deterministic
  CI/preview runs.
- TLS is required by deployment platform; this service only provides HTTP handler
  plumbing and policy guidance.

## Contract envelope

All connector-facing endpoints return:

- `status`: `success`, `validation_required`, or `failure`
- `result_payload`: primary operation payload
- `result`: alias to `result_payload` for compatibility with older manifests
- `warnings`: list of non-blocking notices
- `trace_id`: correlation identifier for auditability
