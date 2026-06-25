# Julia General Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Julia`
- Registry: `General registry`
- Package candidate: `NationalWeightedActivityUnitWrapper`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/julia-binding/Project.toml`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

`NationalWeightedActivityUnitWrapper` was submitted through Julia General PR `https://github.com/JuliaRegistries/General/pull/156254`. Checks were successful for PR head `bb63b2a81ec2ded2c5675f09fb6cd63128f10a07`, and the PR merged on `2026-05-28T15:34:44Z`. Publication is now verified by the accepted registry merge. The earlier `NwauCore v0.1.0` Registrator PR remains recorded as superseded evidence: PR `https://github.com/JuliaRegistries/General/pull/156236` is open/unmerged, but reviewer follow-up says it is not intended to merge because the `NwauCore`/`Core` name is misleading.

## Preparation Evidence

- Public registry discovery: `https://juliahub.com/api/packages/NationalWeightedActivityUnitWrapper` returned `404 Not Found`.
- Superseded package discovery: `https://juliahub.com/api/packages/NwauCore` returned `404 Not Found`.
- Test command: `julia --project=microcosting_healthservices/julia-binding -e 'using Pkg; Pkg.instantiate(); Pkg.test()'`
- Test result: existing Julia binding tests passed before the replacement registration rename; this evidence pass intentionally did not edit `julia-binding` files.
- License: MIT license present in the Julia package top-level folder.
- Active repository: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Active tag: `v0.1.0`
- Active commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- Package UUID: `58dad789-f56a-4ab3-a66f-c15139bf9cbe`
- Earlier superseded feedback addressed: package name was moved to `NwauCore`, public repository is `NwauCore.jl`, and tag `v0.1.0` was moved to the corrected commit.
- Current live review blocker: reviewer feedback accepted replacing `NwauCore` with `NationalWeightedActivityUnitWrapper`; PR `#156236` is superseded and not expected to merge.

## Submission Evidence

- Replacement package candidate: `NationalWeightedActivityUnitWrapper`
- Replacement payload state: published via General merge.
- Active repository: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Active Registrator trigger issue: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`
- Active General registry PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Active PR head: `bb63b2a81ec2ded2c5675f09fb6cd63128f10a07`
- Active commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- Active tag: `v0.1.0`
- Package UUID: `58dad789-f56a-4ab3-a66f-c15139bf9cbe`
- Active state: published/verified by the accepted General merge; checks successful.
- Superseded repository: `https://github.com/edithatogo/NwauCore.jl`
- Tag: `v0.1.0`
- Superseded Registrator trigger issue: `https://github.com/edithatogo/NwauCore.jl/issues/1`
- Superseded General registry PR: `https://github.com/JuliaRegistries/General/pull/156236`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156200`, `https://github.com/JuliaRegistries/General/pull/156235`
- Superseded state: `NwauCore` PR is superseded/not expected to merge.
- Release notes comment: `https://github.com/edithatogo/NwauCore.jl/issues/1#issuecomment-4533258242`
- Registrator update confirmation: `https://github.com/edithatogo/NwauCore.jl/issues/1#issuecomment-4533259247`
- TagBot workflow: `https://github.com/edithatogo/NwauCore.jl/blob/main/.github/workflows/TagBot.yml`
- Rename response: `https://github.com/JuliaRegistries/General/pull/156236#issuecomment-4534823787`
- Reviewer follow-up: `https://github.com/JuliaRegistries/General/pull/156236#issuecomment-4534836505`

## Publication Evidence

- General PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Merged at: `2026-05-28T15:34:44Z`
- Verification note: accepted registry merge is the authoritative publication evidence for this package.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
