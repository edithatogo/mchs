# IHACPA Capability Matrix Runtime Truth

## Overview

The deployed tool and repository documentation must expose the same support status for each year, stream, classifier, and runtime surface.

## Requirements

- Generate capability matrices from canonical manifests and support-state contracts.
- Expose statuses such as `source_available`, `executable`, `validated`, `blocked_licensed`, and `out_of_scope`.
- Ensure CLI, MCP/API, docs, and generated package metadata use the same source.
- Prevent placeholder execution paths from returning ambiguous success when calculation is not implemented.
- Link capability gaps to Conductor tracks and GitHub issues.

## Acceptance Criteria

- Runtime status APIs and docs match generated matrix fixtures.
- Unsupported or source-only calculator requests fail closed with actionable status and provenance.
- MCP/API calculator responses distinguish validation, source availability, and missing implementation.
- CI catches manual drift in committed capability outputs.

## Out of Scope

- Implementing all calculator formulas.
- Adding licensed assets.
