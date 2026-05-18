# Plan: Power Platform ALM CI/CD

## Phase 1: Local ALM Commands

- [ ] Task: Harden local scripts
    - [ ] Verify `pac` and `az` versions
    - [ ] Add pack, unpack, validate, checker, export, and import command wrappers
    - [ ] Document command preconditions and auth setup
- [ ] Task: Add deterministic checks
    - [ ] Validate solution XML structure
    - [ ] Validate connector OpenAPI
    - [ ] Validate environment variable and connection reference names
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Local ALM Commands' (Protocol in workflow.md)

## Phase 2: GitHub Actions ALM

- [ ] Task: Create CI workflows
    - [ ] Run static validation on pull requests
    - [ ] Pack unmanaged and managed artifacts on release candidates
    - [ ] Upload artifacts with evidence metadata
- [ ] Task: Create protected deployment workflow
    - [ ] Require environment approval for NSW deployment
    - [ ] Use GitHub secrets/OIDC or service principal only
    - [ ] Record import and checker evidence
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: GitHub Actions ALM' (Protocol in workflow.md)
