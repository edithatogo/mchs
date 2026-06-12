# Stata SSC Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Stata`
- Registry: `SSC / Stata package distribution`
- Package candidate: `mchs-stata-interop`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/stata`
- Current status: `submitted_pending_ssc_maintainer_review`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. A Stata ado/help/pkg bundle exists with README, license, notes, and examples for maintainer review. No Stata executable is installed locally, so no ado runtime validation is claimed. The remaining blocker is external SSC maintainer submission and review.

## Preparation Evidence

- Discovery: IDEAS/RePEc search page for `mchs-stata-interop` was reachable from CLI, but no clean machine-readable SSC publication proof was available.
- Bundle: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`
- SHA256: `58592db4e6feb5bdfc78a3fd34b91e0e86f859dc06de5fdf40cd7a8f2a7b0ffd`
- Contents: `mchs.ado`, `mchs.sthlp`, `pkg-mchs.pkg`, `README.md`, `LICENSE`, `examples/*.do`, `stata-interop-notes.md`
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
