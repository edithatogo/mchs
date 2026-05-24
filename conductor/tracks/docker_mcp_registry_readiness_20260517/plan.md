# Plan: Docker MCP Registry Readiness

## Phase 1: Contract and Docker Submission Shape

- [x] Task: Confirm Docker MCP Registry requirements against current documentation.
    - [x] Record local containerized server requirements.
    - [x] Record remote server alternative and why it is not the first Docker path.
    - [x] Record Docker-built versus self-provided image tradeoffs.
- [x] Task: Define Docker metadata.
    - [x] Choose Docker-safe server name, category, tags, title, and description.
    - [x] Define config/env/secrets as omitted for discovery.
    - [x] Define PR evidence and validation commands.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Docker Submission Shape' (Protocol in workflow.md)

## Phase 2: Container Runtime

- [x] Task: Add container smoke tooling.
    - [x] Test image startup command shape.
    - [x] Test MCP `initialize` over stdio.
    - [x] Test `tools/list` over stdio.
- [x] Task: Add Dockerfile and runtime docs.
    - [x] Install the checkout reproducibly.
    - [x] Run `mchs-mcp` by default.
    - [x] Exclude private archives, tests, and unnecessary tooling from the build context.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Container Runtime' (Protocol in workflow.md)

## Phase 3: Docker MCP Registry Candidate

- [x] Task: Prepare registry submission files.
    - [x] Create candidate `servers/mchs/server.yaml` content.
    - [x] Add `tools.json` fallback metadata.
    - [x] Add `readme.md` documentation content.
- [x] Task: Prepare Docker MCP Registry validation instructions.
    - [x] Record `task validate -- --name mchs` requirement in the contract.
    - [x] Record `task build -- --tools mchs` requirement in the contract.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Docker MCP Registry Candidate' (Protocol in workflow.md)

## Phase 4: Submission and Evidence

- [x] Task: Prepare Docker MCP Registry PR path.
    - [x] Record fork/branch requirement.
    - [x] Record Docker PR template and validation evidence requirement.
    - [x] Capture explicit blocker: PR not opened in this repository-only implementation step.
- [x] Task: Update registry evidence.
    - [x] Update MCP registry decision docs.
    - [x] Update release/publication evidence without claiming catalog publication.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Submission and Evidence' (Protocol in workflow.md)
