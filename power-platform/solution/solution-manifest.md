# Solution Manifest Skeleton

## Solution Identity

- Solution display name: `Microcosting Health Services ALM`
- Solution unique name: `mchs_alm_orchestration`
- Solution type: solution-based app orchestration package
- Versioning strategy: semantic versioning tracked in source control

## Packaging Contract

- Authoring format: unpacked source tree.
- Build format: packed solution artifact for import into target environments.
- Promotion format: managed solution for downstream environments.

Machine-readable root manifest:

- `source-controlled-metadata.json`: solution package identity and component map for source-control and tooling checks.

## Included Asset Placeholders

- App surface manifest: `apps/mchs-orchestrator/app-surface-manifest.json`.
- Environment variables: `environment-variables.json`.
- Connection references: `connection-references.json`.
- Flow definition: `flows/mchs-submit-calculation.json`.
- Custom connector/service-boundary binding captured in connection references.

## Observed Deployed State

- Target environment observed through PAC:
  `611bca65-0b2a-eaa1-9e74-23bbba8eeec4`.
- Deployed solution observed: `mchs_alm_orchestration` version `0.2.2.0`.
- Deployed solution is managed, so PAC export is blocked in this environment.
- Runtime evidence and remaining blockers are recorded in
  `runtime-evidence-20260525.md`.

## Exclusions

- Calculator formulas.
- Embedded business logic that duplicates the core engine.
- Direct production data handling outside the secure service boundary.
