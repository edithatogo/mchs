# Historical IHACPA Source Inventory

Scope: 2012-13 through 2026-27.

## Provenance rules

- Canonical official sources are the IHACPA URLs listed below.
- Local archive evidence is taken from `archive/ihacpa/raw/manifest.csv`, `archive/ihacpa/raw/manifest.json`, and the downloaded files under `archive/ihacpa/raw/<year>/...`.
- No hashes are fabricated in this inventory. Byte counts are only used when they are already present in the archive manifest.
- `2012-13` calculator status remains `gap/unknown` unless a direct artifact is later proven.
- NHCDC materials are recorded as cost evidence only and are not treated as calculator parity sources.

## Canonical source register

| Category | Canonical official URL | Local archive evidence |
| --- | --- | --- |
| NEP determinations | `https://www.ihacpa.gov.au/health-care/pricing/national-efficient-price-determination` | `archive/ihacpa/raw/manifest.csv` plus year-specific NEP-linked files where present |
| 2012-13 NEP determination | `https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2012-13` | Official page only; no calculator file is assumed from this page |
| Technical specifications | `https://www.ihacpa.gov.au/health-care/pricing/national-pricing-model-technical-specifications` | `archive/ihacpa/raw/manifest.csv` plus year-specific calculator bundles where applicable |
| 2012-13 technical specification | `https://www.ihacpa.gov.au/resources/national-pricing-model-technical-specifications-2012-13` | Official page only; separate from calculator evidence |
| NWAU calculators | `https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators` | `archive/ihacpa/raw/manifest.csv` and downloaded files under `archive/ihacpa/raw/<year>/...` |
| NHCDC public sector | `https://www.ihacpa.gov.au/health-care/costing/national-hospital-cost-data-collection/national-hospital-cost-data-collection-public-sector` | Costing evidence only; not calculator parity evidence |

## Foundational 2012-13 downloadable evidence

The current technical-specification index omits 2012-13, but the standalone
resource page remains available. The 2012-13 PDFs below were downloaded from
the official IHACPA resource-page links and hashed on 12 May 2026.

| Artifact | Official URL | Size | SHA-256 | Audit interpretation |
| --- | --- | --- | --- | --- |
| National Efficient Price 2012-13 PDF | `https://www.ihacpa.gov.au/sites/default/files/2022-02/National%20Efficient%20Price%202012%E2%80%9313.pdf` | 1,846,862 bytes | `460a69489e2bb4210203d35f5095851f8440d55b6a610afc1d580534c7f1983d` | Confirms pricing determination evidence only; does not prove calculator availability |
| National Pricing Model Technical Specification 2012-13 PDF | `https://www.ihacpa.gov.au/sites/default/files/2022-02/National%20Pricing%20Model%20Technical%20Specification%202012-13.pdf` | 1,625,499 bytes | `0ef844f901347b13746d9b7cb27ab98f97fb303c93ed497e0f188b0e771c7e9c` | Confirms specification evidence only; does not prove calculator availability |

## Historical coverage matrix

Legend:

- `validated` = official IHACPA page plus local archive evidence are aligned for that category.
- `partial` = official page exists, but local archive evidence is only indirect or incomplete.
- `gap/unknown` = no direct artifact has been proven in this audit.

| Year | NEP determination | Technical spec | NWAU calculators | Price weights | NHCDC / cost evidence | Validation status | Conservative provenance note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2012-13 | validated; official page at `https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2012-13` | validated; official page at `https://www.ihacpa.gov.au/resources/national-pricing-model-technical-specifications-2012-13` | gap/unknown; no direct 2012-13 calculator artifact proven | gap/unknown; do not infer from 2013-14 archive files | validated as cost evidence only; NHCDC public-sector page lists 2012-13 | partial | NEP13/NEC13 and the 2012-13 technical spec are confirmed; calculator support is not claimed |
| 2013-14 | validated via official NEP index and archived 2013 bundle | validated via technical-spec index and archived 2013 bundle | validated; archive has `archive/ihacpa/raw/2013/sas/nep13_sas_nwau_calculator.zip` and 2013 Excel calculators | validated as bundled calculator content; no standalone weight file separated | validated; NHCDC public-sector page lists 2013-14 | validated | Manifest coverage starts here for calculators; this is the first year with direct archive evidence |
| 2014-15 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2014/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2015-16 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2015/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2016-17 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2016/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2017-18 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2017/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2018-19 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2018/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2019-20 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2019/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2020-21 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2020/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2021-22 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2021/...` and the SAS bundle is recorded as a Box HTML capture | validated as bundled calculator content | validated | validated | The archive capture is partly indirect for SAS, but still records public availability |
| 2022-23 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2022/...` and the SAS bundle is recorded as a Box HTML capture | validated as bundled calculator content | validated | validated | The archive capture is partly indirect for SAS, but still records public availability |
| 2023-24 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2023/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2024-25 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2024/...` | validated as bundled calculator content | validated | validated | Local archive includes SAS and Excel calculator artifacts for the year |
| 2025-26 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2025/...` | validated as bundled calculator content | gap/unknown; NHCDC public-sector page does not yet list 2025-26 | validated for pricing sources; NHCDC pending publication | Current public NHCDC coverage stops at 2024-25 in the official index |
| 2026-27 | validated via official NEP index | validated via technical-spec index | validated; archive has `archive/ihacpa/raw/2026/...` | validated as bundled calculator content | gap/unknown; NHCDC public-sector page does not yet list 2026-27 | validated for pricing sources; NHCDC pending publication | Current public NHCDC coverage stops at 2024-25 in the official index |

## Validation summary

- `2012-13`: confirmed for NEP, technical specification, and NHCDC indexing; calculator support remains unproven.
- `2013-14` through `2024-25`: direct archive evidence exists for NWAU calculator coverage; NHCDC public-sector coverage is also present.
- `2025-26` and `2026-27`: pricing materials are present, but NHCDC public-sector publication coverage has not yet caught up.

## Residual gaps

- No direct 2012-13 NWAU calculator artifact was found in the local archive evidence reviewed for this audit.
- Price-weight evidence is tracked conservatively as bundled calculator content unless a separate standalone weight artifact is later identified.
- NHCDC materials should continue to be treated as cost evidence, not as proof of annual NWAU calculator parity.
- A full historical hash census for every NEP, technical-specification, calculator, and NHCDC downloadable artifact is outside this track; this track records the foundational 2012-13 hashes plus existing local archive evidence and requires follow-on hashing before any stronger historical support claim.
