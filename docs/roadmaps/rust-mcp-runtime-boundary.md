# Rust MCP Runtime Boundary

This note defines the runtime contract for the first MCP migration slice.

## Runtime Status Wording

| Status | Meaning |
| --- | --- |
| Python stdio transport | The MCP process is still launched by the Python `mchs-mcp` stdio shim. This describes transport compatibility only and is not a formula-runtime claim. |
| Python default | Existing MCP calculation requests keep the current boundary response unless a caller explicitly requests Rust execution. |
| Rust canary | Rust kernels and Python bindings exist for selected calculations, but they are not full MCP default coverage. |
| Rust opt-in | A caller may request Rust with `options.runtime = "rust"` for validated MCP surfaces only. Unsupported requests fail closed. |
| Rust default | A future state that requires published CLI and MCP parity, diagnostics, and release evidence. This track does not claim that state. |

## Runtime Selection

`mchs.calculate` accepts `options.runtime` with values `python`, `rust`, or
`auto`. Missing runtime and `auto` preserve Python/default compatibility during
migration. Explicit `rust` requests use the Rust-backed dispatcher only for
validated surfaces.

The Python stdio transport may remain in place during transition. Promoted
formula execution must go through the Rust-backed dispatcher and must not shell
out to the CLI; the dispatcher must not shell out to the CLI.

## First Supported Rust Slice

The first Rust-backed MCP slice is:

- tool: `mchs.calculate`
- calculator: `acute`
- pricing year: `2025`
- input shape: one JSON object representing one acute episode row
- response shape: existing MCP tool response with `structuredContent`
- implementation: `nwau_py.calculators.acute.calculate_acute_rust_2025`

Non-acute calculators, non-2025 pricing years, unvalidated response formats,
and non-calculation tools remain Python/default or unsupported until separate
evidence promotes them.

## Parity Contract

Acute 2025 MCP parity compares Rust-backed MCP output against the Rust-backed
CLI path and the golden fixture set in `tests/fixtures/golden/acute_2025`.
Numeric parity uses `rtol=1e-4` and `atol=1e-4`; no MCP-specific rounding is
introduced beyond JSON serialization of the calculated row.

Schema parity sources:

- MCP tool contract: `contracts/mcp/tools.md`
- MCP resource contract: `contracts/mcp/resources.md`
- MCP registry metadata: `contracts/mcp/registry/server.json`
- CLI runtime boundary: `docs/roadmaps/rust-cli-runtime-boundary.md`
- acute 2025 golden input and expected output: `tests/fixtures/golden/acute_2025`

## Diagnostics

Rust runtime requests fail closed with stable diagnostic codes:

| Code | Condition |
| --- | --- |
| `MCHS-MCP-RUNTIME-INVALID` | `options.runtime` is not `python`, `rust`, or `auto`. |
| `MCHS-MCP-RUST-UNSUPPORTED` | Rust is requested for an unsupported calculator, year, tool, or response format. |
| `MCHS-MCP-RUST-UNAVAILABLE` | Rust is requested for a supported surface but the Rust extension cannot be loaded. |

Python fallback is allowed only for missing runtime, `python`, and transitional
`auto`. It is not allowed when the caller explicitly requests `rust`.
