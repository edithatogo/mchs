# Specification: CLI/File Contracts

## Overview

Define the stable CLI and file boundary for Rust Core GA. This is the first
execution surface because it is reproducible, batch-friendly, and useful for
researchers and enterprise engineers.

## Requirements

- Define commands: `schema`, `validate`, `run`, `explain`,
  `list-calculators`, `list-streams`, `list-years`, and `diagnose`.
- Define stable exit codes.
- Define stdin/stdout/stderr behavior.
- Require machine-readable `--json`.
- Define JSON manifest plus Arrow/Parquet batch file contracts.
- Preserve diagnostics and provenance in every run.

## Acceptance Criteria

- CLI contract docs exist.
- File contract schemas exist.
- Pass and fail fixtures cover exit codes, JSON output, and provenance.
- The CLI does not implement separate formula logic.
