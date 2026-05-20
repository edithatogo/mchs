# Power Platform GitHub Live Gate Bootstrap

Use `./scripts/bootstrap-power-platform-github-live-gate.sh` to prepare the
official GitHub live gate without claiming a run.

## What it does

- Checks the repository secrets required by the live gate.
- Prints exact `gh secret set` commands with placeholders for any missing
  secrets.
- Refuses to dispatch the workflow until the required secrets are present.
- Dispatches the workflow only when you pass `--dispatch`.

## Required secrets

- `POWER_PLATFORM_ENVIRONMENT_URL`
- `POWER_PLATFORM_APPLICATION_ID`
- `POWER_PLATFORM_CLIENT_SECRET`
- `POWER_PLATFORM_TENANT_ID`

## Suggested flow

```bash
./scripts/bootstrap-power-platform-github-live-gate.sh
./scripts/bootstrap-power-platform-github-live-gate.sh --dispatch
```

If the first command reports missing secrets, set them manually with the exact
commands it prints, then re-run with `--dispatch`.

## Placeholder values

The script prints commands with placeholder bodies for each secret:

- `POWER_PLATFORM_ENVIRONMENT_URL` -> `<dataverse-environment-url>`
- `POWER_PLATFORM_APPLICATION_ID` -> `<application-client-id>`
- `POWER_PLATFORM_CLIENT_SECRET` -> `<application-client-secret>`
- `POWER_PLATFORM_TENANT_ID` -> `<azure-tenant-id>`

## Workflow target

The script dispatches `Power Platform Official Actions` from
`.github/workflows/power-platform-official-actions.yml` with
`run_live_checks=true`.

## Safety boundary

- Do not paste real secret values into the repo.
- Do not claim a successful workflow run unless GitHub actually creates one and
  the evidence file is updated separately.
