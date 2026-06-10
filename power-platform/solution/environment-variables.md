# Environment Variables

## Contract

These names are source-controlled declarations for the Power Platform
orchestration layer. Environment-specific values are supplied at deployment
time.

- `mchs_api_base_url`
- `mchs_api_contract_version`
- `mchs_api_default_calculator_id`
- `mchs_api_default_pricing_year`
- `mchs_fixture_gate`

## Rules

- Values are environment-specific.
- No secrets are stored in source control.
- Sensitive endpoints are injected through deployment-time configuration.
- API keys and other secrets belong in connection references or platform secret
  stores, not in environment variable source files.
- These variables select the service boundary and default request metadata only.
  Calculator and pricing-year availability comes from
  `listMchsCalculatorCapabilities`, not from environment-variable defaults, and
  these variables do not encode formula logic.
