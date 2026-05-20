# Power Automate Flow-Smoke Capture Runbook

This runbook is the operator package for collecting Power Automate flow-smoke
run metadata and turning it into evidence. It does not claim a live run on its
own.

## Purpose

- Capture the real run identifiers for the four NSW flow-smoke surfaces.
- Keep the capture synthetic, minimal, and free of patient-level data.
- Prevent placeholder records from being mistaken for real evidence.

## Required capture fields

- `flowLogicalName`
- `flowId`
- `runId`
- `runStatus`
- `runUrl`

## Expected flow set

- `mchs-validate-input`
- `mchs-calculate-request`
- `mchs-evidence-export`
- `mchs-deployment-smoke`

## Capture procedure

1. Open the real run history for each flow in the target Power Platform
   environment.
2. Record the flow ID, run ID, run status, and run URL for each logical flow
   name.
3. Keep the capture to synthetic or operational metadata only.
4. Start from `flow-smoke-capture-sample.json` and replace every placeholder
   value with the real capture details.
5. Save the completed capture as a working JSON file outside the blocked
   template path if you need to preserve the operator draft.
6. Run `scripts/update_power_platform_flow_smoke_evidence.py` with the working
   capture file and the blocked template.

## Suggested command

```bash
python3 scripts/update_power_platform_flow_smoke_evidence.py \
  --capture /path/to/completed-flow-smoke-capture.json \
  --output power-platform/evidence/power-automate-flow-smoke-20260521.json
```

## Blocking rules

- Do not use the sample capture file as evidence.
- Do not claim a successful flow-smoke run unless every placeholder has been
  replaced with real values and the updater returns a non-blocked result.
- If any required field is missing, the updater stays blocked and writes no
  live evidence file.

## Output check

- `captured_real_flow_smoke_passed` means every required flow run entry was
  supplied and every recorded run status was `succeeded`.
- `captured_real_flow_smoke_with_non_success_runs` means real runs were
  supplied but at least one status was not `succeeded`.
- `blocked_pending_real_flow_run_capture` means the capture is still
  incomplete or still contains placeholder values.
