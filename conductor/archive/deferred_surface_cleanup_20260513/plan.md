# Plan: Deferred Surface Cleanup

## Phase 1: Inventory
- [x] Task: Inventory deferred surface artefacts.
    - [x] Scala/Spark.
    - [x] Swift.
    - [x] Go.
    - [x] MATLAB.
    - [x] SQL/DuckDB.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Inventory' (Protocol in workflow.md)

## Phase 2: Policy Decision
- [x] Task: Decide keep, quarantine, or remove.
    - [x] Keep Stata and Julia if valid.
    - [x] Keep no-new-development artefacts only if they do not affect CI.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Policy Decision' (Protocol in workflow.md)

## Phase 3: Cleanup
- [x] Task: Apply cleanup.
    - [x] Remove or quarantine generated artefacts if needed.
    - [x] Update tests and docs to reflect deferred status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Cleanup' (Protocol in workflow.md)
