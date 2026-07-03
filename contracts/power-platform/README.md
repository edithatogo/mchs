# Power Platform Binding Contract

This contract turns the Power Platform binding from a roadmap-only surface into
credential-free, service-boundary artifacts that can be checked in CI.

The Power Platform solution remains orchestration-only:

- Canvas apps and flows collect inputs, submit requests, and display structured
  results.
- The custom connector calls the shared calculator service boundary.
- Formula logic, pricing-year rules, and classification rules stay in the shared
  runtime, not in Power Fx, Dataverse, flows, or connector policy templates.

## Artifacts

- [`power-platform-binding.schema.json`](./power-platform-binding.schema.json)
  defines the checked contract bundle shape.
- [`power-platform-binding.contract.json`](./power-platform-binding.contract.json)
  declares the supported custom connector, flow, environment variable, ALM, and
  validation gates.
- [`calculator-capability-matrix.json`](./calculator-capability-matrix.json)
  declares every Power Apps calculator selector and every pricing year state
  the app may display without overclaiming support. The declared display window
  is the archived IHACPA evidence horizon from 2013 through 2026.
- [`custom-connector.openapi.yaml`](./custom-connector.openapi.yaml) defines the
  local custom connector boundary for request/response generation.
- [`examples/validation.pass.json`](./examples/validation.pass.json) records a
  synthetic passing orchestration example.
- [`examples/capabilities.pass.json`](./examples/capabilities.pass.json)
  records selector coverage expectations for the capability matrix.
- [`examples/validation.fail.json`](./examples/validation.fail.json) records the
  rejected pattern: Power Platform-owned formula logic or direct calculation.

## Local Validation

The focused test suite validates the contract files without contacting Power
Platform:

```bash
uv run pytest tests/test_power_platform_binding_track.py
python scripts/validate_power_platform_capabilities.py
```

The test checks JSON/YAML parseability, required contract fields, OpenAPI
operation boundaries, capability-matrix coverage, environment variable
declarations, and no-formula ownership assertions.
