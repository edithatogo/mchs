# Subagent Orchestration

## Purpose

This project may use subagents to parallelise research, implementation,
documentation, validation, review, and publication work. Subagents are useful
only when their assignments are bounded, auditable, and integrated back into the
Conductor workflow.

## Supported Model Policy

Subagent model names are execution-environment specific. The orchestration plan
may request model profiles such as:

- `gpt-5.4-mini` for bounded, low-risk tasks such as fixture drafting, docs
  cleanup, straightforward test scaffolding, and localised refactors.
- `gpt-5.4`, `gpt-5.5`, or equivalent frontier models for architecture,
  validation design, security-sensitive changes, and cross-track integration.
- `deepseek-v4` or another external coding/reasoning model only when the local
  runner exposes it and repository policy allows its use.

If a requested model is unavailable, the lead agent must record the fallback
model used and why the fallback is acceptable for the task risk.

## Subagent Roles

Use these roles when delegating:

| Role | Purpose | Typical Output |
| --- | --- | --- |
| `explorer` | Research codebase, docs, external sources, or requirements | findings, source links, gap list |
| `worker` | Implement a bounded file/module slice | code, tests, docs, changed-file list |
| `reviewer` | Review a completed slice against spec, tests, docs, and risks | findings, fixes, residual risks |
| `validator` | Run or design validation evidence and conformance checks | validation report, commands, artifacts |
| `docs` | Create or update documentation and examples | docs pages, tutorials, checked snippets |
| `release` | Inspect publishing, CI, packages, tags, and repo metadata | release/readiness report |

## Delegation Contract

Every subagent assignment must include:

- Track ID and phase.
- Role.
- Model preference and fallback rule.
- Owned files or modules.
- Files or areas explicitly out of scope.
- Required actions: implementation, tests, docs, review, validation, release
  checks, or audit evidence.
- Acceptance criteria.
- Validation commands or evidence required.
- Handoff requirements.
- Instruction not to revert or overwrite work owned by others.

## Required Handoff

Every subagent must report:

- Summary of work completed.
- Files changed or inspected.
- Tests, checks, or validations run.
- Documentation updated.
- Review findings fixed.
- Remaining blockers or risks.
- Recommended next action.

For code-changing tasks, the handoff must explicitly state whether public
contracts, schemas, docs, examples, or validation evidence were updated.

## Multi-Level Delegation

Multi-level delegation is allowed when it reduces coupling and each nested task
has a bounded contract. The lead agent must define a tree of work packages before
delegation:

- Level 0: lead orchestrator owns requirements, design, integration, and final
  release evidence.
- Level 1: coordinators own contract, implementation, validation, docs, release,
  or audit streams.
- Level 2: workers own disjoint files or modules within a stream.
- Level 3+: only use when a worker can safely split independent discovery,
  fixture, docs, or validation subtasks without introducing merge conflicts.

Nested subagents inherit the same evidence obligations as direct subagents. A
subagent may not mark a nested task done without implementation evidence,
validation evidence, docs impact, review findings, and residual risks.

## Anti-Stub Rule

Subagents must not satisfy a task by creating only stubs, fakes, TODOs,
placeholder schemas, empty adapters, mocked-only tests, or aspirational docs.
If a scaffold is the only safe output, the handoff must mark the work
`scaffold-only`, explain what is blocked, and create or recommend a remediation
track.

## Review and Documentation Requirement

Subagents are not done when code compiles. A delegated implementation task is
complete only when it has addressed:

- tests or validation evidence;
- documentation or examples affected by the change;
- type/lint/security implications;
- contract/schema compatibility;
- source/provenance updates if the task touches IHACPA data or validation;
- review findings from `conductor-review` or a reviewer subagent.

If a subagent cannot complete one of these requirements, it must record the gap
and create or recommend a follow-up task.

## Parallelism Rules

- Delegate independent tasks with disjoint write sets.
- Prefer sidecar research, docs, review, or validation tasks that do not block
  the lead agent's next step.
- Do not assign two workers to the same files unless a lead agent explicitly
  coordinates the merge.
- Explorers may run in parallel when they answer different questions.
- Worker tasks must state ownership boundaries.

## Phase-End Automation

At the end of every phase:

1. Subagents hand off their completed work and residual risks.
2. The lead agent integrates outputs.
3. `conductor-review` runs automatically.
4. High-confidence fixes are applied automatically.
5. Narrow validation is rerun.
6. Documentation and evidence are updated.
7. The phase checkpoint is created.
8. The phase changes are committed when the worktree is safe and attributable.
9. Work automatically progresses to the next phase unless blocked.
10. At the end of a track, public-state changes are pushed only after strict
    validation, review evidence, and release/publication gates pass or are
    explicitly gap-recorded.

## Example Assignment

```markdown
Role: worker
Model preference: gpt-5.4-mini; fallback to current default model if unavailable
Track: reference_data_manifest_schema_20260512
Phase: Phase 2
Owned files:
- nwau_py/manifests/
- tests/test_reference_data_manifest.py
Out of scope:
- docs-site/
- release workflows
Required actions:
- Implement typed manifest models.
- Add valid and invalid manifest tests.
- Update docstrings.
- Report whether JSON Schema export is implemented or blocked.
Acceptance criteria:
- Tests cover valid, missing-source, gap-record, and invalid-status cases.
- No calculator formula logic is changed.
Handoff:
- List changed files, validation commands run, docs updated, and residual risks.
```
