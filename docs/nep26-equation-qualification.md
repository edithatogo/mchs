# NEP26 acute equation qualification

Issue #398, parent #396. The additive API
`nwau_py.calculators.nep26_equation.evaluate` implements the equation in
[IHACPA technical specifications section 2.3](https://www.ihacpa.gov.au/sites/default/files/2026-03/National_Pricing_Model_Technical_Specifications_2026-27.PDF).
The source is March 2026, NEP 2026–27. Source: Independent Health and Aged Care
Pricing Authority; this implementation is not endorsed by IHACPA.

It returns pre-floor activity NWAU and AUD separately, requires all Decimal terms,
and does not carry the older COVID multiplier forward. ART means radiotherapy;
ATreat means treatment remoteness. ICU eligibility and the hourly weight must be
resolved upstream. A bundled-ICU flag is not an hourly weight. Shadowed HAC/AHR
terms remain explicit rather than being silently activated or zeroed.

This is an equation qualification, with a hand-calculated nonzero fixture.
It is not official-calculator parity or a complete NEP26 calculator: class weight
selection, length-of-stay categories, remoteness, facility eligibility, flooring,
rounding stages and grouping require their own evidence. Negative pre-floor
values remain inspectable. Missing data cannot be interpreted as no care.

Historical 2025 APIs remain unchanged. In particular, the historical Excel JSON
label NWAU25 includes multiplication by NEP and therefore denotes currency;
this new API does not silently redefine that legacy label. Current-year valuation
and historical-year expenditure are different estimands. No automatic regrouping
of historical ICD/DRG editions is implemented here.
