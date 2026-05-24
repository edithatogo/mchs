# Plan: Docker MCP Registry Readiness

## Phase 1: Contract and Docker Submission Shape

- [x] Task: Confirm Docker MCP Registry requirements against current documentation.
    - [x] Record local containerized server requirements.
    - [x] Record remote server alternative and why it is not the first Docker path.
    - [x] Record Docker-built versus self-provided image tradeoffs.
- [x] Task: Define Docker metadata.
    - [x] Choose Docker-safe server name, category, tags, title, and description.
    - [x] Define whether config/env/secrets are omitted or required.
    - [x] Define PR evidence and validation commands.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Docker Submission Shape' (Protocol in workflow.md)

## Phase 2: Container Runtime

- [x] Task: Write failing container smoke tests.
    - [x] Test image startup.
    - [x] Test MCP `initialize` over stdio.
    - [x] Test `tools/list` over stdio.
- [x] Task: Add Dockerfile and runtime docs.
    - [x] Install the package or checkout reproducibly.
    - [x] Run `mchs-mcp` by default.
    - [x] Exclude private archives, tests, and unnecessary tooling from the final image.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Container Runtime' (Protocol in workflow.md)

## Phase 3: Docker MCP Registry Candidate

- [x] Task: Prepare registry submission files.
    - [x] Create candidate `servers/mchs/server.yaml` content.
    - [x] Add `tools.json` only if Docker listing cannot run the container directly.
    - [x] Add `readme.md` or documentation link content.
- [ ] Task: Validate in Docker MCP Registry tooling.
    - [ ] Run `task validate -- --name mchs` or current equivalent.
    - [ ] Run `task build -- --tools mchs` or current equivalent.
    - [ ] Record any tool-listing fallback evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Docker MCP Registry Candidate' (Protocol in workflow.md)

## Phase 4: Submission and Evidence

- [~] Task: Open or prepare Docker MCP Registry PR.
    - [ ] Fork/branch the Docker registry repository as needed.
    - [ ] Use Docker's PR template and include validation evidence.
    - [x] Capture PR URL or explicit gate record.
- [x] Task: Update registry evidence.
    - [x] Update MCP registry decision docs.
    - [x] Update release/publication evidence without claiming catalog publication until Docker review completes.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Submission and Evidence' (Protocol in workflow.md)
