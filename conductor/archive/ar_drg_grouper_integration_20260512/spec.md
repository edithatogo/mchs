# Specification: AR-DRG Grouper Integration

## Overview
Define an integration path for AR-DRG workflows that accepts precomputed AR-DRG inputs or derives AR-DRGs from ICD-10-AM/ACHI/ACS-coded admitted episode data using a licensed external grouper or user-supplied grouping service. The package should not reimplement proprietary grouping logic and should not bundle licensed grouping tables or software.

This package does not reimplement proprietary grouping logic.

## Contract
- Inputs: admitted episode records already coded with ICD-10-AM/ACHI/ACS, or
  precomputed AR-DRG values supplied by the user.
- Outputs: validated AR-DRG results plus provenance metadata for the
  originating grouper workflow.
- Supported integration modes: precomputed AR-DRG ingestion and
  package-mediated calls to a user-supplied licensed grouper.
- Failure rule: incompatible, missing, or unsupported grouper combinations
  must fail closed rather than falling back to guessed or placeholder grouping.
- Scope boundary: this track covers integration, validation, and provenance;
  it does not claim to ship proprietary grouper internals or official vendor
  support.

## Functional Requirements
- Allow precomputed AR-DRG inputs to flow through validation and provenance capture without re-grouping.
- Define a pluggable grouper interface for admitted acute episodes.
- Support user-supplied external grouper command, service, or file-exchange integration for local licensed use.
- Validate grouper version compatibility with selected pricing year.
- Capture provenance for derived AR-DRG outputs, including grouper version, coding-set version, timestamp, and input hash.
- Explicitly reject any workflow that implies bundled proprietary grouping logic inside the repository.

## Non-Functional Requirements
- Keep proprietary grouping logic and licensed tables outside the repository unless licensing explicitly permits inclusion.
- Never silently group with an incompatible version.
- Preserve deterministic audit trails for grouped outputs.
- Prefer transparent error reporting over implicit fallback behavior.

## Evidence Surfaces
- Track files in this directory: `index.md`, `spec.md`, `plan.md`, and
  `metadata.json`.
- Adapter and validation tests that cover compatible, incompatible, missing,
  and failed grouper cases.
- Workflow notes that describe supported and unsupported integration modes.
- Provenance records that capture grouper version, coding-set version,
  timestamp, input hash, and source mode.
- Review notes or checkpoint records from each Conductor phase gate.

## Phases
1. Phase 1 establishes the interface contract, compatibility rules, and
   failure semantics for precomputed and external-grouper flows.
2. Phase 2 exercises a mock adapter and records provenance and rejection
   behavior for the supported and unsupported cases.
3. Phase 3 documents the operational workflow, local licensing caveats, and
   the limits of what this repository can claim about grouper support.

## Acceptance Criteria
- A clear interface exists for precomputed DRGs and external-grouper-derived DRGs.
- Validation rejects mismatched grouper/coding-set/pricing-year combinations.
- Docs explain precomputed input support, local licensed external grouping support, and the explicit non-support for bundled proprietary grouping logic.
- The repository never states or implies that proprietary grouper logic is
  implemented locally.
- The phase checkpoints capture the evidence needed to advance without
  overclaiming support.

## Source Evidence
- IHACPA AR-DRGs: https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system
- IHACPA admitted acute care: https://www.ihacpa.gov.au/health-care/classification/admitted-acute-care
