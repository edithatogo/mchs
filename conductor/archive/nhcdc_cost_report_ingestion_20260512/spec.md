# Specification: NHCDC Cost Report Ingestion

## Overview
Add tooling to ingest public NHCDC cost report appendices and data request specifications where IHACPA publishes them. This supports costing-study tutorials, benchmarking examples, and public cost-weight analysis without incorporating confidential patient-level submissions.

## Functional Requirements
- Discover and manifest NHCDC public sector reports, appendices, and data request specification files by year.
- Ingest public appendix tables into versioned Arrow/Parquet or CSV-normalized datasets where licensing permits.
- Preserve source URLs, checksums, publication dates, retrieval dates, and table-level provenance.
- Add data dictionary extraction for public data request specification fields where feasible.
- Link cost report tables to cost bucket registry concepts where applicable.

## Non-Functional Requirements
- Public reports are aggregate/reference material, not patient-level costing datasets.
- Ingested tables must be reproducible and reviewable.
- Missing or format-changing appendices must be recorded as gaps.

## Acceptance Criteria
- At least one public NHCDC appendix ingestion can be represented through a manifest and normalized output.
- Tests cover workbook/table parsing using safe fixtures.
- Docs explain what can and cannot be inferred from public NHCDC cost reports.

## Source Evidence
- NHCDC public sector: https://www.ihacpa.gov.au/health-care/costing/national-hospital-cost-data-collection/national-hospital-cost-data-collection-public-sector
- NHCDC public sector 2023-24: https://www.ihacpa.gov.au/resources/national-hospital-cost-data-collection-nhcdc-public-sector-2023-24
- NHCDC public sector report 2015-16: https://www.ihacpa.gov.au/resources/national-hospital-cost-data-collection-nhcdc-public-sector-report-2015-16
