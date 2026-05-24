# Power Platform Subrepo Closure Operator Runbook

Use `./scripts/write_power_platform_subrepo_closure.py` to record the current
subrepo closure state for the governed Power Platform boundary.

## Purpose

- Capture the blocked default record when no standalone remote or explicit
  waiver is ready.
- Record a standalone remote closure when the split has been provisioned.
- Record an explicit waiver when the split is deferred and governance has
  approved the risk.

## Boundary

- This runbook documents closure inputs and evidence only.
- It does not claim repo-health 9.9.
- It does not claim production readiness.
- It does not replace the existing ALM import, smoke, or live-gate checks.

## Files

- `scripts/write_power_platform_subrepo_closure.py`: writes the blocked,
  standalone remote, or explicit waiver closure record.
- `power-platform/repository/standalone-subrepo-remote-or-waiver-closure-template.json`:
  blocked closure template that stays in source control.
- `power-platform/evidence/standalone-subrepo-remote-input-template.json`:
  sample standalone remote operator input.
- `power-platform/evidence/explicit-waiver-input-template.json`: sample
  explicit waiver operator input.

## Recommended workflow

1. Decide whether the closure path is `standalone-remote` or `explicit-waiver`.
2. Fill the matching sample input template with real values.
3. Run the writer with either the explicit flags or values copied from the
   template.
4. Keep the blocked default record if neither closure path is complete.

## Blocked default

```bash
python3 scripts/write_power_platform_subrepo_closure.py
```

This writes `power-platform/repository/subrepo-closure-20260521.json` with the
blocked `blocked_pending_remote_or_explicit_waiver` state.

## Standalone remote path

Sample input template:

```json
{
  "asOf": "2026-05-21",
  "remoteUrl": "https://github.com/example/power-platform-subrepo.git",
  "defaultBranch": "main",
  "syncProcedure": "git pull --ff-only; git push --follow-tags",
  "importOwner": "NSW import owner"
}
```

Command example:

```bash
python3 scripts/write_power_platform_subrepo_closure.py \
  standalone-remote \
  --remote-url https://github.com/example/power-platform-subrepo.git \
  --default-branch main \
  --sync-procedure 'git pull --ff-only; git push --follow-tags' \
  --import-owner 'NSW import owner'
```

If you want to drive the command from the sample template, extract the fields
with `jq` and pass them as flags.

## Explicit waiver path

Sample input template:

```json
{
  "asOf": "2026-05-21",
  "approvedBy": "NSW platform governance",
  "approvalRecord": "GOV-2026-05-21-001",
  "reason": "Standalone remote is deferred pending repository split approval.",
  "reviewDate": "2026-05-21",
  "riskAcceptance": "Accepted by product owner for the governed boundary."
}
```

Command example:

```bash
python3 scripts/write_power_platform_subrepo_closure.py \
  explicit-waiver \
  --approved-by 'NSW platform governance' \
  --approval-record GOV-2026-05-21-001 \
  --reason 'Standalone remote is deferred pending repository split approval.' \
  --review-date 2026-05-21 \
  --risk-acceptance 'Accepted by product owner for the governed boundary.'
```

## Notes

- Use the `standalone-remote` path when the governed boundary has a real remote,
  default branch, sync procedure, and import owner.
- Use the `explicit-waiver` path only when the governance approval record is
  explicit and current.
- Do not describe the resulting record as a 9.9 completion claim unless the
  rest of the closure and live evidence package is actually complete.
