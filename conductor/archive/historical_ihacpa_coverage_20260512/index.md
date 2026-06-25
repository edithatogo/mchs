# Track historical_ihacpa_coverage_20260512 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)

## Current State

- Historical coverage has been audited from 2012-13 through 2026-27 across NEP determinations, national pricing model technical specifications, NWAU calculator artifacts, price-weight evidence, NHCDC/costing evidence, and validation status.
- The 2012-13 NEP determination and technical specification are confirmed and hashed, but 2012-13 NWAU calculator support remains an explicit gap.
- Current calculator archive evidence starts at 2013-14 and continues through 2026-27.
- NHCDC material is documented as costing-study evidence only; it is not calculator parity evidence.
- The executable guard is `scripts/validate_historical_ihacpa_inventory.py`.
