# Specification: Public Clinical Dataset Worked Example

## Overview

Create a conservative worked example that shows how real public clinical data
can be prepared for the NWAU calculator contract without overclaiming
Australian classification support.

The track must first evaluate candidate public datasets, then default to a
worked example around MIMIC-IV Clinical Database Demo v2.2 if the assessment
continues to support that choice. MIMIC-IV Demo can support real-data ETL and
episode staging, but it cannot produce authoritative Australian AR-DRG or NWAU
outputs unless precomputed Australian grouping provenance or a local licensed
grouper is supplied.

## Functional Requirements

- Reference and satisfy Conductor requirements `MUST-013`, `SHOULD-006`,
  `COULD-004`, and `WONT-005`, and follow the Public Dataset Worked Example
  design in `conductor/design.md`.
- Follow the Conductor workflow strictly: commit after every implementation
  task, include `Commit notes:` in each task commit body, attach equivalent git
  notes, push the branch and `refs/notes/commits` after each task and phase,
  run `conductor-review` after every phase, and review GitHub Actions after the
  whole track is complete.
- Inventory plausible public datasets, including at least:
  - MIMIC-IV Clinical Database Demo v2.2
  - MIMIC-IV-ED Demo v2.2
  - MIMIC-IV Demo in MEDS
  - MIMIC-IV Clinical Database Demo on FHIR
  - Synthea or another fully synthetic FHIR/EHR candidate as a comparison point
- For each candidate, record access path, license, citation, file size,
  required credentials, redistribution rules, clinical fields available, update
  cadence, and fit for NWAU calculator examples.
- Select one initial worked-example dataset, defaulting to MIMIC-IV Clinical
  Database Demo v2.2 unless discovery finds a better fit.
- Keep raw public dataset files out of git; use local download/cache paths,
  committed manifests, and tiny safe fixtures only.
- Classify raw, staged, calculator-ready, calculated, report, and docs outputs
  as commit-safe or local-only, with disclosure-risk checks for small cells,
  rare combinations, direct identifiers, admission IDs, dates, and joined
  clinical features.
- Build a real-data staging example from MIMIC admissions, ICU stays,
  diagnoses, procedures, and available DRG or billing metadata.
- Fail closed when Australian AR-DRG provenance is missing.
- Allow an explicitly labelled synthetic AR-DRG overlay fixture so the tutorial
  can run end-to-end without licensed assets.
- Demonstrate advanced provenance and data-quality features where they help the
  worked example: source manifests, local-file diagnostics, schema validation,
  episode lineage, field-completeness reports, classification provenance,
  support-status output, Python API execution, CLI/file interop, MCP boundary
  validation, API/OpenAI contract documentation, and comparison between raw
  staging, calculator-ready input, and calculated output.
- Add a bounded scenario/sensitivity appendix that compares baseline,
  fail-closed/no-provenance, and synthetic-overlay cases without implying that
  synthetic overlays are authoritative.
- Do not overclaim MCP, API, or OpenAI runtime execution; demonstrate boundary
  validation or documented contract examples where those surfaces do not yet
  execute formulas.
- Record any new feature gaps found while building the worked example and open
  GitHub issues for follow-on work that should not be bundled into the initial
  MIMIC-IV Demo acute example.
- Document that MIMIC US DRGs, ICD-9-CM, ICD-10-CM, and ICD-10-PCS are not
  authoritative Australian AR-DRG, ICD-10-AM, ACHI, or ACS inputs.
- Publish a docs-site tutorial explaining dataset access rules, ETL,
  provenance, caveats, and the runnable workflow.

## Non-Functional Requirements

- Do not commit raw MIMIC files or other public patient-level dataset extracts.
- Do not redistribute restricted clinical classification assets, mapping
  tables, or proprietary grouping logic.
- Data access diagnostics must be explicit about local prerequisites and
  licensing boundaries.
- The worked example must preserve provenance fields and make synthetic overlay
  behavior visible in outputs and docs.
- The worked example must keep real public-data derived outputs local-only
  unless a disclosure-risk review classifies them as commit-safe.
- Documentation must distinguish real deidentified source data from synthetic
  Australian classification overlays.
- Follow-on examples must be separate tracks unless Phase 1 proves they reuse
  the same dataset contract without new access, classification, or data-model
  decisions.

## Acceptance Criteria

- A dataset assessment records candidates, access rules, pros, cons, and
  suitability decisions.
- MIMIC-IV Demo or the selected alternative has a committed manifest and
  local-cache policy.
- Raw public dataset files are ignored and guarded from accidental commits.
- MIMIC-shaped tiny fixtures prove episode staging, local-file diagnostics, and
  fail-closed classification behavior.
- An end-to-end example runs with a synthetic AR-DRG overlay and existing acute
  test weights.
- The example exposes at least one advanced feature beyond a basic CSV run:
  provenance report, data-quality summary, support-status summary, or
  CLI/file-interoperability bundle.
- The example includes a safe-output/disclosure-risk summary and a bounded
  scenario/sensitivity comparison using tiny fixtures or synthetic overlays.
- The example explicitly covers the safe core surfaces available at the time of
  implementation: Python API execution, CLI/file execution, docs tutorial
  output, MCP boundary validation, and API/OpenAI contract documentation where
  runtime execution is not yet supported.
- GitHub issues exist for warranted follow-on features discovered by the track,
  including ED, FHIR/MEDS, dataset suitability registry, and reusable
  downloader/cache guard work if still justified by Phase 1.
- Requirements and design references in `conductor/requirements.md` and
  `conductor/design.md` are updated before implementation claims completion.
- Each implementation task and phase has commit, git-note, push,
  `conductor-review`, and validation evidence recorded.
- The completed track includes a GitHub Actions review note for the pushed
  branch or PR.
- Docs explain how users with local MIMIC-IV Demo files can run the workflow
  and why authoritative NWAU claims require Australian classification
  provenance.

## Out of Scope

- Bundling raw MIMIC files.
- Redistributing restricted clinical or grouping assets.
- Claiming authoritative Australian NWAU calculation from MIMIC alone.
- Implementing a proprietary AR-DRG grouper.
- Mapping US classifications to Australian classifications as if validated.
