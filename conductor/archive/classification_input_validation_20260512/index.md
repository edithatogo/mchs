# Track classification_input_validation_20260512 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)

## Current State

Phase 1 has a conservative compatibility matrix for AR-DRG, AECC, UDG, Tier 2,
and AMHCC. The matrix is a validation input, not the canonical coding-set
registry: durable version ownership remains with the coding-set registry and
licensed-product workflow tracks.

The shared preflight validator exists in `nwau_py.classification_validation`
and is exported through `nwau_py`. It validates stream-specific required fields
and pricing-year-specific versions without redistributing licensed classification
products. The archived scope is complete for the shared validator and matrix,
with an accepted gap that not every calculator and CLI entry point is documented
as enforcing the validator end-to-end.
