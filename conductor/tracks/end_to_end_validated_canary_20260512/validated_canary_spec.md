# Validated Canary Specification

## Selected Canary

- **Stream:** Acute admitted
- **Pricing Year:** 2025 (2025-26 financial year)
- **Rationale:** Acute 2025 has source metadata, a source-only formula
  parameter bundle, synthetic golden fixtures, a Python baseline, a Rust
  canary, Arrow/Parquet fixture-bundle evidence, Starlight documentation, and a
  reusable template. It is locally complete as a lifecycle template with
  explicit official parity gaps.

## Lifecycle Phases

### Phase 1: Source Discovery and Archive

- **Source authority:** IHACPA 2025 NEP, technical specification, SAS
  calculator, Excel calculator workbook.
- **Archive location:** `reference-data/2025/`
- **Manifest:** `reference-data/2025/manifest.yaml`
- **Evidence:**
  - Source URLs and retrieval dates recorded in manifest.
  - Source hashes (SHA-256) recorded in manifest.
  - Source authority and license terms documented.
  - Gaps: any missing or restricted source artifacts are explicitly recorded.

### Phase 2: Formula Extraction and Bundle

- **Formula bundle location:** `reference-data/2025/formula-bundle/`
- **Contents:**
  - Extracted SAS logic for acute NWAU 2025.
  - Parameter tables (weights, thresholds, adjustments).
  - Classification version references (AR-DRG v11.0, etc.).
  - NEP price weights and activity weights.
- **Evidence:**
  - SAS source parity: **blocked** until official SAS comparison evidence is
    recorded.
  - Excel formula parity: **source-formula-only** because the workbook and
    extracted formula/weights are committed, but workbook-output comparison
    evidence is not recorded.
  - Formula bundle schema validated against manifest schema contract.

### Phase 3: Fixture Parity

- **Fixture pack:** acute-2025 fixture pack
- **Fixture manifest:** `tests/fixtures/acute-2025/manifest.json`
- **Parity types:**
  - Output parity: Python and Rust canary outputs match synthetic golden
    fixture outputs within declared tolerance.
  - SAS parity: blocked pending official SAS calculator outputs.
  - Excel formula parity: blocked pending official Excel workbook outputs.
- **Evidence:**
  - Fixture parity report with tolerance and rounding policy.
  - Cross-engine comparison: Python, Rust canary, CLI/Arrow.
  - Residual caveats documented (e.g., unlicensed grouper outputs).

### Phase 4: Cross-Engine Conformance

| Engine | Status | Evidence |
|---|---|---|
| Python (nwau_py) | Baseline | Synthetic acute 2025 golden fixtures pass |
| Rust canary | Candidate | Opt-in Rust wrapper matches Python on synthetic acute 2025 fixtures |
| CLI (`funding-calculator`) | Gap-recorded | Full official CLI conformance report not recorded |
| Arrow/Parquet file output | Local fixture pass | Arrow/Parquet output parity not recorded for official sources; synthetic fixture bundle loads |

### Phase 5: Documentation and Template

- **Starlight docs page:** complete; Starlight canary page committed at
  `docs-site/src/content/docs/governance/end-to-end-validated-canary.mdx`.
- **Template guidance:** complete; Reusable canary template committed at
  `conductor/tracks/end_to_end_validated_canary_20260512/template.md`.
- **Contents:**
  - Canary lifecycle overview.
  - Source manifest and extraction process.
  - Parity evidence and validation status.
  - Caveats (restricted groupers, licensed mappings).
  - Future-year implementation checklist.

## Validation Status Ladder

Current ladder position for acute 2025:

| Step | Status | Evidence |
|---|---|---|
| Discovered | Partial | Source metadata recorded for the canary bundle |
| Archived | Partial | Source-only bundle exists under `reference-data/2025/` |
| Extracted | Source-only | Formula parameter bundle loads but does not claim parity |
| Source-parity-checked | Blocked | Official SAS/Excel parity not recorded |
| Fixture-parity-checked | Partial | Python/Rust agree on synthetic golden fixtures |
| Cross-engine-checked | Partial | Python and Rust agree; Arrow/Parquet fixture bundle passes; official CLI report remains gap-recorded |
| Validated | Blocked | Official SAS/Excel parity not recorded |

## Template for Future Years

Future years can follow the same lifecycle by:

1. Adding source artifacts to `reference-data/<year>/`.
2. Creating a manifest.yaml from the schema template.
3. Extracting formula bundles for each stream.
4. Creating fixture packs from trusted reference outputs.
5. Running cross-engine validation.
6. Publishing docs from the canary template.
7. Updating validation status in the manifest.

## Caveats

- This canary proves acute 2025 behavior only. Do not generalise results to
  other years or streams without separate lifecycle evidence.
- AR-DRG grouping depends on licensed grouper outputs. Synthetic fixtures use
  precomputed DRGs where licensed groupers cannot be redistributed.
- Rust canary is opt-in. Python remains the validated public API.
- Restricted classification products (ICD-10-AM, ACHI, ACS, AR-DRG) are not
  committed. Local licensed copies must be user-supplied.

## References

- `reference-data/2025/manifest.yaml`
- `reference-data/2025/formula-bundle/`
- `tests/fixtures/golden/acute_2025/`
- `tests/fixtures/bundles/acute_2025/`
- `conductor/tracks/end_to_end_validated_canary_20260512/canary_lifecycle_evidence.json`
- `docs-site/src/content/docs/governance/end-to-end-validated-canary.mdx`
- `conductor/archive/formula_parameter_bundle_pipeline_20260512/`
- `conductor/archive/pricing_year_validation_gates_20260512/`
- `conductor/archive/rust_acute_python_poc_20260510/`
