# Plan: MCP Server Readiness and Registry Submission

## Phase 1: Server Shape and Packaging

- [x] Task: Define the initial MCP runtime shape.
    - [x] Confirm stdio is the first supported transport.
    - [x] Record Docker as optional and out of initial scope.
    - [x] Identify the package or entry point that will launch the server.
- [x] Task: Add the MCP server entry point.
    - [x] Implement a thin server module over `nwau_py` and existing contracts.
    - [x] Add a console script or equivalent launch command.
    - [x] Ensure tool names match `contracts/mcp/tools.md`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Server Shape and Packaging' (Protocol in workflow.md)
    - [x] Evidence: `nwau_py/mcp_server.py`, `pyproject.toml` script `mchs-mcp`, and stdio smoke output.

## Phase 2: Contracted Tools and Resources

- [x] Task: Implement contracted tools.
    - [x] Implement `mchs.list_calculators`.
    - [x] Implement `mchs.get_schema`.
    - [x] Implement `mchs.validate_input`.
    - [x] Implement `mchs.calculate`.
    - [x] Implement `mchs.explain_result`.
    - [x] Implement `mchs.get_evidence`.
- [x] Task: Implement contracted resources.
    - [x] Expose canonical schemas.
    - [x] Expose support status.
    - [x] Expose release and validation evidence.
    - [x] Expose public documentation links.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Contracted Tools and Resources' (Protocol in workflow.md)
    - [x] Evidence: `tests/test_mcp_server.py` covers tool listing, tool calls, resources, and evidence output.

## Phase 3: Tests and Evidence

- [x] Task: Add protocol and contract tests.
    - [x] Test tool listing and schema metadata.
    - [x] Test pass, fail, and unsupported examples from `contracts/mcp/examples/`.
    - [x] Test diagnostics and provenance preservation.
    - [x] Test that MCP server code delegates instead of duplicating formula logic.
- [x] Task: Add local client smoke evidence.
    - [x] Document a local stdio invocation.
    - [x] Record MCP inspector or protocol-level smoke output.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Tests and Evidence' (Protocol in workflow.md)
    - [x] Evidence: `uv run pytest tests/test_mcp_server.py` and stdio JSON-RPC `initialize`/`tools/list` smoke test pass.

## Phase 4: Registry Metadata

- [x] Task: Prepare official MCP Registry metadata.
    - [x] Add `server.json` or equivalent registry metadata.
    - [x] Use a verified namespace appropriate for the repository owner.
    - [x] Point metadata to a public package, repository, or endpoint.
    - [x] Include license, support scope, known limitations, and security notes.
    - [x] Re-check official MCP Registry PyPI package and ownership-verification requirements on 2026-05-17.
- [x] Task: Prepare secondary registry decisions.
    - [x] Add Glama listing evidence or blocked note.
    - [x] Add Smithery listing evidence or blocked note.
    - [x] Add Docker MCP Registry as deferred unless a container is added.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Registry Metadata' (Protocol in workflow.md)
    - [x] Evidence: `contracts/mcp/registry/server.json`, `contracts/mcp/registry/submission-decisions.md`, and `.github/workflows/publish-mcp-registry.yml`.

## Phase 5: Submission and Publication Evidence

- [x] Task: Submit to the official MCP Registry.
    - [x] Submit metadata through the official registry flow.
    - [x] Record submission URL, PR, registry entry, or blocked credential/review note.
- [x] Task: Submit or list with eligible secondary registries.
    - [x] Submit to Glama if public indexing requirements are met.
    - [x] Submit to Smithery only if HTTP or MCPB packaging requirements are met.
    - [x] Do not submit to Docker MCP Registry unless a Docker distribution exists.
- [x] Task: Update package and release documentation.
    - [x] Update registry status tables.
    - [x] Update MCP contract README with final registry evidence.
    - [x] Update release evidence bundle fields.
    - [x] Add release/publish artifact gates for MCP server entry point, package data, README verification marker, clean archive boundaries, and license metadata.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 5: Submission and Publication Evidence' (Protocol in workflow.md)
    - [x] Evidence: Official MCP Registry metadata and OIDC publish workflow are prepared; secondary submissions are documented as prepared/deferred with reasons; package artifact validation is wired into release and PyPI publish workflows; no public listing is overclaimed.
