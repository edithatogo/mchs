# Plan: Public Clinical Dataset Worked Example

## Phase 1: Dataset Discovery and Access Assessment
- [ ] Task: Inventory candidate public clinical datasets.
    - [ ] Record dataset name, URL, DOI/citation, license, access policy, credential requirements, download path, size, and update cadence.
    - [ ] Assess required fields for acute, ED, and costing-study examples.
    - [ ] Record pros, cons, risks, and whether each dataset can be used in committed fixtures, local-only downloads, docs, or runtime examples.
- [ ] Task: Select the initial worked-example dataset and record rationale.
    - [ ] Default to MIMIC-IV Clinical Database Demo v2.2 unless the assessment finds a better fit.
    - [ ] Record why MIMIC-IV-ED, MEDS, FHIR, and Synthea are deferred or secondary.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Dataset Discovery and Access Assessment' (Protocol in workflow.md)

## Phase 2: Dataset Manifest and License Boundary
- [ ] Task: Add public dataset manifest and local cache policy.
    - [ ] Add source URL, DOI, license, expected file list, checksums where available, and citation text.
    - [ ] Ensure raw dataset files are ignored and never required in git.
    - [ ] Add diagnostics for missing local data and clear download instructions.
- [ ] Task: Add tests for manifest parsing and license/access guardrails.
    - [ ] Public metadata must pass.
    - [ ] Raw patient-level dataset files in committed paths must fail guard checks.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Dataset Manifest and License Boundary' (Protocol in workflow.md)

## Phase 3: MIMIC-IV Demo ETL and Fail-Closed Contract
- [ ] Task: Implement MIMIC-IV Demo staging from local CSV files.
    - [ ] Derive episode-level facts from admissions, ICU stays, and hospital metadata.
    - [ ] Emit a staging table that preserves MIMIC provenance and does not claim Australian classification.
- [ ] Task: Add calculator-input preparation with classification provenance checks.
    - [ ] Fail closed when no Australian AR-DRG or approved synthetic overlay is supplied.
    - [ ] Support a committed synthetic AR-DRG overlay fixture for runnable documentation only.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: MIMIC-IV Demo ETL and Fail-Closed Contract' (Protocol in workflow.md)

## Phase 4: Worked Example, Docs, and Additional Improvements
- [ ] Task: Add a runnable worked example.
    - [ ] Generate staging, calculator input, and synthetic-overlay NWAU output from tiny committed fixtures.
    - [ ] Provide commands for users with local MIMIC-IV Demo files.
- [ ] Task: Publish docs-site tutorial and improvement backlog.
    - [ ] Explain dataset access, license, citation, field mapping, limitations, and Australian classification caveats.
    - [ ] Recommend follow-on improvements: dataset suitability registry, reusable public-dataset downloader, provenance reports, and optional ED/FHIR/MEDS tutorial tracks.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Worked Example, Docs, and Additional Improvements' (Protocol in workflow.md)
