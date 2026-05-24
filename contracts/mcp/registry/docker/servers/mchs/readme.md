# MCHS Health Services Microcosting MCP Server

MCHS exposes synthetic-data-safe Model Context Protocol tools for Australian
health-services microcosting, NWAU pricing support-scope inspection, canonical
schema discovery, and publication evidence.

## Runtime

The Docker catalog candidate runs the local stdio MCP server:

```bash
mchs-mcp
```

The server requires no secrets for discovery or read-only metadata calls.

## Safety boundary

- Do not submit PHI, patient-level records, or private institutional costing
  data.
- The MCP adapter delegates to the canonical runtime and does not duplicate
  calculator formula logic.
- The registry demo surface is intended for synthetic/public-data-safe
  workflows.

## Source

- Repository: https://github.com/edithatogo/mchs
- Official MCP Registry name: `io.github.edithatogo/mchs`
- PyPI package: `nwau-py`
