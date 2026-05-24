# Plan: Power Platform Subrepo ALM Foundation

## Phase 1: Repository Boundary Audit

- [x] Task: Inventory current gitlink, submodule, subtree, and local worktree state
    - [x] Record whether `microcosting_healthservices` is a submodule, subtree, or nested repo
    - [x] Identify missing `.gitmodules` or remote metadata
    - [x] Record all dirty unrelated changes that must not be overwritten
- [x] Task: Choose the supported source-control model
    - [x] Select submodule, subtree, or standalone repository with documented synchronization rules
    - [x] Define branch, remote, and ownership rules
    - [x] Define how Conductor tracks reference the Power Platform repo
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Repository Boundary Audit' (Protocol in workflow.md)

## Phase 2: ALM Source Layout

- [x] Task: Create the Power Platform source root contract
    - [x] Define folders for unpacked solution, connector, apps, flows, deployment settings, and evidence
    - [x] Add README ownership rules and forbidden generated-file edits
    - [x] Define generated artifact boundaries for packed solution zips
- [x] Task: Add subrepo health checks
    - [x] Check that the configured Power Platform repo is reachable
    - [x] Check that required folders exist
    - [x] Check that no broken gitlink state remains
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: ALM Source Layout' (Protocol in workflow.md)
