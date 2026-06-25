# Repository Topology

## Authority

`microcosting_healthservices` is the canonical implementation repository for
MCHS. The parent `mchs` checkout is a transitional wrapper and must not be used
as the source of truth for package ownership, support status, release evidence,
or Conductor completion.

The canonical repo remains a monorepo for now. Python, Rust, docs, language
bindings, Power Platform source models, registry packaging, contracts, and
evidence records are governed as package surfaces inside this root unless the
future repo split playbook approves extraction.

## Permitted Layouts

- Ordinary source directories owned by the canonical repo.
- Package subdirectories with manifests registered in
  `contracts/repository-topology/package-surfaces.json`.
- External source archives and raw evidence directories when governed by source
  archive policy and support-status caveats.
- Generated artifacts only when ignored, release-attached, or explicitly
  evidence-owned by a track.

## Prohibited Layouts

- Nested `.git` directories below the canonical root.
- Gitlinks without a matching `.gitmodules` section and an approved owner.
- Package manifests without a package surface registry entry.
- Generated dependency or build directories committed as source.
- Wrapper-level source or evidence files that duplicate canonical paths without
  a migration manifest.

## Ownership Rules

Every package surface must declare:

- local path and manifest files, if implemented in the monorepo;
- owner Conductor track;
- support status using the approved vocabulary;
- CI or validation gate;
- release target and version source;
- evidence boundary for publication and support claims;
- artifact retention policy.

Package surfaces are adapters over shared calculator contracts. They must not
duplicate calculator formula logic.

## Wrapper Rule

The outer wrapper may only be used as migration input. Its source and evidence
files must be classified before deletion or migration. If the wrapper is kept as
a real superproject, it must have a valid `.gitmodules` entry for every gitlink
and a documented reason to remain.

## Completion Rule

Local repository completion and external registry, reviewer, or account gates
are different blocker classes. A local topology gate can pass while a registry
publication remains submitted or blocked.
