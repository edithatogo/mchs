# Power Platform Pipelines

This directory documents the promotion path for the Power Platform ALM app.

## Current Contract

- GitHub Actions validates solution documentation scaffold files and the ALM
  command contract before environment-sensitive deployment jobs.
- `pac` is the solution lifecycle tool for pack/check/import operations.
- Managed solution promotion remains the downstream target.
- Static, deterministic gates run in CI without credential requirements.

## Lifecycle Gates

- **Pack gate**: ensures pack/unpack command surfaces are present.
- **Check gate**: ensures checker command surface is present.
- **Import gate**: ensures import command surface is present.

For the gate command matrix and evidence format, see
[`pack-check-import-gates.md`](pack-check-import-gates.md).

## Execution Plan (Current)

1. Run deterministic contract checks on workflow and scaffold files.
2. Run pack/check/import gate smoke checks with local command availability.
3. Proceed to environment-aware deployment only after credentials and approvals
   are available.

## Future Expansion

- Add environment-aware import/export jobs when deployment credentials and target
  environments are provisioned.
- Add environment and approval annotations to the check and import job logs.
