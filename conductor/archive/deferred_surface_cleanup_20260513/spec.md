# Specification: Deferred Surface Cleanup

## Overview

Review generated Scala/Spark, Swift, Go, MATLAB, standalone C, and SQL/DuckDB
surface artefacts after Cline finishes. Existing work may be retained, but no
new development should be merged unless explicitly reprioritized.

## Requirements

- Inventory generated deferred surface artefacts.
- Decide keep-as-roadmap, quarantine, or remove.
- Ensure tests do not require deferred surfaces.
- Preserve Stata where it has a health-economics audience.
- Preserve Julia where existing binding work is valid.

## Acceptance Criteria

- Deferred surfaces are not required for CI.
- No deferred surface is marked active, preview, RC, or GA.
- Any retained artefacts are clearly marked `no_new_development` or
  `historical`.
