# MCP Release Execution: v0.2.2

Date prepared: 2026-05-17

## Executed State

- GitHub release `v0.2.2` is published:
  `https://github.com/edithatogo/mchs/releases/tag/v0.2.2`.
- PyPI package `nwau-py 0.2.2` is published:
  `https://pypi.org/project/nwau-py/0.2.2/`.
- Official MCP Registry entry `io.github.edithatogo/mchs` version `0.2.2` is
  published and active.
- Local package artifact validation checks the
  wheel/sdist for the MCP entry point, README verification marker, package
  data, clean archive boundaries, and license metadata.
- The PyPI publish workflow verifies release evidence artifacts in `dist/` but
  stages only wheel and source distribution files into `dist-pypi/` for upload.

## Completed Release Sequence

1. Release source committed and pushed to `master`.
2. Tag `v0.2.2` created and pushed.
3. GitHub release workflow completed successfully.
4. GitHub release assets were cleaned to wheel, source distribution,
   `checksums.txt`, and `sbom.cdx.json`.
5. Python publish workflow completed successfully and published
   `nwau-py 0.2.2`.
6. MCP Registry workflow completed successfully with GitHub OIDC and published
   `io.github.edithatogo/mchs` version `0.2.2`.
7. Official MCP Registry search returned the active/latest entry.

## Commands

```bash
RELEASE_REF_NAME=v0.2.2 RELEASE_REF_TYPE=tag uv run python .github/scripts/validate_release_metadata.py
uv run python .github/scripts/validate_mcp_package_artifacts.py
uv run pytest tests/test_mcp_server.py tests/test_release_evidence_automation.py tests/test_release_governance.py
uv run ruff check nwau_py/mcp_server.py tests/test_mcp_server.py .github/scripts/validate_release_metadata.py .github/scripts/validate_mcp_package_artifacts.py
```

## Do Not Claim

- Do not claim Smithery hosted `run.tools` runtime readiness or search-index
  visibility beyond the accepted stdio MCPB release evidence recorded in
  `contracts/mcp/registry/smithery/accepted-release-20260526.json`.
- Do not claim Docker MCP Catalog publication until Docker MCP Registry PR
  `https://github.com/docker/mcp-registry/pull/3799` merges or visible catalog
  listing evidence exists.
- Do not claim conda-forge, crates.io, npm, CRAN, NuGet, or other package
  registry publication unless a public registry page exists.
