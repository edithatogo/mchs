#!/usr/bin/env python3
"""Write the Power Platform subrepo closure evidence record.

The default output is a blocked record that preserves the current
"blocked_pending_remote_or_explicit_waiver" state. Use the explicit
subcommands to write a complete standalone remote record or a complete
explicit waiver record.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT / "power-platform" / "repository" / "subrepo-closure-20260521.json"
)
DEFAULT_AS_OF = "2026-05-21"

REQUIRED_REMOTE_FIELDS = ("remoteUrl", "defaultBranch", "syncProcedure", "importOwner")
REQUIRED_WAIVER_FIELDS = (
    "approvedBy",
    "approvalRecord",
    "reason",
    "reviewDate",
    "riskAcceptance",
)

BLOCKED_RECORD: dict[str, Any] = {
    "schemaVersion": 1,
    "evidenceType": "power_platform_subrepo_closure",
    "status": "blocked_pending_remote_or_explicit_waiver",
    "currentMode": "in_repository_governed_subrepo_boundary",
    "acceptableClosureOptions": [
        {
            "option": "standalone_remote",
            "requiredFields": list(REQUIRED_REMOTE_FIELDS),
            "requiredEvidence": [
                "remote URL",
                "default branch",
                "sync direction",
                "sync procedure",
                "release owner",
                "import owner",
                "promotion branch policy",
            ],
        },
        {
            "option": "explicit_waiver",
            "requiredFields": list(REQUIRED_WAIVER_FIELDS),
            "requiredEvidence": [
                "waiver approver",
                "approval record",
                "reason",
                "review date",
                "risk acceptance",
            ],
        },
    ],
    "requiredClosureFields": {
        "standaloneRemote": list(REQUIRED_REMOTE_FIELDS),
        "explicitWaiver": list(REQUIRED_WAIVER_FIELDS),
    },
    "selectedOption": None,
    "claimBoundary": {
        "standaloneRemoteProvisioned": False,
        "explicitWaiverRecorded": False,
        "subrepoClosureComplete": False,
    },
    "standaloneRemote": {
        "provisioned": False,
        "remoteUrl": None,
        "defaultBranch": None,
        "syncProcedure": None,
        "importOwner": None,
        "provisioningStatus": "not_provisioned",
    },
    "waiver": {
        "required": True,
        "status": "blocked",
        "reason": (
            "No standalone remote has been supplied for the governed "
            "Power Platform boundary; runtime closure cannot claim "
            "subrepo separation."
        ),
        "approvedBy": None,
        "approvalRecord": None,
        "reviewDate": None,
        "riskAcceptance": None,
    },
    "subrepoBoundary": {
        "mode": "in_repository_governed_subrepo_boundary",
        "path": "power-platform/",
        "parentRepository": "https://github.com/edithatogo/mchs",
    },
}


def _clone_blocked_record(as_of: str) -> dict[str, Any]:
    record = deepcopy(BLOCKED_RECORD)
    record["asOf"] = as_of
    return record


def _require_text(value: str | None, label: str) -> str:
    if value is None or not str(value).strip():
        raise ValueError(f"{label} must be provided and non-empty")
    return value.strip()


def build_blocked_record(as_of: str = DEFAULT_AS_OF) -> dict[str, Any]:
    return _clone_blocked_record(as_of)


def build_standalone_remote_record(
    *,
    remote_url: str,
    default_branch: str,
    sync_procedure: str,
    import_owner: str,
    as_of: str = DEFAULT_AS_OF,
) -> dict[str, Any]:
    record = _clone_blocked_record(as_of)
    record["status"] = "standalone_remote_recorded"
    record["selectedOption"] = "standalone_remote"
    record["claimBoundary"] = {
        "standaloneRemoteProvisioned": True,
        "explicitWaiverRecorded": False,
        "subrepoClosureComplete": True,
    }
    record["standaloneRemote"] = {
        "provisioned": True,
        "remoteUrl": _require_text(remote_url, "remote-url"),
        "defaultBranch": _require_text(default_branch, "default-branch"),
        "syncProcedure": _require_text(sync_procedure, "sync-procedure"),
        "importOwner": _require_text(import_owner, "import-owner"),
        "provisioningStatus": "provisioned",
    }
    record["waiver"] = {
        "required": False,
        "status": "not_required",
        "reason": (
            "Standalone remote is provisioned, so an explicit waiver "
            "is not required."
        ),
        "approvedBy": None,
        "approvalRecord": None,
        "reviewDate": None,
        "riskAcceptance": None,
    }
    return record


def build_explicit_waiver_record(
    *,
    approved_by: str,
    approval_record: str,
    reason: str,
    review_date: str,
    risk_acceptance: str,
    as_of: str = DEFAULT_AS_OF,
) -> dict[str, Any]:
    record = _clone_blocked_record(as_of)
    record["status"] = "explicit_waiver_recorded"
    record["selectedOption"] = "explicit_waiver"
    record["claimBoundary"] = {
        "standaloneRemoteProvisioned": False,
        "explicitWaiverRecorded": True,
        "subrepoClosureComplete": True,
    }
    record["standaloneRemote"] = {
        "provisioned": False,
        "remoteUrl": None,
        "defaultBranch": None,
        "syncProcedure": None,
        "importOwner": None,
        "provisioningStatus": "not_provisioned",
    }
    record["waiver"] = {
        "required": True,
        "status": "recorded",
        "reason": _require_text(reason, "reason"),
        "approvedBy": _require_text(approved_by, "approved-by"),
        "approvalRecord": _require_text(approval_record, "approval-record"),
        "reviewDate": _require_text(review_date, "review-date"),
        "riskAcceptance": _require_text(risk_acceptance, "risk-acceptance"),
    }
    return record


def _write_record(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Write the Power Platform subrepo closure evidence record. "
            "Defaults to the blocked record unless a closure branch is chosen."
        )
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output JSON file (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--as-of",
        default=DEFAULT_AS_OF,
        help=f"Evidence date stamp (default: {DEFAULT_AS_OF})",
    )
    subparsers = parser.add_subparsers(dest="mode")

    blocked = subparsers.add_parser(
        "blocked",
        help="Write the default blocked closure record",
    )
    blocked.set_defaults(mode="blocked")

    remote = subparsers.add_parser(
        "standalone-remote",
        help="Write a complete standalone remote closure record",
    )
    remote.add_argument("--remote-url", required=True)
    remote.add_argument("--default-branch", required=True)
    remote.add_argument("--sync-procedure", required=True)
    remote.add_argument("--import-owner", required=True)
    remote.set_defaults(mode="standalone_remote")

    waiver = subparsers.add_parser(
        "explicit-waiver",
        help="Write a complete explicit waiver closure record",
    )
    waiver.add_argument("--approved-by", required=True)
    waiver.add_argument("--approval-record", required=True)
    waiver.add_argument("--reason", required=True)
    waiver.add_argument("--review-date", required=True)
    waiver.add_argument("--risk-acceptance", required=True)
    waiver.set_defaults(mode="explicit_waiver")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.mode == "standalone_remote":
        record = build_standalone_remote_record(
            remote_url=args.remote_url,
            default_branch=args.default_branch,
            sync_procedure=args.sync_procedure,
            import_owner=args.import_owner,
            as_of=args.as_of,
        )
    elif args.mode == "explicit_waiver":
        record = build_explicit_waiver_record(
            approved_by=args.approved_by,
            approval_record=args.approval_record,
            reason=args.reason,
            review_date=args.review_date,
            risk_acceptance=args.risk_acceptance,
            as_of=args.as_of,
        )
    else:
        record = build_blocked_record(as_of=args.as_of)

    _write_record(args.output, record)
    print(f"Wrote {record['status']} closure record to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
