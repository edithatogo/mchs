# Specification: Emergency UDG/AECC Transition Registry

## Overview
Add a roadmap capability for emergency care classification versioning and transition handling. Emergency care classification historically used Urgency Disposition Groups (UDG) and now uses the Australian Emergency Care Classification (AECC). This track is limited to registry metadata, validation rules, and documentation for the transition boundary. It does not introduce a new clinical grouping method, and it does not assume that UDG and AECC codes are interchangeable.

## Contract
- This track owns the emergency classification transition registry contract for UDG and AECC versioning, pricing-year applicability, and emergency-stream compatibility.
- The registry is the source of truth for whether a pricing year expects UDG, AECC, a transition-period allowance, or no emergency classification input.
- The registry does not perform code conversion, crosswalk synthesis, or grouper execution.

## Functional Requirements
- Extend the coding-set registry with UDG and AECC version records and explicit source provenance.
- Track pricing-year applicability for UDG, AECC, and transition-period handling.
- Represent emergency service versus emergency department stream compatibility where the source documentation supports that distinction.
- Add validation that rejects incompatible UDG/AECC inputs for a selected pricing year.
- Document the transition from UDG to AECC, including how users should supply source fields and when precomputed classification codes are required.
- Document the difference between accepted, transitional, shadow-priced, and incompatible inputs without inventing any crosswalk.

## Non-Functional Requirements
- Do not silently translate UDG to AECC unless an official mapping or validated local mapping is supplied.
- Do not invent a crosswalk, fallback mapping, or equivalence class between UDG and AECC.
- Preserve explicit provenance for any mapping table, grouper output, or derived registry entry.
- Keep emergency classification status separate from NWAU pricing validation status.
- Respect source licensing constraints. If an official mapping or manual is licensed or otherwise restricted, capture its existence and provenance in metadata rather than redistributing raw tables in this repository.

## Acceptance Criteria
- Registry records identify which pricing years expect UDG, AECC, transition-period handling, or no emergency classification input.
- Emergency calculator validation can distinguish valid, transitional, shadow-priced, missing, and incompatible emergency classification inputs.
- Documentation explains UDG versus AECC, the supported source fields, and the fact that no invented conversion path exists.
- Documentation includes examples for pre-transition, transition-period, and post-transition usage.

## Source Evidence
- IHACPA AECC: https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc
- IHACPA UDG: https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg
- IHACPA emergency care classification: https://www.ihacpa.gov.au/health-care/classification/emergency-care

## Validation Surfaces
- Registry load-time validation for version, year, and stream compatibility.
- Emergency calculator input validation for selected pricing year and supplied source fields.
- Import or ETL validation when users provide precomputed emergency classification codes.
- Documentation review to confirm that every example is framed as an example and not a derived crosswalk.

## Evidence Surfaces
- `metadata.json` records the primary contract, dependency chain, validation status, publication status, completion evidence, and licensing caveats.
- `plan.md` stages the governance, registry, validation, and documentation work.
- Registry manifests and validator tests demonstrate compatibility handling for valid, transitional, missing, and incompatible inputs.
- Documentation shows how to prepare source fields without claiming unsupported conversion paths.

## Examples
- A pre-transition pricing year may accept UDG records if the registry marks UDG as valid for that year.
- A post-transition pricing year may accept AECC records and reject UDG records unless the registry explicitly marks a transition-period allowance.
- A transition-period record may be accepted for validation, flagged as transitional or shadow-priced, and still require provenance from the official source rather than automatic conversion.
- A missing emergency classification code should be reported as missing, not coerced into UDG or AECC.

## Completion Caveats
- This track is not complete until the registry logic, validator behavior, and documentation are all backed by evidence in the repository.
- Do not mark the track complete based on roadmap intent alone.
- Do not infer completion from the existence of source links, examples, or prose unless implementation or validation evidence is present.
