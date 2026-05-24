# Power Platform Solution Scaffold

This directory is the tracked source-control home for the Power Platform ALM app.

## Scope

- Solution-based ALM only.
- Orchestration-only app surface.
- No calculator formula logic.
- Managed-solution promotion downstream.

## Intended Contents

- `solution-manifest.md`: solution identity, versioning, and packaging contract.
- `environment-variables.md`: environment variable names and default semantics.
- `connection-references.md`: connector and service connection references.
- `app-surface.md`: app orchestration responsibilities and non-responsibilities.

## Source-Control Rule

Unpacked solution assets are the editable source-of-truth representation for the
Power Platform app. Build and promotion use `pac`-driven pack/unpack operations.

## Implemented Source-Control Payload

- `source-controlled-metadata.json`: root solution metadata and component map.
- `environment-variables.json`: environment-variable contract source of truth.
- `connection-references.json`: connection-reference contract source of truth.
- `apps/mchs-orchestrator/app-surface-manifest.json`: app orchestration surface contract.
- `flows/mchs-submit-calculation.json`: orchestration flow definition used by the app.
