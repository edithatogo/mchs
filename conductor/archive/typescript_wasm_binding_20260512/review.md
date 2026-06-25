# Review: TypeScript and WASM Binding

## Verdict

Complete, with browser readiness still gated. The TypeScript WASM adapter, browser-demo docs, repository tests, CI notes, and verified npm publication are recorded, but calculator readiness depends on WASM golden fixture parity.

## Scope

Browser-safe WASM contract, synthetic-only demos, TypeScript facade/export validation, Node/browser prototype surfaces, no formula ownership in TypeScript, and conservative CI posture.

## Residual Gaps

- Dedicated WASM CI should wait for deterministic generated WASM artifact, generated/validated TypeScript contract, and fixture set in-repo.
- Browser-level tests should use a stable headless command once added.

## Validation

- `cd rust && cargo test`
- `cd rust && cargo fmt --all --check`
- `cd rust && cargo clippy --all-targets --all-features -- -D warnings`
- `cd docs-site && npm ci`
- `cd docs-site && npm run build`
- `uv run pytest tests/test_typescript_wasm_binding_track.py -q`
