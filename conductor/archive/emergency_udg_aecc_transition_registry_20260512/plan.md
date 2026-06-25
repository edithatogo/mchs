# Plan: Emergency UDG/AECC Transition Registry

## Scope Notes
- Limit work to documentation, registry metadata, validation surfaces, and transition semantics for emergency care classification.
- Do not invent a UDG-to-AECC crosswalk or imply that any unpublished mapping exists.
- Treat licensing on source manuals and mappings as a first-class constraint; capture provenance, do not redistribute restricted source content.
- Keep completion contingent on observable evidence in the repository.
- Keep the track metadata aligned with the governing fields: primary contract, dependencies, completion evidence, publication status, validation status, licensing caveats, and evidence surfaces.

## Phase 1: Transition Model
- [x] Task: Normalize the governance-facing track metadata and evidence surfaces.
    - [x] Keep the primary contract explicit and tied to the registry contract rather than a generic scaffold label.
    - [x] Keep the validation status and publication status explicit.
    - [x] Preserve the evidence surfaces that will back completion claims.
- [x] Task: Define UDG and AECC version records and pricing-year applicability.
    - [x] Identify emergency department versus emergency service stream compatibility.
    - [x] Represent transitional or shadow-pricing periods separately from active pricing, without implying equivalence between UDG and AECC.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Transition Model' (Protocol in workflow.md)

## Phase 2: Registry and Validators
- [x] Task: Add emergency classification registry entries and compatibility validators.
    - [x] Test valid UDG, valid AECC, transition-period, incompatible-year, and missing-classification cases.
    - [x] Link emergency calculator input schemas to the registry.
    - [x] Validate that no fabricated crosswalk or fallback mapping is introduced.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Registry and Validators' (Protocol in workflow.md)

## Phase 3: Documentation
- [x] Task: Document UDG, AECC, transition handling, and user data-preparation requirements.
    - [x] Explain when precomputed emergency classification codes are required.
    - [x] Explain when mapping/grouper integration may be used.
    - [x] Include examples for pre-transition, transition-period, and post-transition behavior.
    - [x] Include licensing caveats and completion caveats.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)
