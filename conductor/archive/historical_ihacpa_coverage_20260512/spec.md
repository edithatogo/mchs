# Specification: Historical IHACPA Coverage Audit

## Overview
Audit how far IHACPA public materials go back and update the project roadmap accordingly. Current evidence shows NEP and national pricing model technical specifications go back to 2012-13, while the public NWAU calculator page appears to expose calculator downloads from 2013-14 onward. NHCDC and costing evidence go further back but should not be treated as annual NWAU calculator support.

## Functional Requirements
- Verify all available NEP determinations from 2012-13 through current year.
- Verify National Pricing Model Technical Specifications from 2012-13 through current year, including 2012-13 not listed on the current index page.
- Verify public NWAU calculator download coverage and record whether 2012-13 calculators exist or are absent.
- Inventory older NHCDC reports and cost-weight tables separately from NWAU calculator sources.
- Update source manifests, docs, and roadmap matrices to distinguish pricing specifications, calculator artifacts, and costing evidence.

## Non-Functional Requirements
- Do not infer calculator support from cost reports alone.
- Treat 2012-13 as a special foundational ABF year requiring explicit caveats.
- Keep source provenance auditable with URLs, publication dates, and file hashes where downloadable.

## Acceptance Criteria
- Historical coverage matrix includes separate columns for NEP determination, technical spec, NWAU calculator, price weights, NHCDC report, and validation status.
- 2012-13 is represented accurately with a gap or source record for calculators.
- Older NHCDC/costing materials are documented as costing-study evidence rather than calculator parity sources.

## Source Evidence
- National Pricing Model Technical Specifications 2012-13: https://www.ihacpa.gov.au/resources/national-pricing-model-technical-specifications-2012-13
- National Efficient Price Determination 2012-13: https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2012-13
- National Efficient Price Determination index: https://www.ihacpa.gov.au/health-care/pricing/national-efficient-price-determination
- NWAU calculators: https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators
- NHCDC public sector: https://www.ihacpa.gov.au/health-care/costing/national-hospital-cost-data-collection/national-hospital-cost-data-collection-public-sector
