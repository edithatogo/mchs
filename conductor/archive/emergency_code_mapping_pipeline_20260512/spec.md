# Specification: Emergency Code Mapping Pipeline

## Overview
Define a table-driven pipeline for emergency-care mapping bundles that convert declared source emergency fields into UDG-era or AECC-era classification inputs. This track is limited to mapping provenance, validation, and documentation for the emergency-code mapping path. It does not define pricing logic, clinical coding logic, or inferred crosswalks between UDG and AECC.

The pipeline must remain versioned, deterministic, and provenance-aware so every mapped output can be traced back to a specific mapping bundle, source reference, and validation status.

## Contract
- This track owns the emergency code mapping pipeline contract for source emergency fields that resolve to UDG or AECC outputs.
- The emergency UDG/AECC transition registry is the governing dependency for pricing-year and stream applicability.
- The pipeline does not synthesize a crosswalk, translate between UDG and AECC without declared source evidence, or claim compatibility that is not supported by the registry.

## Scope
- In scope: bundle schema, local reference handling, bundle validation, dry-run diagnostics, and audit-preserving mapped outputs.
- In scope: explicit linkage to the UDG/AECC transition registry so the registry selects the applicable bundle or declares the applicable era.
- Out of scope: invented crosswalks, heuristic code translation, pricing policy, and any mapping not backed by a declared official or validated local reference.

## Functional Requirements
- Define a mapping-bundle schema that declares source-field names, target classification family, bundle version, effective pricing years, checksum, provenance, and validation status.
- Support local official or locally validated mapping references as first-class inputs. References must identify the source artifact, version/date, and checksum or equivalent integrity marker.
- Add mapping diagnostics for unknown, unmapped, deprecated, invalid, and era-incompatible source values.
- Add strict rules that prevent UDG/AECC crosswalk use without a declared mapping reference and an explicit registry decision about the applicable era.
- Support dry-run mapping summaries for data-quality review and bundle comparison.

## Mapping Bundle Semantics
- A mapping bundle is an immutable, versioned artifact that binds:
  - the exact source fields it consumes,
  - the classification family it produces,
  - the pricing-year or era range it applies to,
  - the provenance reference used to justify the bundle,
  - and the validation status of the bundle.
- Bundles must be diffable by version. A new bundle version is required when the source reference, row set, validity window, or validation status changes.
- Bundles must never silently synthesize missing rows. If a source value is not present in the declared bundle, the result must be diagnostic rather than inferred.

## Source Fields
- The bundle schema must declare the source field set explicitly rather than relying on positional assumptions.
- At minimum, the bundle documentation must identify the source field categories used by the pipeline, such as:
  - emergency episode or encounter date used for era selection,
  - source emergency classification code or code fragment,
  - source system or table identifier when multiple feeds exist,
  - and any registry keys needed to align a record to the UDG/AECC transition registry.
- Raw source values must be preserved alongside mapped output fields for auditability and replay.

## UDG/AECC Transition Registry Relationship
- The transition registry is the policy layer that declares whether a record belongs to the UDG-era or AECC-era mapping path.
- The pipeline may consume registry entries, but it must not infer era boundaries or fabricate a bridge between eras.
- If the registry and a mapping bundle disagree, the record must surface a validation failure or incompatibility diagnostic rather than guess a mapping.

## Validation Surfaces
- Bundle validation must check declared source fields, effective years, checksum integrity, provenance completeness, and validation status.
- Record-level validation must emit diagnostics for mapped, unmapped, invalid, deprecated, unknown, and era-incompatible source values.
- Dry-run validation must summarize coverage, missing rows, and bundle-version mismatches for data-quality review.
- Documentation must show how to validate a bundle against a local official reference or a locally validated internal reference before publication.

## Examples
- UDG-era example: a record whose registry lookup places it in the UDG-era path should resolve through a UDG mapping bundle with a declared source reference and a preserved raw source code.
- AECC-era example: a record whose registry lookup places it in the AECC-era path should resolve through an AECC mapping bundle with a separate versioned reference and corresponding diagnostics if the source code is not found.
- Validation example: a record with a valid source code but no bundle row must surface as unmapped, not translated by heuristic fallback.

## Caveats
- Do not invent crosswalks where official or local validated mapping references are unavailable.
- Do not reuse a UDG mapping row as an AECC row unless the mapping reference explicitly authorizes that reuse.
- Do not collapse diagnostics into successful mappings; validation output must remain visible in dry-run and record-level outputs.
- Do not hide provenance. Every bundle must point to its local official or validated source reference.
- Do not redistribute licensed emergency classification tables, manuals, or grouper outputs unless the source license explicitly permits it.

## Evidence Surfaces
- `metadata.json` records the primary contract, dependency chain, completion evidence, publication status, validation status, licensing caveats, and evidence surfaces.
- `plan.md` stages governance, schema, registry-gated validation, and documentation work.
- Mapping-bundle manifests and validator tests demonstrate compatibility handling for valid, transitional, missing, deprecated, and incompatible inputs.
- Documentation shows how to prepare source fields without claiming unsupported conversion paths.

## Acceptance Criteria
- Mapping bundles can represent at least one UDG-era and one AECC-era example using explicit source references.
- Tests cover mapped, unmapped, invalid, deprecated, unknown, and era-incompatible cases.
- Docs explain how to add future emergency mapping tables and how to register or validate local official references.

## Source Evidence
- IHACPA AECC: https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc
- IHACPA UDG: https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg
