# Stata SSC Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Stata`
- Registry: `SSC / Stata package distribution`
- Package candidate: `mchs-stata-interop`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/stata`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally, submitted, and published on the Boston College SSC/RePEc archive. A Stata ado/help/pkg bundle exists with README, license, notes, and examples for maintainer review. No Stata executable is installed locally, so no ado runtime validation is claimed. SSC maintainer feedback requested author contact information in `mchs.sthlp`; this was corrected locally before publication evidence was captured. No corrected-archive follow-up email is needed because public installability evidence now exists.

## Preparation Evidence

- Discovery/publication: `http://fmwww.bc.edu/repec/bocode/m/mchs.pkg`, `http://fmwww.bc.edu/repec/bocode/m/mchs.ado`, and `http://fmwww.bc.edu/repec/bocode/m/mchs.sthlp` are live SSC/RePEc publication evidence.
- Bundle: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`
- SHA256: `7cd12328f7b9e061fb2fe42c72ee6812f055f64ccabb2338ef45c26cdf98ce1a`
- Contents: `mchs.ado`, `mchs.sthlp`, `pkg-mchs.pkg`, `README.md`, `LICENSE`, `examples/*.do`, `stata-interop-notes.md`
- Runtime note: no Stata executable is installed locally.
- Maintainer feedback: on 2026-06-12 Christopher Baum replied that author contact information seems to be missing from `mchs.sthlp`.
- Local feedback fix: on 2026-06-13 `mchs.sthlp` gained an Author section with Dylan Mordaunt, `dylan.mordaunt@vuw.ac.nz`, and the repository URL; the SSC ZIP was rebuilt.
- Remaining external blocker: none for SSC publication. SSC public `.pkg` metadata does not expose the local semantic archive version; version `0.1.0` remains local archive evidence, while installability is verified through the public package manifest, ado file, and help file.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
