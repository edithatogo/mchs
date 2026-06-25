# Specification: Python Tooling and CI Modernization

## Goal

Move the Python project toward the approved toolchain: `uv`, a committed `uv.lock`, Python 3.10-3.14, Codecov, `ty`, Ruff, Hypothesis, mutmut, Scalene, Renovate, Vale, and staged CI.

## Current State

- The migration is underway.
- Legacy compatibility files and tools still exist in the repository snapshot this track is documenting, but they are transitional rather than authoritative.
- The track should describe the intended toolchain explicitly so the implementation work can replace the transitional surface without ambiguity.
- Phase 4, Maintenance Automation and Prose Quality, is complete. The Renovate/Vale contract is finalized and the remaining text now serves as the authoritative record for that tooling surface.

## Requirements

- Dependency resolution must come from `pyproject.toml` plus a committed `uv.lock`; `requirements*.txt` are transitional only.
- CI must test Python 3.10 through 3.14.
- Fast PR CI must follow the sequence install -> format -> lint -> type check -> tests -> coverage -> Codecov upload.
- Coverage must report to Codecov.
- `ty` replaces `mypy` as the forward type-checking direction.
- Hypothesis, mutmut, and Scalene must be available without slowing every normal PR run.
- Renovate must propose dependency and GitHub Actions updates.
- Vale must lint documentation prose and validation claims.
- The docs should distinguish transitional compatibility artifacts from the intended migrated toolchain in every acceptance statement.
- Phase 3's validation-jobs slice is complete and documented as such in the plan.

## Acceptance Criteria

- Fast PR CI includes `uv` install/sync, formatting, linting, type checks, tests, coverage, and Codecov upload.
- Slower mutation/property/profiling workflows are separate, scheduled, or manual.
- Documentation explains the local `uv`, Ruff, `ty`, pytest, and Vale commands.
- The lockfile and supported Python matrix are documented as the intended source of truth for installs and CI.
- The track documents which files or tools are transitional and which are intended-state.
