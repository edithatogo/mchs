# Plan: Repository Topology Authority

## Phase 1: Authority Baseline

- [x] Task: Establish the canonical root decision.
    - [x] Record `microcosting_healthservices` as the canonical implementation root.
    - [x] Record the outer repo as transitional and non-authoritative.
    - [x] Separate local topology completion from external registry gates.
- [x] Task: Define permitted repository layouts.
    - [x] Allow ordinary package subdirectories managed by the monorepo.
    - [x] Ban unmanaged nested `.git` directories.
    - [x] Ban gitlinks without a valid `.gitmodules` entry and owner.
- [x] Task: Conductor - User Manual Verification 'Authority Baseline' (Protocol in workflow.md)

## Phase 2: Topology Policy

- [x] Task: Write the repository topology policy.
    - [x] Classify source, generated, evidence, archive, vendor, and local-environment directories.
    - [x] Define deletion and migration rules for transitional wrapper files.
    - [x] Define ownership handoff rules for package surfaces.
- [x] Task: Cross-link governance.
    - [x] Link package ownership, release boundary, artifact retention, worktree hygiene, and split playbook tracks.
    - [x] Update Conductor registry references.
- [x] Task: Conductor - User Manual Verification 'Topology Policy' (Protocol in workflow.md)

## Phase 3: Validation and Review

- [x] Task: Add topology policy tests.
    - [x] Assert canonical root and outer wrapper vocabulary.
    - [x] Assert unmanaged gitlinks are prohibited.
    - [x] Assert package surfaces must be registry-owned.
- [x] Task: Run focused validation.
    - [x] Run `uv run pytest tests/test_repository_topology_governance.py`.
    - [x] Run `uv run python scripts/validate_repository_topology.py`.
- [x] Task: Conductor - User Manual Verification 'Validation and Review' (Protocol in workflow.md)
