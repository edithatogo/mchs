# Healthcare Weighted Activity Unit and Local Price Strategy

The library should use the generic term **healthcare weighted activity unit
(HWAU)** for its domain abstraction. Australia-specific National Weighted
Activity Unit terminology remains important source terminology, but it should
not be the generic library name.

Status: roadmap intent only. The active HWAU, jurisdiction price, state/local
price, NSW funding, and parallel valuation tracks are `[~]` /
`complete-with-gaps`; no public sourced state/local pricing support claim is
made until official provenance rows, runtime registry APIs, and behavior tests
are complete.

## Terminology model

- `hwau`: canonical library abstraction for a weighted activity unit.
- `nwau`: Australian national source terminology and compatibility alias.
- `price_per_hwau`: generic price applied to a weighted activity unit.
- `national_efficient_price`: Australian NEP source concept.
- `local_price`: jurisdiction, state, local health network, or institutional
  price applied instead of the national efficient price.
- `discounted_price`: calculated or declared price that applies a discount,
  adjustment, or local rule to a base price.

## Price registry scope

The price registry should source and version:

- National Efficient Price by year where applicable.
- State or jurisdiction-specific prices by year.
- Local health network, hospital, or program-specific prices where public or
  locally licensed sources exist.
- Discount rules, discount factors, caps, floors, or local override formulas.
- Provenance, source URL/path, retrieved date, checksum, licence, and support
  status.

## Australian jurisdiction model scope

The registry should treat each Australian state and territory as a separate
jurisdiction model, because public funding documents show local implementation
differences.

| Jurisdiction | Initial model status | Evidence to source |
| --- | --- | --- |
| NSW | Explicit model required | NSW State Price per NWAU by financial year, district/network return basis, local health district service agreement notes, activity and price adjustments. |
| VIC | Explicit model required | National Funding Model transition from WIES/SWIES/WASE/NAESGs to NWAU, Victorian admitted acute funding approach, VCDC/VicABC costing material, residual block/special streams. |
| QLD | Explicit model required | Queensland Efficient Price, Queensland WAUs, Queensland ABF modifications to the national model, purchasing and funding guidelines. |
| WA | Explicit model required | WA ABF model, state-specific adjustments, Health Service Allocation Price or state price references, WA activity data policy. |
| SA | Explicit model required | State Efficient Price, SA funding model exclusions, NEP-equivalent cost per NWAU, LHN service agreement/KPI definitions. |
| TAS | Explicit model required | Tasmanian Health Service activity and funding schedules using NWAU plus block grants and supplementary lines. |
| ACT | Explicit model required | ACT applicable price, ABF service funding agreement, transition from block funding to ABF, state supplementary grant/adjustments. |
| NT | Explicit model required | NT service plans with price per WAU, purchased activity, ABF allocation, block funding, and remote/territory-specific funding considerations. |

Every jurisdiction model should support:

- Source-specific terminology such as NWAU, WAU, QWAU, WIES, or local efficient
  price terms.
- Mapping to the generic HWAU abstraction.
- Financial-year versioning.
- Stream-specific applicability.
- Local adjustments, supplements, exclusions, caps, and block-funded components.
- A clear distinction between public-source data and local-only/licensed data.

## Valuation outputs

The calculator should support producing multiple valuations from the same
activity result:

- HWAU only.
- HWAU times national efficient price.
- HWAU times state-specific price.
- HWAU times territory-specific price.
- HWAU times local price.
- HWAU times discounted price.
- Parallel comparison output across national, state, local, and discounted
  scenarios.

## Parallel production rule

Pricing outputs should be producible in parallel from the same normalized
activity result. Formula execution and pricing application must remain separate:

1. Calculate HWAU.
2. Select one or more price schedules.
3. Apply price schedules independently.
4. Emit comparable valuation columns and provenance for each schedule.

## Deferred language posture

Do not remove existing roadmap entries for dropped/deferred languages, but do
not develop them while Rust Core GA and contract surfaces are incomplete.

Active or retained surfaces:

- Rust core.
- Rust CLI/file.
- Rust MCP.
- HTTP API.
- Python.
- R.
- Julia.
- SAS.
- Stata.
- C#/.NET.
- TypeScript/WASM optional web surface.

Deferred/no-new-development surfaces:

- Scala/Spark.
- Swift.
- Go.
- MATLAB.
- Kotlin/Native unless a native Kotlin user appears.
- Standalone C language support.

Removed from active strategy:

- SQL/DuckDB. Existing references should be treated as historical or optional
  analysis ideas, not active roadmap priorities.
