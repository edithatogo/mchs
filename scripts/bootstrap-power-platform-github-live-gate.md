# Power Platform GitHub Live Gate Bootstrap

Use `./scripts/bootstrap-power-platform-github-live-gate.sh` to prepare the
official GitHub live gate without claiming a run.

## What it does

- Validates a sanitized local operator-inputs env file before any dispatch.
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
cp docs/runbooks/github-live-gate.env.example docs/runbooks/github-live-gate.env
# Edit docs/runbooks/github-live-gate.env so it contains no placeholder values.
./scripts/bootstrap-power-platform-github-live-gate.sh --inputs-file docs/runbooks/github-live-gate.env
./scripts/bootstrap-power-platform-github-live-gate.sh --dispatch
```

If the first command reports missing secrets, set them manually with the exact
commands it prints, then re-run with `--inputs-file docs/runbooks/github-live-gate.env --dispatch`.

## Placeholder values

The script prints commands with placeholder bodies for each secret, but the
sanitized env file must not keep any of the example placeholder values:

- `POWER_PLATFORM_ENVIRONMENT_URL` -> `<dataverse-environment-url>`
- `POWER_PLATFORM_APPLICATION_ID` -> `<application-client-id>`
- `POWER_PLATFORM_CLIENT_SECRET` -> `<application-client-secret>`
- `POWER_PLATFORM_TENANT_ID` -> `<azure-tenant-id>`
- `LIVE_GATE_TAG` must not remain `v0.0.0`
- `NSW_OPERATOR_NAME` must not remain `NSW operator name`
- `NSW_OPERATOR_EMAIL` must not remain `operator@example.nsw.gov.au`
- `NSW_APPROVER_NAME` must not remain `NSW approver name`
- `NSW_APPROVER_EMAIL` must not remain `approver@example.nsw.gov.au`
- `NSW_RELEASE_REASON` must not remain `Manual live-gate dispatch for GitHub release or registry publication`
- `NSW_RELEASE_NOTES` must not remain `Document the evidence bundle, dispatch time, and approval reference here`
- `GITHUB_TOKEN` and `GH_TOKEN` must stay absent or use the runtime sentinel `provided_by_github_actions`

## Workflow target

The script dispatches `Power Platform Official Actions` from
`.github/workflows/power-platform-official-actions.yml` with
`run_live_checks=true`.

## Safety boundary

- Do not paste real secret values into the repo.
- Do not claim a successful workflow run unless GitHub actually creates one and
  the evidence file is updated separately.
