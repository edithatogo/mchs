# Plan: Public Clinical Dataset Worked Example

## Required Execution Discipline
- [ ] Task: Apply Conductor task lifecycle to every implementation task.
    - [ ] Commit after each task with a `Commit notes:` body section.
    - [ ] Attach equivalent git notes to each task commit.
    - [ ] Push the branch and `refs/notes/commits` after each task and phase checkpoint.
    - [ ] Run `conductor-review` after each phase and at whole-track completion.
    - [ ] Review GitHub Actions after the completed track is pushed and record the result in track evidence.
- [ ] Task: Keep requirements and design authority synchronized.
    - [ ] Maintain references to `MUST-013`, `SHOULD-006`, `COULD-004`, and `WONT-005` from `conductor/requirements.md`.
    - [ ] Maintain references to the Public Dataset Worked Example design section in `conductor/design.md`.
    - [ ] Update requirements/design again if implementation discovers new public-dataset contract or governance needs.

## Phase 1: Dataset Discovery and Access Assessment
- [ ] Task: Inventory candidate public clinical datasets.
    - [ ] Record dataset name, URL, DOI/citation, license, access policy, credential requirements, download path, size, and update cadence.
    - [ ] Assess required fields for acute, ED, and costing-study examples.
    - [ ] Record pros, cons, risks, and whether each dataset can be used in committed fixtures, local-only downloads, docs, or runtime examples.
    - [ ] Include current-source checks for PhysioNet access, license, file tables, citation, and whether local credentialing or terms acceptance are required.
- [ ] Task: Select the initial worked-example dataset and record rationale.
    - [ ] Default to MIMIC-IV Clinical Database Demo v2.2 unless the assessment finds a better fit.
    - [ ] Record why MIMIC-IV-ED, MEDS, FHIR, and Synthea are deferred or secondary.
    - [ ] Record whether each deferred dataset warrants a separate follow-on track or only a backlog note.
- [ ] Task: Open GitHub issues for warranted follow-on examples and infrastructure.
    - [ ] Create issues for ED, FHIR/MEDS, dataset suitability registry, downloader/cache guard, reusable provenance/data-quality report, worked-example surface conformance harness, disclosure-risk policy, and scenario/sensitivity report work only when evidence shows they are useful and separate.
    - [ ] Link created issue numbers and URLs from track metadata or dataset assessment evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Dataset Discovery and Access Assessment' (Protocol in workflow.md)

## Phase 2: Dataset Manifest and License Boundary
- [ ] Task: Add public dataset manifest and local cache policy.
    - [ ] Add source URL, DOI, license, expected file list, checksums where available, and citation text.
    - [ ] Ensure raw dataset files are ignored and never required in git.
    - [ ] Define commit-safe versus local-only paths for raw, staged, calculator-ready, calculated, report, and docs outputs.
    - [ ] Add diagnostics for missing local data and clear download instructions.
- [ ] Task: Add tests for manifest parsing and license/access guardrails.
    - [ ] Public metadata must pass.
    - [ ] Raw patient-level dataset files in committed paths must fail guard checks.
- [ ] Task: Add data-quality and provenance contract outputs.
    - [ ] Emit a machine-readable provenance report for dataset source, local file inventory, derivation steps, overlay status, and support-state claims.
    - [ ] Emit a data-quality summary covering row counts, missing required fields, duplicate identifiers, date/LOS sanity checks, ICU aggregation coverage, and classification provenance state.
    - [ ] Emit a disclosure-risk summary covering small cells, rare combinations, direct identifiers, admission IDs, dates, and joined clinical features.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Dataset Manifest and License Boundary' (Protocol in workflow.md)

## Phase 3: MIMIC-IV Demo ETL and Fail-Closed Contract
- [ ] Task: Implement MIMIC-IV Demo staging from local CSV files.
    - [ ] Derive episode-level facts from admissions, ICU stays, diagnoses, procedures, and hospital metadata.
    - [ ] Emit a staging table that preserves MIMIC provenance and does not claim Australian classification.
    - [ ] Include stable episode lineage from source files and row identifiers to staged rows.
- [ ] Task: Add calculator-input preparation with classification provenance checks.
    - [ ] Fail closed when no Australian AR-DRG or approved synthetic overlay is supplied.
    - [ ] Support a committed synthetic AR-DRG overlay fixture for runnable documentation only.
    - [ ] Make overlay provenance visible in every calculator-ready and calculated output.
- [ ] Task: Demonstrate advanced calculator-tooling features in the worked example.
    - [ ] Produce raw staging, calculator-ready CSV, calculated CSV, provenance report, data-quality report, and support-status summary.
    - [ ] Exercise Python API and CLI/file interoperability where they are already supported, without adding a new runtime surface.
    - [ ] Exercise MCP boundary validation and API/OpenAI contract documentation where those surfaces are available, without claiming formula execution if the existing contract does not support it.
    - [ ] Add a scenario/sensitivity appendix comparing no-provenance fail-closed behavior, synthetic-overlay behavior, and any local precomputed AR-DRG path if supplied.
    - [ ] Record any missing feature needed for a better public-dataset workflow as a GitHub issue rather than expanding this track.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: MIMIC-IV Demo ETL and Fail-Closed Contract' (Protocol in workflow.md)

## Phase 4: Worked Example, Docs, and Additional Improvements
- [ ] Task: Add a runnable worked example.
    - [ ] Generate staging, calculator input, and synthetic-overlay NWAU output from tiny committed fixtures.
    - [ ] Provide commands for users with local MIMIC-IV Demo files.
- [ ] Task: Publish docs-site tutorial and improvement backlog.
    - [ ] Explain dataset access, license, citation, field mapping, limitations, and Australian classification caveats.
    - [ ] Recommend follow-on improvements: dataset suitability registry, reusable public-dataset downloader, reusable provenance/data-quality report contracts, worked-example surface conformance harnesses, disclosure-risk policy, scenario/sensitivity report patterns, and optional ED/FHIR/MEDS tutorial tracks.
- [ ] Task: Review GitHub Actions and finalize track evidence.
    - [ ] Push the branch and git notes before reviewing GitHub Actions.
    - [ ] Review relevant GitHub Actions runs for the pushed branch or PR.
    - [ ] Record pass/fail/blocked status, run URLs, and any external gates in metadata, review notes, or final evidence docs.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Worked Example, Docs, and Additional Improvements' (Protocol in workflow.md)
