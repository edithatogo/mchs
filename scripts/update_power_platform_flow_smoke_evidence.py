#!/usr/bin/env python3
"""Update Power Platform flow-smoke evidence from a real capture payload.

The committed evidence stays blocked until a complete capture is supplied.
This script merges a real capture payload into the blocked template only when
every required flow run field is present.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = (
    ROOT / "power-platform" / "evidence" / ("flow-smoke-evidence-template.json")
)
DEFAULT_OUTPUT = (
    ROOT / "power-platform" / "evidence" / ("power-automate-flow-smoke-20260521.json")
)
REQUIRED_CAPTURE_FIELDS = ("flowId", "runId", "runStatus", "runUrl")
GUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_list(payload: dict) -> list[dict]:
    entries = payload.get("flowRuns")
    if entries is None:
        entries = payload.get("realNswRunEvidence")
    if not isinstance(entries, list):
        raise ValueError("capture payload must include flowRuns or realNswRunEvidence")
    return entries


def _normalize_https_url(url: object) -> str | None:
    if not isinstance(url, str):
        return None
    candidate = url.strip()
    if not candidate:
        return None
    parsed = urlparse(candidate)
    if parsed.scheme != "https" or not parsed.netloc:
        return None
    if parsed.query or parsed.fragment:
        return None
    return candidate


def _capture_by_flow_logical_name(payload: dict) -> dict[str, dict]:
    entries = _as_list(payload)
    capture: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("each flow capture entry must be an object")
        logical_name = entry.get("flowLogicalName")
        if not isinstance(logical_name, str) or not logical_name.strip():
            raise ValueError("each flow capture entry must include flowLogicalName")
        if logical_name in capture:
            raise ValueError(
                f"duplicate flowLogicalName in capture payload: {logical_name}"
            )
        capture[logical_name] = entry
    return capture


def _missing_fields(entry: dict) -> list[str]:
    missing: list[str] = []
    for field in REQUIRED_CAPTURE_FIELDS:
        value = entry.get(field)
        if not isinstance(value, str) or not value.strip():
            missing.append(field)
    if "flowId" not in missing:
        flow_id = entry.get("flowId", "")
        if not isinstance(flow_id, str) or not GUID_RE.match(flow_id):
            missing.append("flowId")
    if "runUrl" not in missing and _normalize_https_url(entry.get("runUrl")) is None:
        missing.append("runUrl")
    return sorted(set(missing))


def build_flow_smoke_evidence(
    template: dict,
    capture_payload: dict,
    output_path: Path = DEFAULT_OUTPUT,
) -> tuple[int, dict, dict | None]:
    template_entries = {
        entry["flowLogicalName"]: entry
        for entry in template.get("realNswRunEvidence", [])
        if isinstance(entry, dict) and "flowLogicalName" in entry
    }
    capture_entries = _capture_by_flow_logical_name(capture_payload)
    missing_logical_names = sorted(set(template_entries) - set(capture_entries))
    extra_logical_names = sorted(set(capture_entries) - set(template_entries))

    missing_fields = {
        logical_name: _missing_fields(entry)
        for logical_name, entry in capture_entries.items()
        if logical_name in template_entries
    }
    missing_fields = {name: fields for name, fields in missing_fields.items() if fields}

    blocked_summary = {
        "status": "blocked_pending_real_flow_run_capture",
        "template": DEFAULT_TEMPLATE.as_posix(),
        "output": output_path.as_posix(),
        "requiredCaptureFields": list(REQUIRED_CAPTURE_FIELDS),
        "missingFlowLogicalNames": missing_logical_names,
        "extraFlowLogicalNames": extra_logical_names,
        "missingFields": missing_fields,
        "nextAction": (
            "Provide a capture entry for every flow logical name with flowId, "
            "runId, runStatus, and runUrl, then rerun the script."
        ),
    }

    if missing_logical_names or extra_logical_names or missing_fields:
        return 2, blocked_summary, None

    merged = copy.deepcopy(template)
    runs = merged.setdefault("results", {})
    merged_entries = []
    successful_run_ids: list[str] = []
    failed_run_ids: list[str] = []
    executed_flow_ids: list[str] = []
    all_succeeded = True

    for entry in merged.get("realNswRunEvidence", []):
        logical_name = entry["flowLogicalName"]
        capture_entry = capture_entries[logical_name]
        entry["flowId"] = capture_entry["flowId"]
        entry["runId"] = capture_entry["runId"]
        entry["runStatus"] = capture_entry["runStatus"]
        entry["runUrl"] = _normalize_https_url(capture_entry["runUrl"])
        merged_entries.append(entry)
        executed_flow_ids.append(entry["flowId"])
        if entry["runStatus"] == "succeeded":
            successful_run_ids.append(entry["runId"])
        else:
            failed_run_ids.append(entry["runId"])
            all_succeeded = False

    merged["asOf"] = capture_payload.get("asOf", date.today().isoformat())
    merged["status"] = (
        "captured_real_flow_smoke_passed"
        if all_succeeded
        else "captured_real_flow_smoke_with_non_success_runs"
    )
    merged["connectionReference"]["connectionConfigured"] = True
    merged["claimBoundary"]["flowSmokePassed"] = all_succeeded
    merged["claimBoundary"]["realComponentConfigured"] = True
    merged["claimBoundary"]["productionReadinessClaimed"] = False

    runs["executedFlowIds"] = executed_flow_ids
    runs["successfulRunIds"] = successful_run_ids
    runs["failedRunIds"] = failed_run_ids
    runs["correlationIds"] = capture_payload.get("correlationIds", [])
    runs["lastFailure"] = capture_payload.get("lastFailure")

    summary = {
        "status": merged["status"],
        "output": output_path.as_posix(),
        "capturedFlowLogicalNames": [
            entry["flowLogicalName"] for entry in merged_entries
        ],
        "successfulRunCount": len(successful_run_ids),
        "failedRunCount": len(failed_run_ids),
        "flowSmokePassed": all_succeeded,
    }
    return 0, summary, merged


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Path to the blocked flow-smoke template.",
    )
    parser.add_argument(
        "--capture",
        type=Path,
        required=True,
        help=(
            "Path to a JSON payload containing real flowRuns or "
            "realNswRunEvidence entries."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write the updated flow-smoke evidence.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        template = _json(args.template)
        capture = _json(args.capture)
        exit_code, summary, merged = build_flow_smoke_evidence(
            template,
            capture,
            output_path=args.output,
        )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        summary = {
            "status": "blocked_pending_real_flow_run_capture",
            "template": args.template.as_posix(),
            "output": args.output.as_posix(),
            "error": str(error),
        }
        merged = None
        exit_code = 2

    if merged is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
