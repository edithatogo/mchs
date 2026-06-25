# Specification: Classification Input Validation

## Overview
Add explicit validation and documentation for classification systems that feed NWAU calculations: AR-DRG, AECC, UDG, Tier 2, and AMHCC. The project should validate required fields and classification-version compatibility before calculator execution.

## Functional Requirements
- Build a year-by-year classification compatibility matrix.
- Add strict input schema validators for each calculator stream.
- Add field-level diagnostics for missing or incompatible classification inputs.
- Document licensed or externally supplied classification products that cannot be redistributed.
- Add tests for valid, missing, invalid, and version-mismatched inputs.

## Non-Functional Requirements
- Validation must be deterministic and must not silently coerce incompatible classification versions.
- Error messages should be useful for analysts preparing activity datasets.
- Keep validation separate from formula execution where practical.

## Acceptance Criteria
- Docs identify required classification inputs for every stream.
- Tests cover each stream's input validation failure modes.
- Public API or CLI produces clear errors before calculation for invalid inputs.

## Source Evidence
- AR-DRG: https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system
- AECC: https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc
- UDG: https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg
- Tier 2: https://www.ihacpa.gov.au/health-care/classification/non-admitted-care/tier-2-non-admitted-services-classification
- AMHCC: https://www.ihacpa.gov.au/what-we-do/development-australian-mental-health-care-classification
