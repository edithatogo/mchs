# Specification: Expert Panel Remediation

## Overview
Convert the simulated expert-panel findings into actionable Conductor
priorities. The expert panel identified that the project should prioritise
governance, executable contracts, validation gates, source/licensing controls,
one complete stream/year canary, Rust-core promotion, classification/grouper
capabilities, documentation, costing tutorials, bindings/apps, and publication
expansion in that order.

## Functional Requirements
- Review the expert panel synthesis and chaired deliberation.
- Map each high-priority recommendation to an existing track or create a new
  track if no owner exists.
- Add missing dependencies or gate notes to affected tracks.
- Ensure SAS parity and Excel formula parity are explicit in validation tracks.
- Ensure restricted classification/product handling is explicit in source,
  classifier, and publication tracks.
- Ensure polyglot binding tracks depend on shared contracts and conformance
  tests.
- Ensure costing-study and policy/tutorial tracks include appropriate-use and
  overclaiming caveats.

## Non-Functional Requirements
- Do not implement broad bindings before shared contracts and validation gates.
- Do not mark roadmap updates as implementation completion.
- Keep expert-panel documents clearly marked as simulated planning artifacts.

## Acceptance Criteria
- Every expert-panel priority has an owning Conductor track.
- The dependency order from the deliberation is represented in the registry or
  track specs.
- Critical recommendations have explicit follow-up tasks or acceptance criteria.
- Remaining gaps are recorded in a remediation checklist.

## Source Artifacts
- `docs/reviews/20260512-expert-panel/synthesis.md`
- `docs/reviews/20260512-expert-panel/deliberation-and-prioritisation.md`
