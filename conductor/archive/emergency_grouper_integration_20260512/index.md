# Track emergency_grouper_integration_20260512 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)

## Governance Summary

- Primary contract: `nwau_py.emergency_grouper` integration boundary for precomputed UDG/AECC outputs and licensed external grouper or mapping-service workflows, with registry-driven era selection and provenance capture.
- Dependencies: `emergency_udg_aecc_transition_registry_20260512`; `emergency_code_mapping_pipeline_20260512`.
- Completion evidence: interface contract docs, adapter and compatibility tests, provenance records, workflow documentation, and review notes.
- Publication status: `not-ready`
- Validation status: `not-validated`
- Licensing caveats: do not embed or redistribute licensed emergency grouper tables, manuals, or mapping bundles unless the source license explicitly permits it; do not invent UDG-to-AECC crosswalks or silently convert between eras without registry-backed provenance.
- Evidence surfaces: `metadata.json`, `spec.md`, `plan.md`, `index.md`, adapter tests, workflow documentation, provenance records, and registry/mapping pipeline outputs.
