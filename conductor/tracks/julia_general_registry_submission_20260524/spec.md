# Julia General Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Julia`
- Registry: `General registry`
- Package candidate: `NwauCore`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/julia-binding/Project.toml`
- Current status: `submitted_pending_general_merge`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally and resubmitted to Registrator after AutoMerge feedback on the previous PRs. `Pkg.instantiate()` and `Pkg.test()` passed for `NwauCore v0.1.0`, a dedicated public repository exists at `https://github.com/edithatogo/NwauCore.jl`, tag `v0.1.0` points to corrected commit `99da36f0b417fe89060d6dbc649783265303d563`, and a Registrator trigger issue is open. Registry consistency and treecheck now pass on the replacement General PR; the remaining blocker is merge and public registry propagation.

## Preparation Evidence

- Public registry discovery: `https://juliahub.com/api/packages/NwauCore` returned `404 Not Found`.
- Test command: `julia --project=microcosting_healthservices/julia-binding -e 'using Pkg; Pkg.instantiate(); Pkg.test()'`
- Test result: `NwauCore tests passed`
- License: MIT license present in the Julia package top-level folder.
- Feedback addressed: package name is `NwauCore`, public repository is `NwauCore.jl`, and tag `v0.1.0` was moved to the corrected commit.
- Remaining external blocker: General AutoMerge new-package stopwatch/review.

## Submission Evidence

- Repository: `https://github.com/edithatogo/NwauCore.jl`
- Tag: `v0.1.0`
- Registrator trigger issue: `https://github.com/edithatogo/NwauCore.jl/issues/1`
- General registry PR: `https://github.com/JuliaRegistries/General/pull/156236`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156200`, `https://github.com/JuliaRegistries/General/pull/156235`
- State: open, mergeable, registry consistency and treecheck passing, AutoMerge approved; waiting for merge and public registry propagation.
- Release notes comment: `https://github.com/edithatogo/NwauCore.jl/issues/1#issuecomment-4533258242`
- Registrator update confirmation: `https://github.com/edithatogo/NwauCore.jl/issues/1#issuecomment-4533259247`
- TagBot workflow: `https://github.com/edithatogo/NwauCore.jl/blob/main/.github/workflows/TagBot.yml`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
