# Review: Coding-Set Version Registry

Scope audited against:
- [`conductor/archive/coding_set_version_registry_20260512/spec.md`](./spec.md)
- [`conductor/archive/coding_set_version_registry_20260512/plan.md`](./plan.md)
- [`conductor/tracks.md`](../../tracks.md)
- [`conductor/tracks/classification_input_validation_20260512/index.md`](../classification_input_validation_20260512/index.md)
- [`conductor/tracks/classification_input_validation_20260512/classification_matrix.md`](../classification_input_validation_20260512/classification_matrix.md)
- [`nwau_py/classification_validation.py`](../../../nwau_py/classification_validation.py)
- [`nwau_py/reference_manifest.py`](../../../nwau_py/reference_manifest.py)
- [`docs-site/src/content/docs/governance/reference-data-manifests.mdx`](../../../docs-site/src/content/docs/governance/reference-data-manifests.mdx)
- [`docs-site/src/content/docs/governance/calculator-coverage.mdx`](../../../docs-site/src/content/docs/governance/calculator-coverage.mdx)

## Findings

1. High: The track is still roadmap-only, while the implementation that exists is a narrow classification preflight helper rather than the requested coding-set registry.
   - Evidence: the track itself is unchecked in `conductor/tracks.md:213-215`, and the plan still shows all registry schema/data/docs tasks open in `conductor/archive/coding_set_version_registry_20260512/plan.md:3-19`.
   - Evidence: the adjacent classification-validation track says its matrix is "a validation input, not the canonical coding-set registry" and that durable ownership remains with the coding-set registry track at `conductor/tracks/classification_input_validation_20260512/index.md:9-19`.
   - Impact: the acceptance criteria in `spec.md:17-20` are not yet satisfiable because there is no registry artifact, no registry data file, and no registry-backed validator path to resolve expected coding-set versions.

2. High: The current Python model only covers five classification systems, but the registry scope requires eight families plus licensing metadata and pricing-year applicability.
   - Evidence: `nwau_py/classification_validation.py:69-91` hard-codes only `AR-DRG`, `AECC`, `UDG`, `Tier 2`, and `AMHCC`, and `LICENSED_CLASSIFICATIONS` only marks `ar_drg` as licensed at `nwau_py/classification_validation.py:77`.
   - Evidence: the year/version matrix in `nwau_py/classification_validation.py:93-170` stops at the five systems above and does not include `ICD-10-AM`, `ACHI`, or `ACS`.
   - Evidence: the registry spec explicitly requires `AR-DRG, AECC, UDG, Tier 2, AMHCC, ICD-10-AM, ACHI, and ACS` and asks for release dates, implementation dates, redistribution constraints, and applicable pricing years at `spec.md:4-15`.
   - Impact: the current implementation cannot represent the full intended registry scope, and it cannot yet distinguish public metadata from restricted classification products in the way the spec requires.

3. Medium: The reference-manifest schema only stores a minimal coding-set stub, so it cannot yet link manifests to a durable registry record with the fields the track calls for.
   - Evidence: `nwau_py/reference_manifest.py:183-203` defines `ReferenceCodingSet` with `name`, `version`, `status`, `source_url`, `note`, and optional `official_page_version` only.
   - Evidence: `nwau_py/reference_manifest.py:206-220` defines validation status, but there is no registry key, no release date, no implementation date, and no licensing/redistribution field on the coding-set object itself.
   - Evidence: the manifest docs say coding sets should carry "coding-set versions and any transition notes" and a support link, but they do not define a registry-backed identifier or a place to store redistribution constraints at `docs-site/src/content/docs/governance/reference-data-manifests.mdx:34-49`.
   - Impact: manifests can note a coding-set version, but they cannot yet satisfy the spec requirement to link pricing-year manifests to registry entries or to capture the registry ownership model explicitly.

4. Medium: The public docs explain validation and coverage, but they do not yet explain the coding-set registry boundary or the acquisition path for licensed classification products beyond the existing AR-DRG note.
   - Evidence: the classification matrix warns that AR-DRG is licensed / non-redistributable and says not to redistribute those products, but the note is AR-DRG-specific at `conductor/tracks/classification_input_validation_20260512/classification_matrix.md:22-28`.
   - Evidence: the calculator-coverage page says classification input coverage is tracked separately and that the preflight validator is not yet wired end-to-end, but it does not point to a registry document or explain where licensed code lists or groupers are sourced at `docs-site/src/content/docs/governance/calculator-coverage.mdx:18-22`.
   - Evidence: the manifest docs describe gaps and provenance, but the registry-specific distinction between public metadata and restricted code lists is still absent from the public docs set at `docs-site/src/content/docs/governance/reference-data-manifests.mdx:51-130`.
   - Impact: the docs requirement in `spec.md:10,20` is only partially met, because users still do not have a single public explanation of the registry boundary, restricted artifacts, and how those relate to the manifests.

## Blockers

- Resolved in integration: `nwau_py.coding_set_registry` now provides a
  metadata-only registry for AR-DRG, AECC, UDG, Tier 2, AMHCC, ICD-10-AM, ACHI,
  ACS, and AN-SNAP.
- Resolved in integration: compatibility validators cover compatible,
  incompatible, missing, and restricted-artifact cases.
- Resolved in integration: public Starlight docs now explain public metadata
  versus restricted licensed products.
- Remaining caveat: reference-data manifests still store compact coding-set
  references rather than full registry-entry identifiers. A later schema
  evolution can add explicit registry keys.

## Recommended validation commands

- `uv run pytest tests/test_classification_validation.py`
- `uv run pytest tests/test_reference_data_manifest_schema.py`
- `uv run pytest tests/test_docs_site_migration.py`
- `uv run pytest tests/test_fixture_manifest.py`
- `uv run python -m nwau_py.cli.main --help`
