# Review: Outer Wrapper Retirement Migration

## Verdict

Reviewed; keep live as `in-progress`.

## Findings

1. This track is explicitly `status: new` and `current_state: in-progress`.
2. Archive is blocked by design: wrapper inventory, migration manifest, checksums, preservation evidence, retirement decision, and outer-root validation are not complete.
3. Current topology validation is not clean: it reports tracked generated archive artifacts under `bindings/matlab/` and `bindings/stata/`, and the repository-topology test also still detects a README registry-status wording gap for Swift Package Index evidence.

## Validation

- `uv run pytest tests/test_repository_topology_governance.py -q`
- `uv run python scripts/validate_repository_topology.py --json` currently fails with tracked generated-artifact diagnostics.
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Complete the outer wrapper inventory.
- Preserve source and evidence slices with checksums.
- Record the delete/archive/formalize decision.
- Re-run canonical and outer-root topology validation after migration.
- Resolve or evidence-classify the tracked MATLAB/Stata zip artifacts and reconcile README registry-status wording.
