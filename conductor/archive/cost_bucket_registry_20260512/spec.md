# Specification: Cost Bucket Registry

## Overview
Add a versioned cost bucket registry for IHACPA/NHCDC costing-bucket definitions, cost line-item mappings, and review findings. This should support costing-study workflows without treating cost buckets as NWAU formula inputs unless a source explicitly requires it.

## Functional Requirements
- Represent cost bucket names, identifiers, descriptions, version/effective year, and source document provenance.
- Represent relationships to AHPCS cost ledger concepts, cost centres, line items, production centres, overhead allocation, and final/intermediate products.
- Capture known limitations from IHACPA cost bucket review material, including granularity and jurisdictional consistency caveats.
- Link cost bucket metadata to NHCDC public reports and data request specifications where applicable.
- Support local jurisdiction-specific mapping overlays without committing sensitive or non-public data.

## Non-Functional Requirements
- Do not bundle confidential NHCDC submissions or jurisdiction-specific non-public mappings.
- Cost bucket metadata must be versioned and source-cited.
- The registry must distinguish public IHACPA definitions from local costing-study mappings.

## Acceptance Criteria
- At least one public AHPCS/NHCDC-era registry example is represented.
- Registry tests cover versioned definitions, public source provenance, and local overlay references.
- Docs explain cost bucket use for costing analysis versus NWAU calculation.

## Source Evidence
- AHPCS: https://www.ihacpa.gov.au/health-care/costing/australian-hospital-patient-costing-standards
- NHCDC public sector: https://www.ihacpa.gov.au/health-care/costing/national-hospital-cost-data-collection/national-hospital-cost-data-collection-public-sector
- Cost Bucket Review 2025: https://www.ihacpa.gov.au/sites/default/files/2025-11/cost_bucket_review_2025.pdf
