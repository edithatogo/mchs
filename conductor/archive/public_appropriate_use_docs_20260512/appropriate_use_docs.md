# Public Appropriate-Use Documentation

## Purpose

This document defines the content contract for public-facing appropriate-use
documentation. It distinguishes validated behavior from experimental, roadmap-
only, and future-only surfaces, and prevents overclaiming by stating licensing
boundaries, policy caveats, and non-endorsement clearly.

## Content Contract

### 1. Appropriate-Use Page

**Target:** `docs-site/src/content/docs/appropriate-use.mdx`

#### Required Sections

1. **What this project is:**
   - A Python and multi-language reflection of IHACPA NWAU funding calculators.
   - Intended for analysts, developers, health funding specialists, and
     maintainers.
   - Not an official IHACPA product unless separately endorsed.

2. **What this project is not:**
   - Not a complete funding determination system.
   - Not an IHACPA-endorsed calculator.
   - Not a substitute for official IHACPA tools or advice.
   - Not a certified costing or pricing system.

3. **Validation and support claims explained.**
   - Reference `Validation-Status and Support Claims` page for the full
     classification system.

4. **Source licensing:**
   - IHACPA NEP, technical specifications, SAS calculators, and Excel
     workbooks are copyright IHACPA. Used under the terms of the relevant
     licence (see `Source Licensing` page).
   - ICD-10-AM, ACHI, ACS, and AR-DRG classification products are licensed
     through the relevant health authority. They are not committed to this
     repository.
   - All other content is published under the repository licence (see
     `LICENSE`).

5. **Non-endorsement statement:**
   - This project cites IHACPA sources but is not official IHACPA software.
   - IHACPA does not endorse this project or its outputs.
   - Any representation to the contrary is unauthorised.

6. **Funding, pricing, and policy disclaimer:**
   - NWAU and NEP calculations are analytical aids, not complete funding
     determinations.
   - Actual funding outcomes depend on additional factors including but not
     limited to: hospital-specific adjustments, jurisdictional pricing
     policies, service-level agreements, and data quality.
   - Costing study results are synthetic examples unless explicitly stated
     otherwise.

### 2. Validation-Status and Support Claims Page

**Target:** `docs-site/src/content/docs/validation-status.mdx`

#### Required Sections

1. **Validation vocabulary summary.**
   - Reference `conductor/validation-vocabulary.md` for the complete
     definitions.
   - Quick reference table:

     | Status | Meaning |
     |---|---|
     | Validated | Behaviour checked against trusted source with recorded evidence |
     | Source-only | Sources discovered and archived but not fully extracted |
     | Experimental | Implementation exists but lacks full parity evidence |
     | Roadmap-only | Planned but not implemented |
     | Future-only | Intended for future pricing years only |

2. **Pricing-year support table.**
   - For each pricing year and calculator stream, list the current validation
     status.
   - Link to the corresponding manifest and evidence records.
   - Mark unsupported years explicitly.

3. **Classification and coding-set compatibility.**
   - For each stream, list the required AR-DRG, ICD-10-AM, ACHI, ACS, UDG,
     AECC, and AMHCC versions.
   - Note which products are licensed and cannot be redistributed.

4. **Cross-language support matrix.**
   - For each surface (Python, Rust, CLI, R, Julia, C#, etc.), state:
     - Packaging status (published, unpublished, future-only).
     - Validation status relative to Python baseline.
     - Conformance test coverage.

### 3. Source and Licensing Caveats Page

**Target:** `docs-site/src/content/docs/licensing-caveats.mdx`

#### Required Sections

1. **IHACPA source materials:**
   - NEP, technical specifications, SAS calculators, Excel workbooks.
   - Copyright IHACPA. Use subject to IHACPA licence terms.
   - Archived sources are not redistributed where restricted.

2. **Licensed classification products:**
   - ICD-10-AM, ACHI, ACS: Copyright Australian Consortium for Classification
     Development (ACCD) or relevant authority.
   - AR-DRG: Copyright relevant health authority.
   - These products are not committed to the repository.
   - Users must supply their own licensed copies.

3. **Local-only and user-supplied assets:**
   - Licensed groupers, code tables, and mapping files are treated as
     user-supplied artifacts.
   - Path placeholders and manifest references exist in the repository, not
     the restricted payloads themselves.

4. **Third-party dependencies:**
   - Open-source packages used by the project are under their respective
     licences.
   - See `uv.lock` / `Cargo.lock` for the full dependency tree.

### 4. README Links

Update `README.md` to include:

- Link to Appropriate-Use page: `[Appropriate Use](./docs/appropriate-use/)`
- Link to Validation Status: `[Validation Status](./docs/validation-status/)`
- Link to Licensing Caveats: `[Licensing Caveats](./docs/licensing-caveats/)`

## Wording Conventions

| Term | Usage |
|---|---|
| Validated | Only when evidence record exists and is linked |
| Supported | Must specify what surface and year, with validation qualifier |
| Experimental | Use when implementation exists but lacks formal parity evidence |
| Roadmap | Use for planned but unimplemented features |
| Future-only | Use for intended future pricing years |
| Not official IHACPA software | Required in all public-facing descriptions |
| Analytical aid | Required disclaimer on NWAU/NEP output pages |

## Review Cadence

- These docs should be reviewed when adding new pricing years, calculator
  streams, bindings, or publication targets.
- Validation status tables must be updated at least quarterly or after each
  NEP/NWAU release.
- Non-endorsement statements must not be removed or weakened without legal
  advice.

## References

- `conductor/validation-vocabulary.md`
- `conductor/roadmap-governance.md`
- `conductor/tracks/docs_release_publication_readiness_20260510/`
- `docs/reviews/20260512-expert-panel/synthesis.md`
- `docs/reviews/20260512-expert-panel/deliberation-and-prioritisation.md`
