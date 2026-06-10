# Power Platform Solution Scaffold

This directory is the tracked source-control home for the Power Platform ALM app.

## Scope

- Solution-based ALM only.
- Orchestration-only app surface.
- No calculator formula logic.
- Managed-solution promotion downstream.

## Intended Contents

- `solution-manifest.md`: solution identity, versioning, and packaging contract.
- `environment-variables.md`: environment variable names and default semantics.
- `connection-references.md`: connector and service connection references.
- `app-surface.md`: app orchestration responsibilities and non-responsibilities.
- `app-surface.json`: source-controlled app model for capability-driven
  selectors, validation, calculation submission, and diagnostics display.

## Source-Control Rule

Unpacked solution assets are the editable source-of-truth representation for the
Power Platform app. Build and promotion use `pac`-driven pack/unpack operations.

## Local Validation

```bash
python scripts/validate_power_platform_capabilities.py
uv run pytest tests/test_power_platform_binding_track.py
```
