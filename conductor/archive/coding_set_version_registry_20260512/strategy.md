# Strategy: Coding-Set Version Registry

## Decision
Use a versioned, machine-readable registry as the authoritative source for
coding-set version compatibility, pricing-year applicability, stream
applicability, and licensing boundaries.

The registry is a data contract, not a narrative note. It should be consumed by
the classification input validator, the licensed-product workflow, and any
future mapping or grouper registry tracks.

## Registry shape

Each registry entry should carry:

- coding-set family name
- version
- release or effective date
- applicable pricing years
- applicable stream or streams
- status such as `current`, `legacy`, `planned`, or `restricted`
- public metadata
- source basis
- license boundary notes
- local-only or restricted artifact locator when relevant

## Compatibility policy

- Accept only versions explicitly supported by the published IHACPA source
  set.
- Fail closed on unknown versions, ambiguous pricing-year applicability, or
  unclear licensing boundaries.
- Do not silently coerce between UDG and AECC, AR-DRG versions, or other
  classification families.
- Treat the published compatibility matrix as the current validation anchor for
  2022-23 through 2026-27 until a future back-cast rule says otherwise.

## Downstream consumers

- `classification_input_validation_20260512` consumes the registry for
  preflight checks.
- `icd_achi_acs_license_workflow_20260512` owns the handling rules for
  restricted products and local-only assets.
- AR-DRG and emergency transition registry tracks should inherit the same
  version and licensing vocabulary rather than redefining it.

## Readiness bar

- This track implements a metadata-only registry and compatibility validators.
- Do not claim licensed artifact redistribution or grouper integration from
  this registry alone.
- Do not treat the registry as complete until the current IHACPA classification
  families are represented and the documented license boundary rules are wired
  into validation.
