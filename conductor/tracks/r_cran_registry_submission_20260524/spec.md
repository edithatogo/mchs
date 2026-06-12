# R CRAN Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `R`
- Registry: `CRAN`
- Package candidate: `nwauR`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/r-binding/DESCRIPTION`
- Current status: `submitted_pending_cran_confirmation_link_action`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally, submitted, and confirmed. `R CMD build r-binding` created `nwauR_0.1.0.tar.gz`, `R CMD check --no-manual nwauR_0.1.0.tar.gz` completed with `Status: OK`, package-local CRAN-style `_R_CHECK_CRAN_INCOMING_REMOTE_=false R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz` completed with `Status: OK`, and live `R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz` completed with `Status: 1 NOTE`; the only reported NOTE is the expected CRAN incoming `New submission` note. The package was submitted through the CRAN web upload workflow on 2026-06-12. The CRAN maintainer confirmation email was received in Outlook at 02:17 Australia/Sydney on 2026-06-12, and the user clicked the confirmation link. The CRAN confirmation result page displayed: `The package has been uploaded successfully to CRAN submission team.` The remaining blocker is incoming/pretest evidence, reviewer response if requested, and public package publication.

## Preparation Evidence

- Public registry discovery: `https://crandb.r-pkg.org/nwauR` returned `not_found`.
- Build command: `R CMD build r-binding`
- Package artifact: `microcosting_healthservices/nwauR_0.1.0.tar.gz`
- Check command: `R CMD check --no-manual nwauR_0.1.0.tar.gz`
- Check result: `Status: OK`
- Package-local CRAN-style check command: `_R_CHECK_CRAN_INCOMING_REMOTE_=false R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz`
- Package-local CRAN-style check result: `Status: OK`
- Live CRAN remote incoming metadata check: `R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz` completed with `Status: 1 NOTE`; the only reported NOTE is the expected CRAN incoming `New submission` note.
- Submission surface: `https://cran.r-project.org/submit.html`
- Submission state: submitted through the CRAN web upload workflow on 2026-06-12.
- Confirmation email: received in Outlook on 2026-06-12 02:17 Australia/Sydney from `CRAN Package Submission Form <root-xmpalantir@xmbombadil.wu.ac.at>` with subject `CRAN Submission of nwauR 0.1.0 - Confirmation Link`; the link/code is not stored in repository evidence.
- Confirmation result: CRAN page `https://xmpalantir.wu.ac.at/cransubmit/index.php?strErr=96&redirect=1` displayed `The package has been uploaded successfully to CRAN submission team.`
- Remaining external blocker: incoming/pretest evidence, reviewer response if requested, and public package publication.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
