# Plan: AR-DRG Grouper Integration

## Phase 1: Interface Design [checkpoint: archived]
- [x] Task: Define precomputed and external-grouper integration interfaces.
    - [x] Specify required inputs, outputs, errors, and provenance metadata.
    - [x] Define version compatibility checks.
- [x] Task: Conductor review checkpoint for Phase 1.
    - [x] Confirm the contract boundaries, fail-closed behavior, and supported integration modes.
    - [x] Confirm the evidence surfaces needed before adapter work begins.

## Phase 2: Adapter Prototype [checkpoint: archived]
- [x] Task: Add a mock external-grouper adapter and tests.
    - [x] Test compatible, incompatible, failed, and missing-grouper cases.
    - [x] Preserve input/output provenance records.
- [x] Task: Conductor review checkpoint for Phase 2.
    - [x] Confirm the adapter rejects unsupported combinations and records provenance.
    - [x] Confirm the test surface covers the supported and unsupported workflows.

## Phase 3: Workflow Documentation [checkpoint: archived]
- [x] Task: Document admitted acute grouping workflows.
    - [x] Explain precomputed AR-DRG inputs versus package-mediated external grouping.
    - [x] Spell out command, service, and file-exchange patterns for local licensed grouper use.
    - [x] State that bundled proprietary grouping logic is out of scope.
    - [x] Include costing-study and validation caveats for version matching, parity claims, and provenance.
- [x] Task: Conductor review checkpoint for Phase 3.
    - [x] Confirm the docs separate current support from future or licensed-only possibilities.
    - [x] Confirm the final evidence surfaces are linked and the proprietary boundary is explicit.

## Phase 4: Archive Repair [checkpoint: repaired]
- [x] Task: Repair archive metadata and plan evidence.
    - [x] Restore `metadata.json` archive-policy fields for completion policy, support scope, archive evidence, and explicit gap register.
    - [x] Restore `plan.md` checkpoint markers so the archived plan remains auditable after migration.
    - [x] Keep the public claim boundary unchanged: proprietary grouper support remains unclaimed, licensed grouping tools remain user supplied, and ICD-to-AR-DRG calculation is not inferred without a licensed local provider.
- [x] Task: Conductor review checkpoint for Archive Repair.
    - [x] Confirm focused tests cover repaired metadata and plan evidence.
    - [x] Confirm no proprietary grouping logic, licensed tables, or redistributable grouper assets were added.
