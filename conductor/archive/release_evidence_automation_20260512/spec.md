# Specification: Release Evidence Automation

## Overview
Automate release and publication evidence so the repository can prove whether
GitHub Releases, PyPI, conda-forge, GitHub Pages, and future registries are
published, current, and version-consistent.

## Functional Requirements
- Add a command or workflow that reports release evidence in JSON and Markdown.
- Check source version, git tag, GitHub Release, PyPI version, docs deployment,
  conda-forge status, and future registry placeholders.
- Detect stale README badges, stale homepage links, and version mismatches.
- Include latest workflow status for release, publish, docs, PR CI, and conda
  recipe workflows.

## Acceptance Criteria
- A release evidence report can be generated before and after release.
- Publication claims in docs can be backed by report output.
- Missing registries are marked future-only or unpublished, not implied
  published.
