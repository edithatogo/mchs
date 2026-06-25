# Cost Bucket Analytics Tutorials

## Overview

These tutorials show how cost bucket information can support costing studies, benchmarking, and cost-versus-NWAU analysis. All examples use synthetic data and public aggregate NHCDC tables, not confidential patient-level submissions.

**Important**: Tutorials avoid implying that public aggregate data is patient-level costing data. Analytical caveats from the IHACPA Cost Bucket Review 2025 are surfaced throughout.

---

## Tutorial 1: Cost Bucket Distribution Analysis by Stream

### Goal

Compare cost bucket distributions across admitted acute, emergency, subacute, and outpatient streams using synthetic cost data mapped to public NHCDC cost bucket categories.

### Data

Synthetic cost ledger with the following structure:

| cost_centre | line_item | amount | stream | cost_bucket |
|---|---|---|---|---|
| Ward 3A | Nursing salaries | 1,200,000 | admitted_acute | A1 - Ward Nursing |
| ED North | Medical supplies | 450,000 | emergency | B2 - ED Supplies |
| OT 1 | Prostheses | 800,000 | admitted_acute | A3 - Surgical Supplies |
| Clinic B | Allied health | 300,000 | outpatient | C1 - Allied Health |

### Steps

1. Load the synthetic cost ledger into a DataFrame.
2. Group costs by `stream` and `cost_bucket`.
3. Calculate the percentage of total stream cost represented by each bucket.
4. Plot a stacked bar chart comparing bucket distributions across streams.

### Key Observations

- Admitted acute typically has the highest proportion of ward nursing and surgical costs.
- Emergency has proportionally higher ED-specific staffing and supply costs.
- Variation across streams validates expected cost structure differences.

### Caveats

- This is a synthetic example, not actual jurisdictional data.
- Actual cost bucket distributions vary significantly by hospital peer group and jurisdiction.
- The public NHCDC aggregate tables show national averages, not individual hospital profiles.

---

## Tutorial 2: Observed Cost versus NWAU-Funded Revenue

### Goal

Compare observed cost per episode (from synthetic cost data mapped to cost buckets) against NWAU-funded revenue for a sample of AR-DRGs.

### Data

Synthetic costing data for 3 sample AR-DRGs:

| DRG | Separations | Total Cost | Cost per Sep | NWAU Weight | NWAU Price ($) | Revenue per Sep |
|---|---|---|---|---|---|---|
| E62A | 250 | 6,250,000 | 25,000 | 2.50 | 10,000 | 25,000 |
| F62B | 500 | 8,000,000 | 16,000 | 1.75 | 10,000 | 17,500 |
| G62C | 150 | 3,750,000 | 25,000 | 2.80 | 10,000 | 28,000 |

### Steps

1. Calculate observed cost per separation from the cost ledger.
2. Calculate funded revenue per separation using NWAU weight and national efficient price (NEP).
3. For each DRG, compute the ratio of observed cost to funded revenue.
4. Identify DRGs where cost exceeds revenue (potential under-funding) and vice versa.
5. Plot observed cost versus funded revenue with a reference line showing parity.

### Key Observations

- DRGs can vary significantly in cost-to-revenue ratio even within the same stream.
- Systematic differences may reflect mix of cost buckets (e.g., high prostheses use vs high nursing).
- Cost bucket analysis can identify which cost categories drive above- or below-parity ratios.

### Caveats

- NWAU-funded revenue depends on the current pricing year NEP and weight; these are illustrative.
- Cost per separation depends on local costing methodology and data quality.
- Cost-to-revenue comparisons are analysis aids, not compliance or efficiency claims.

---

## Tutorial 3: Public Aggregate NHCDC Table Interpretation

### Goal

Learn how to interpret public NHCDC aggregate tables, including cost weight tables, average cost per separation, and cost bucket distribution tables.

### What the Tables Show

- **Cost weight tables**: Average cost per separation by AR-DRG and peer group.
- **Average cost per separation**: Mean and median cost across jurisdictions.
- **Cost bucket distribution**: Percentage of total cost attributed to each cost bucket (ward nursing, ICU, operating rooms, etc.).

### Common Pitfalls

- Aggregate tables show **averages**, not individual hospital profiles.
- Peer group averages mask within-group variation.
- Changes over time may reflect methodology changes, not true cost shifts.
- Small cell sizes may be suppressed or unreliable.

### Safe Interpretation Guidelines

1. Always reference the specific report year and methodology notes.
2. Compare cost bucket percentages rather than raw dollar amounts across years.
3. Use cost weight tables as benchmarks, not targets.
4. Cross-reference with the cost bucket registry for definition changes.

---

## Tutorial 4: Local Cost Bucket Mapping Overlays

### Goal

Demonstrate how a jurisdiction might define local cost bucket mapping overlays that extend or refine the national cost bucket registry definitions.

### Data

| overlay_id | jurisdiction | bucket_id | local_name | effective_year | caveat |
|---|---|---|---|---|---|
| NSW-001 | NSW | A1 - Ward Nursing | Nursing Intensity Weighting | 2025-26 | Uses local nursing hours data |
| VIC-001 | VIC | B2 - ED Supplies | ED Clinical Consumables | 2025-26 | Bundles supply and pharmacy costs |
| QLD-001 | QLD | C1 - Allied Health | Allied Health Activity | 2025-26 | Uses outpatient occasion data |

### Steps

1. Load the local overlay definitions.
2. Merge with the national cost bucket registry to show combined metadata.
3. Verify that overlays are clearly labelled as jurisdiction-specific.
4. Validate that no sensitive or non-public data is included.

### Key Observations

- Local overlays typically refine national definitions to match jurisdictional data structures.
- Some jurisdictions bundle cost buckets differently, affecting comparability.
- Overlays must be versioned and source-cited like the national registry entries.

### Caveats

- Never commit confidential jurisdictional costing data or patient-level information.
- Overlays are analysis tools, not official IHACPA definitions.
- Cross-jurisdictional comparisons using overlays require careful mapping validation.

---

## References

- IHACPA Costing: https://www.ihacpa.gov.au/what-we-do/costing
- NHCDC Public Sector: https://www.ihacpa.gov.au/health-care/costing/national-hospital-cost-data-collection/national-hospital-cost-data-collection-public-sector
- Cost Bucket Review 2025: https://www.ihacpa.gov.au/sites/default/files/2025-11/cost_bucket_review_2025.pdf
- AHPCS: https://www.ihacpa.gov.au/health-care/costing/australian-hospital-patient-costing-standards
- Cost Bucket Registry: `../cost_bucket_registry_20260512/cost_bucket_registry_schema.md`
- AHPCS Model: `../ahpcs_costing_process_model_20260512/ahpcs_model.md`
