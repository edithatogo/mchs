# Track Template: Repository Publication and SOTA Audit

Use this template to create a recurring audit track for local and remote repository completeness: branches, PRs, CI, Pages, homepage, packages, releases, tags, dependency currency, publication, docs quality, examples, and tutorials.

## Template Variables

- `TRACK_ID`: `repository_publication_sota_audit_<YYYYMMDD>`
- `TRACK_TITLE`: `Repository Publication and SOTA Audit`
- `AUDIT_DATE`: `<YYYY-MM-DD>`
- `REMOTE`: `<owner/repo>`
- `AUDITOR`: `<name or role>`
- `TRACK_STATUS`: `new` for a created track, or another valid lifecycle status

## metadata.json

```json
{
  "track_id": "TRACK_ID",
  "type": "chore",
  "status": "TRACK_STATUS",
  "track_class": "audit",
  "current_state": "roadmap-only",
  "primary_contract": "repository publication and SOTA audit report",
  "dependencies": [
    "GitHub repository state",
    "package registry state",
    "conductor/roadmap-governance.md"
  ],
  "completion_evidence": [
    "branch and PR findings",
    "CI and publication status table",
    "dependency/tooling recommendations",
    "remediation backlog"
  ],
  "publication_status": "not-applicable",
  "created_at": "AUDIT_DATET00:00:00Z",
  "updated_at": "AUDIT_DATET00:00:00Z",
  "description": "Audit local and remote repository completeness, publication state, SOTA dependencies, docs, examples, and release/package health for REMOTE."
}
```

## spec.md

```markdown
# Specification: TRACK_TITLE

## Overview
Audit the local and remote repository to determine whether it is complete, current, published, and professionally maintained. The audit should include branches, PRs, dependency automation, CI, security, GitHub Pages, homepage metadata, releases, tags, package registries, docs, examples, tutorials, and dependency/library modernization opportunities.

## Audit Questions
- Are all local and remote branches merged or intentionally retained?
- Are Renovate, Dependabot, security, or release PRs open, failing, blocked, or stale?
- Are CI workflows passing on the default branch and on active PRs?
- Is GitHub Pages deployed, complete, linked from the repo homepage, and free of stale repo names or broken links?
- Is the GitHub homepage complete: description, URL, topics, README badges, citation, license, releases, packages, security, and social preview where applicable?
- Are tags, GitHub releases, PyPI, conda-forge, GitHub Packages, npm/WASM, crates.io, NuGet, or other package targets correctly published or clearly marked future-only?
- Are package versions synchronized across source metadata, tags, releases, docs, and registries?
- Are dependencies, GitHub Actions, docs tooling, linting/type/security tools, and packaging tools current and SOTA?
- Are governance documents, validation vocabulary, and recurring audit templates current enough for the size of the roadmap?
- Are better/new libraries warranted for typing, validation, docs, packaging, scientific Python, Rust, bindings, dataframes, Arrow, security, or CI?
- Are new examples, tutorials, notebooks, costing-study guides, or API docs warranted?

## Required Evidence
- Local branch list, remote branch list, and merge status.
- Open/closed PRs from Renovate, Dependabot, and maintainers.
- Latest workflow runs and failing logs where relevant.
- GitHub repo metadata, Pages status, releases, tags, package registry pages, and security settings.
- Package metadata from `pyproject.toml`, conda recipe, Rust crates, docs site package files, and future language package manifests.
- Dependency update review using package manager metadata, official docs, and current release notes where needed.
- Documentation completeness review for README, docs site, examples, tutorials, API references, and roadmap pages.

## Acceptance Criteria
- All branches and PRs are classified as merged, pending, intentionally retained, or requiring action.
- Publication status is explicit for GitHub Release, PyPI, conda-forge, Pages, and future package registries.
- Version/tag/release/package metadata is consistent or follow-up tasks exist.
- Dependency and tooling modernization recommendations are recorded with rationale.
- Docs/homepage/tutorial gaps are fixed or turned into tracks.
- Security and repo settings gaps are fixed or turned into tracks.

## Out of Scope
- Blindly upgrading dependencies without reviewing calculator-risk implications.
- Publishing to registries that require unavailable credentials or unapproved release decisions.
```

## plan.md

```markdown
# Plan: TRACK_TITLE

## Phase 1: Branch, PR, and CI Audit
- [ ] Task: Audit local branches, remote branches, PRs, and CI status.
    - [ ] Classify Renovate/Dependabot PRs and merge readiness.
    - [ ] Identify stale branches, unmerged work, failing workflows, and blocked checks.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Branch, PR, and CI Audit' (Protocol in workflow.md)

## Phase 2: Publication and Repository Metadata Audit
- [ ] Task: Audit GitHub homepage, Pages, releases, tags, packages, and security settings.
    - [ ] Verify description, homepage, topics, README badges, citation, license, releases, tags, and package registry links.
    - [ ] Verify PyPI, conda-forge, GitHub Releases, GitHub Pages, and future registry status.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Publication and Repository Metadata Audit' (Protocol in workflow.md)

## Phase 3: SOTA Dependency and Tooling Review
- [ ] Task: Review package, workflow, docs, security, linting, typing, and scientific/data tooling currency.
    - [ ] Evaluate whether packages/actions/tools should be updated, replaced, pinned, or held.
    - [ ] Record calculator-risk implications for dependency updates.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: SOTA Dependency and Tooling Review' (Protocol in workflow.md)

## Phase 4: Docs, Examples, and Tutorial Completeness
- [ ] Task: Audit documentation, examples, notebooks, tutorials, API reference, and roadmap pages.
    - [ ] Identify missing costing-study, classification, package-install, polyglot, and future-year examples.
    - [ ] Fix high-confidence stale links and create tracks for larger content gaps.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Docs, Examples, and Tutorial Completeness' (Protocol in workflow.md)

## Phase 5: Remediation and Release Readiness
- [ ] Task: Apply safe fixes and create follow-up tracks for remaining gaps.
    - [ ] Merge safe dependency PRs where checks pass and risk is low.
    - [ ] Update versions, tags, releases, or docs only when evidence supports the claim.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 5: Remediation and Release Readiness' (Protocol in workflow.md)
```
