# NEP25 correction and canonical values

Issue #201, related parent #396. IHACPA's [19 March 2025 release](https://www.ihacpa.gov.au/news/ihacpa-releases-national-efficient-price-and-national-efficient-cost-determinations-2025-26)
states AUD7,258 per NWAU25. The prior 7,434 value was incorrect. NEP26 remains
7,418. The change affects dollar conversions, not activity weights.

Reference manifest NEP values now generate the packaged JSON resource through
`scripts/generate_pricing_constants.py`; runtime code loads that resource without
requiring a source checkout. A test checks exact manifest/resource agreement.
Documentation and tests for real price values are corrected. Synthetic historical
price-difference fixture inputs are retained as synthetic examples.

NEC metadata and broader validation-status generation are not migrated in this
bounded fix; #201 remains open for its remaining acceptance criteria. No claim of
full calculator parity follows from correcting a price constant.
