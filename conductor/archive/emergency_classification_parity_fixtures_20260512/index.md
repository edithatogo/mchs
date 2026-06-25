# Track emergency_classification_parity_fixtures_20260512 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)

## Governance Summary

- Primary contract: `nwau_py.emergency_classification_parity_fixtures` metadata-only emergency parity fixture contract for synthetic and local-only licensed fixtures covering UDG, AECC, transition handling, and downstream emergency NWAU validation under registry-backed era selection.
- Dependencies: `emergency_udg_aecc_transition_registry_20260512`; `emergency_code_mapping_pipeline_20260512`; `emergency_grouper_integration_20260512`.
- Completion evidence: metadata contract alignment, fixture schema and loader tests, fixture workflow documentation, and review notes.
- Publication status: `not-ready`
- Validation status: `not-validated`
- Licensing caveats: do not embed or redistribute licensed UDG, AECC, mapping, or grouper tables unless the source license explicitly permits it; keep local official and user-supplied reference fixtures outside the repository unless they are synthetic or otherwise redistributable; do not imply a UDG-to-AECC crosswalk or fallback mapping that the source evidence does not support.
- Evidence surfaces: `metadata.json`, `spec.md`, `plan.md`, `index.md`, fixture manifests and loader tests, fixture workflow documentation, and review notes.
