# Review: Outer Wrapper Retirement Migration

## Verdict

Phase 2 reviewed; continue to validation.

## Findings

1. This track is explicitly `status: new` and `current_state: in-progress`.
2. Phase 1 inventory is now complete: `conductor/outer-wrapper-migration-manifest.json` records the unmanaged gitlink, tracked generated logs, untracked source/governance slices, Power Platform evidence files, dispositions, and SHA-256 checksums where files exist.
3. Phase 2 preservation is complete within the canonical repo: the migration
   manifest records `preserved-in-canonical-root`, retained external evidence,
   generated-log cleanup eligibility, and the `retire-wrapper` decision for the
   unmanaged gitlink.
4. No outer-wrapper files were deleted by this canonical-repo track. The
   remaining parent-wrapper work is a user-owned cleanup gate.
5. Current outer-root topology validation is expected to fail until the wrapper
   gitlink is retired or formalized and tracked generated logs are removed or
   archived.

## Validation

- `uv run pytest tests/test_repository_topology_governance.py -q`
- `uv run python scripts/validate_repository_topology.py --json`
- `uv run python scripts/validate_repository_topology.py --json --outer-root /Volumes/PortableSSD/GitHub/mchs` currently fails with unmanaged gitlink and nested-repo diagnostics, as recorded in the cleanup gate.
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Re-run Phase 3 validation and record the residual gates.
- Retire or formalize `/Volumes/PortableSSD/GitHub/mchs` outside this canonical
  repo track when the user is ready to remove the local wrapper.
