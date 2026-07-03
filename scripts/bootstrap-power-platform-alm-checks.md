# Power Platform ALM Bootstrap Checks

## Purpose

Use `./scripts/bootstrap-power-platform-alm.sh` to verify the supported Power Platform ALM toolchain for this track. The script is verification-only by default so CI and local checks remain deterministic and non-destructive.

## Supported Toolchain

- `pac >= 1.35.0`
- `az >= 2.70.0`
- Optional installer support:
  - `dotnet` for `pac`
  - `brew` for `az` install or upgrade on Homebrew-managed machines

## Commands

```bash
./scripts/bootstrap-power-platform-alm.sh
./scripts/bootstrap-power-platform-alm.sh --check-auth
./scripts/bootstrap-power-platform-alm.sh --install-missing --upgrade --check-auth
```

## Prerequisites

- Install supported package managers before using opt-in remediation:
  - `.NET SDK` for `pac`
  - `Homebrew` for automated `az` install or upgrade
- Ensure `~/.dotnet/tools` is allowed on `PATH` for shells that use global dotnet tools.
- Use a Dataverse-capable Power Platform environment and an Azure tenant/subscription that is allowed for ALM work.
- Keep credentials outside the repository. Do not commit tokens, profiles, exported secrets, or auth files.

## Auth Prerequisites

The bootstrap script can report auth readiness, but it does not create or persist credentials.

- Run `az login` in your user shell before environment-sensitive ALM operations.
- Run `pac auth create` in your user shell before Dataverse solution operations.
- Select the correct Azure subscription and Dataverse environment before import, export, checker, or pipeline commands.
- Do not store usernames, passwords, client secrets, refresh tokens, or exported auth artifacts in this repo.

## `pacx` Decision

`pacx` is rejected in this track.

- Reason: this track standardizes on supported and documented `pac` and `az` command surfaces for Power Platform ALM.
- Result: if `pacx` appears on `PATH`, treat it as out of scope and continue with `pac`.
- CI rule: do not add `pacx` recipes, references, or substitutions in bootstrap steps for this track.

## Deterministic Check Surface

Before tenant-bound `pac` operations, the local source gate also runs:

- `python scripts/validate_power_platform_capabilities.py`
- `uv run pytest tests/test_power_platform_binding_track.py tests/test_power_platform_alm_app_track.py`

Those checks prove the capability matrix, app-surface model, connector contract,
OpenAPI/schema files, and examples agree on calculator and pricing-year support.

The bootstrap script verifies:

- `command -v pac`
- `command -v az`
- `pac --help`
- `pac auth --help`
- `pac org --help`
- `pac solution --help`
- `pac solution checker --help`
- `pac pipeline --help`
- `az version`
- `az account --help`

This keeps the phase-2 contract lightweight, explicit, and suitable for CI documentation checks.

## Subrepo Closure Operator Runbook

Use `./scripts/write_power_platform_subrepo_closure.py` with the companion
`scripts/bootstrap-power-platform-subrepo-closure.md` runbook when you need to
prepare the subrepo closure evidence package.

- Start with the blocked default record if neither closure path is ready.
- Use the standalone remote sample when the boundary has a real remote and
  import owner.
- Use the explicit waiver sample only when governance has signed off on the
  deferred split.
- Do not describe any of these records as a 9.9 completion claim unless the
  rest of the live evidence package is actually complete.
