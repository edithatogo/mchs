# Review: Outer Wrapper Retirement Migration

## Verdict

Reviewed; locally complete with an explicit outer-wrapper cleanup gate.

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
6. Phase 3 validation is recorded in
   `conductor/outer-wrapper-migration-manifest.json`: canonical topology passes,
   focused governance tests pass, the stub detector reports zero findings, and
   the explicit outer-root validation fails closed with the expected diagnostics.

## Validation

- `uv run pytest tests/test_repository_topology_governance.py -q`
- `uv run python scripts/validate_repository_topology.py --json`
- `uv run python scripts/validate_repository_topology.py --json --outer-root /Volumes/PortableSSD/GitHub/mchs` currently fails with unmanaged gitlink and nested-repo diagnostics, as recorded in the cleanup gate.
- `uv run ruff check tests/test_repository_topology_governance.py scripts/validate_repository_topology.py`
- `uv run ty check tests/test_repository_topology_governance.py scripts/validate_repository_topology.py`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

No local canonical-repo archive blocker remains. The only residual gate is
user-owned parent-wrapper cleanup: retire or formalize
`/Volumes/PortableSSD/GitHub/mchs` outside this canonical repo track when the
user is ready to remove the local wrapper.
