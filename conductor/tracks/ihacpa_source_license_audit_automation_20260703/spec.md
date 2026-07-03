# Specification: IHACPA Source/License Audit Automation

## Overview
Add review-only automation that turns IHACPA source-scanner output into draft artifacts for source manifests, Conductor tracks, and GitHub issue updates. The automation must preserve the existing non-redistribution boundary: public metadata and review summaries may be drafted, but restricted assets must never be copied into the repository.

## Contract
- Scanner output remains the source of truth for discovered URLs, gaps, and review status.
- Draft artifacts may include manifest text, Conductor track scaffolds, and GitHub issue bodies.
- Restricted or licensed source content must remain referenced, not copied.
- The audit package must be deterministic for the same scanner input.
- Draft outputs must not overstate validation, parity, or publication readiness.

## Functional Requirements
- Build a review-only audit package from source scanner results.
- Render draft Conductor track metadata, spec, plan, and registry text from the scanner package.
- Render a GitHub issue body that summarizes the audit boundary and validation expectations.
- Preserve gap records, review notes, and licensing caveats in the generated drafts.
- Expose the package through the installed CLI so maintainers can generate drafts from offline fixtures or URL lists.

## Non-Functional Requirements
- The automation must not require live IHACPA access in CI.
- The generated drafts must remain conservative and human-reviewable.
- The implementation must keep restricted content out of version control.
- The package should be easy to reuse for future audit or discovery tracks.

## Acceptance Criteria
- A source scan can produce an audit package with manifest, track, and issue draft text.
- The draft issue body links to the local Conductor track path and states the licensing boundary.
- The draft Conductor track includes metadata, spec, plan, and registry entry text.
- The CLI can emit the audit package without mutating restricted source material.
- Tests prove the outputs are deterministic and do not embed restricted content.

## Out of Scope
- Fetching or downloading restricted source assets.
- Auto-merging GitHub issues or committing draft outputs without review.
- Replacing the existing source scanner contract.
- Adding new licensing interpretations beyond explicit manifest and gap records.

## Source Evidence
- GitHub issue: https://github.com/edithatogo/mchs/issues/209
- Source scanner: `nwau_py.source_scanner`
- Licensed asset workflow: `nwau_py.licensed_product_workflow`
- Source scanner contract fixtures: `contracts/source-scanner/`
