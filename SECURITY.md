# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability, please use GitHub Security Advisories:

- Go to the repository `Security` tab
- Select `Report a vulnerability`
- Fill in the impact, reproduction steps, affected versions, and relevant artifacts

For sensitive issues, include minimal reproducer details until the advisory is triaged.

## Scope

This project publishes software for funding-calculation workflows and data-processing tools.

Scope includes:

- Python package: `nwau-py`
- Rust workspace: `rust/`
- Documentation and scripts under `docs-site/`, `scripts/`, `conductor/`, `archive/`
- External publishing surfaces configured for this repository (`PyPI`, GitHub Releases, planned registries)

## Supported versions

Security triage applies to tags/releases with active maintenance and a published
release on the default branch.

- Supported: `master` branch and currently released tag lines maintained by active
  `v*` release tracks.
- Experimental or historical scaffold surfaces without active release support may have
  a longer triage window.

## Security tooling and process

- Dependency review is enforced in pull requests via workflow.
- SAST and static checks are run in CI (`ruff --select S`, `bandit`, `pip-audit`, Rust audit).
- Secret-prone patterns are flagged by CI checks and repository conventions.
- Coverage and release integrity are enforced with automated CI gates and artifact attestation.

## Response process

The [Grype dependency evidence contract](docs/grype-dependency-evidence.md)
describes the initial Critical release gates, advisory pull-request scans,
retained release rescans and their inventory boundaries. Workflow configuration
alone is not successful scanner or release evidence.

- We acknowledge security reports within a few business days.
- Reproduction and severity are validated against active CI and pinned evidence.
- A patched version is prioritized by impact and dependency risk.
- When appropriate, advisories are published privately and fixed via reviewed PRs.
