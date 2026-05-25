# App Surface

## Responsibilities

- Collect user inputs.
- Orchestrate calls to the secure service boundary.
- Present structured results and validation messages.

## Non-Responsibilities

- Do not calculate the business result in the app layer.
- Do not duplicate formula logic.
- Do not store sensitive business rules inside forms, flows, or tables.

## Runtime Contract

- The app is a user-facing orchestration shell.
- The app consumes environment variables and connection references.
- The app must stay aligned with the service-boundary contract.
- Runtime execution must be proven through app-player smoke evidence before the
  app is described as runnable in the target tenant. The 2026-05-25 evidence
  records authenticated PAC access but not app-player execution.

Machine-readable definition:

- `power-platform/apps/mchs-orchestrator/app-surface-manifest.json`
