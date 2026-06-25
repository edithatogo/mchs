# Review: Outer Wrapper Retirement Migration

## Verdict

Reviewed; keep live as `in-progress`.

## Findings

1. This track is explicitly `status: new` and `current_state: in-progress`.
2. Phase 1 inventory is now complete: `conductor/outer-wrapper-migration-manifest.json` records the unmanaged gitlink, tracked generated logs, untracked source/governance slices, Power Platform evidence files, dispositions, and SHA-256 checksums where files exist.
3. Archive is still blocked by design: preservation evidence, retirement decision, and post-migration outer-root validation are not complete.
4. Current outer-root topology validation is expected to fail until the wrapper gitlink is retired or formalized and tracked generated logs are removed or archived.

## Validation

- `uv run pytest tests/test_repository_topology_governance.py -q`
- `uv run python scripts/validate_repository_topology.py --json --outer-root /Volumes/PortableSSD/GitHub/mchs` currently fails with unmanaged gitlink diagnostics.
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Preserve source and evidence slices according to the migration manifest.
- Record the delete/archive/formalize decision.
- Re-run canonical and outer-root topology validation after migration.
- Resolve or evidence-classify tracked generated artifacts before wrapper cleanup.
