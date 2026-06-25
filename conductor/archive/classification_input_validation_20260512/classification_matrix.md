# Classification compatibility matrix

Conservative validation rule: accept only versions that IHACPA explicitly supports in the cited public sources. Do not silently coerce between versions. Treat older years as legacy/back-cast only unless a separate rule is added later.

Validation legend:

- `current` = in force for the stated year
- `legacy` = historical only; do not accept for new validation without a back-cast rule
- `planned` = announced by IHACPA but not yet effective as of `2026-05-12`
- `n/a` = no official version in force for that classification in that year

## Year-by-year matrix

| Financial year | AR-DRG | AECC (ED levels 3B-6) | UDG (emergency service levels 1-3A) | Tier 2 | AMHCC | Validation status |
| --- | --- | --- | --- | --- | --- | --- |
| 2022-23 | 10.0 | n/a | 1.3 | 7.0 | 1.0 | legacy |
| 2023-24 | 11.0 | 1.0 | 1.3 | 8.0 | 1.0 | current |
| 2024-25 | 11.0 | 1.0 | 1.3 | 9.0 | 1.0 | current |
| 2025-26 | 11.0 | 1.1 | 1.3 | 9.1 | 1.1 | current |
| 2026-27 | 12.0 | 1.1 | 1.3 | 10.0 | 1.1 | planned for go-live on 1 Jul 2026 |

## Notes for input validation

- `AR-DRG` is the licensed / non-redistributable stream. IHACPA says the manuals, mapping tables and code lists are purchased under licence, via Lane Print. Do not redistribute those products.
- `AECC` applies to emergency department presentations. `UDG` remains the emergency service classification. Do not treat them as interchangeable.
- `Tier 2` has a current-source discrepancy for 2025-26: the current Tier 2 resource page says `Version 9.1`, while the 2025-26 three-year data plan table still shows `Version 9.0`. Use the current Tier 2 resource page and NEP25/NEP26 publications as the validation source of truth.
- `AMHCC` Version 1.0 was approved in 2016 and implemented on a best-endeavours basis from 1 July 2016. IHACPA’s 2025-26 pricing framework uses `AMHCC Version 1.1` for both admitted and community mental health care.
- For years earlier than 2022-23, reject by default unless you add explicit historical back-cast mappings. The public sources show earlier versions exist, but they are outside the conservative validation window for this track.

## Official transition anchors

- `AR-DRG`: Version 8.0 implemented from 1 July 2016, Version 9.0 from 1 July 2018, Version 10.0 from 1 July 2020, Version 11.0 from 1 July 2023, Version 12.0 proposed from 1 July 2026.
- `AECC`: Version 1.0 used for NEP24 / 2024-25; Version 1.1 is used for NEP25 / 2025-26 and NEP26 / 2026-27.
- `UDG`: Version 1.2 was used in NEP12 / 2012-13, Version 1.3 has been used since NEP13 / 2013-14 and remains current.
- `Tier 2`: Version 8.0 was used for NEP23 / 2023-24, Version 9.0 for NEP24 / 2024-25, Version 9.1 for NEP25 / 2025-26, and Version 10.0 for NEP26 / 2026-27.
- `AMHCC`: Version 1.0 is the baseline legacy version; Version 1.1 is the current pricing version in NEP25 / 2025-26 and NEP26 / 2026-27.

