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

## Final Canonical Decision

The canonical repository preservation decision is complete for this track:
source and governance slices needed for continued implementation are represented
in `microcosting_healthservices`, and evidence-bearing wrapper files are
manifested with checksums instead of being silently discarded. The recommended
wrapper outcome is `retire-wrapper-after-canonical-preservation`.

The parent `/Volumes/PortableSSD/GitHub/mchs` checkout still has user-owned
cleanup work because it is a dirty outer repository containing an unmanaged
`microcosting_healthservices` gitlink, generated Playwright logs, local caches,
and evidence files. This track does not delete those outer files. Cleanup must
use `conductor/outer-wrapper-migration-manifest.json` as the authority for
whether each file is already preserved, should be retained externally, can be
ignored, or can be deleted after evidence review.

Run these validations when making the outer cleanup decision:

```bash
uv run python scripts/validate_repository_topology.py --json
uv run python scripts/validate_repository_topology.py --json --outer-root /Volumes/PortableSSD/GitHub/mchs
uv run pytest tests/test_repository_topology_governance.py -q
```

The explicit `--outer-root` validation is expected to fail until the parent
wrapper is actually retired or formalized as a valid superproject with
`.gitmodules`. That failure is an outer-wrapper cleanup gate, not evidence that
the canonical repo preservation work is incomplete.

## Outer Cleanup Actions

No automated deletion of `/Volumes/PortableSSD/GitHub/mchs` files is performed
by this canonical-repo track. The cleanup actions are:

1. Review evidence entries in the migration manifest before deleting outer
   files.
2. Remove or archive generated Playwright logs and local caches from the parent
   wrapper.
3. Retire the parent wrapper or formalize it as a superproject by adding
   `.gitmodules` metadata for the `microcosting_healthservices` gitlink.
4. Rerun the explicit `--outer-root` topology validation and treat any remaining
   unmanaged gitlink or nested-repo diagnostic as an outer-wrapper cleanup
   blocker.

## Non-Goals

Wrapper retirement does not publish packages, complete external reviews, or
change calculator runtime behavior.
