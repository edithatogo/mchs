# Service-Boundary Public HTTPS Endpoint Operator Package

This package is for creating and collecting evidence from a real public HTTPS
service-boundary endpoint. The checked-in JSON files are examples only and do
not claim that a live endpoint exists.

## Required inputs

- A real public HTTPS base URL
- A deployed API key or equivalent secret material for the service boundary
- `GET /healthz`
- `GET /.well-known/mcp/server-card.json`

## Example artifacts

- `power-platform/evidence/service-boundary-endpoint-template.json`
- `power-platform/evidence/examples/service-boundary-endpoint-operator-input.example.json`
- `power-platform/evidence/examples/service-boundary-probe-result.example.json`

## Live endpoint procedure

1. Create a local config from the checked-in template and set the real base
   URL.

```bash
REAL_BASE_URL='https://your-real-public-host.example'

jq --arg url "$REAL_BASE_URL" \
  '.serviceBoundary.httpsBaseUrl = $url | .serviceBoundary.apiKeySecretConfigured = true' \
  power-platform/evidence/service-boundary-endpoint-template.json \
  > /tmp/mchs-service-boundary-config.json
```

2. Validate the config shape before probing.

```bash
python3 scripts/validate_power_platform_service_boundary_endpoint.py \
  --config /tmp/mchs-service-boundary-config.json \
  > /tmp/mchs-service-boundary-validate.json
```

3. Probe the real endpoint and capture the validator output as JSON.

```bash
python3 scripts/validate_power_platform_service_boundary_endpoint.py \
  --config /tmp/mchs-service-boundary-config.json \
  --probe \
  > /tmp/mchs-service-boundary-probe.json
```

4. Render the evidence record from the real probe result.

```bash
python3 scripts/update_power_platform_service_boundary_endpoint_evidence.py \
  --https-base-url "$REAL_BASE_URL" \
  --probe-result /tmp/mchs-service-boundary-probe.json \
  --output power-platform/evidence/live-service-boundary-smoke-$(date +%F).json
```

## Dry-run package

Use the example probe payload only to confirm the updater wiring.

```bash
python3 scripts/update_power_platform_service_boundary_endpoint_evidence.py \
  --https-base-url 'https://service-boundary.example' \
  --probe-result power-platform/evidence/examples/service-boundary-probe-result.example.json \
  --output /tmp/mchs-service-boundary-evidence-preview.json
```

## Guardrails

- Do not replace `null` or placeholder values in checked-in files with a
  fabricated production claim.
- Do not set `productionReadinessClaimed` manually.
- Only publish `power-platform/evidence/live-service-boundary-smoke-<date>.json`
  after the validator probe succeeds against a real public HTTPS endpoint.
