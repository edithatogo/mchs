# Plan: Power Platform Subrepo ALM Foundation

## Phase 1: Repository Boundary Audit

- [ ] Task: Inventory current gitlink, submodule, subtree, and local worktree state
    - [ ] Record whether `microcosting_healthservices` is a submodule, subtree, or nested repo
    - [ ] Identify missing `.gitmodules` or remote metadata
    - [ ] Record all dirty unrelated changes that must not be overwritten
- [ ] Task: Choose the supported source-control model
    - [ ] Select submodule, subtree, or standalone repository with documented synchronization rules
    - [ ] Define branch, remote, and ownership rules
    - [ ] Define how Conductor tracks reference the Power Platform repo
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Repository Boundary Audit' (Protocol in workflow.md)

## Phase 2: ALM Source Layout

- [ ] Task: Create the Power Platform source root contract
    - [ ] Define folders for unpacked solution, connector, apps, flows, deployment settings, and evidence
    - [ ] Add README ownership rules and forbidden generated-file edits
    - [ ] Define generated artifact boundaries for packed solution zips
- [ ] Task: Add subrepo health checks
    - [ ] Check that the configured Power Platform repo is reachable
    - [ ] Check that required folders exist
    - [ ] Check that no broken gitlink state remains
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: ALM Source Layout' (Protocol in workflow.md)
