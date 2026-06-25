# Generated Artifact Retention Policy

## Purpose

Generated artifacts must not be confused with source. Some artifacts are useful
release or registry evidence, but they need ownership and retention reasons.

## Retention Classes

- `source`: authored source, configuration, schemas, and docs.
- `generated-ignore`: build outputs, caches, dependency installs, and temporary
  tool state that should not be tracked.
- `release-attachment`: package artifacts built from source and attached to a
  release or registry workflow.
- `evidence-allowed`: screenshots, browser captures, API responses, or logs
  retained because they prove a claim and have an owning track.
- `external-archive`: raw source archives or licensed/local artifacts governed
  by source archive policy.
- `local-only`: credentials, user profile state, local tool history, and
  non-portable files.

## Blocked Patterns

Tracked files should not appear under `node_modules`, `.build`, `target`,
`.pytest_cache`, `.ruff_cache`, `.mypy_cache`, `.hypothesis`, `dist`, `build`,
`.venv`, `__pycache__`, or package check output directories.

## Evidence Rules

Evidence artifacts must name the owning track, the claim they support, whether
they are public-safe, and whether they can be regenerated. Credential-bearing or
patient-level evidence must not be committed.

## Package Artifacts

Artifacts such as `.vsix`, `.zip`, `.tar.gz`, wheels, and registry bundles are
not source. They may be retained only as release attachments or explicit
evidence. Otherwise they should be ignored or regenerated from source.

## Power Platform

Power Platform exports can be source-controlled only when they are normalized,
credential-free, and tied to the service-boundary contract. Browser captures and
manual portal evidence belong in the evidence class, not in source directories.
