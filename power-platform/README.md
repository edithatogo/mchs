# MCHS Power Platform ALM Surface

This tree is the source-controlled Power Platform delivery surface for MCHS.
It is intentionally orchestration-only: apps, flows, and custom connectors call
an approved service boundary and must not implement calculator formula logic.

## Source-Control Model

The current repository uses an in-repository Power Platform source tree under
`power-platform/`. The previous top-level workspace contained a gitlink-like
`microcosting_healthservices` entry without a `.gitmodules` mapping; that state
is treated as legacy and must not be used as deployment evidence.

If this surface is later split into a standalone subrepo, add an explicit
`.gitmodules` entry or documented subtree import procedure before claiming a
subrepo-managed deployment.

## Required Layout

- `repository/`: subrepo/subtree ownership and synchronization contract.
- `settings/`: environment-neutral solution settings and deployment templates.
- `connectors/`: service-boundary contract and custom connector source assets.
- `service/`: deployable HTTP service boundary used by the connector.
- `solution/src/`: unpacked solution source tree.
- `apps/`: app source manifests or exported source packages.
- `flows/`: Power Automate flow source definitions.
- `pipelines/`: local and CI ALM command documentation.
- `deployment/`: target-environment deployment plans and blocked/complete evidence.
- `evidence/`: validation, checker, import, smoke, and governance evidence.
- `governance/`: privacy, DLP, monitoring, and support controls.

## Claim Boundary

A track is complete only when its artifacts exist and its evidence is recorded.
NSW deployment, managed promotion, and production readiness must not be claimed
until target-environment import and smoke evidence exists.
