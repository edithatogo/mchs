# MATLAB File Exchange Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `MATLAB`
- Registry: `MATLAB File Exchange`
- Package candidate: `mchs-matlab-interop`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/matlab`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved. A File Exchange source upload bundle exists for the MATLAB file/CLI interop adapter and was published on MathWorks File Exchange as version `0.1.0`. MATLAB/Octave are not installed locally, so no MATLAB runtime validation is claimed.

## Preparation Evidence

- Discovery: MathWorks File Exchange exact-title search for `"MCHS MATLAB Interop"` was probed on 2026-06-12 before publication. A direct CLI fetch returned HTTP 200 and displayed that the search did not match any add-ons; subsequent scripted live probes may return Akamai HTTP 403.
- Bundle: `microcosting_healthservices/bindings/matlab/mchs-matlab-interop-0.1.0.zip`
- SHA256: `d78cc11a9ab23080b38604e21c5d21ba9c8801ae0cf6219888f1797834cf2336`
- Contents: `README.md`, `LICENSE`, `file-exchange-submission.json`, `matlab-interop-notes.md`, `mchs/*.m`, `examples/*.m`
- Runtime note: MATLAB and Octave are not installed locally.
- Publication evidence: `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop` was published and directly observed in Chrome on 2026-06-13; the page title was `MCHS MATLAB Interop - File Exchange - MATLAB Central`, the page stated `Your submission has been published in File Exchange`, and the page exposed version `0.1.0`, add-on id `184067`, add-on UUID `91133d3e-f475-413c-85bc-544188a60074`, author Dylan, and tags `cli`, `csv`, `health economics`, `matlab`, `microcosting`, and `parquet`.
- Archive note: the original uploaded archive SHA-256 was `1156f506cda8ab797b5d07adebc35ecccb36bd9758cffaf011029c71c9d2515a`; after publication, the local bundle was corrected so README and metadata no longer say no File Exchange upload occurred, producing SHA-256 `d78cc11a9ab23080b38604e21c5d21ba9c8801ae0cf6219888f1797834cf2336`. A new-version draft exists at `https://www.mathworks.com/contribute/submissions/aaea44a8-4710-4e2c-a17d-a97aede040de/edit`, but no corrected replacement publication is claimed because the browser automation backend could not complete a trusted replacement ZIP upload.
- Remaining external blocker: none for File Exchange publication.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
