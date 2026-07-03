# Rust CLI/MCP Promotion Evidence

Scope: `rust_cli_mcp_promotion_evidence_20260703`

## Decision

Rust remains opt-in for CLI and MCP acute 2025. No Rust-default surface is
promoted by this track.

No Rust-default surface is promoted.

The default runtime decision is recorded in
`contracts/runtime/rust-cli-mcp-promotion-matrix.json` as
`remain-python-default-rust-opt-in`.

## Evidence Standard

Rust default promotion requires all of the following to pass from committed
commands and committed fixtures:

- Rust core and C ABI tests: `cargo test -p nwau-core -p nwau-c-abi`
- Python compatibility tests for MCP, CLI, and migration governance
- CLI parity tests for promoted fixtures
- MCP parity tests for promoted fixtures
- Unsupported-surface inventory proving non-acute and non-2025 surfaces are not
  hidden by broad completion language

## Current Surface Result

| Surface | Status | Default runtime |
| --- | --- | --- |
| CLI acute 2025 CSV | Rust opt-in | Python |
| CLI ED 2025 CSV | Python-only | Python |
| CLI non-admitted 2025 CSV | Python-only | Python |
| MCP calculate acute 2025 JSON | Rust opt-in | Python boundary |
| MCP validate_input acute 2025 JSON | Rust opt-in | Python boundary |
| MCP calculate ED 2025 JSON | Unsupported for Rust | None |
| MCP metadata tools/resources | Python-only | Python |

## Conformance Gate

Run:

```text
python3 scripts/validate_rust_cli_mcp_promotion.py --json
PYTHONPATH=. uv run pytest -q tests/test_rust_cli_mcp_promotion_evidence.py tests/test_rust_cli_core_migration.py tests/test_rust_mcp_core_migration.py tests/test_mcp_server.py tests/test_rust_migration_track_hardening.py
cargo test -p nwau-core -p nwau-c-abi
```

The same gate is wired into
`.github/workflows/rust-cli-mcp-promotion.yml`.

Local validation result for this track:

```text
python3 scripts/validate_rust_cli_mcp_promotion.py --json
passed=true; rustDefaultAllowed=false; rust-opt-in=3; python-only=3; unsupported=1

PYTHONPATH=. uv run pytest -q tests/test_rust_cli_mcp_promotion_evidence.py tests/test_rust_cli_core_migration.py tests/test_rust_mcp_core_migration.py tests/test_mcp_server.py tests/test_rust_migration_track_hardening.py
49 passed, 2 skipped

cargo test -p nwau-core -p nwau-c-abi
36 passed
```

## Rollback

- CLI: use `--runtime python` or unset `NWAU_RUNTIME`.
- MCP: omit `options.runtime` or set `options.runtime = "python"`.

No user-facing CLI or MCP contract is removed while Rust remains opt-in.
