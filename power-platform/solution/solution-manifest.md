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

## Exclusions

- Calculator formulas.
- Embedded business logic that duplicates the core engine.
- Direct production data handling outside the secure service boundary.
