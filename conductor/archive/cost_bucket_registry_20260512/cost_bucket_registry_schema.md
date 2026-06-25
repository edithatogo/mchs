# Cost Bucket Registry Schema

## Overview

The cost bucket registry provides a versioned, source-cited representation of IHACPA/NHCDC costing-bucket definitions, cost line-item mappings, and review findings. It supports costing-study workflows without treating cost buckets as NWAU formula inputs unless a source explicitly requires it.

## Registry Schema

### CostBucketEntry

| Field | Type | Description |
|-------|------|-------------|
| `bucket_id` | string | Unique identifier for the cost bucket |
| `bucket_name` | string | Display name of the cost bucket |
| `description` | string | Description of what the cost bucket captures |
| `effective_year` | string | Pricing year or year range the definition applies to |
| `source_document` | string | URL or citation of the source document |
| `source_checksum` | string | SHA-256 checksum of the source document |
| `source_publication_date` | string | Publication date of the source document |
| `ahpcs_concepts` | list[string] | Related AHPCS cost ledger concepts |
| `cost_centre` | string | Associated cost centre |
| `line_item` | string | Associated line item |
| `production_centre` | string | Associated production centre |
| `overhead_allocation` | string | Overhead allocation method or reference |
| `final_product` | string | Associated final product |
| `intermediate_product` | string | Associated intermediate product |
| `caveats` | list[string] | Known limitations or jurisdictional consistency notes |
| `data_kind` | string | Either `public` for IHACPA-published definitions or `local_overlay` for jurisdiction-specific mappings |

### LocalOverlay

| Field | Type | Description |
|-------|------|-------------|
| `overlay_id` | string | Unique identifier for the overlay |
| `jurisdiction` | string | Jurisdiction code |
| `bucket_id` | string | Reference to the parent CostBucketEntry |
| `description` | string | Jurisdiction-specific description or mapping note |
| `effective_year` | string | Year range the overlay applies to |
| `caveats` | list[string] | Local data-handling caveats |
| `data_kind` | string | Always `local_overlay` |

## Provenance Model

- Every bucket entry must link to a public IHACPA or NHCDC source document with checksum.
- Local jurisdiction overlays must be clearly distinguished from public definitions.
- The registry must never bundle confidential NHCDC submissions or jurisdiction-specific non-public data.

## Cost Bucket Use for Costing Analysis vs NWAU Calculation

Cost buckets describe how hospital costs are categorised, attributed, and reported under
AHPCS and NHCDC frameworks. They are not NWAU formula inputs unless a specific pricing
specification or calculator source explicitly uses them as such. Use the registry to:

- Map cost ledger line items to cost buckets for costing studies.
- Compare jurisdictional cost bucket structures.
- Relate cost bucket definitions to NHCDC public report tables.
- Understand the granularity and caveats documented in the Cost Bucket Review 2025.

Do not use the registry as a substitute for local costing policy or data governance.
