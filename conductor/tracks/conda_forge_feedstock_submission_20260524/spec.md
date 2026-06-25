# conda-forge Feedstock Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Conda`
- Registry: `conda-forge`
- Package candidate: `nwau-py`
- Version candidate: `0.2.2`
- Local surface: `microcosting_healthservices/pyproject.toml`
- Current status: `submitted_checks_passed_pending_staged_recipes_review`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally and submitted upstream. A conda-forge recipe exists, its source SHA256 matches the published PyPI sdist for `nwau-py==0.2.2`, and a staged-recipes PR is open. Automated lint feedback was addressed and pushed to the PR branch, the branch was updated against upstream `main`, and current authenticated live evidence shows head `bffc5bf1a85389dc695adfd96c87bf2413f4db25` with passing linter, conda-forge-linter, staged-recipes, build fast finish, linux_64, osx_64, win_64, build status, and check skip. The 2026-06-25 live monitor shows the PR still open, `mergedAt=null`, `draft=False`, `mergeable=MERGEABLE`, and `mergeStateStatus=BLOCKED`; no maintainer review decision is present, and no actionable comments appear after the 2026-06-11 author follow-up. Anaconda API still returns HTTP 404 for `conda-forge/nwau-py`, and the `conda-forge/nwau-py-feedstock` repository still returns HTTP 404. The remaining blocker is external: conda-forge maintainer review, merge, and feedstock publication.

## Preparation Evidence

- Public registry discovery: `https://api.anaconda.org/package/conda-forge/nwau-py` returned package not found.
- Recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Source distribution: `https://files.pythonhosted.org/packages/90/5f/b64f960d692ac550af6ac05239f34c61f40093cc41d7d9f529c434bb204b/nwau_py-0.2.2.tar.gz`
- SHA256: `c0998035a2e0ceebe913717170994ef668159c6e384524932c55c18fc1ce0480`
- Tooling note: `conda` is installed; `conda-build`, `boa`, and `rattler-build` are not installed locally.
- Fixed lint feedback: added recipe maintainers, tests, build number, `license_file`, `setuptools` build backend, noarch Python minimum pins, `pypi.org` source URL, runtime dependencies, and entry points.
- Latest live PR probe: 2026-06-25 authenticated live monitor returned `state=open`, `mergedAt=null`, `draft=False`, `mergeable=MERGEABLE`, `mergeStateStatus=BLOCKED`, head `bffc5bf1a85389dc695adfd96c87bf2413f4db25`, successful current check rollup, no review decision, and no actionable comments after the 2026-06-11 status follow-up. Anaconda API and the `conda-forge/nwau-py-feedstock` repository still return HTTP 404.
- Remaining external blocker: staged-recipes maintainer review, merge, and feedstock publication.

## Submission Evidence

- PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Fork branch: `edithatogo/staged-recipes:add-nwau-py-0.2.2`
- State: open, linter and Azure platform builds passing, pending review/merge.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, and publication remains blocked with a concrete review/merge reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
