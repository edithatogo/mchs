# Julia General Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Julia`
- Registry: `General registry`
- Package candidate: `NationalWeightedActivityUnitWrapper`
- Version candidate: `0.1.0`
- Local surface: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/Project.toml`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

None. Reviewer feedback converged on abandoning `NwauCore` because the `Core` suffix
was misleading for a thin wrapper. The active replacement package is
`NationalWeightedActivityUnitWrapper v0.1.0` in
`https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`.
`Pkg.instantiate()` and `Pkg.test()` passed locally, tag `v0.1.0` points to
commit `56ddec5ae29513e80717d4625f82c024a211c949`, and Registrator opened
General PR `https://github.com/JuliaRegistries/General/pull/156254`, which
merged on 2026-05-28T15:34:44Z. Julia General raw registry files now verify
`NationalWeightedActivityUnitWrapper v0.1.0` with git-tree-sha1
`bb22d4bd44689549064bd441092fd540b5d852cf`.

The superseded PRs `#156236`, `#156235`, and `#156200` are closed. Reviewer
clarification on the replacement PR was answered with `[noblock]`, confirming
that "National" refers to Australia's National Weighted Activity Unit context.

## Preparation Evidence

- Public registry discovery: JuliaHub still returns 404, but General registry raw files under `https://raw.githubusercontent.com/JuliaRegistries/General/master/N/NationalWeightedActivityUnitWrapper/` return HTTP 200 for `Package.toml`, `Versions.toml`, `Compat.toml`, and `Deps.toml`.
- Test command: `julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.test()'`
- Test result: `NationalWeightedActivityUnitWrapper` tests passed with command assembly and missing input guard testsets.
- License: MIT license present in the Julia package top-level folder.
- Feedback addressed: package name is `NationalWeightedActivityUnitWrapper`, public repository is `NationalWeightedActivityUnitWrapper.jl`, and tag `v0.1.0` points to `56ddec5ae29513e80717d4625f82c024a211c949`.
- Remaining external blocker: none for Julia General raw registry publication evidence. JuliaHub search/API propagation may lag and is not used as the publication source of truth.

## Submission Evidence

- Repository: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Tag: `v0.1.0`
- Commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- UUID: `58dad789-f56a-4ab3-a66f-c15139bf9cbe`
- Registrator trigger issue: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`
- General registry PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156236`, `https://github.com/JuliaRegistries/General/pull/156235`, `https://github.com/JuliaRegistries/General/pull/156200`
- State: merged on 2026-05-28T15:34:44Z; General registry raw files verify version `0.1.0` with git-tree-sha1 `bb22d4bd44689549064bd441092fd540b5d852cf`.
- Release notes comment: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1#issuecomment-4535380457`
- Registrator update confirmation: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1#issuecomment-4535381791`
- TagBot workflow: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/blob/main/.github/workflows/TagBot.yml`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is claimed only from public General registry raw-file evidence and the merged upstream PR.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
