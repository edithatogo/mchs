# Specification: SQL and DuckDB Historical Boundary

## Overview
Retain the SQL/DuckDB material as historical design context only. Current
governance classifies SQL/DuckDB as a non-active surface with no new
development, no owned contract bundle, and no separate query/runtime adapter.

If a future accountable audience reopens the surface, the only acceptable
shape is a read/query file-boundary adapter over pre-computed CLI/file outputs
such as Parquet or CSV. The SQL layer must not host calculator formula logic,
classifier logic, grouper logic, or pricing-year parameter interpretation.

## Functional Requirements
- Keep prior strategy notes available for traceability.
- Align the track status with the support matrix and roadmap gate:
  `historical` / not ready for implementation.
- Document that there is no current DuckDB extension, SQL UDF, table-valued
  function, or contract bundle.
- Preserve the non-formula boundary rule for any future SQL reprioritisation.

## Acceptance Criteria
- Track metadata and docs do not claim production, preview, fixture, or adapter
  readiness for SQL/DuckDB.
- Static validation confirms SQL/DuckDB remains historical and not ready for
  implementation.
- No formula logic is hand-copied into SQL snippets or described as belonging
  in DuckDB.
