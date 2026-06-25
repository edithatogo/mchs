# Review: Repository Topology CI Gate

## Status

Reviewed on 2026-06-25. Archive eligible as a completed governance-control
track.

## Scope Reviewed

- `scripts/validate_repository_topology.py` validates nested `.git`
  directories, unmanaged gitlinks, unregistered package manifests, missing
  owner tracks, missing manifests, duplicate manifest ownership, generated
  artifact drift, and explicit outer-wrapper gitlink state.
- `.github/workflows/pr-ci.yml` runs the validator in PR CI.
- `tests/test_repository_topology_governance.py` exercises valid current state,
  synthetic unmanaged outer gitlink detection, generated artifact policy
  helpers, and PR-CI wiring.

## Findings

- The validator is fail-closed and local; it does not require registry
  credentials.
- Automatic repair of invalid topology is intentionally out of scope.

## Validation

- `uv run python scripts/validate_repository_topology.py --json`
- `uv run pytest tests/test_repository_topology_governance.py`
- `python conductor/scripts/stub_detector.py --root . --json`
