# Specification: Roadmap Portfolio Governance Backfill

## Overview
Backfill the expanded Conductor roadmap with consistent governance metadata. The project now includes many roadmap-only and future-state tracks, so each track needs a clear class, dependency model, explicit contract, completion evidence, and current-state label.

## Functional Requirements
- Classify every active and archived track using `conductor/roadmap-governance.md` track classes.
- Add or verify dependency statements for roadmap-heavy tracks.
- Add or verify explicit contracts and required completion evidence.
- Mark roadmap-only, scaffold-only, complete-with-gaps, and complete states accurately.
- Identify tracks whose registry status is inconsistent with durable evidence.

## Non-Functional Requirements
- Do not mark implementation complete because a roadmap exists.
- Preserve historical track content while correcting inaccurate current-state claims.
- Keep future-state claims separate from validated behavior.

## Acceptance Criteria
- Every active roadmap track has class, dependency, contract, and evidence metadata or a documented gap.
- Completed tracks with missing evidence are reclassified or receive remediation tracks.
- The registry and track metadata use consistent current-state language.
