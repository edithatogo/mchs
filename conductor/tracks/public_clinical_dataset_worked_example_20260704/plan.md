# Plan: Public Clinical Dataset Worked Example

## Required Execution Discipline
- [x] Task: Apply Conductor task lifecycle to every implementation task.
    - [x] Commit after each task with a `Commit notes:` body section.
    - [x] Attach equivalent git notes to each task commit.
    - [x] Push the branch and `refs/notes/commits` after each task and phase checkpoint.
    - [x] Run `conductor-review` after each phase and at whole-track completion.
    - [x] Review GitHub Actions after the completed track is pushed and record the result in track evidence.
- [ ] Task: Keep requirements and design authority synchronized.
    - [ ] Maintain references to `MUST-013`, `SHOULD-006`, `COULD-004`, and `WONT-005` from `conductor/requirements.md`.
    - [ ] Maintain references to the Public Dataset Worked Example design section in `conductor/design.md`.
    - [ ] Update requirements/design again if implementation discovers new public-dataset contract or governance needs.

## Phase 1: Dataset Discovery and Access Assessment [checkpoint: edbd88c]
- [x] Task: Inventory candidate public clinical datasets. `b3352d5`
    - [x] Record dataset name, URL, DOI/citation, license, access policy, credential requirements, download path, size, and update cadence.
    - [x] Assess required fields for acute, ED, and costing-study examples.
    - [x] Record pros, cons, risks, and whether each dataset can be used in committed fixtures, local-only downloads, docs, or runtime examples.
    - [x] Include current-source checks for PhysioNet access, license, file tables, citation, and whether local credentialing or terms acceptance are required.
- [x] Task: Select the initial worked-example dataset and record rationale. `b3352d5`
    - [x] Default to MIMIC-IV Clinical Database Demo v2.2 unless the assessment finds a better fit.
    - [x] Record why MIMIC-IV-ED, MEDS, FHIR, and Synthea are deferred or secondary.
    - [x] Record whether each deferred dataset warrants a separate follow-on track or only a backlog note.
- [x] Task: Open GitHub issues for warranted follow-on examples and infrastructure. `b3352d5`
    - [x] Create issues for ED, FHIR/MEDS, dataset suitability registry, downloader/cache guard, reusable provenance/data-quality report, worked-example surface conformance harness, disclosure-risk policy, and scenario/sensitivity report work only when evidence shows they are useful and separate.
    - [x] Link created issue numbers and URLs from track metadata or dataset assessment evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Dataset Discovery and Access Assessment' (Protocol in workflow.md) `edbd88c`

## Phase 2: Dataset Manifest and License Boundary [checkpoint: 043cf0c]
- [x] Task: Add public dataset manifest and local cache policy. `4f322c2`
    - [x] Add source URL, DOI, license, expected file list, checksums where available, and citation text.
    - [x] Ensure raw dataset files are ignored and never required in git.
    - [x] Define commit-safe versus local-only paths for raw, staged, calculator-ready, calculated, report, and docs outputs.
    - [x] Add diagnostics for missing local data and clear download instructions.
- [x] Task: Add tests for manifest parsing and license/access guardrails. `4f322c2`
    - [x] Public metadata must pass.
    - [x] Raw patient-level dataset files in committed paths must fail guard checks.
- [x] Task: Add data-quality and provenance contract outputs. `4f322c2`
    - [x] Emit a machine-readable provenance report for dataset source, local file inventory, derivation steps, overlay status, and support-state claims.
    - [x] Emit a data-quality summary covering row counts, missing required fields, duplicate identifiers, date/LOS sanity checks, ICU aggregation coverage, and classification provenance state.
    - [x] Emit a disclosure-risk summary covering small cells, rare combinations, direct identifiers, admission IDs, dates, and joined clinical features.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Dataset Manifest and License Boundary' (Protocol in workflow.md) `043cf0c`

## Phase 3: MIMIC-IV Demo ETL and Fail-Closed Contract [checkpoint: 2bfd7eb]
- [x] Task: Implement MIMIC-IV Demo staging from local CSV files. `f27a15c`
    - [x] Derive episode-level facts from admissions, ICU stays, diagnoses, procedures, and hospital metadata.
    - [x] Emit a staging table that preserves MIMIC provenance and does not claim Australian classification.
    - [x] Include stable episode lineage from source files and row identifiers to staged rows.
- [x] Task: Add calculator-input preparation with classification provenance checks. `f27a15c`
    - [x] Fail closed when no Australian AR-DRG or approved synthetic overlay is supplied.
    - [x] Support a committed synthetic AR-DRG overlay fixture for runnable documentation only.
    - [x] Make overlay provenance visible in every calculator-ready and calculated output.
- [x] Task: Demonstrate advanced calculator-tooling features in the worked example. `f27a15c`
    - [x] Produce raw staging, calculator-ready CSV, calculated CSV, provenance report, data-quality report, and support-status summary.
    - [x] Exercise Python API and CLI/file interoperability where they are already supported, without adding a new runtime surface.
    - [x] Exercise MCP boundary validation and API/OpenAI contract documentation where those surfaces are available, without claiming formula execution if the existing contract does not support it.
    - [x] Add a scenario/sensitivity appendix comparing no-provenance fail-closed behavior, synthetic-overlay behavior, and any local precomputed AR-DRG path if supplied.
    - [x] Record any missing feature needed for a better public-dataset workflow as a GitHub issue rather than expanding this track.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: MIMIC-IV Demo ETL and Fail-Closed Contract' (Protocol in workflow.md)

## Phase 4: Worked Example, Docs, and Additional Improvements
- [x] Task: Add a runnable worked example. `cc6c2f1`
    - [x] Generate staging, calculator input, and synthetic-overlay NWAU output from tiny committed fixtures.
    - [x] Provide commands for users with local MIMIC-IV Demo files.
- [x] Task: Publish docs-site tutorial and improvement backlog. `cc6c2f1`
    - [x] Explain dataset access, license, citation, field mapping, limitations, and Australian classification caveats.
    - [x] Recommend follow-on improvements: dataset suitability registry, reusable public-dataset downloader, reusable provenance/data-quality report contracts, worked-example surface conformance harnesses, disclosure-risk policy, scenario/sensitivity report patterns, and optional ED/FHIR/MEDS tutorial tracks.
- [x] Task: Review GitHub Actions and finalize track evidence. `93d46d6`
    - [x] Push the branch and git notes before reviewing GitHub Actions.
    - [x] Review relevant GitHub Actions runs for the pushed branch or PR.
    - [x] Record pass/fail/blocked status, run URLs, and any external gates in metadata, review notes, or final evidence docs.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Worked Example, Docs, and Additional Improvements' (Protocol in workflow.md)
