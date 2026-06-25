# Swift binding contract fixtures

This directory contains synthetic fixtures and contract metadata for the Swift
binding workstream.

## Contents

- `swift-binding.schema.json`: JSON Schema for the Swift binding contract bundle.
- `swift-binding.contract.json`: Contract document describing request/response
  structs, file-exchange, CLI, C ABI, and service transport modes, diagnostics,
  provenance, errors, fixture gates, and module readiness.
- `examples/service.pass.json`: Synthetic service-bound fallback pass example.
- `examples/file-exchange.pass.json`: Synthetic file-exchange primary pass
  example.
- `examples/diagnostics.pass.json`: Synthetic diagnostics pass example.
- `examples/binding.fail.json`: Synthetic binding failure example.
- `examples/diagnostics.fail.json`: Synthetic diagnostics failure example.

## Scope

These fixtures describe the transport boundary only. They do not include
calculator logic, production outputs, patient data, or licensed payloads.

The request and response shapes are aligned to the public calculator contract
and describe transport-specific fields for the Swift binding surface only.

## Rules

- Keep all committed examples synthetic.
- Mirror the public calculator contract fields explicitly.
- Prefer file exchange first (Parquet/CSV) for offline and batch workflows;
  use the concrete CLI adapter on macOS or the service boundary when a caller
  needs programmatic integration.
- Keep diagnostics, provenance, and errors explicit and machine readable.
- Keep fixture gates local-only and user-supplied.
- Do not embed formula logic or duplicate calculator rules in the Swift binding
  contract.
