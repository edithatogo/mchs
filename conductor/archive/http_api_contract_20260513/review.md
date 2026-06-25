# Review: HTTP API Contract

## Status

Reviewed on 2026-06-25. Archive eligible as a completed contract-surface
track.

## Scope Reviewed

- `contracts/http-api/openapi.yaml` defines the OpenAPI 3.1 domain API.
- `contracts/http-api/examples/` contains synthetic pass/fail and async
  examples.
- `scripts/validate_http_api_contract.py` rejects duplicate YAML keys and checks
  required paths, schemas, response placement, async job schema structure, and
  validation-failure response coverage.

## Findings

- Fixed duplicate/misplaced response keys around async job polling.
- Fixed `/support/years` so it is a complete path operation rather than a
  fragment split across `components`.
- Fixed `AsyncJobStatus` and explanation/diagnostics schemas so they live under
  `components.schemas`, while reusable error responses live under
  `components.responses`.
- No deployed production API is claimed by this track.

## Validation

- `uv run python scripts/validate_http_api_contract.py`
- `uv run pytest tests/test_core_contract_surface_tracks.py`
- `python conductor/scripts/stub_detector.py --root . --json`
