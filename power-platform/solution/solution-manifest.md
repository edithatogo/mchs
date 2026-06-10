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

## Included Asset Placeholders

- Canvas or model-driven app surface.
- Source-controlled app selector model:
  `power-platform/solution/app-surface.json`.
- Environment variables.
- Connection references.
- Custom connector or service-boundary binding.
- Optional Dataverse tables for orchestration metadata only.
- Contract-bound connector artifact:
  `contracts/power-platform/custom-connector.openapi.yaml`.
- Contract bundle:
  `contracts/power-platform/power-platform-binding.contract.json`.
- Calculator capability matrix:
  `contracts/power-platform/calculator-capability-matrix.json`.

## Exclusions

- Calculator formulas.
- Embedded business logic that duplicates the core engine.
- Direct production data handling outside the secure service boundary.

## Local Validation

Credential-free validation is provided by:

```bash
python scripts/validate_power_platform_capabilities.py
uv run pytest tests/test_power_platform_binding_track.py
```

Tenant-bound validation such as `pac solution check` remains an external ALM
gate and is not required for local contract checks.
