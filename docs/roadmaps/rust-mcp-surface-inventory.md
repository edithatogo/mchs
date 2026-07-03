# Rust MCP Surface Inventory

This inventory records the MCP surfaces considered by the Rust MCP core
migration track.

## Tools

| Tool | Current role | Python implementation | Rust status |
| --- | --- | --- | --- |
| `mchs.list_calculators` | Lists calculator metadata and support status. | `nwau_py.mcp_server.list_calculators` | Metadata-only; no formula runtime. |
| `mchs.get_schema` | Returns canonical schema metadata. | `nwau_py.mcp_server.get_schema` | Metadata-only; no formula runtime. |
| `mchs.validate_input` | Validates common request shape and support scope. | `nwau_py.mcp_server.validate_input` | Python boundary validation retained. |
| `mchs.calculate` | Validates and calculates or returns compatibility boundary response. | `nwau_py.mcp_server.calculate` | Rust opt-in for `acute` year `2025` through `calculate_acute_rust_2025`. |
| `mchs.explain_result` | Explains the MCP boundary steps for a request. | `nwau_py.mcp_server.explain_result` | Python-only explanation; no formula runtime. |
| `mchs.get_evidence` | Returns registry and release evidence. | `nwau_py.mcp_server.get_evidence` | Evidence-only; no formula runtime. |

## Resources

| Resource | Purpose | Rust status |
| --- | --- | --- |
| `mchs://schemas` | Lists canonical schema identifiers. | Metadata-only. |
| `mchs://schemas/{schemaId}` | Returns packaged or repo-local schemas. | Metadata-only. |
| `mchs://support/status` | Returns bounded support status. | Updated to distinguish Python stdio transport from Rust formula runtime. |
| `mchs://calculators` | Returns calculator metadata. | Includes per-calculator support status. |
| `mchs://evidence/{bundleId}` | Returns evidence references. | Evidence-only. |

## Registry-Facing Metadata

The published registry surface remains a local stdio server launched as
`mchs-mcp`. The migration does not claim hosted HTTP, Docker catalog readiness,
Smithery hosted runtime readiness, or a new registry release.

Registry metadata source:

- `contracts/mcp/registry/server.json`
- `contracts/mcp/registry/submission-decisions.md`

## Dispatcher Boundary

The Rust-backed MCP dispatcher performs:

1. Validate MCP request shape using the existing tool schema boundary.
2. Resolve `options.runtime`.
3. For `runtime = "rust"`, verify calculator/year coverage.
4. Convert the single-row JSON `inputs` object to the canonical tabular row.
5. Invoke `nwau_py.calculators.acute.calculate_acute_rust_2025` directly.
6. Shape the calculated row back into the existing MCP response envelope.

The dispatcher must not shell out to the CLI. CLI parity is a validation target,
not the MCP architecture.

## Follow-On Coverage

ED, non-admitted, subacute, mental health, adjustment, multi-row inputs,
non-2025 pricing years, and hosted/remote MCP transports remain follow-on work
until separate fixtures, schemas, and release evidence promote them.
