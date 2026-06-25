# Review: TypeScript/WASM npm Registry Submission

## Status

Reviewed on 2026-06-25. Archive eligible as a published-verified registry
track.

## Scope Reviewed

- npm registry exposes `@edithatogo/mchs-wasm-binding@0.1.0`.
- Publication evidence records tarball URL, integrity string, and publish time.
- The track remains a package publication claim, not a browser formula-parity
  claim.

## Validation

- `npm view @edithatogo/mchs-wasm-binding@0.1.0 name version dist.tarball dist.integrity time --json --registry=https://registry.npmjs.org`
- `uv run pytest tests/test_typescript_npm_registry_submission_track.py`
- `python conductor/scripts/stub_detector.py --root . --json`
