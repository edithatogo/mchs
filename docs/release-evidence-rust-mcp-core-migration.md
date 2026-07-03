# Rust MCP Core Migration Evidence

Scope: `rust_mcp_core_migration_20260703`

## Implemented Behaviour

- Added `options.runtime = "python" | "rust" | "auto"` handling to
  `mchs.calculate`.
- Preserved Python stdio transport compatibility and default MCP boundary
  behaviour.
- Routed `mchs.calculate` with `calculatorId = "acute"`, `year = "2025"`, and
  `options.runtime = "rust"` through
  `nwau_py.calculators.acute.calculate_acute_rust_2025`.
- Added fail-closed Rust diagnostics:
  - `MCHS-MCP-RUNTIME-INVALID`
  - `MCHS-MCP-RUST-UNSUPPORTED`
  - `MCHS-MCP-RUST-UNAVAILABLE`

## Validation Evidence

Focused tests:

```text
uv run pytest -q tests/test_mcp_server.py tests/test_rust_mcp_core_migration.py tests/test_rust_cli_core_migration.py
```

Local focused result:

```text
PYTHONPATH=. uv run pytest -q tests/test_mcp_server.py tests/test_rust_mcp_core_migration.py tests/test_rust_cli_core_migration.py
35 passed, 2 skipped
```

Rust core and C ABI tests:

```text
cargo test -p nwau-core -p nwau-c-abi
36 passed
```

The skipped Python tests are optional Rust-extension parity checks guarded when
the extension is unavailable in the local Python environment.

Final review validation:

```text
PYTHONPATH=. uv run pytest -q tests/test_mcp_server.py tests/test_rust_mcp_core_migration.py tests/test_rust_cli_core_migration.py tests/test_rust_migration_track_hardening.py
44 passed, 2 skipped
```

## Support Claim

This evidence supports an opt-in Rust-backed MCP calculation path for acute
2025 only. It does not claim Rust default MCP status, hosted HTTP runtime
readiness, Docker catalog publication, Smithery hosted runtime readiness, or
full Rust migration of all MCP tools.

## Residual Gaps

- The MCP stdio process remains a Python transport shim.
- Non-acute calculators remain Python/default or unsupported for Rust requests.
- Non-2025 pricing years remain unsupported for Rust MCP execution.
- MCP validation, schema, evidence, and explanation tools remain Python
  metadata/contract surfaces, not formula-runtime surfaces.
