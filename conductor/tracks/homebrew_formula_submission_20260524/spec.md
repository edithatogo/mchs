# Homebrew Formula Submission

## Overview

Track discovery, local preparation, submission, and publication evidence for the Homebrew tap/core registry without overclaiming publication.

## Registry

- Ecosystem: `Homebrew`
- Registry: `Homebrew tap/core`
- Package candidate: `nwau-py`
- Version candidate: `0.2.2`
- Local surface: `pyproject.toml`
- Current status: `personal_tap_published_verified_homebrew_core_optional`

## Functional Requirements

- Query the public registry or authoritative submission system for existing package/version evidence.
- Record absence, submission, or publication evidence in the language registry contract.
- Prepare registry-specific metadata or artifacts only from committed package surfaces.
- Submit only through an authenticated, authorized publisher account or upstream review workflow.
- Keep external legal, credential, maintainer-review, and propagation blockers explicit.

## Current Blocker

None for personal tap publication. The personal Homebrew tap is published and verified with audit, source install, `brew test`, and a 2026-06-12 `brew info edithatogo/mchs/nwau-py --json=v2` probe showing stable version `0.2.2`, tap head `fa12ed26c1d6a289b40bf59c9bacbb9a5e42f823`, formula SHA-256 `6f987bc4a81f3ac78cbc893d6a502fc572a534905f9f1f89cfc05600ff4ddff3`, and linked keg `0.2.2`. Homebrew/core publication remains optional and is not claimed.

## Evidence

- Submission URL: https://github.com/edithatogo/homebrew-mchs
- Contract source: `contracts/language-registry-submissions/language-registry-submissions.contract.json`
- External gate roadmap: `docs/roadmaps/language-registry-external-gates.md`

## Acceptance Criteria

- Track context exists for the contract's `homebrew_formula_submission_20260524` reference.
- Current status and blocker language match the checked-in language registry contract.
- Publication is claimed for the public personal tap only when public registry evidence verifies the target version. Homebrew/core publication is not claimed.

## Out of Scope

- Accepting CLAs, publisher agreements, or legal terms on behalf of a contributor.
- Inventing credentials, namespace ownership, API keys, or registry maintainer approval.
- Claiming publication from local artifacts alone.
