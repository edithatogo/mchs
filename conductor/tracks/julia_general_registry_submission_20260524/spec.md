# Julia General Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Julia`
- Registry: `General registry`
- Package candidate: `NationalWeightedActivityUnitWrapper`
- Version candidate: `0.1.0`
- Local surface: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Current status: `replacement_registration_submitted_pending_general_checks_review_and_automerge_wait`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

The earlier `NwauCore` registration was abandoned after Julia General reviewer feedback that the `Core` suffix and acronym-style package name were misleading for a thin wrapper. A replacement public package repository now exists at `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`, tag `v0.1.0` points at commit `56ddec5ae29513e80717d4625f82c024a211c949`, `Pkg.instantiate()` and `Pkg.test()` passed, and Registrator opened replacement General PR `https://github.com/JuliaRegistries/General/pull/156254`. The remaining blocker is external: General checks/review, AutoMerge waiting period, merge, and public registry propagation.

## Preparation Evidence

- Public registry discovery: `https://juliahub.com/api/packages/NationalWeightedActivityUnitWrapper` returned `404 Not Found` before General merge.
- Test command: `julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.test()'` in `/tmp/NationalWeightedActivityUnitWrapper.jl`.
- Test result: `NationalWeightedActivityUnitWrapper tests passed` with two passing testsets.
- License: MIT license present in the Julia package top-level folder.
- Feedback addressed: reviewers on General PR `https://github.com/JuliaRegistries/General/pull/156236` said `NwauCore` / `Core` was misleading; replacement package uses the descriptive `NationalWeightedActivityUnitWrapper` name.
- Remaining external blocker: General checks/review, AutoMerge new-package stopwatch, merge, and public registry propagation.

## Submission Evidence

- Repository: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Tag: `v0.1.0`
- Commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- Registrator trigger issue: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`
- Registrator confirmation: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1#issuecomment-4535378120`
- Release notes comment: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1#issuecomment-4535380457`
- General registry PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Superseded naming PR: `https://github.com/JuliaRegistries/General/pull/156236`
- State: open; checks running and AutoMerge stopwatch/review pending. Publication is not claimed.
- TagBot workflow: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/blob/main/.github/workflows/TagBot.yml`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
