# Specification: Costing-Study Tutorials and Examples

## Overview
Create comprehensive tutorials showing how analysts can use the package for costing studies, not only calculator parity. Tutorials should use synthetic data and explain the relationship between calculated NWAU, NEP, patient-level costs, NHCDC, AHPCS, and stream-level benchmarking.

## Functional Requirements
- Add a docs section for costing-study workflows.
- Add synthetic datasets that resemble activity and cost inputs without exposing protected hospital data.
- Demonstrate funded revenue calculation using NWAU multiplied by NEP.
- Demonstrate observed cost versus efficient price comparisons.
- Demonstrate stream-level and classification-level summaries.
- Explain how AHPCS and NHCDC relate to source data quality and interpretation.

## Non-Functional Requirements
- Examples must be runnable in docs or tests where practical.
- Tutorials must avoid implying that synthetic examples are official IHACPA outputs.
- Documentation must distinguish pricing, funding, costing, and benchmarking concepts.

## Acceptance Criteria
- Starlight docs include at least three costing-study tutorials.
- Synthetic data fixtures are committed with clear provenance and no real-patient data.
- Tutorials include reproducible commands or code snippets.

## Source Evidence
- Costing overview: https://www.ihacpa.gov.au/health-care/costing/costing-overview
- NHCDC: https://www.ihacpa.gov.au/health-care/costing/national-hospital-cost-data-collection
- AHPCS: https://www.ihacpa.gov.au/ahpcs
- Costing studies: https://www.ihacpa.gov.au/what-we-do/costing-studies
- NHCDC public sector report: https://www.ihacpa.gov.au/resources/national-hospital-cost-data-collection-nhcdc-public-sector-2022-23
