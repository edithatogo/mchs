# MATLAB File Exchange Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `MATLAB`
- Registry: `MATLAB File Exchange`
- Package candidate: `mchs-matlab-interop`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/matlab`
- Current status: `prepared_pending_file_exchange_upload_review`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. A File Exchange source upload bundle exists for the MATLAB file/CLI interop adapter. MATLAB/Octave are not installed locally, so no MATLAB runtime validation is claimed. The remaining blocker is external: MathWorks account upload and File Exchange review.

## Preparation Evidence

- Discovery: MathWorks File Exchange search page for `mchs-matlab-interop` was reachable from CLI, but no authenticated listing/API proof was available.
- Bundle: `microcosting_healthservices/bindings/matlab/mchs-matlab-interop-0.1.0.zip`
- SHA256: `1156f506cda8ab797b5d07adebc35ecccb36bd9758cffaf011029c71c9d2515a`
- Contents: `README.md`, `LICENSE`, `file-exchange-submission.json`, `matlab-interop-notes.md`, `mchs/*.m`, `examples/*.m`
- Runtime note: MATLAB and Octave are not installed locally.
- Remaining external blocker: MathWorks File Exchange upload/review.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
