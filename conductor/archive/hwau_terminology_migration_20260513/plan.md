# Plan: HWAU Terminology Migration

## Phase 1: Terminology Contract
- [x] Task: Define HWAU and NWAU terminology rules.
    - [x] Add HWAU as the generic schema field.
    - [x] Add NWAU as Australian source terminology and compatibility alias.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Terminology Contract' (Protocol in workflow.md) [checkpoint: archived]

## Phase 2: Documentation and Compatibility
- [x] Task: Update docs and examples.
    - [x] Explain HWAU versus NWAU.
    - [x] Preserve Australian examples that use NWAU source terminology.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Documentation and Compatibility' (Protocol in workflow.md) [checkpoint: archived]

## Phase 3: Tests and Migration Guards
- [x] Task: Add alias and compatibility tests.
    - [x] Assert HWAU is generic.
    - [x] Assert NWAU is source-specific.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Tests and Migration Guards' (Protocol in workflow.md) [checkpoint: archived]

## Phase 4: Runtime and Schema Alias Evidence
- [x] Task: Add a shared runtime helper that normalizes `hwau`/`nwau` result aliases and rejects conflicting values.
- [x] Task: Update public HTTP API and OpenAI adapter examples to expose generic `hwau` while preserving the Australian `nwau` compatibility alias.
- [x] Task: Add focused tests for runtime alias behavior, public contract examples, OpenAPI schema wording, metadata evidence, and archived registry status.
- [x] Task: Update metadata.json with completion policy, archive evidence, partially resolved alias-test gap, and bounded complete-with-gaps scope.
- [x] Task: Update conductor/tracks.md so the archived track is marked complete instead of in progress.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Runtime and Schema Alias Evidence' (Protocol in workflow.md) [checkpoint: repaired]
