# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `CRAN` for existing `nwauR` publication.
    - [x] Capture registry URL/API response or absence evidence.
    - [x] Compare discovered version against `0.1.0`.
    - [x] Update `language-registry-submissions.contract.json` status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Discovery' (Protocol in workflow.md)

## Phase 2: Preparation

- [x] Task: Prepare registry-specific package metadata.
    - [x] Confirm package name, ownership, license, README, keywords, repository URL, and support policy.
    - [x] Remove placeholder/example/private flags that block publication.
    - [x] Build the package artifact using the registry-native pack command.
    - [x] Capture checksum/SBOM/provenance where supported.
- [x] Task: Verify CRAN-style local readiness without authenticated submission.
    - [x] Run `R CMD check --no-manual nwauR_0.1.0.tar.gz`; result `Status: OK`.
    - [x] Run `_R_CHECK_CRAN_INCOMING_REMOTE_=false R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz`; result `Status: OK`.
    - [x] Record live CRAN incoming metadata. Plain `R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz` completed with `Status: 1 NOTE`; the only reported NOTE is the expected CRAN incoming `New submission` note.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [x] Task: Assemble CRAN submission steps and evidence capture.
    - [x] Create a track-local submission checklist with commands, upload URL, and evidence capture points.
    - [x] Link the shared runbook back to the track-local checklist.
- [x] Task: Submit to `CRAN` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Not applicable because CRAN submission is a maintainer web-upload/review workflow; upload was submitted through `https://cran.r-project.org/submit.html` on 2026-06-12.
    - [x] Capture submission URL, version, owner, and review state. Submission surface: `https://cran.r-project.org/submit.html`; package `nwauR` version `0.1.0`; maintainer `Dylan Mordaunt <dylan.mordaunt@vuw.ac.nz>`; review state `submitted_confirmed_pending_cran_pretest_review_publication`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Submission performed; publication evidence remains pending.

## Phase 4: Publication Evidence

- [~] Task: Verify external publication. Pending CRAN incoming/pretest evidence, CRAN acceptance, and public package propagation.
    - [x] Query public registry after propagation. 2026-07-05 live probe: CRAN package page and CRANDB return HTTP 404/not found; `src/contrib/PACKAGES` returns HTTP 200 but does not contain `Package: nwauR`.
    - [x] Record immutable URL/API response/checksum. Current absence evidence is recorded in `live_probe_20260705.json`; publication checksum remains pending because no public package exists.
    - [ ] Mark track complete only if publication or accepted-review evidence exists. Publication is not claimed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
