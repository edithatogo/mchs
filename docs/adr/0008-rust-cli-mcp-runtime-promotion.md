# ADR 0008: Rust CLI/MCP Runtime Promotion

Date: 2026-07-03

## Status

Accepted

## Decision: keep Python/default compatibility

Keep CLI and MCP runtime defaults on the existing Python/default compatibility
paths. Rust-backed execution remains opt-in for acute 2025 only.

No CLI or MCP Rust-default claim is made.

## Rationale

The committed evidence proves Rust-backed acute 2025 execution for selected CLI
and MCP paths, but it does not prove Rust coverage for ED, non-admitted,
non-2025 years, hosted MCP, Docker catalog runtime, or every response format.

Default promotion would overclaim the current evidence.

## Rollback

- CLI: pass `--runtime python` or unset `NWAU_RUNTIME`.
- MCP: omit `options.runtime` or set it to `python`.

The rollback path must remain available until the promotion matrix records Rust
default coverage for every public surface affected by a default change.
