# Plan: multilevel agent execution

## Phase 1: Scope and Contract

- [x] Task: Map this track to MoSCoW requirement IDs and design sections.
- [x] Task: Identify the explicit contract, owning files, dependencies, and out-of-scope areas.
- [x] Task: Define positive, negative, and publication evidence required before completion.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Scope and Contract' (Protocol in workflow.md) [checkpoint: archived]

## Phase 2: Parallel Work Packages

- [x] Task: Create subagent work packages with disjoint ownership.
    - [x] Work package A: implementation or policy artifact.
    - [x] Work package B: tests, validation, or audit evidence.
    - [x] Work package C: documentation and examples.
    - [x] Work package D: release, GitHub, or publication checks where applicable.
- [x] Task: Require each subagent handoff to include changed files, validation commands, docs updates, review findings, and residual risks.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Parallel Work Packages' (Protocol in workflow.md) [checkpoint: archived]

## Phase 3: Integration and Evidence

- [x] Task: Integrate subagent outputs and resolve conflicts without overwriting unrelated work.
- [x] Task: Run strict validation or record why a validation is blocked.
- [x] Task: Update Conductor index, tracks registry, docs, and contract references.
- [x] Task: Commit phase evidence and prepare push or release evidence if public state changed.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Integration and Evidence' (Protocol in workflow.md) [checkpoint: archived]

## Phase 4: Archive Repair

- [x] Task: Repair metadata.json to record a governance-only complete-with-gaps scope, completion policy, archive evidence, and explicit handoff-evidence gaps.
- [x] Task: Repair plan.md to preserve phase checkpoints and state the governance-only complete-with-gaps scope.
- [x] Task: Update conductor/tracks.md so the archived track is not left marked in progress.
- [x] Task: Add focused validation for archive metadata, plan checkpoints, subagent orchestration requirements, and archived registry status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Archive Repair' (Protocol in workflow.md) [checkpoint: repaired]
