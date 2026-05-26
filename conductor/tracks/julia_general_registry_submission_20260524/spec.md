# Julia General Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Julia`
- Registry: `General registry`
- Package candidate: `NationalWeightedActivityUnitWrapper`
- Version candidate: `0.1.0`
- Local surface: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/Project.toml`
- Current status: `replacement_submitted_pending_general_automerge_stopwatch`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Reviewer feedback converged on abandoning `NwauCore` because the `Core` suffix
was misleading for a thin wrapper. The active replacement package is
`NationalWeightedActivityUnitWrapper v0.1.0` in
`https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`.
`Pkg.instantiate()` and `Pkg.test()` passed locally, tag `v0.1.0` points to
commit `56ddec5ae29513e80717d4625f82c024a211c949`, and Registrator opened
General PR `https://github.com/JuliaRegistries/General/pull/156254`.
Registry consistency, treecheck, AutoMerge, and AutoMerge-stopwatch checks pass
on the replacement General PR; the remaining blocker is General merge and
public registry propagation.

The superseded PRs `#156236`, `#156235`, and `#156200` are closed. Reviewer
clarification on the replacement PR was answered with `[noblock]`, confirming
that "National" refers to Australia's National Weighted Activity Unit context.

## Preparation Evidence

- Public registry discovery: `https://juliahub.com/api/packages/NationalWeightedActivityUnitWrapper` has no confirmed public listing before General merge.
- Test command: `julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.test()'`
- Test result: `NationalWeightedActivityUnitWrapper` tests passed with command assembly and missing input guard testsets.
- License: MIT license present in the Julia package top-level folder.
- Feedback addressed: package name is `NationalWeightedActivityUnitWrapper`, public repository is `NationalWeightedActivityUnitWrapper.jl`, and tag `v0.1.0` points to `56ddec5ae29513e80717d4625f82c024a211c949`.
- Remaining external blocker: General merge and public registry propagation.

## Submission Evidence

- Repository: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Tag: `v0.1.0`
- Commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- UUID: `58dad789-f56a-4ab3-a66f-c15139bf9cbe`
- Registrator trigger issue: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`
- General registry PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156236`, `https://github.com/JuliaRegistries/General/pull/156235`, `https://github.com/JuliaRegistries/General/pull/156200`
- State: open, registry consistency, treecheck, AutoMerge, and AutoMerge-stopwatch checks passing; merge and propagation pending.
- Release notes comment: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1#issuecomment-4535380457`
- Registrator update confirmation: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1#issuecomment-4535381791`
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
