# Specification: Generated Artifact Retention Policy

## Overview

Define the retention model for generated files so build outputs, browser logs,
package artifacts, Power Platform exports, screenshots, and registry evidence do
not blur source ownership. The policy must distinguish committed evidence from
unreviewed generated output.

## Functional Requirements

- Classify artifacts as source, generated-ignore, release-attachment,
  evidence-allowed, external-archive, or local-only.
- Block tracked build outputs such as `node_modules`, `.build`, `target`,
  `.pytest_cache`, `.ruff_cache`, `dist`, `build`, and package check outputs.
- Allow evidence artifacts only when they have an owning track, retention reason,
  and claim boundary.
- Require Power Platform exports to be source-controlled only when they are
  normalized and credential-free.
- Require package artifacts such as `.vsix`, `.zip`, and tarballs to be tied to
  release evidence or ignored.

## Non-Functional Requirements

- Avoid deleting artifacts in policy-only changes.
- Keep generated artifact checks deterministic and local.
- Do not inspect or commit credentials.

## Acceptance Criteria

- `conductor/generated-artifact-retention-policy.md` documents allowed and
  blocked classes.
- The topology validator blocks tracked generated artifact patterns.
- The package surface registry records each surface artifact policy.

## Out of Scope

- Rebuilding package artifacts.
- Uploading evidence artifacts.
- Cleaning the outer wrapper directly.
