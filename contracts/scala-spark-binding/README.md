# Scala/Spark binding contract fixtures

This directory contains synthetic metadata-only fixtures for the Scala/Spark
binding workstream.

## Contents

- `scala-spark-binding.schema.json`: JSON Schema for the Scala/Spark binding
  contract bundle.
- `scala-spark-binding.contract.json`: Contract document describing request
  and response structs, service, file-exchange (Parquet/Arrow), and SQL
  boundaries, diagnostics, provenance, errors, fixture gates, and module
  readiness.
- `examples/parquet-file.pass.json`: Synthetic Parquet file-exchange primary
  pass example.
- `examples/service.pass.json`: Synthetic service-bound fallback pass example.
- `examples/sql-boundary.pass.json`: Synthetic SQL boundary pass example.
- `examples/binding.fail.json`: Synthetic binding failure example.
- `examples/diagnostics.fail.json`: Synthetic diagnostics failure example.

## Scope

These fixtures are metadata only. They do not include calculator logic,
generated code, production outputs, patient data, or licensed payloads.

The request and response shapes are aligned to the public calculator contract
and describe transport-specific fields for the Scala/Spark binding surface only.

## Rules

- Keep all committed examples synthetic.
- Mirror the public calculator contract fields explicitly.
- Prefer Parquet/Arrow file exchange for batch and lakehouse workloads; use the
  service boundary for online queries; use SQL/DuckDB for analytical workflows.
- Keep diagnostics, provenance, and errors explicit and machine readable.
- Keep fixture gates local-only and user-supplied.
- Do not embed formula logic or duplicate calculator rules in the Scala/Spark
  binding contract.
