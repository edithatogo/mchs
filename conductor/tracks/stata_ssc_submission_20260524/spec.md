# Stata SSC Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Stata`
- Registry: `SSC / Stata package distribution`
- Package candidate: `mchs` (`mchs-stata-interop` bundle)
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/contracts/stata-interop-binding`
- Current status: `submitted_pending_ssc_maintainer_review`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. A Stata ado/help/pkg bundle exists and has been packaged. No Stata executable is installed locally, so no ado runtime validation is claimed. The SSC submission email has been sent with the prepared ado/help bundle. The remaining blocker is external SSC maintainer review and public archive publication.

## Preparation Evidence

- Discovery: IDEAS/RePEc search page for `mchs-stata-interop` was reachable from CLI, but no clean machine-readable SSC publication proof was available.
- Bundle: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0-ssc.zip`
- SHA256: `ae0b0adf12aba71dc4e844282bbfcd88bd09b2fd2c2237f565cbc1cfe9d8f225`
- Contents: `mchs.ado`, `mchs.sthlp`
- SSC package/install name: `mchs`
- Submission draft: `conductor/tracks/stata_ssc_submission_20260524/ssc-submission-email-draft.md`
- Runtime note: no Stata executable is installed locally.
- Submission evidence: Gmail sent message id `19e5ffd483ef5841` on thread `19e5ff9a74554b3a` to `baum@bc.edu` with `bindings/stata/mchs-stata-interop-0.1.0-ssc.zip` attached.
- Remaining external blocker: SSC maintainer review and public archive publication.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
