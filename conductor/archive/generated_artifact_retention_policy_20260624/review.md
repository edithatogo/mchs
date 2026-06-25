# Review: Generated Artifact Retention Policy

## Status

Reviewed on 2026-06-25. Archive eligible as a completed governance-control
track.

## Scope Reviewed

- `conductor/generated-artifact-retention-policy.md` defines source,
  generated-ignore, release-attachment, evidence-allowed, external-archive, and
  local-only classes.
- `scripts/validate_repository_topology.py` blocks tracked generated paths,
  cache/build directories, and package artifact suffixes unless an explicit
  evidence pattern allows them.
- `contracts/repository-topology/package-surfaces.json` records
  `artifact_policy` for package surfaces.

## Findings

- The policy is deterministic and local.
- Existing tracked SAS archive zip files and VSIX release evidence are explicit
  evidence exceptions, not general permission to track generated output.
- Bulk cleanup of local untracked generated folders remains separate hygiene
  work.

## Validation

- `uv run pytest tests/test_repository_topology_governance.py`
- `python conductor/scripts/stub_detector.py --root . --json`
