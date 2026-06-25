# Plan: Worktree, Branch, and PR Hygiene

## Phase 1: Workflow Policy

- [x] Task: Define clean-worktree workflow.
    - [x] Start rescue work from a clean temporary worktree.
    - [x] Apply only one focused source slice.
    - [x] Validate and push the slice before moving to the next one.
- [x] Task: Define branch and push policy.
    - [x] Use `codex/` branch prefixes for new work.
    - [x] Use `--force-with-lease` only for owned branch updates.
    - [x] Avoid broad dirty branch merges.
- [x] Task: Conductor - User Manual Verification 'Workflow Policy' (Protocol in workflow.md)

## Phase 2: Subagent Handoffs

- [x] Task: Define subagent boundaries.
    - [x] Assign disjoint write scopes.
    - [x] Require validation evidence and residual risk notes.
    - [x] Require external gates to be named separately from local readiness.
- [x] Task: Conductor - User Manual Verification 'Subagent Handoffs' (Protocol in workflow.md)

## Phase 3: CI and Publication Evidence

- [x] Task: Define publication readiness.
    - [x] Require GitHub Actions status before marking a PR slice complete.
    - [x] Attach registry evidence only after public proof exists.
    - [x] Record manual gates without treating them as local failures.
- [x] Task: Conductor - User Manual Verification 'CI and Publication Evidence' (Protocol in workflow.md)
