# Worktree, Branch, and PR Hygiene

## Default Workflow

For noisy or long-running work, start from a clean temporary worktree based on
current `origin/master`, apply one focused source slice, validate it, commit it,
push it, and then move to the next slice.

## Branch Rules

- Use the `codex/` prefix for new branches unless continuing an existing PR
  branch or registry-required branch.
- Keep one topic per branch.
- Do not merge broad dirty branches into focused PR branches.
- Use `--force-with-lease` only on branches owned by the current task.
- Never revert unrelated user changes while cleaning generated artifacts.

## PR Rules

- Each PR should have a clear local completion boundary.
- CI must pass or the residual failures must be named with exact blockers.
- external registry, reviewer, account, or maintainer gates are not local code
  completion.
- Registry claims require public evidence links or explicitly submitted states.

## Subagent Handoff Rules

Subagent handoffs must state owned files, out-of-scope areas, validation
commands, changed files, docs touched, review findings, residual risks, and
external blockers. Delegated work must not mark scaffolds complete without
implementation and evidence.
