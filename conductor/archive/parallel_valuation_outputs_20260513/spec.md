# Specification: Parallel Valuation Outputs

## Overview

Allow one HWAU calculation to produce multiple price valuations in parallel.
Formula execution and pricing application must remain separate.

## Requirements

- Produce HWAU-only output.
- Produce national efficient price valuation where available.
- Produce state-specific price valuation where available.
- Produce local price valuation where available.
- Produce discounted price valuation from declarative discount rules.
- Preserve provenance for every valuation column.
- Support parallel output through CLI/file, HTTP API, MCP, and OpenAI adapter
  surfaces.

## Acceptance Criteria

- Valuation output schema supports multiple named price schedules.
- Each valuation records price source, rule, year, jurisdiction, and checksum.
- Missing price schedules fail closed or return blocked status.
- Tests cover parallel national, state, local, and discounted valuations.
