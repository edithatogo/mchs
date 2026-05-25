# MATLAB Interop Binding Contract Fixtures

This directory contains synthetic metadata-only fixtures for the MATLAB
interoperability binding workstream.

## Contents

- `matlab-interop-binding.schema.json`: JSON Schema for the MATLAB interop
  binding contract bundle.
- `matlab-interop-binding.contract.json`: Contract document describing
  request/response structures, file-import, CLI-invocation, MAT-exchange,
  and C ABI MEX transport modes, diagnostics, provenance, errors, fixture
  gates, and module readiness.
- `examples/file-import.pass.json`: Synthetic file-import primary pass example.
- `examples/cli-invocation.pass.json`: Synthetic CLI-invocation primary pass
  example.
- `examples/diagnostics.pass.json`: Synthetic diagnostics pass example.
- `examples/binding.fail.json`: Synthetic binding failure example.
- `examples/diagnostics.fail.json`: Synthetic diagnostics failure example.

## Scope

These fixtures are metadata only. They do not include calculator logic,
generated code, production outputs, patient data, or licensed payloads.

The request and response shapes are aligned to the public calculator contract
and describe transport-specific fields for the MATLAB interop binding surface
only.

## Rules

- Keep all committed examples synthetic.
- Mirror the public calculator contract fields explicitly.
- Prefer file-import (CSV/Parquet/MAT) and CLI-invocation for primary paths;
  use C ABI MEX only when in-process execution with MATLAB toolchain matching
  is required.
- Keep diagnostics, provenance, and errors explicit and machine readable.
- Keep fixture gates local-only and user-supplied.
- Do not embed formula logic or duplicate calculator rules in the MATLAB
  interop binding contract.
