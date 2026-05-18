# Power Platform Repository Boundary Contract

## Decision

Use the in-repository `power-platform/` tree as the canonical editable source
until a real remote subrepo is provisioned. Do not rely on a gitlink without a
`.gitmodules` mapping as evidence of managed ALM.

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

## Synchronization Rules

If split into a subrepo later, record:

- remote URL
- default branch
- commit pinned by the parent repository
- push/pull procedure
- release artifact procedure
- responsible owner for NSW environment import
