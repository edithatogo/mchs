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
- `power-platform/solution/app-surface.json`: app selector, capability discovery,
  and no-formula surface contract validated by
  `scripts/validate_power_platform_capabilities.py`.

## Included Source Assets

- App surface manifest: `apps/mchs-orchestrator/app-surface-manifest.json`.
- App capability surface: `app-surface.json`.
- Environment variables: `environment-variables.json`.
- Connection references: `connection-references.json`.
- Flow definition: `flows/mchs-submit-calculation.json`.
- Custom connector/service-boundary binding:
  `contracts/power-platform/power-platform-binding.contract.json` and
  `contracts/power-platform/custom-connector.openapi.yaml`.

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
