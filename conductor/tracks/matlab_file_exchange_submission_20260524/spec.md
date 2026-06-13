# MATLAB File Exchange Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `MATLAB`
- Registry: `MATLAB File Exchange`
- Package candidate: `mchs-matlab-interop`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/contracts/matlab-interop-binding`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved and publicly verified. A File Exchange upload bundle exists for the MATLAB interop scaffold, and the public File Exchange listing `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop` returned HTTP 200 with title `MCHS MATLAB Interop - File Exchange - MATLAB Central` on 2026-06-14. MATLAB/Octave are not installed locally, so no MATLAB runtime validation is claimed.

## Preparation Evidence

- Discovery: MathWorks File Exchange search page for `mchs-matlab-interop` was reachable from CLI, but no authenticated listing/API proof was available.
- Bundle: `microcosting_healthservices/bindings/matlab/mchs-matlab-interop-0.1.0.zip`
- SHA256: `7e4b0e628fa72b7f21f133e89d321d64291a8e4c087e34c207c7040610765f3c`
- Contents: `mchs/README.md`, `mchs/validateInput.m`, `mchs/importResultTable.m`, `mchs/invokeCli.m`, `examples/cli_invocation_demo.m`, `examples/file_import_demo.m`, `README.md`, `matlab-interop-notes.md`, `file-exchange-submission.json`
- Runtime note: MATLAB and Octave are not installed locally.
- Publication evidence: `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop` returned HTTP 200 with title `MCHS MATLAB Interop - File Exchange - MATLAB Central` on 2026-06-14.
- Remaining runtime blocker: MATLAB/Octave runtime validation is not claimed because neither runtime is installed locally.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
