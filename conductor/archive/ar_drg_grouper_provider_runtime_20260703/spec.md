# Specification: AR-DRG Grouper Provider Runtime

## Overview
Support pluggable AR-DRG grouper providers without redistributing proprietary grouping logic. The runtime must describe provider workflows, validate them conservatively, and preserve provenance-bearing outputs for precomputed and externally derived AR-DRG values.

## Contract
- Provider metadata must distinguish precomputed, local command, local service, file exchange, and optional container workflows.
- Compatibility checks must fail closed when the provider type, reference, year, or runtime metadata is missing or unsupported.
- Provider output records must remain provenance-bearing and validated before calculator consumption.
- The runtime may describe local-only or user-supplied workflows, but it must not ship proprietary grouper logic, vendor binaries, or restricted mapping tables.
- Support status surfaced by the runtime must be explicit and machine-readable, including `source_available`, `executable`, `validated`, `blocked_licensed`, and `out_of_scope`.

## Functional Requirements
- Expose a provider runtime registry that enumerates supported AR-DRG provider workflows.
- Support metadata-only references for precomputed outputs and local-only provider workflows.
- Validate provider compatibility for admitted-acute pricing years and fail closed for unsupported combinations.
- Build provenance-bearing AR-DRG output records from supported provider workflows.
- Surface the provider runtime through the library and CLI without requiring licensed assets to be present.

## Non-Functional Requirements
- No proprietary grouping logic may be implemented or redistributed.
- Runtime records must be deterministic and machine-readable.
- The provider runtime should reuse the existing AR-DRG grouping/provenance helpers instead of duplicating them.
- Missing licensed providers must report blocked or unsupported status instead of falling back silently.

## Acceptance Criteria
- The runtime exposes supported provider types and support-status metadata.
- Compatibility validation rejects unsupported provider/runtime combinations with clear diagnostics.
- Precomputed and local-only provider fixtures can produce validated provenance-bearing outputs.
- CLI/library consumers can inspect provider status without executing proprietary logic.
- Documentation states the local-only and container limitations clearly.

## Out of Scope
- Executing proprietary grouper binaries shipped in the repository.
- Redistributing licensed grouper software or mapping tables.
- Automatic calls to vendor-managed remote services.
- Replacing the existing AR-DRG grouping helpers with a new grouping algorithm.

## Source Evidence
- IHACPA AR-DRGs: https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system
- IHACPA admitted acute care: https://www.ihacpa.gov.au/health-care/classification/admitted-acute-care
- Track issue: https://github.com/edithatogo/mchs/issues/206

