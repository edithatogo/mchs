# Specification: Worktree, Branch, and PR Hygiene

## Overview

Define the operational workflow for cleaning and publishing changes from a noisy
local tree. The policy should make clean temporary worktrees, minimal commits,
subagent boundaries, CI verification, and external gate reporting the default
for MCHS.

## Functional Requirements

- Prefer clean temporary worktrees based on current `origin/master` for PR
  rescue and focused publication work.
- Require minimal branch slices with one topic and one evidence boundary.
- Require branch names to use the `codex/` prefix unless a PR or registry gate
  requires an existing branch.
- Require pushes to use safe non-interactive commands and avoid force updates
  except `--force-with-lease` on owned branches.
- Require subagent handoffs to name owned files, validations, residual risks,
  and external blockers.
- Require local completion and registry/admin/reviewer gates to be reported
  separately.

## Non-Functional Requirements

- Do not merge broad dirty branches into clean PR branches.
- Do not revert user work while cleaning generated artifacts.
- Keep CI proof attached to the smallest practical change slice.

## Acceptance Criteria

- `conductor/worktree-branch-pr-hygiene.md` documents the policy.
- Tests verify the policy mentions clean temporary worktrees and
  `--force-with-lease`.
- Track plans reference the phase completion protocol.

## Out of Scope

- Creating or pushing branches in this setup slice.
- Rewriting existing PR history.
- Resolving external reviewer comments.
