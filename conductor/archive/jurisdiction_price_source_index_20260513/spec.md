# Specification: Jurisdiction Price Source Index

## Overview

Create a source index for Australian jurisdiction price and activity-unit
models before extracting or committing values.

## Requirements

- Cover NSW, VIC, QLD, WA, SA, TAS, ACT, and NT.
- Record source title, URL/path, checksum, licence status, retrieval date,
  source unit, mapped HWAU unit, stream applicability, and extraction notes.
- Mark restricted or unclear sources as `blocked` or `local_only`.
- Prevent hard-coded values without provenance.

## Acceptance Criteria

- Source index schema exists.
- Public-safe source rows exist for each jurisdiction or blocked-source rows are
  explicit.
- Price extraction tracks depend on the source index.
