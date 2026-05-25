# Environment Variables

## Contract

These names are declared for the Power Platform orchestration layer.

- `mchs_api_base_url`
- `mchs_api_contract_version`
- `mchs_api_calculator_id`
- `mchs_api_pricing_year`

Canonical declaration:

- `power-platform/solution/environment-variables.json`

## Rules

- Values are environment-specific.
- No secrets are stored in source control.
- Sensitive endpoints are injected through deployment-time configuration.
- As of the current runtime evidence, the deployed custom connector still
  points to `https://example.invalid/`; do not claim a runnable service-boundary
  endpoint until `mchs_api_base_url` and the connector host are configured for a
  real target environment.
