# Specification: Rust Crate Boundaries and HWAU Rename

## Overview

Define target Rust crate boundaries and plan the public migration from NWAU
terminology to HWAU without bulk-renaming active implementation files.

## Requirements

- Define target crates for contracts, core, CLI, MCP, API, Python, .NET, and
  optional WASM.
- Keep `nwau` compatibility aliases for Australian source terminology.
- Avoid broad crate renames while another agent is editing Rust files.
- Treat C ABI as an implementation boundary, not standalone C support.

## Acceptance Criteria

- Crate-boundary roadmap exists.
- Rename strategy uses compatibility shims and migration tests.
- Active Rust files are not bulk-renamed by this planning track.
