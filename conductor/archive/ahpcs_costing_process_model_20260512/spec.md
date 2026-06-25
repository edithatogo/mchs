# Specification: AHPCS Costing Process Model

## Overview
Model Australian Hospital Patient Costing Standards (AHPCS) costing-process concepts so users can prepare and validate costing-study inputs. This complements NWAU calculation by providing structure for cost ledger, cost centres, products, allocation methods, and cost bucket analysis.

## Functional Requirements
- Represent AHPCS concepts including cost ledger, production cost centres, overhead cost centres, products, intermediate products, final products, line items, offsets, recoveries, and relative value units.
- Add optional validation models for costing-study input tables.
- Add docs that map AHPCS stages to package-supported workflows.
- Keep costing-process validation separate from NWAU formula kernels.

## Non-Functional Requirements
- AHPCS models are guidance/validation aids, not replacement official standards.
- The package must not claim compliance certification.
- Users must remain responsible for local costing policy and data governance.

## Acceptance Criteria
- AHPCS concept model and docs exist for costing-study workflows.
- Synthetic examples show cost ledger to cost bucket preparation.
- Tests validate basic schema and diagnostic behavior.

## Source Evidence
- AHPCS: https://www.ihacpa.gov.au/health-care/costing/australian-hospital-patient-costing-standards
- AHPCS Version 4.0 costing guidelines: https://www.ihacpa.gov.au/resources/australian-hospital-patient-costing-standards-version-40
