# Track icd_achi_acs_license_workflow_20260512 Context

- Contract: define a local-only workflow for licensed ICD-10-AM, ACHI, ACS, and related admitted-acute classification products without bundling restricted content.
- Boundary: user-supplied licensed assets may be referenced through local paths, environment variables, and manifests, but they must stay out of version control and published artifacts.
- Evidence surfaces: spec, plan, metadata, guards, setup docs, and synthetic-safe tests.
- Caveats: the track documents lawful local use only and does not redistribute, mirror, or vendor licensed products.

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)

## Governance Summary
- Contract: local-only handling for user-supplied ICD-10-AM, ACHI, ACS, and grouper assets.
- Boundary: no restricted products, manuals, or binaries may be committed, mirrored, or redistributed from this repository.
- Evidence: docs, repository guards, and synthetic-safe tests only.
- Caveat: the user is responsible for lawful access to any licensed classification content.
