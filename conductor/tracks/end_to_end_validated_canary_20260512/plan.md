# Plan: End-to-End Validated Canary

## Phase 1: Canary Selection and Source Bundle [checkpoint: 55333c7]
- [x] Task: Select stream/year and assemble source manifest.
    - [x] Confirm SAS and Excel source availability or explicit gaps.
    - [x] Record URLs, hashes, retrieval dates, and source authority.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Canary Selection and Source Bundle' (Protocol in workflow.md)

## Phase 2: Formula and Fixture Evidence [checkpoint: 55333c7]
- [x] Task: Extract formula/parameter bundle and create parity evidence.
    - [x] Record SAS parity and Excel formula parity.
    - [x] Add fixture parity report with tolerance and rounding policy.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Formula and Fixture Evidence' (Protocol in workflow.md)

## Phase 3: Cross-Engine Canary [checkpoint: 55333c7]
- [x] Task: Validate Python baseline, Rust canary, and CLI/Arrow output.
    - [x] Run shared fixtures across surfaces.
    - [x] Record conformance results and residual caveats.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Cross-Engine Canary' (Protocol in workflow.md)

## Phase 4: Documentation and Template Extraction [checkpoint: 55333c7]
- [x] Task: Publish canary lifecycle docs and future-year template guidance.
    - [x] Add Starlight docs page.
    - [x] Convert lessons into reusable implementation checklist.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Documentation and Template Extraction' (Protocol in workflow.md)

## Phase 5: Complete-with-Gaps Closeout
- [x] Task: Record bounded canary lifecycle closeout. [89f40d9]
    - [x] Add machine-readable canary lifecycle evidence.
    - [x] Commit Starlight docs page and reusable template guidance.
    - [x] Keep official SAS and Excel workbook-output parity as explicit gaps.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 5: Complete-with-Gaps Closeout' (Protocol in workflow.md) [14652bf]
