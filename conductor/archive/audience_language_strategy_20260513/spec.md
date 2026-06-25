# Specification: Audience Language Strategy

## Overview

Refocus language support around two primary audiences: researchers and
enterprise engineers. This strategy prevents language sprawl and keeps Rust Core
GA, canonical contracts, CLI/file, API, MCP, C#/.NET, Python, R, Julia, SAS,
Stata, and optional TypeScript/WASM as higher priorities than additional
bindings.

## Requirements

- Define researcher-priority surfaces.
- Define enterprise-engineer-priority surfaces.
- Mark conditional and deprioritized languages.
- Keep existing SAS, Stata, and Julia work where it exists.
- Keep TypeScript/WASM as the optional web/GitHub Pages surface.
- Mark Scala/Spark, Swift, Go, MATLAB, standalone C, and SQL/DuckDB as
  no-new-development by default.
- Require a named audience, owner, contract tests, fixtures, examples, and
  release evidence before any language moves forward.
- Preserve the rule that adapters cannot own formula logic.

## Acceptance Criteria

- Audience language strategy roadmap exists.
- Conductor tracks identify deferred language work.
- Future binding promotion requires audience and evidence justification.
