# Plan: Pricing-Year Validation Gates

## Phase 1: Status Model [checkpoint: 6d24d63]
- [x] Task: Define validation statuses and allowed transitions.
    - [x] Document required evidence for each transition.
    - [x] Add manifest fields for status and evidence references.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Status Model' (Protocol in workflow.md)

## Phase 2: Gate Implementation [checkpoint: 6d24d63]
- [x] Task: Implement `funding-calculator validate-year <year>` and CI validation checks.
    - [x] Test missing source, missing extraction, missing fixture, and invalid transition cases.
    - [x] Ensure docs/API support matrices use manifest status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Gate Implementation' (Protocol in workflow.md)

## Phase 3: Documentation [checkpoint: 6d24d63]
- [x] Task: Document validation policy and support-claim rules.
    - [x] Add maintainer guidance for advancing a pricing year.
    - [x] Add examples of acceptable evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)
