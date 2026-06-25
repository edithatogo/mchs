# Review: Repository Topology Authority

## Status

Reviewed on 2026-06-25. Archive eligible as a completed governance-control
track.

## Scope Reviewed

- `conductor/repository-topology.md` names `microcosting_healthservices` as the
  canonical implementation repository and treats the outer `mchs` checkout as a
  transitional wrapper.
- The policy bans unmanaged nested `.git` directories, unmanaged gitlinks,
  unregistered package manifests, tracked generated directories, and duplicate
  wrapper-level source without migration evidence.
- `scripts/validate_repository_topology.py` and
  `tests/test_repository_topology_governance.py` provide executable guardrails.

## Findings

- This track establishes governance authority only; it does not move wrapper
  files, split repositories, or publish packages.
- Outer wrapper migration remains owned by
  `outer_wrapper_retirement_migration_20260624`.

## Validation

- `uv run pytest tests/test_repository_topology_governance.py`
- `uv run python scripts/validate_repository_topology.py --json`
- `python conductor/scripts/stub_detector.py --root . --json`
