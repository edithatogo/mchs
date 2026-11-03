# Indirect relative stay index

Implemented the Python analysis entry point in nwau_py.calculators.relative_stay. Pass disjoint StayStratum rows (stratum, separation count, total observed patient days, optional exclusion reason), the reference mean days per eligible separation for each stratum, and a benchmark identifier. The result contains actual and expected patient days, eligible count, excluded counts by reason, benchmark identifier and the ratio of totals. Missing reference strata fail the analysis.

Published arithmetic validation uses Table 4 of [Kamaraju et al.](https://ace.amegroups.org/article/view/6987/html). Multiplying the subgroup sample size by each published mean reconstructs totals at the precision available. The 174-case row reproduces 1.06 and the 44-case row reproduces 0.77. These are US observed/expected results and validate arithmetic only. The independent synthetic two-stratum test checks unequal weights and exclusions. Seven focused tests passed on Python 3.15.1.

Local application requires additional evidence. Select the indirect RSI specification and reference period, confirm AR-DRG and coding editions, local patient-day/leave rules, peer population, stratifiers and exclusions. Obtain eligible acute separations with an assigned versioned AR-DRG or inpatient coding and a qualified grouper. The existing MCHS grouper adapter accepts externally derived results. The emergency diagnosis shortlist only classifies ED diagnoses. Compare a local cohort with an independently reported aggregate before operational interpretation. An ED-defined cohort additionally requires a validated episode crosswalk.

Australian method reference: [AIHW technical appendix](https://www.aihw.gov.au/getmedia/cc34a01a-3909-4c3d-a430-686773940d88/16772-apb.pdf.aspx).

## Multi-year use and benchmark qualification

Verified that caller-supplied year-qualified strata can reproduce annual and pooled indirect results. Synthetic annual totals 60/50 and 72/80 give annual indices 1.20 and 0.90, pooled 132/130 = 1.01538. The current function does not select year, version or cohort. Pool only comparable measurements and separately disclose changes in reference. A fixed benchmark trend requires harmonised coding and eligibility across years.

Recommended extension: a versioned benchmark loader keyed by financial year, AR-DRG edition and stratum, with provenance, eligibility, day definition, duplicate/missing-key checks, numerator coverage and an annual/pooled report. Prefer separation date for fiscal assignment under a separation-based specification. Test the 30 June/1 July boundary and mixed editions. IHACPA price-determination Appendix H contains conditional ALOS for [2025–26](https://www.ihacpa.gov.au/sites/default/files/2025-03/national_efficient_price_determination_2025-26.pdf) and [2026–27](https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_price_determination_2026-27.pdf). These are candidates for a separately labelled pricing-reference analysis. The exclusions for designated same-day and unbundled ICU need matching local data. No official RSI denominator qualified in this review.

## Implemented multi-year loader, 3 November 2026

Local Python API in nwau_py.calculators.stay_benchmarks. Supply a UTF-8 CSV with columns kind,start_year,edition,stratum,expected_days,source. Use one coherent series per kind per file, with a stable source identifier documenting population, exclusions and day rules. Load with load_benchmarks(path). Pass dated, disjoint StayStratum records wrapped in DatedStay to calculate_stay_report(rows, registry, kind=...). Choose pricing_alos or rsi explicitly. Assignment uses separation date and financial-year starting year. Annual and pooled results retain source, edition, eligible and excluded counts and patient-day totals. Missing strata or mismatched eligible editions stop calculation. Caller qualifies the source and applies eligibility before aggregation. The CSV label does not establish official benchmark status. A year with no eligible denominator cannot yield an index.

Tested the same published pricing stratum on 30 June and 1 July 2026 with different editions, synthetic observed days, independent annual and pooled arithmetic, missing RSI references, and wrong editions. Eleven focused tests passed with the existing RSI tests on Python 3.15.1. This is a normalised CSV loader; official Appendix H workbooks are not bundled or automatically converted.

## All-year official pricing ALOS import — 3 November 2026

[scripts/import_pricing_alos.py](../scripts/import_pricing_alos.py) imports the official annual sources pinned in the [source register](../scripts/ihacpa_pricing_alos_sources.json). Download the entries with a non-null check_801B to one directory using their specified filenames. With the pricing-import extra and Poppler pdftotext installed, run `.venv/bin/python scripts/import_pricing_alos.py SOURCE_DIR OUTPUT.csv`. Source SHA-256, edition header, DRG uniqueness, positive finite published values and the independently read annual 801B control are checked before replacing the output. This feeds load_benchmarks directly. All rows use pricing_alos exclusively.

| FY starting | Edition | Input | Numeric ALOS values |
|---|---|---|---:|
| 2012, 2013 | 6.x | Published acute tables contain bounds and weights without a usable ALOS column | 0 |
| 2014, 2015 | 7.0 | Published determination PDF tables (historical fallback) | 768 each |
| 2016, 2017 | 8.0 | Official ZIP / XLSB | 802 each |
| 2018, 2019 | 9.0 | Official ZIP / XLSB | 798 each |
| 2020, 2021, 2022 | 10.0 | Official XLSX | 792 each |
| 2023, 2024, 2025 | 11.0 | Official XLSX | 798 each |
| 2026 | 12.0 | Official XLSX | 807 |

All 10,313 year/DRG rows loaded on Python 3.15.1. All 8,777 numeric workbook rows were compared with the corresponding annual determination PDF tables, including a separate five-code check for the final shifted columns in 2018. The 1,536 historical PDF values are single-source extracts with edition and control checks. In 2016–2019 Z60A and Z60B have blank ALOS and are omitted. All twelve consecutive June/July switches and pooled results passed using the imported 801B series; the existing eleven RSI/loader tests passed. This is a pricing comparator with its source day rules. No official clinical RSI denominator or local DRG assignment follows from the import.
