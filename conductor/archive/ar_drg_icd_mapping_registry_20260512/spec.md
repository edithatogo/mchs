# Specification: AR-DRG ICD/ACHI/ACS Mapping Registry

## Overview
Add a roadmap capability for versioned mapping between ICD-10-AM diagnosis codes, ACHI intervention codes, ACS coding standards, and AR-DRG versions. AR-DRGs are derived from coded admitted-episode data using version-specific grouping logic and tables, so the project needs explicit version tracking and table provenance rather than treating AR-DRG as a simple input column.

## Contract
- The registry is a provenance-aware metadata layer, not a redistribution channel for licensed classification products.
- Registry records must identify the code family, version, effective period, pricing-year applicability, and source basis for each supported relationship.
- Public metadata, locally supplied licensed files, and derived validation fixtures must remain distinct and machine-identifiable.
- Compatibility checks must fail closed when the ICD-10-AM, ACHI, ACS, or AR-DRG version relationship is incomplete, unsupported, or ambiguous.
- Track outputs are documentation, registry metadata, and validation rules; they do not include proprietary grouping logic or restricted source tables unless the user supplies them locally and the license permits use.

## Functional Requirements
- Extend the coding-set registry with explicit relationships between ICD-10-AM, ACHI, ACS, and AR-DRG versions.
- Track mapping table families by AR-DRG version and effective pricing years.
- Represent version-specific code validity, diagnosis/intervention mapping, and grouping-table provenance where legally available.
- Support local references to licensed mapping tables without committing restricted content.
- Link admitted-acute input validation to the expected ICD-10-AM/ACHI/ACS and AR-DRG version set.

## Non-Functional Requirements
- Do not redistribute licensed IHACPA classification products unless permitted.
- Registry entries must distinguish public metadata, user-supplied licensed files, and derived validation fixtures.
- Mapping metadata must be strict enough to prevent mixing incompatible ICD-10-AM/ACHI/ACS and AR-DRG versions.
- Registry and documentation should stay conservative whenever a source table, version relationship, or license boundary cannot be verified from public evidence.

## Acceptance Criteria
- The roadmap defines how AR-DRG versions relate to ICD-10-AM/ACHI/ACS versions by pricing year.
- Admitted acute validation can identify incompatible coding-set combinations.
- Documentation explains which mapping/grouping assets users must supply locally.
- The track contract clearly distinguishes registry metadata from licensed tables and grouping logic.
- The plan and checkpoints stay aligned with the current roadmap-only state until implementation evidence exists.

## Source and Licensing Caveats
- IHACPA materials describe the classification system, but they do not grant permission to redistribute licensed code lists or grouping tables.
- Any local file references to ICD-10-AM, ACHI, ACS, or AR-DRG assets must stay outside version control unless the license explicitly allows committing them.
- When a relationship is known only from user-supplied licensed files, the registry should record the local reference and avoid asserting public provenance.
- If a source relationship cannot be confirmed, the track should prefer a conservative placeholder over inventing a crosswalk.

## Source Evidence
- IHACPA admitted acute care: https://www.ihacpa.gov.au/health-care/classification/admitted-acute-care
- IHACPA AR-DRGs: https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system
- IHACPA AR-DRG Version 12.0: https://www.ihacpa.gov.au/resources/ar-drg-version-120
