# Outer Wrapper Retirement

## Purpose

The parent `mchs` checkout currently behaves like a transitional wrapper around
the canonical `microcosting_healthservices` repo. It also contains source-like
Power Platform files, scripts, tests, evidence captures, and tracked generated
logs. The wrapper must be retired or formalized only after source and evidence
are preserved.

## Migration Classes

- `migrate`: unique source, tests, docs, contracts, or Power Platform models
  that belong in the canonical repo.
- `archive`: evidence that supports a release, registry, browser, or ALM claim
  and should be retained with checksums and ownership.
- `delete`: generated or duplicate artifacts with no evidence value.
- `ignore`: local caches, browser state, tool history, and temporary outputs.
- `retain-external`: files that remain outside the canonical repo because they
  are user-local, credential-bearing, or not redistributable.
- `duplicate`: files already represented in the canonical repo.

## Required Manifest

Before removing or migrating wrapper files, create a manifest that records path,
classification, destination or retention reason, checksum for preserved files,
owning track, validation command, and residual blocker if any. The current
Phase 1 manifest is `conductor/outer-wrapper-migration-manifest.json`.

The manifest is inventory evidence, not cleanup authority. It may classify a
path as `delete` or `ignore`, but no outer-wrapper file may be removed until
the path has either been preserved, proven duplicate, or explicitly accepted as
local-only/generated.

## Retirement Sequence

1. Inventory tracked files, untracked files, ignored files, and gitlinks.
2. Compare each source-like path with the canonical repo.
3. Preserve unique source and evidence slices.
4. Remove or ignore generated output after preservation.
5. Resolve the broken gitlink by retiring the wrapper or converting it into a
   valid superproject with `.gitmodules`.
6. Record remaining user or external gates separately from local repo cleanup.

## Non-Goals

Wrapper retirement does not publish packages, complete external reviews, or
change calculator runtime behavior.
