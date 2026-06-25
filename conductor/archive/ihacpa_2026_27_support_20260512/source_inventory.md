# IHACPA 2026-27 source inventory

Scope: official IHACPA sources for 2026-27 NEP, NEC, technical specifications, NWAU calculators, and price-weight downloads. This inventory records what is publicly available now, what the primary provenance is, and where the current gaps remain.

## Inventory

| Area | Official IHACPA source | Public artefacts / availability | Publication / update | Provenance / licensing notes | Status / notes |
| --- | --- | --- | --- | --- | --- |
| NEP | [National Efficient Price Determination 2026–27](https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27) | PDF download and separate XLSX price-weight tables linked from the page. Direct file observed: [NEP PDF](https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_price_determination_2026-27_2.pdf) | Page says `Date published: 11 March 2026`; page `Last updated: 16 Mar 2026`; PDF cover is `March 2026` and the instrument is dated `4 March 2026` | PDF states CC BY 4.0, except IHACPA logo/photos/images/signatures and where otherwise stated | NEP26 is explicitly set at **$7,418 per NWAU(26)** (NEP Determination 2026–27, clause 9, p. 8). The PDF TOC includes price-weight appendices H-N, so the PDF is also a valid source for the embedded tables. |
| NEC | [National Efficient Cost Determination 2026–27](https://www.ihacpa.gov.au/resources/national-efficient-cost-determination-2026-27) | PDF download only on the resource page. Direct file observed: [NEC PDF](https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_cost_determination_2026-27.pdf) | Page says `Date published: 11 March 2026`; page `Last updated: 13 Mar 2026`; PDF cover is `March 2026` and the instrument is dated `4 March 2026` | PDF states CC BY 4.0, except IHACPA logo/photos/images/signatures and where otherwise stated | NEC26 headline values are visible in the resource page: fixed cost `$3.127m`, variable cost `$8,003`, and 364 small rural hospitals in scope. |
| Technical specification | [National Pricing Model Technical Specifications 2026–27](https://www.ihacpa.gov.au/resources/national-pricing-model-technical-specifications-2026-27) | PDF and DOCX downloads, plus HAC and AHR companion technical specs. Direct file observed: [Technical Specs PDF](https://www.ihacpa.gov.au/sites/default/files/2026-03/National_Pricing_Model_Technical_Specifications_2026-27.PDF) | Page says `Date published: 11 March 2026`; page `Last updated: 13 Mar 2026`; PDF cover is `March 2026` | PDF states CC BY 4.0, except IHACPA logo/photos/images/signatures and where otherwise stated | The PDF explicitly says the 2026-27 national pricing model comprises an NEP, price weights, and adjustments. It also states the model is based on 2023-24 cost and activity data. |
| Classification versions | [National Efficient Price Determination 2026–27](https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27) and [AR-DRG Version 12.0](https://www.ihacpa.gov.au/resources/ar-drg-version-120) | NEP26 states admitted acute care uses AR-DRG Version 12.0 and non-admitted services use Tier 2 Non-Admitted Services Classification Version 10.0 | NEP26 page says `Date published: 11 March 2026`; AR-DRG v12.0 page is the stable classification landing page | Classification documents may include licensed classification material; keep source links/provenance without bundling restricted tables | Record AR-DRG v12.0 and Tier 2 Version 10.0 compatibility as source metadata. Do not derive or redistribute licensed grouper/classification content. |
| NWAU calculators | [NWAU calculators](https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators) | 2026-27 SAS-based calculators are available from the year section; service-stream `.xlsb` files are linked individually and the page also exposes a 2026-27 archive download | Page `Last updated: 7 May 2026`; no `Date published` field displayed | Page states the calculators are hosted on an external file-sharing site (Box.com) and warns some networks may block access; no separate archive license statement was captured in this pass | 2026-27 coverage is present with 7 Excel calculators and 1 SAS `.7Z` archive. See artifact table below for full details. |
| Price weights | NEP determination page plus NEP PDF | Public download availability is the XLSX table on the NEP resource page, and the NEP PDF includes price-weight appendices. No separate standalone price-weight page was found. | Same publication surface as NEP: page `11 March 2026` / `16 Mar 2026`; PDF `March 2026` | Same licensing as the NEP PDF for the embedded tables; the XLSX download is an official IHACPA artefact but its standalone license statement was not separately captured here | Use the XLSX as the primary machine-readable price-weight source; use the PDF appendices when cross-checking the narrative and appendix tables. Checksum status: captured for the XLSX download; standalone file-level licence remains not separately captured. |

## NEP26 headline value

The National Efficient Price for 2026–27 is **$7,418 per NWAU(26)**.

- **Source:** National Efficient Price Determination 2026–27, clause 9, p. 8.
- **Direct URL:** [NEP26 PDF](https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_price_determination_2026-27_2.pdf)
- **Citation:** Independent Health and Aged Care Pricing Authority, *National Efficient Price Determination 2026–27*, March 2026.

## Artifacts: NWAU 2026-27 calculators

All artifacts obtained from the [IHACPA NWAU calculators page](https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators) (Last updated: 7 May 2026). Hosted on IHACPA's Box.com distribution point. These are official IHACPA-published files and redistribution is restricted per the IHACPA website terms of use.

All checksums are SHA-256, computed 12 May 2026 against the locally archived copies.

### SAS archive (not extracted)

| File | Path | Size | SHA-256 | Published | Extraction status |
| --- | --- | --- | --- | --- | --- |
| `NEP26_SAS_NWAU_Calculator.7Z` | `archive/ihacpa/raw/2026/sas/NEP26_SAS_NWAU_Calculator.7Z` | 43 MB | `28b10b972992e6b655f402367d781de73ebc469fad34709fae112629173eb7da` | 7 May 2026 | Not extracted — raw `.7Z` archive; contents unknown without extraction |

### Excel calculators (raw, unmodified)

All files are IHACPA-published `.xlsb` workbooks stored under `archive/ihacpa/raw/2026/excel/`. No modifications have been made to the downloaded originals.

| File | Path | Size | SHA-256 | Published |
| --- | --- | --- | --- | --- |
| `nwau26_calculator_for_acute_activity.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_acute_activity.xlsb` | 1.4 MB | `7a2b95ce139ad49b0f8b57f4d2438c887e8358ab7553298ec731fcca0ca59ad6` | 7 May 2026 |
| `nwau26_calculator_for_ed_activity_aecc.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_ed_activity_aecc.xlsb` | 131 KB | `26f9d57e7d1def79377575d81f3930239868d25b4ab224f2c97d33b00f9d54a3` | 7 May 2026 |
| `nwau26_calculator_for_ed_activity_udg.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_ed_activity_udg.xlsb` | 75 KB | `498f954d1ef5cd312e6e45f554e4ad68ed0aecd1b3f7852d4ae1e6846ef50357` | 7 May 2026 |
| `nwau26_calculator_for_mental_health_activity_admitted.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_mental_health_activity_admitted.xlsb` | 707 KB | `89903a6e32c7f14b6ecccf1ebac6d33c0789bff318717681bf9452abf963152b` | 7 May 2026 |
| `nwau26_calculator_for_mental_health_activity_community.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_mental_health_activity_community.xlsb` | 627 KB | `0d797cb0637cf2017121e1ecc02828e81828ec6bc393648a7da8ea4bda4d6145` | 7 May 2026 |
| `nwau26_calculator_for_non-admitted_activity.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_non-admitted_activity.xlsb` | 118 KB | `5f4a465371606a686f6194601056ee479b0e13654a7e959e6a1c4dfe5810328d` | 7 May 2026 |
| `nwau26_calculator_for_subacute_activity.xlsb` | `archive/ihacpa/raw/2026/excel/nwau26_calculator_for_subacute_activity.xlsb` | 149 KB | `80222d5afc6fd565ae47692354ac08f719b982eb6ca176cc100ea2f10c204f55` | 7 May 2026 |

### Determination and technical specification downloads

These hashes were computed 12 May 2026 against fresh downloads from the official
IHACPA resource-page links. They are not proof of calculator parity; they only
record source-file identity for provenance.

| File | URL | Size | SHA-256 | Publication surface |
| --- | --- | --- | --- | --- |
| `national_efficient_price_determination_2026-27_2.pdf` | `https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_price_determination_2026-27_2.pdf` | 2,575,944 bytes | `2162d941f5b75548b1bbf82377e20b0a63c215afefbb8e9b920b85dac5611aab` | NEP page, published 11 March 2026, updated 16 Mar 2026 |
| `National_Efficient_Price_Determination_2026-27_Price_Weight_Tables.XLSX` | `https://www.ihacpa.gov.au/sites/default/files/2026-03/National_Efficient_Price_Determination_2026-27_Price_Weight_Tables.XLSX` | 140,297 bytes | `cca4212fccca2e40b741ee4279d8cf67c2b35a277049865c8453d485f6086fc3` | NEP page, published 11 March 2026, updated 16 Mar 2026 |
| `national_efficient_cost_determination_2026-27.pdf` | `https://www.ihacpa.gov.au/sites/default/files/2026-03/national_efficient_cost_determination_2026-27.pdf` | 833,101 bytes | `29f2f526aa54d09d5cf7a98a83598ef23ee4f5774fb66b6648ab49ec0a624836` | NEC page, published 11 March 2026, updated 13 Mar 2026 |
| `National_Pricing_Model_Technical_Specifications_2026-27.PDF` | `https://www.ihacpa.gov.au/sites/default/files/2026-03/National_Pricing_Model_Technical_Specifications_2026-27.PDF` | 1,902,530 bytes | `ff6d8e34dd56633559de0a4e58c6d0a563e62ca317f737b8439783111c86aa98` | Technical specifications page, published 11 March 2026, updated 13 Mar 2026 |
| `National_Pricing_Model_Technical_Specifications_2026-27.DOCX` | `https://www.ihacpa.gov.au/sites/default/files/2026-03/National_Pricing_Model_Technical_Specifications_2026-27.DOCX` | 1,535,462 bytes | `47f28004b9b47050d921e5090a690d041126543ca436d051b20af75b5fcadc40` | Technical specifications page, published 11 March 2026, updated 13 Mar 2026 |

### Checksum coverage

- **Captured:** SHA-256 hashes are recorded above for the 2026-27 NWAU SAS archive, all seven Excel calculator workbooks, the NEP PDF, the NEP price-weight XLSX, the NEC PDF, and the national pricing model technical-specification PDF/DOCX downloads.
- **Not yet captured:** HAC and AHR companion technical-specification downloads are listed on the technical-specification page but are outside this track's core NEP/NEC/model source contract; they should be covered by a safety-and-quality follow-on track before HAC/AHR parity claims are expanded.
- **Boundary:** where a downloadable artefact exists but has not yet been archived and hashed locally, treat checksum status as unknown rather than inferred.

### Licensing and provenance notes

- All artifacts listed above are published by the Independent Health and Aged Care Pricing Authority (IHACPA).
- The NEP and NEC PDFs are published under CC BY 4.0 (excluding IHACPA logo/photos/images/signatures and where otherwise stated).
- The NWAU calculator files are hosted on IHACPA's Box.com distribution. They are official IHACPA publications but no standalone open license (e.g. CC BY) is declared on the calculators page. Redistribution is subject to IHACPA website terms of use.
- Locally archived copies are stored in `archive/ihacpa/raw/2026/` and must not be redistributed outside the project without verifying terms.
- SHA-256 checksums were computed 12 May 2026 against local copies. Checksums should be re-verified when re-downloading from IHACPA.

### Source and redistribution boundaries

- The official IHACPA resource pages are the provenance source for publication/update dates and download availability.
- File contents are the provenance source for embedded tables, cover dates, instrument dates, and file-level licence statements.
- The NEP PDF is the canonical source for the narrative determination text and the embedded price-weight appendices; the XLSX download is a machine-readable companion, not a separate policy statement.
- Do not infer redistribution rights from file availability alone. If a file-level licence statement is missing or not yet captured, record that as a gap and keep the artefact inside the project boundary.
- Do not bundle or redistribute IHACPA-published source files outside the project unless the applicable file-level and website terms have been checked.

## Explicit gaps

- **Unavailable: NEP26 compiled/Python reference files from IHACPA.** IHACPA distributes NWAU calculators only as SAS `.7Z` archives and `.xlsb` Excel workbooks. No standalone Python, R, or compiled reference implementation is published. Any Python reimplementation must be validated directly against the SAS and/or Excel outputs.
- **Unavailable: NEP26 user guides or calculator documentation.** The NWAU calculators page (as of 7 May 2026) links only to the calculator files themselves. No separate methodology guide, technical note, or user manual specific to the 2026-27 calculators has been identified.
- **Deferred: HAC and AHR companion technical-specification checksums.** These companion downloads are visible on the technical-specification page but are not part of this track's core NEP/NEC/model-source completion evidence.
- **Unavailable: separate standalone NEC price-weight table file.** Price-weight material is published through the NEP determination and its appendix tables only.
- **Unavailable: file-level licence statements on the resource pages themselves.** Licence status was taken from the PDFs where available, and the calculators page does not declare a separate open licence for the `.7Z` or `.xlsb` artefacts.
- **Unexamined: the SAS `.7Z` archive has not been extracted.** Its internal contents (SAS programs, lookup tables, macros, etc.) are not enumerated here. Extraction and census of those contents is a downstream task.
- **Unexamined: Excel `.xlsb` files are raw, unmodified copies** of the IHACPA-published originals. No attempt has been made to unpack or audit the internal worksheet structure in this pass.

## Source notes

- NEP and NEC determinations both refer back to the 2026-27 pricing model and the IHACPA pricing framework.
- The technical-specification PDF is the best provenance source for model methodology and the relationship between NEP, price weights, and adjustments.
- The NWAU calculators page is the best provenance source for operational calculator availability, but it is intentionally conservative about access and hosting details.
- The publication date for all NWAU calculator artifacts is inferred from the NWAU calculators page `Last updated: 7 May 2026`. Individual files do not carry independent date stamps on the page.
- Where the inventory cannot confirm a checksum, publication date, or licence from the captured source surface, it records that as an explicit gap rather than inferring from nearby artefacts.
- NEP26 calculator parity validation is not claimed by this inventory. Parity requires SAS and/or Excel output comparison tests, not source-file availability alone.
