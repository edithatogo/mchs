# Specification: Emergency Grouper Integration

## Overview
Define the `nwau_py.emergency_grouper` integration boundary for deriving emergency classification outputs through precomputed inputs or an official, licensed, or user-supplied grouper or mapping service where available. This parallels the AR-DRG external-grouper pattern while preserving UDG/AECC transition semantics and registry-backed era selection.

## Governance and Dependencies
- Primary contract: `nwau_py.emergency_grouper` integration boundary for precomputed UDG/AECC outputs and licensed external grouper or mapping-service workflows, with provenance capture for tool, table, and input state.
- Dependencies: `emergency_udg_aecc_transition_registry_20260512` for era selection, pricing-year applicability, and compatibility checks; `emergency_code_mapping_pipeline_20260512` for source-field mapping bundles and provenance-aware mapping outputs.
- Publication status: `not-ready`
- Validation status: `not-validated`
- Licensing caveats: do not embed or redistribute licensed emergency grouper tables, manuals, or mapping bundles unless the source license explicitly permits it; do not invent UDG-to-AECC crosswalks or silently convert between eras without declared source provenance.
- Evidence surfaces: `metadata.json`, `index.md`, `plan.md`, adapter tests, workflow documentation, provenance records, and registry/mapping pipeline outputs.

## Functional Requirements
- Define a pluggable emergency classifier interface for source emergency records.
- Support precomputed UDG/AECC inputs, external command integration, service integration, or file-exchange integration.
- Resolve supported era, pricing year, and stream compatibility through the emergency transition registry before invoking any external tool or accepting precomputed outputs.
- Consume mapping pipeline outputs when source emergency fields require versioned, provenance-aware mapping into UDG or AECC classification inputs.
- Capture provenance for derived emergency classification outputs, including tool version, table version, timestamp, and input hash.
- Support no-op validation mode for users who provide precomputed official classifications.
- Fail closed when the declared tool, table, pricing year, or stream combination is incompatible or unmapped.

## Non-Functional Requirements
- Do not embed restricted or proprietary grouping/mapping logic unless permitted.
- Never silently convert between UDG and AECC without declared source provenance.
- Keep tool errors and unmapped code diagnostics visible to users.
- Preserve evidence for review, release, and validation surfaces so the track can be audited without exposing restricted source material.

## Acceptance Criteria
- Interface covers precomputed and externally derived UDG/AECC outputs with registry-backed compatibility checks.
- Validation rejects incompatible tool/table/pricing-year/stream combinations and unmapped source fields.
- Docs explain supported emergency classification integration workflows, licensing boundaries, and evidence surfaces.

## Source Evidence
- IHACPA emergency care classification: https://www.ihacpa.gov.au/health-care/classification/emergency-care
