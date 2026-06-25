# Plan: SQL and DuckDB Historical Boundary

## Phase 1: Reclassification
- [x] Task: Reconcile the SQL/DuckDB track with current governance.
    - [x] Confirm support matrix classifies SQL/DuckDB as `historical`.
    - [x] Confirm `conductor/tracks.md` says not to develop SQL/DuckDB as an
      active surface.
    - [x] Confirm no `contracts/sql-duckdb/` or DuckDB binding folder exists.
    - [x] Remove readiness claims for DuckDB prototypes, examples, fixtures, or
      tests from this track.

## Phase 2: Future Reopen Gate
- [x] Task: Record that reopening requires accountable audience, owner, and evidence case.
    - [x] Require a concrete read/query file-boundary adapter over pre-computed
      CLI/file outputs before any future implementation.
    - [x] Require a `contracts/sql-duckdb/` contract bundle before claiming
      adapter readiness.
    - [x] Require SQL/DuckDB fixture tests that read shared outputs without
      formula, classifier, grouper, or parameter logic in SQL.
    - [x] Require support matrix status to remain `historical` until those
      gates exist.
