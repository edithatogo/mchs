# AHPCS Costing Process Model

## Overview

This model represents Australian Hospital Patient Costing Standards (AHPCS) costing-process concepts as validation aids for costing studies. It complements NWAU calculation by providing structure for cost ledger, cost centres, products, allocation methods, and cost bucket analysis.

**Important**: These models are guidance and validation aids, not a replacement for official AHPCS standards. The package does not claim compliance certification. Users remain responsible for their local costing policy and data governance.

## Concept Model

### Cost Ledger

The cost ledger is the master record of all costs incurred by a hospital or health service. It captures:

- Total expenditure by cost centre and line item
- Direct and indirect cost attribution
- Offsets, recoveries, and adjustments
- Relative value units (RVUs) for allocation

### Production Cost Centres

Cost centres that deliver patient care services directly. Examples:

- Inpatient wards (by specialty)
- Emergency departments
- Operating theatres
- Intensive care units
- Outpatient clinics

Each production cost centre has:

- Direct costs (labour, supplies, drugs)
- Overhead allocation from support cost centres
- Output measures (separations, occasions of service, weighted activity)

### Overhead Cost Centres

Cost centres that support production activities but do not deliver direct patient care. Examples:

- Hospital administration
- Information technology
- Facilities management
- Human resources
- Finance and accounting

Overhead costs are allocated to production cost centres using allocation keys based on usage, activity, or other agreed principles.

### Products

#### Final Products

Costed patient output measured by episode type:

- Admitted acute separations (by AR-DRG)
- Emergency presentations (by URG/AECC category)
- Subacute and non-acute care days (by AN-SNAP class)
- Outpatient service events (by clinic type)
- Mental health care days (by AMHCC class)

#### Intermediate Products

Supporting goods or services consumed in producing final products:

- Pathology tests
- Medical imaging procedures
- Pharmacy dispensations
- Allied health consultations

### Line Items

Detailed cost categories within a cost centre:

- Labour (nursing, medical, allied health, administrative)
- Supplies (medical, surgical, pharmaceutical)
- Drugs (ward stock, imprest, patient-charged)
- On-costs (superannuation, workers compensation)
- Depreciation
- Contracted services

### Offsets and Recoveries

- **Offsets**: Reductions to gross costs (e.g., trade discounts, rebates)
- **Recoveries**: Cost reimbursements from third parties (e.g., medicare, private health funds, patients)

### Relative Value Units (RVUs)

RVUs express the relative resource intensity of products or services within a cost centre. They are used to allocate costs from cost centres to individual products. Examples:

- Nursing workload measures (e.g., nursing intensity weights)
- Operating theatre minutes
- Imaging relative value scales
- Pharmacy dispensing weights

## Allocation Model

The standard AHPCS allocation flow is:

1. Collect total costs in each cost centre from the general ledger.
2. Identify overhead cost centres and allocate their costs to production cost centres using allocation keys.
3. Within each production cost centre, allocate total costs to intermediate and final products using RVUs.
4. Attribute allocated costs to individual patient episodes or service events.

## Relationship to NWAU Calculation

| AHPCS Concept | NWAU Calculation Relationship |
|---|---|
| Cost centres | Cost centres produce the activity that NWAU weights apply to |
| Products | NWAU prices are defined per final product (DRG, UDG, AN-SNAP) |
| Cost buckets | Cost bucket analysis can validate cost versus NWAU revenue |
| RVUs | NWAU weights are standardized RVUs applied at the national level |

## Validation Model

The package provides optional validation schemas for costing-study input tables:

- **Cost ledger schema validation**: Check required fields exist (`cost_centre`, `line_item`, `amount`, `period`)
- **Allocation key validation**: Verify allocation keys sum to 100% within each cost centre group
- **Product mapping validation**: Confirm each patient episode maps to a valid final product
- **Cost bucket mapping validation**: Check cost line items are mapped to known cost buckets

## Caveats

- AHPCS is a national standard; local health services may use modified approaches.
- Costing-process models must be adapted to jurisdictional data availability.
- The package does not replace institutional costing expertise.
- Public NHCDC tables provide aggregate reference data, not patient-level cost.
