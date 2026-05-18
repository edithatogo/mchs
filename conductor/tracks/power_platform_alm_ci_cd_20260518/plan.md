# Plan: Power Platform ALM CI/CD

## Phase 1: Local ALM Commands

- [x] Task: Harden local scripts
    - [x] Verify `pac` and `az` versions
    - [x] Add pack, unpack, validate, checker, export, and import command wrappers
    - [x] Document command preconditions and auth setup
- [x] Task: Add deterministic checks
    - [x] Validate solution XML structure
    - [x] Validate connector OpenAPI
    - [x] Validate environment variable and connection reference names
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Local ALM Commands' (Protocol in workflow.md)

## Phase 2: GitHub Actions ALM

- [x] Task: Create CI workflows
    - [x] Run static validation on pull requests
    - [x] Pack unmanaged and managed artifacts on release candidates
    - [x] Upload artifacts with evidence metadata
- [x] Task: Create protected deployment workflow
    - [x] Require environment approval for NSW deployment
    - [x] Use GitHub secrets/OIDC or service principal only
    - [x] Record import and checker evidence
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: GitHub Actions ALM' (Protocol in workflow.md)
