# Homebrew Formula Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Homebrew`
- Registry: `Homebrew tap/core`
- Package candidate: `nwau-py`
- Version candidate: `0.2.2`
- Local surface: `microcosting_healthservices/pyproject.toml`
- Current status: `published_verified` for the personal tap; Homebrew/core is an optional upstream review gate.

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Gate

Resolved locally and published to a personal tap. A Homebrew formula exists with exact PyPI sdist URL, SHA256, Python virtualenv helper include, explicit `python@3.13` dependency, Click PyPI resource, and a temporary lazy CLI import patch for the published `nwau-py==0.2.2` sdist. `edithatogo/homebrew-mchs` is public, `brew audit --strict --online edithatogo/mchs/nwau-py` passes, `brew install --build-from-source edithatogo/mchs/nwau-py` succeeds, and `brew test edithatogo/mchs/nwau-py` passes. Homebrew/core publication remains an optional upstream PR/review gate, not a blocker to the personal-tap publication claim.

## Preparation Evidence

- Public registry discovery: `brew info nwau-py --json=v2` returned `No available formula with the name nwau-py`; live probes on 2026-05-26 returned HTTP 404 for `https://formulae.brew.sh/api/formula/nwau-py.json` and the Homebrew formula page, while the personal tap repository API returned HTTP 200.
- Formula: `microcosting_healthservices/packaging/homebrew/nwau-py.rb`
- Source distribution: `https://files.pythonhosted.org/packages/90/5f/b64f960d692ac550af6ac05239f34c61f40093cc41d7d9f529c434bb204b/nwau_py-0.2.2.tar.gz`
- SHA256: `c0998035a2e0ceebe913717170994ef668159c6e384524932c55c18fc1ce0480`
- Local fix: added `Language::Python::Virtualenv` include, exact PyPI source URL, source checksum, explicit `python@3.13` dependency, Click PyPI resource, and lazy CLI `inreplace` patch.
- Audit result: `brew audit --strict --online edithatogo/mchs/nwau-py` passed.
- Install/test result: `brew install --build-from-source edithatogo/mchs/nwau-py` and `brew test edithatogo/mchs/nwau-py` passed.
- Local package fix: root `funding-calculator --help` no longer eagerly imports pandas, numpy, pydantic, or pyreadstat; the tap carries an equivalent temporary patch until a new PyPI release includes the fix.
- Optional upstream gate: Homebrew/core PR and review.

## Submission Evidence

- Tap: `https://github.com/edithatogo/homebrew-mchs`
- Formula: `https://raw.githubusercontent.com/edithatogo/homebrew-mchs/main/Formula/nwau-py.rb`
- Tap commit: `fa12ed26c1d6a289b40bf59c9bacbb9a5e42f823`
- Formula HTTP status: `200`
- Homebrew/core API status: `404`
- Formula SHA256: `6f987bc4a81f3ac78cbc893d6a502fc572a534905f9f1f89cfc05600ff4ddff3`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists for the personal tap, with audit, source install, and `brew test` passing.
- Publication is claimed only for the public personal tap URL; Homebrew/core is not claimed unless accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
