# Specification: IHACPA 2026-27 Support

## Overview
Add support planning and implementation coverage for IHACPA 2026-27 pricing materials. IHACPA has published NEP26 with NEP set at $7,418 per NWAU and classification changes including AR-DRG Version 12.0 for admitted acute care and Tier 2 Version 10.0 for non-admitted services.

## Functional Requirements
- Add a structured source manifest entry for 2026-27 NEP, NEC, technical specifications, price-weight tables, and calculator downloads when available.
- Add versioned pricing constants for NEP26 and related metadata.
- Add ingestion support for 2026-27 price-weight tables with provenance metadata.
- Add compatibility tracking for AR-DRG v12.0 and Tier 2 v10.0.
- Update docs and validation matrices to distinguish available source material, extracted data, and validated calculator output.

## Non-Functional Requirements
- Do not claim calculator parity until verified against official IHACPA calculator outputs or source logic.
- Preserve source traceability for every 2026-27 value.
- Keep validation conservative and auditable.

## Acceptance Criteria
- 2026-27 appears in the supported-year matrix with explicit validation status.
- NEP26 value is available through a tested API or data accessor.
- 2026-27 source links and checksums are captured where downloadable artifacts are available.
- Documentation explains classification version impacts.

## Source Evidence
- IHACPA National Efficient Price Determination 2026-27: https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27
- IHACPA National Pricing Model Technical Specifications index: https://www.ihacpa.gov.au/health-care/pricing/national-pricing-model-technical-specifications
- IHACPA NWAU calculators: https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators
