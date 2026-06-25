# Future Repo Split Playbook

## Default

Keep package surfaces in the canonical monorepo unless there is evidence that a
split is safer. The monorepo is the current authority for shared calculator
contracts, Rust core promotion, bindings, docs, release evidence, and support
status.

## Split Eligibility

A surface may become a split candidate only when all are true:

- the package surface registry has an owner, support status, release target,
  validation command, and evidence boundary;
- the surface is a thin adapter over shared contracts;
- split benefits are concrete, such as registry requirements, independent
  release cadence, ecosystem norms, or CI isolation;
- source and release history can be preserved;
- docs and registry metadata can be updated without breaking users.

Do not split a surface to hide scaffold work, failing tests, or missing
publication evidence.

## Extraction Procedure

Use `git subtree split` or an equivalent audited history-preserving procedure.
The extracted repo must retain license, README, package manifest, CI, tags or
version lineage, support status, and compatibility tests against the shared
contract.

## Continuity Requirements

Before switching users or registries to an extracted repo, prove:

- package name and version continuity;
- registry metadata points to the correct repository;
- CI passes in the extracted repo;
- compatibility tests pass against canonical fixtures;
- rollback instructions exist.

## Rollback

If publication proof, CI, or compatibility fails, keep the monorepo source as
authoritative and mark the split candidate as blocked until the cause is fixed.
