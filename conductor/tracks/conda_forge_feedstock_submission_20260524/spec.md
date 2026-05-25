# conda-forge Feedstock Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Conda`
- Registry: `conda-forge`
- Package candidate: `nwau-py`
- Version candidate: `0.2.2`
- Local surface: `microcosting_healthservices/pyproject.toml`
- Current status: `submitted_checks_passing_pending_conda_forge_review`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally and submitted upstream. A conda-forge recipe exists, its source SHA256 matches the published PyPI sdist for `nwau-py==0.2.2`, and a staged-recipes PR is open. Automated lint feedback was addressed and pushed to the PR branch in commit `e6ff7985c94b78471457e446e8fe3abfbe61fa41`. The refreshed PR branch has linter, check-skip, aggregate staged-recipes, linux_64, osx_64, and win_64 checks passing. The remaining blocker is external: conda-forge review, merge, feedstock publication, and public Anaconda propagation.

## Preparation Evidence

- Public registry discovery: `https://api.anaconda.org/package/conda-forge/nwau-py` returned package not found.
- Recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Source distribution: `https://files.pythonhosted.org/packages/90/5f/b64f960d692ac550af6ac05239f34c61f40093cc41d7d9f529c434bb204b/nwau_py-0.2.2.tar.gz`
- SHA256: `c0998035a2e0ceebe913717170994ef668159c6e384524932c55c18fc1ce0480`
- Tooling note: `conda` is installed; `conda-build`, `boa`, and `rattler-build` are not installed locally.
- Fixed lint feedback: added recipe maintainers, tests, build number, `license_file`, `setuptools` build backend, noarch Python minimum pins, `pypi.org` source URL, runtime dependencies, and entry points.
- Remaining external blocker: staged-recipes review, merge, feedstock publication, and public Anaconda propagation.

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
