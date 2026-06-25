# NHCDC Ingestion Pipeline

## Overview

Tooling and conventions for discovering, retrieving, parsing, and normalizing public NHCDC cost report appendices and data request specifications published by IHACPA. This supports costing-study tutorials, benchmarking examples, and public cost-weight analysis without incorporating confidential patient-level submissions.

## Source Discovery

### Public NHCDC Reports

IHACPA publishes public NHCDC sector reports by financial year. Each report typically includes:

- Aggregate cost tables by hospital peer group, jurisdiction, and cost bucket.
- Data request specification files documenting the submission schema.
- Appendix tables with cost weights, averages, and distributions.

### Source Inventory Fields

| Field | Description |
|-------|-------------|
| `year` | Financial year of the report |
| `title` | Report title |
| `url` | Source URL |
| `file_type` | File format (PDF, XLSX, CSV, etc.) |
| `checksum` | SHA-256 checksum of the downloaded file |
| `publication_date` | Date IHACPA published the report |
| `retrieval_date` | Date the report was retrieved |
| `table_categories` | Categories of tables included in the report |
| `status` | `available`, `format-changed`, or `missing` |

### Gap Recording

When a report or appendix is unavailable or its format has changed:

- Record the gap with an explicit `gap_id`, `reason`, `scope`, and `expected_resolution`.
- Do not infer content from year-to-year copy-forward.
- Keep the inventory truthful about what is and is not available.

## Parsing and Normalization

### Supported Formats

- XLSX / XLS workbooks (via openpyxl or similar)
- CSV exports
- PDF tables (where extractable)

### Normalized Output Schema

Each ingested table is normalized to Arrow/Parquet or CSV with:

- Table-level provenance (source year, file, sheet, row range)
- Column names mapped to canonical camelCase identifiers
- Data types preserved or cast to appropriate numeric/string types
- Rows annotated with source peer group, jurisdiction, and cost bucket where applicable

### Table Categories

- Cost weight tables
- Average cost per separation tables
- Cost bucket distribution tables
- Data request specification field dictionaries

## Interpretation Limits

### What Public Reports Support

- Costing-study benchmarking and reference comparison
- Cost bucket distribution analysis by stream and product type
- Observed cost versus NWAU-funded revenue analysis
- Understanding of aggregate cost structures across peer groups and jurisdictions

### What Public Reports Do Not Support

- Patient-level costing analysis
- Inference of confidential jurisdictional submissions
- Compliance certification against AHPCS standards
- Substitution for local data governance

## Linking to Cost Bucket Registry

Each ingested table should reference the relevant cost bucket registry entries
where the table's cost buckets can be mapped to the registry definitions. This
linkage enables cross-referencing between aggregate NHCDC tables and the
registry's cost bucket metadata, caveats, and jurisdictional mappings.

## Pipeline Verification

- Each ingestion run must produce a provenance record.
- Missing or format-changing appendices must be recorded as explicit gaps.
- All ingested tables must be reproducible from the source inventory.
