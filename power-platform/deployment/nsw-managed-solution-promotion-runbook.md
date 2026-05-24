# NSW Managed-Solution Promotion Runbook

Purpose: provide a repeatable, auditable path for managing Power Platform solution
promotion while keeping all production claims blocked until credentials and evidence
are present.

> This runbook is a template. It does not assert a live NSW deployment.

## Runbook phases

### 1) Pre-flight checks

- Verify repository checkout and branch are on the approved release commit.
- Confirm solution source version in source control is complete and locked.
- Confirm `Managed` solution is the intended target for non-development
  environments.
- Verify missing-credential blockers are cleared:
  - tenant service principal
  - client secret reference
  - target environment ID
  - network trust path for solution upload

### 2) Environment bootstrap

- Authenticate with tenant deployment principal.
- Validate environment readiness (`dev` -> `test` -> `uat` -> `prod`).
- Capture environment IDs for audit log.

### 3) Import pipeline

For each environment (dev, test, uat, prod):

1. Import managed solution artifact.
2. Run solution checker and record pass/fail output.
3. Run smoke verification commands:
   - service reachability
   - auth handshake
   - contract validation call
4. Record import output in the evidence bundle.

### 4) Promotion handoff

- Record approver and timestamp for each environment handoff.
- Capture rollback artifact hash and location.
- Update evidence bundle with:
  - environment status
  - blocker resolution
  - known operational limits

### 5) Post-promotion monitoring

- Track first-24-hour import and runtime warnings.
- Capture two scheduled smoke checks and incident triage notes.
- Verify no secret leakage or hard-coded tenant values in solution state.

## Hard stops

Any of these conditions **must** stop promotion and keep the surface in `blocked`:

- Missing tenant credentials or secret reference.
- Missing or stale managed-solution artifact checksum.
- Failed solution import check in test or UAT.
- Unresolved tenant-specific compliance objection.

## Rollback template

- Publish/restore the prior managed solution artifact.
- Re-run contract smoke checks.
- Reopen blocker register with root-cause evidence.

## Evidence output expected from this runbook

- Run timestamp and actor identity.
- Environment sequence and import status.
- Error log bundle path.
- Explicit `blocked` / `release_candidate` / `ga` state for each stage.

## No-claim rule

Do not claim NSW deployment, managed-solution promotion, or production readiness
from this runbook alone. Claims require actual target-environment import,
solution checker, app smoke, flow smoke, and evidence bundle records.
