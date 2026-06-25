# Contract Enforcement Plan

Agent coordination note: this file defines how agents prove contracts are real. Do not mark contract tracks complete until the checks below are implemented or explicitly gap-recorded.

## Contract Families

| Family | Artifacts | Required enforcement |
| --- | --- | --- |
| Canonical domain | calculator request/response, diagnostics, errors, provenance, evidence, support status | JSON Schema validation, fixtures, backwards-compatibility checks |
| CLI/file | command manifests, exit codes, stdout/stderr, CSV/JSON/Arrow/Parquet schemas | golden command tests, malformed-input tests, file round-trip tests |
| HTTP API | OpenAPI 3.1, examples, error responses, async job protocol if present | schema validation, request/response conformance tests, docs examples |
| MCP | tools, resources, prompts where applicable | MCP schema tests, agent-safe diagnostics, provenance preservation |
| OpenAI adapter | tool definitions and examples | adapter tests proving it delegates to canonical contracts |
| Bindings | Python, R, Julia, C#, TypeScript/WASM, Stata interop | shared fixtures, no formula duplication checks, packaging checks |
| Release evidence | SBOM, attestations, coverage, security, docs, registry status | CI gates and release evidence bundle |

## Required Checks

- Schema drift check: generated schemas must match committed schemas.
- Fixture conformance check: every public surface must pass shared golden fixtures before support claims.
- Negative conformance check: unsupported years, streams, jurisdictions, classification versions, and surfaces must fail closed with diagnostics.
- Documentation conformance check: docs examples must reference current schemas and validated support statuses.
- Release conformance check: no release may be published without evidence bundle links.
- Stub/fake check: tracks cannot complete if public files contain placeholder implementations without explicit blocked status.

## Completion Gate

A contract is complete only when it has:

- version identifier;
- machine-readable schema or equivalent ABI/API definition;
- examples;
- positive and negative tests;
- documentation;
- compatibility or migration notes;
- release evidence or explicit unpublished status.
