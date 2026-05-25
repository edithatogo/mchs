# Stata SSC Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Stata`
- Registry: `SSC / Stata package distribution`
- Package candidate: `mchs` (`mchs-stata-interop` bundle)
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/contracts/stata-interop-binding`
- Current status: `prepared_pending_ado_package_review_and_ssc_submission`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. A Stata ado/help/pkg bundle exists and has been packaged. No Stata executable is installed locally, so no ado runtime validation is claimed. The remaining blocker is external SSC maintainer submission and review.

## Preparation Evidence

- Discovery: IDEAS/RePEc search page for `mchs-stata-interop` was reachable from CLI, but no clean machine-readable SSC publication proof was available.
- Bundle: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`
- SHA256: `ba2bb2b43b92c8eda0b20ee7f7de888e69be8e2a0abd3480100db6a216ec6bb2`
- Contents: `mchs.ado`, `mchs.sthlp`, `pkg-mchs.pkg`
- SSC package/install name: `mchs`
- Submission draft: `conductor/tracks/stata_ssc_submission_20260524/ssc-submission-email-draft.md`
- Runtime note: no Stata executable is installed locally.
- Remaining external blocker: SSC submission/review.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
