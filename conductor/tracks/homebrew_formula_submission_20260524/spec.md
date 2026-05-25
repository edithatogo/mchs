# Homebrew Formula Submission

## Overview

Track discovery, local preparation, submission, and publication evidence for the Homebrew tap/core registry without overclaiming publication.

## Registry

- Ecosystem: `Homebrew`
- Registry: `Homebrew tap/core`
- Package candidate: `nwau-py`
- Version candidate: `0.2.2`
- Local surface: `pyproject.toml`
- Current status: `submitted_pending_homebrew_core_review_tap_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for existing package/version evidence.
- Record absence, submission, or publication evidence in the language registry contract.
- Prepare registry-specific metadata or artifacts only from committed package surfaces.
- Submit only through an authenticated, authorized publisher account or upstream review workflow.
- Keep external legal, credential, maintainer-review, and propagation blockers explicit.

## Current Blocker

Personal Homebrew tap is published and verified with audit, source install, and brew test passing; Homebrew/core publication still requires upstream PR/review.

## Evidence

- Submission URL: https://github.com/edithatogo/homebrew-mchs
- Contract source: `contracts/language-registry-submissions/language-registry-submissions.contract.json`
- External gate roadmap: `docs/roadmaps/language-registry-external-gates.md`

## Acceptance Criteria

- Track context exists for the contract's `homebrew_formula_submission_20260524` reference.
- Current status and blocker language match the checked-in language registry contract.
- Publication is claimed only when public registry evidence verifies the target version.

## Out of Scope

- Accepting CLAs, publisher agreements, or legal terms on behalf of a contributor.
- Inventing credentials, namespace ownership, API keys, or registry maintainer approval.
- Claiming publication from local artifacts alone.
