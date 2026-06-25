# Contract Schema Export Specification

## Purpose

Export versioned schemas for the public calculator contract and validation
ecosystem. These schemas are the foundation for Rust core, Arrow interfaces,
bindings, CLI/file workflows, docs, and release evidence.

## Schema Inventory

### Required Schemas

| Schema | Domain | Format | Priority |
|---|---|---|---|
| Calculator Input | NWAU calculation inputs per stream/year | JSON Schema | High |
| Calculator Output | NWAU calculation results and diagnostics | JSON Schema | High |
| Pricing-Year Manifest | Source artifacts, validation status, gaps | JSON Schema / YAML | High (existing) |
| Formula Bundle | Extracted SAS/Excel formula parameters | JSON Schema | High (existing) |
| Fixture Manifest | Fixture pack metadata and references | JSON Schema | Medium (existing) |
| Diagnostic Record | Validation run metadata and results | JSON Schema | Medium |
| Provenance Record | Source acquisition, hashes, retrieval dates | JSON Schema | Medium |
| Release Evidence | Registry and workflow status report | JSON Schema | Medium |

### Existing Schemas

These schemas already have typed models and manifest artifacts:

- Pricing-year manifest schema (`nwau_py.reference_manifest`)
- Formula bundle schema (reference-data bundles)
- Fixture manifest schema (fixture pack manifests)

### New Schemas Required

These schemas need explicit JSON Schema exports:

1. **Calculator Input Schema** — Defines the validated input contract for NWAU
   calculation requests per stream and pricing year.
2. **Calculator Output Schema** — Defines the output contract including NWAU
   contributions, adjustments, and diagnostics.
3. **Provenance Record Schema** — Defines source acquisition metadata for audit
   trails.
4. **Diagnostic Record Schema** — Defines validation run results for conformance
   reporting.
5. **Release Evidence Schema** — Defines the registry status report format.

## Versioning Policy

| Artifact | Version Source | Version Example | Change Cadence |
|---|---|---|---|
| Package version | `pyproject.toml` | `0.5.0` | Per release |
| Pricing year | Manifest metadata | `2025` | Annual |
| Schema version | Independent semver | `1.0.0` | Breaking changes only |
| Bundle version | Per-bundle manifest | `acute-2025-v3` | Per extraction |

### Rules

- Schema versions are independent of package versions and pricing years.
- Schema version bumps follow semantic versioning.
- A major schema version change (1.x → 2.x) requires documented migration.
- Existing manifests and fixtures declare their schema version so consumers can
  validate compatibility.
- Arrow schemas are versioned alongside JSON Schema equivalents where both
  formats are published.

## Export Implementation

### JSON Schema Export

- Export JSON Schema artifacts from typed Python models where practical.
- Use `pydantic` or `dataclass` model inspection to derive schema definitions.
- Output directory: `contracts/schemas/`
- Naming convention: `<domain>-<version>.schema.json`

### Arrow Schema Export

- Arrow schemas are embedded in the Parquet/Arrow batch contracts.
- Document Arrow schema boundaries in `contracts/arrow/`.

### Determinism Requirement

Schema export must be deterministic: identical model inputs produce identical
schema output every time. This is verified by tests that:

1. Export a schema to JSON.
2. Export the same schema again.
3. Assert the two outputs are byte-identical.

### Output Locations

| Schema | JSON Schema Path | Arrow Schema Path |
|---|---|---|
| Calculator Input | `contracts/schemas/calculator-input-1.0.schema.json` | `contracts/arrow/calculator-input.arrow` |
| Calculator Output | `contracts/schemas/calculator-output-1.0.schema.json` | `contracts/arrow/calculator-output.arrow` |
| Pricing-Year Manifest | `contracts/schemas/pricing-year-manifest-1.0.schema.json` | — |
| Formula Bundle | `contracts/schemas/formula-bundle-1.0.schema.json` | — |
| Fixture Manifest | `contracts/schemas/fixture-manifest-1.0.schema.json` | — |
| Diagnostic Record | `contracts/schemas/diagnostic-record-1.0.schema.json` | — |
| Provenance Record | `contracts/schemas/provenance-record-1.0.schema.json` | — |
| Release Evidence | `contracts/schemas/release-evidence-1.0.schema.json` | — |

## Binding Conformance References

Binding tracks reference schema artifacts as their input/output contract:

- Python binding: imports typed models from `nwau_py.models`
- Rust binding: derives types from Arrow schemas in `contracts/arrow/`
- CLI binding: validates JSON I/O against `contracts/schemas/*.schema.json`
- Other bindings (R, Julia, C#, Go, JVM, WASM, etc.): consume Arrow schemas
  or JSON Schema as the language-neutral contract

## Documentation

### Docs Page Content

Add a Starlight docs page (`docs-site/src/content/docs/contracts/schemas.mdx`)
that explains:

- The purpose of each public schema.
- Version separation: package, pricing-year, bundle, and schema versions are
  independent.
- How binding implementers consume schema artifacts.
- Migration policy for breaking schema changes.
- How to add a new schema version.

## References

- `conductor/tracks/public_api_contract_20260504/`
- `conductor/archive/reference_data_manifest_schema_20260512/`
- `conductor/archive/formula_parameter_bundle_pipeline_20260512/`
- `conductor/validation-vocabulary.md`
- `nwau_py/reference_manifest.py`
- `contracts/` directory structure
