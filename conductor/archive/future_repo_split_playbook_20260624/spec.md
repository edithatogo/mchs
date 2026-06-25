# Specification: Future Repo Split Playbook

## Overview

Define the criteria and procedure for extracting a package surface from the
monorepo only when it is objectively safer than keeping it in the canonical
repository. The default remains monorepo governance for thin bindings and shared
contracts.

## Functional Requirements

- Define split eligibility criteria based on registry requirements, independent
  release cadence, CI burden, ownership, and external ecosystem norms.
- Require source and contract ownership before extraction.
- Require history-preserving extraction using `git subtree split` or an
  equivalent audited method.
- Require registry continuity, version continuity, CI proof, documentation
  redirects, and rollback instructions.
- Require a post-split compatibility contract so the extracted repo remains a
  thin adapter over the shared core.

## Non-Functional Requirements

- Do not split repos to hide scaffolds or failing tests.
- Do not duplicate calculator formula logic in extracted repos.
- Keep all public claims evidence-backed after extraction.

## Acceptance Criteria

- `conductor/future-repo-split-playbook.md` defines eligibility, extraction,
  validation, and rollback.
- The package surface registry can mark a surface as monorepo, externalized, or
  split-candidate.
- Tests verify the playbook requires history preservation and registry
  continuity.

## Out of Scope

- Performing a repo split now.
- Creating external GitHub repositories.
- Changing package publication credentials.
