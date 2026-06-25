# Binding Strategy: SQL and DuckDB Historical Boundary

## Decision

Do not build or promote SQL/DuckDB as an active binding surface at this time.
Current governance classifies SQL/DuckDB as `historical`, not ready for
implementation, and without an accountable owner or audience evidence case.

The earlier viable strategy remains useful only as traceability: if the surface
is ever reprioritised, it should be a read/query file-boundary over
pre-computed Parquet or CSV outputs from the CLI/file contract. DuckDB must not
become a calculator runtime or a place where formulas are copied.

## Rationale

- The support matrix marks `surface.sql-duckdb` as `historical` and not ready
  for implementation.
- `conductor/tracks.md` explicitly says not to develop SQL/DuckDB as an active
  surface unless a future evidence-backed audience emerges.
- No `contracts/sql-duckdb/` bundle, DuckDB extension, SQL UDF package, or
  binding folder exists in the repository.
- The active architecture keeps calculator logic in the shared core and uses
  file/service boundaries for downstream consumers.

## Historical contract shape

There is no current SQL/DuckDB contract. The historical design assumption was:

- SQL consumers read already-computed calculator outputs.
- Parquet or CSV files are produced by the CLI/file contract, not by SQL.
- DuckDB is used only for analyst-side aggregation, filtering, and joins.
- Diagnostics and provenance come from the producing CLI/file contract.

### Boundary-only SQL example

```sql
-- Read pre-computed calculator outputs as a Parquet table.
CREATE TABLE acute_results AS
SELECT * FROM read_parquet('outputs/acute_2026_results.parquet');

-- Perform analyst-side aggregation or filtering.
-- No calculator formula logic appears here.
SELECT stream, pricing_year, sum(nwau) AS total_nwau
FROM acute_results
GROUP BY stream, pricing_year;
```

This example is intentionally query-only. It is not a DuckDB adapter, extension,
or fixture validation claim.

## Reopen criteria

Before SQL/DuckDB can move beyond historical status, a future track must add:

- a named audience and accountable owner
- a concrete `contracts/sql-duckdb/` bundle
- fixture validation against shared outputs
- documentation that DuckDB is a read/query consumer over file outputs
- explicit tests proving no formula, classifier, grouper, or parameter logic
  is implemented in SQL

### Limitations

- Complex classifiers and groupers (AR-DRG, UDG, AECC) remain in the shared
  core. DuckDB cannot derive these classifications from raw inputs without
  calling the core.
- DuckDB does not host the calculator runtime. All calculated columns must be
  pre-materialized through the CLI or file contract.
- DuckDB UDFs, extensions, and table-valued functions are out of scope for the
  historical track.

## Versioning

- No separate DuckDB-specific version exists.
- Historical notes should not be treated as a versioned public contract.
- If a future adapter is approved, it must introduce explicit contract
  versioning before readiness is claimed.

## Diagnostics and provenance

- DuckDB consumers get diagnostics from the CLI/file contract (output
  provenance, schema metadata, validation gates).
- SQL-level diagnostics are limited to DuckDB-native file read errors or
  schema mismatches.
- No calculator-level diagnostics are re-exposed in SQL; the consumer must
  inspect the pre-computed output and its provenance record.

## Privacy and synthetic examples

- Do not add PHI, patient-level extracts, or licensed classification tables to
  SQL example files.
- Any future examples must use synthetic fixtures and pass through the
  producing contract's validation gate.

## When to use DuckDB SQL vs. native bindings

If this surface is ever reopened, choose DuckDB SQL only when:
- the consumer is an analyst or data engineer working in SQL-centric tooling
- the workflow is batch or read-only (aggregation, filtering, joining with
  other tables)
- the data volume fits a file-based boundary (Parquet or CSV on disk)

Prefer native bindings or the CLI/file boundary when:
- the consumer needs in-process or low-latency calculator calls
- the workflow requires per-row classification or grouper logic
- the integration surface needs bidirectional typed contracts

## Readiness bar

- This track is historical only. No DuckDB extension, UDF, adapter, or
  SQL/DuckDB contract is being built.
- Do not claim SQL/DuckDB preview, production, or adapter readiness from this
  track.
- Reopening requires new evidence and tests, not reinterpretation of these
  historical notes.
