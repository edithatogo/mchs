# ALM Workflow

## Command Flow

1. Run the local source preflight before any tenant-bound operation.
2. Unpack the current solution into source control.
3. Edit unpacked assets, including the app-surface model when calculator
   availability changes.
4. Pack the solution artifact from the unpacked tree.
5. Validate with solution checker.
6. Import into a target environment as a managed solution.

## Local Preflight

Run these checks from the repository root before packaging or handoff:

```bash
python scripts/validate_power_platform_capabilities.py
uv run pytest tests/test_power_platform_binding_track.py tests/test_power_platform_alm_app_track.py
```

The preflight treats the capability matrix, app-surface model, connector contract,
OpenAPI file, JSON schema, and example payloads as one source surface.
It fails when Power Apps could infer unsupported pricing-year coverage, skip the
connector capability operation, or drift from the declared calculator states.

## Supported Tooling

- `pac` for solution lifecycle commands.
- `az` for surrounding authentication and environment access.
- `powerbi` only when BI surface delivery is part of the release.

## Promotion Contract

- Development produces unpacked source and optional unmanaged artifacts.
- Test and production consume managed solutions.
- Promotion must remain gated by solution checker output and tracked approval state.
- `pac solution pack`, `pac solution checker`, and `pac solution import` are an
  external tenant gate. They require authenticated `pac` context, the documented
  target environment, and release approval evidence before they can support a
  production readiness claim.
