# Power Platform Pipelines

This directory documents the promotion path for the Power Platform ALM app.

## Current Contract

- GitHub Actions validates the capability matrix, app-surface model, connector
  contract, OpenAPI/schema files, examples, and ALM command contract before
  environment-sensitive deployment jobs.
- `pac` is the solution lifecycle tool for pack/check/import operations.
- Managed solution promotion remains the downstream target.
- Static, deterministic gates run in CI without credential requirements.

## Execution Plan (Current)

1. Run deterministic contract checks on workflow and Power Platform source
   files.
2. Run `scripts/validate_power_platform_capabilities.py` so the capability
   matrix, app-surface model, connector contract, and examples stay aligned.
3. Run pack/check/import gate smoke checks with local command availability.
4. Treat `pac solution pack`, `pac solution checker`, and
   `pac solution import` as the external tenant gate.
5. Proceed to environment-aware deployment only after credentials and approvals
   are available.

## Future Expansion

- Add environment-aware import/export jobs when deployment credentials and target
  environments are provisioned.
- Keep solution checker and solution pack/unpack as explicit gates.
