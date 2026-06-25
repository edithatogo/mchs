# Specification: Repository Topology CI Gate

## Overview

Add a non-interactive validation gate that enforces the topology authority and
package surface registry. The gate should run locally and in PR CI without
requiring network credentials or registry access.

## Functional Requirements

- Fail when nested `.git` directories exist below the canonical root.
- Fail when the current repo contains gitlinks without `.gitmodules` mappings.
- Detect broken outer-wrapper gitlinks when an outer root is explicitly checked.
- Fail when package manifests are not registered in the package surface registry.
- Fail when implemented surfaces point to missing manifests.
- Fail when tracked generated artifacts match blocked path patterns.
- Emit JSON output for agent consumption and plain text diagnostics for humans.

## Non-Functional Requirements

- Use only Python standard library modules.
- Keep checks deterministic and safe for CI.
- Avoid inspecting secrets, credentials, or registry tokens.

## Acceptance Criteria

- `scripts/validate_repository_topology.py` exists and exits nonzero on invalid
  topology.
- PR CI runs the validator in the quality job.
- Tests exercise valid registry state and broken gitlink detection.

## Out of Scope

- Fixing invalid topology automatically.
- Deleting generated artifacts.
- Validating external registry pages.
