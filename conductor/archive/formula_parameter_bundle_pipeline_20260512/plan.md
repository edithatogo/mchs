# Plan: Formula and Parameter Bundle Pipeline

## Phase 1: Bundle Format
- [x] Task: Define formula and parameter bundle schema, including weights, thresholds, adjustments, formulas, provenance, validation evidence, explicit gap records, and stable serialization for reviewable diffs.
- [x] Task: Preserve source-discovered gap records for price-weight and adjustment extraction until they are closed by fixture evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Bundle Format' (Protocol in workflow.md)

## Phase 2: Extraction and Loading
- [x] Task: Implement extraction and bundle loading for one stream/year canary.
- [x] Task: Add tests for extracted values and bundle-loaded calculator behavior.
- [x] Task: Preserve source references to SAS lines, workbook sheets, or source tables where practical.
- [x] Task: Use the 2026 manifest and add-year source-scanner fixture as the first evidence pair.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Extraction and Loading' (Protocol in workflow.md)

## Phase 3: Future-Year Workflow Docs
- [x] Task: Document the end-to-end future formula incorporation workflow.
- [x] Task: Link source scanning, manifests, bundles, validation gates, and year diffs.
- [x] Task: Add a maintainer checklist for new IHACPA releases.
- [x] Task: Document the explicit gap policy for price-weight and adjustment extraction.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Future-Year Workflow Docs' (Protocol in workflow.md)
