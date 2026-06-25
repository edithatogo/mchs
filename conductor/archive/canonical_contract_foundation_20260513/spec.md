# Specification: Canonical Contract Foundation

## Overview

Create canonical, versioned domain contracts before adding more delivery
surfaces. These contracts are the source of truth for Rust Core GA, CLI/file,
HTTP API, MCP, OpenAI tools, and language adapters.

## Requirements

- Define JSON Schema contracts for calculator request, response, diagnostics,
  errors, provenance, stream/year support status, and evidence bundles.
- Define OpenAPI-compatible schemas without making the HTTP API the source of
  truth.
- Define Arrow/Parquet batch schema derivation rules.
- Require all adapters to validate against these contracts.
- Fail closed for unsupported streams, years, or schema versions.

## Acceptance Criteria

- Canonical schemas are versioned and documented.
- CLI/file, HTTP API, MCP, and OpenAI adapter tracks depend on this foundation.
- Contract tests validate pass and fail examples.
- No formula logic is represented in adapter-specific contracts.
