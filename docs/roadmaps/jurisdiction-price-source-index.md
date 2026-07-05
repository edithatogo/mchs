# Jurisdiction Price Source Index Plan

> Parallel-agent notice: this is a source-index plan, not extracted price data.
> Do not hard-code public or local prices without provenance, licence status,
> checksum, and support status.

## Required source fields

- `jurisdiction`
- `financial_year`
- `source_title`
- `source_url_or_path`
- `retrieved_on`
- `checksum`
- `licence_status`
- `redistribution_status`
- `source_unit`
- `mapped_unit`
- `price_term`
- `stream_applicability`
- `adjustment_notes`
- `support_status`
- `extraction_notes`

## Jurisdictions

- NSW
- VIC
- QLD
- WA
- SA
- TAS
- ACT
- NT

## Initial source classes

- NEP and national pricing determinations.
- State price or efficient price documents.
- LHD, LHN, HHS, hospital network, or territory service agreements.
- Activity schedules using NWAU, WAU, QWAU, WIES, or local terms.
- Block funding and supplementary funding schedules.
- Local discount, local price, cap/floor, or override documents.

## Extraction rule

Extract only values with source provenance and licence status. If a source is
not public or redistribution is uncertain, record metadata and mark values
`blocked` or `local_only` rather than committing restricted data.

## Implemented runtime index

The canonical machine-readable runtime source index is
`nwau_py.jurisdiction_price_sources`. It exposes source rows through
`JurisdictionPriceSourceIndex`, `list_jurisdiction_price_sources()`,
`get_jurisdiction_price_source()`, and `validate_price_source_coverage()`.

The built-in 2025 rows cover NSW, VIC, QLD, WA, SA, TAS, ACT, and NT. Each row
records public-safe source metadata or an explicit blocked status, plus a
deterministic checksum and extraction notes. No source-index row contains a committed jurisdiction price value; value extraction remains a separate
source/licence/unit-mapping gate.

Current row status:

| Jurisdiction | Status | Boundary |
|---|---|---|
| NSW | `blocked` | Source discovery row only; no redistributable NSW price value is committed. |
| VIC | `public_metadata` | Public National Funding Model metadata; numeric price extraction remains gated. |
| QLD | `public_metadata` | Public QWAU/funding-model metadata; QWAU-to-HWAU mapping remains gated. |
| WA | `public_metadata` | Public ABF metadata; reusable price schedule extraction remains gated. |
| SA | `public_metadata` | Public funding-allocation bulletin metadata; numeric extraction remains gated. |
| TAS | `blocked` | Source discovery row only; no redistributable Tasmanian price value is committed. |
| ACT | `public_metadata` | Public ABF service-agreement metadata; numeric extraction remains gated. |
| NT | `blocked` | Source discovery row only; no redistributable Northern Territory price value is committed. |
