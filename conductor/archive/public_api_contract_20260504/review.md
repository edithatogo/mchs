# Review: Public Calculator API Contract

## Verdict

Archive-ready.

## Findings

- No blocking findings remain for the public contract baseline.
- The archived scope is the versioned contract and validation vocabulary. It does not claim every downstream adapter, generated client, registry package, or hosted surface is complete.

## Evidence Reviewed

- `conductor/public-api-contract.md` defines the public contract purpose, versioning, required acute inputs, required outputs, validation status, error model, adapter mapping, and generation-readiness posture.
- `nwau_py/contracts.py` implements strict calculator identifiers, pricing-year validation, schema-version validation, required input/output columns, and structured `ContractValidationError` failures.
- `tests/test_contracts.py` validates supported years, invalid year rejection, calculator identifiers, required column checks, duplicate/blank column rejection, and schema metadata.
- `tests/test_web_demo.py` and docs-site contract tests exercise downstream consumption of public contract metadata without turning those downstream surfaces into completion evidence for this track.

## Validation

- `uv run pytest tests/test_contracts.py tests/test_web_demo.py tests/test_docs_site_sota_refresh.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Notes

Downstream client generation, OpenAPI surfaces, MCP/OpenAI adapters, and language bindings remain owned by their specific implementation tracks. This archive preserves the stable contract baseline they must conform to.
