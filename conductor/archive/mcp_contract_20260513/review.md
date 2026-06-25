# Review: MCP Contract

## Verdict

Archive-ready after remediation. The contract now matches the implemented stdio MCP boundary: tools validate and delegate requests, resources expose support/evidence metadata, and formula execution is not duplicated in the MCP adapter.

## Findings Fixed

- `contracts/mcp/tools.md` used stale `icu-bed-day` examples that do not match the runtime calculator IDs.
- `mchs.calculate` was described as direct calculation execution with a concrete result, while the implementation returns `result: null` plus a delegation diagnostic.
- MCP evidence resources implied calculation-response evidence bundles, which overclaimed the current adapter boundary.

## Validation

- `uv run pytest tests/test_mcp_server.py tests/test_governance_contracts.py::test_api_mcp_openai_relationship_keeps_logic_in_rust_core -q`
- `python conductor/scripts/stub_detector.py --root . --json`
