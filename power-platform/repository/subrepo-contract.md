# Power Platform Repository Boundary Contract

## Decision

Treat `power-platform/` as a governed subrepo boundary inside the parent
repository until a standalone remote is provisioned. The boundary is enforced by
`power-platform/repository/subrepo-manifest.json`, Power Platform ALM tests, and
the repo-health scorecard.

Do not rely on a gitlink without a `.gitmodules` mapping as evidence of managed
ALM. A split to a standalone Git submodule or subtree is allowed only when the
remote URL, pinned commit, sync procedure, and NSW import owner are recorded.
The 9.9 repo-health gate additionally requires either a standalone remote URL
or an explicit waiver approver before the closure can be claimed complete.

## Legacy State

A previous top-level checkout showed `microcosting_healthservices` as mode
`160000` but did not include a `.gitmodules` mapping. That is a broken submodule
configuration from an ALM perspective. The completion program must either:

1. keep Power Platform assets in this repository, or
2. create a valid submodule/subtree with remote URL, branch, and sync commands.

## Ownership Rules

- Editable source lives under `power-platform/`.
- Packed solution zip artifacts are release outputs, not hand-edited source.
- Environment values are templates only; secrets and tenant-specific credentials
  are injected at deployment time.
- Source assets must remain synthetic and public-safe.
- Apps, flows, connector policies, and Dataverse assets must not contain MCHS
  calculator formulas or private NSW operational data.
- Parent repository code must consume this surface through documented service,
  connector, and ALM contracts, not by reaching into generated solution artifacts.
- Power Platform source changes must include evidence updates or an explicit
  blocker in `power-platform/evidence/deployment-status.json`.

## Synchronization Rules

If split into a subrepo later, record:

- remote URL
- default branch
- commit pinned by the parent repository
- push/pull procedure
- release artifact procedure
- responsible owner for NSW environment import
- either the standalone remote URL or the waiver approver before any 9.9 claim

## Current Subrepo Boundary

- Mode: in-repository governed subrepo boundary.
- Path: `power-platform/`.
- Parent repository remote: `https://github.com/edithatogo/mchs`.
- Standalone remote: not provisioned.
- Promotion state: managed solution shell imported into NSW `dylan`; runtime
  app/flow smoke is still blocked.
- Required migration before standalone split: create remote, move history or
  seed source, pin the parent repository to a gitlink or subtree commit, and
  update this contract and `subrepo-manifest.json`.
