# Validation Roadmap: Historical IHACPA Coverage Audit

## Purpose

This roadmap defines how the track will validate historical IHACPA coverage
without collapsing distinct evidence types into a single "support" claim.

The key rule is:

- `2012-13` must be validated first as a specification-extraction problem.
- Calculator parity is a separate follow-on problem.
- NHCDC and older costing materials may support historical context, but they
  do not by themselves prove annual NWAU calculator support.

## Validation Streams

### Stream 1: 2012-13 Specification Extraction

Priority objective:

- Confirm the `2012-13` National Pricing Model Technical Specifications and
  related NEP determination are discoverable, attributable, and archived.
- Extract the year-specific pricing rules, parameter tables, and any public
  references needed to describe the year accurately.
- Record explicit provenance for the source bundle before any parity claim is
  attempted.

Required evidence:

- Official source URL for the `2012-13` specification and determination.
- Publication date, document title, and issuing body.
- Local archive hash or equivalent immutable file fingerprint.
- Notes identifying the extracted year-specific pricing rules and any missing
  sections.

Completion criterion:

- The `2012-13` specification bundle is complete enough to describe the year
  accurately in the manifest and roadmap matrix, even if calculator artifacts
  are still absent.

### Stream 2: Calculator Parity

Priority objective:

- Validate calculator artifacts only after the specification bundle for the
  year is established.
- Compare calculator downloads, inputs, and outputs against the corresponding
  year’s official pricing specification where artifacts exist.
- For `2013-14` onward, confirm whether a public calculator artifact exists and
  whether its behavior is consistent with the published specification.

Required evidence:

- Calculator download URL, publication date, and archive hash.
- Fixture or sample input/output capture for the year under review.
- A documented mapping from calculator behavior to the extracted specification.
- Explicit gap record when a calculator artifact is not present.

Completion criterion:

- Calculator parity can be asserted only when a year has both a source bundle
  and a parity check record.

### Stream 3: Historical Support Claims Gate

This stream controls the language used in docs, manifests, and roadmap tables.

Do not claim "support" for an older year unless all of the following are true:

1. The year has an official NEP or pricing-spec source bundle.
2. The year has a year-scoped provenance record with URL, date, and hash.
3. Calculator artifacts are either present and parity-checked, or the absence
   is explicitly recorded as a gap.
4. Any NHCDC or cost-weight evidence is labeled as costing-study evidence, not
   as calculator parity evidence.
5. The manifest or roadmap matrix includes a validation status for the year.

Support language by evidence level:

| Evidence level | Allowed claim |
| --- | --- |
| Source discovered | "Official source found" |
| Specification extracted | "Year-specific pricing rules documented" |
| Calculator artifact present | "Calculator source available" |
| Calculator parity checked | "Calculator parity validated" |
| Full evidence bundle complete | "Historical year support documented" |

## Year-by-Year Validation Order

1. `2012-13`
   - Extract specification first.
   - Treat calculator parity as a separate follow-up investigation.
   - If the calculator is absent, record a gap instead of inferring support.
2. `2013-14` to current
   - Validate calculator presence and parity year by year.
   - Link each year to its matching pricing specification and source hash.
3. Pre-`2012-13`
   - Treat older NHCDC and costing materials as contextual evidence only.
   - Do not promote them to annual NWAU calculator support without a year-
     specific calculator source bundle and parity record.

## Evidence Required Before Claiming Support for Older Years

Before the repository can state that an older year is supported, the record
must contain:

- The official year-specific pricing source.
- The extracted year-specific parameters or rules.
- A calculator artifact or an explicit absence record.
- A reproducible hash for every downloadable artifact.
- A validation status in the historical coverage matrix.
- A clear note if the evidence comes from costing-study material rather than
  calculator sources.

If any of these items are missing, the correct claim is one of:

- source discovered
- specification extracted
- calculator gap recorded
- costing evidence documented
- validation pending

## Non-Claims

The following are not sufficient to claim historical calculator support:

- NHCDC public-sector reports alone.
- Cost-weight tables alone.
- A year appearing on an index page without a downloadable calculator artifact.
- A technical specification without parity evidence, unless the claim is only
  that the specification has been extracted.

## Deliverables

- A historical coverage matrix with separate statuses for:
  - NEP determination
  - technical specification
  - NWAU calculator
  - price weights
  - NHCDC report
  - validation status
- Explicit gap records for any missing calculator artifacts.
- A cleaned claim taxonomy for docs and manifests so older years are not
  overstated.
