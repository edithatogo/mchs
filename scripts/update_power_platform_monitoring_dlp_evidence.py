#!/usr/bin/env python3
"""Update Power Platform monitoring/DLP evidence from supplied fields.

The updater is fail-closed: it merges the supplied monitoring and policy fields
into the evidence template, but it keeps the record blocked and exits non-zero
until every required field is populated.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = (
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-evidence-template.json"
)
DEFAULT_OUTPUT = (
    ROOT
    / "power-platform"
    / "evidence"
    / "dlp-monitoring-policy-evidence-20260521.json"
)
REQUIRED_FIELDS: tuple[tuple[str, ...], ...] = (
    ("monitoring", "owner"),
    ("monitoring", "failureMetrics", "connectorFailures"),
    ("monitoring", "failureMetrics", "flowRunFailures"),
    ("monitoring", "failureMetrics", "serviceBoundaryHealth"),
    ("monitoring", "failureMetrics", "appHealthMetrics"),
    ("monitoring", "failureMetrics", "correlationIdsWithoutPatientData"),
    ("dlp", "policyId"),
    ("dlp", "policyName"),
    ("dlp", "policyClassification"),
    ("dlp", "policyCaptureState"),
    ("connectorPolicy", "policyId"),
    ("connectorPolicy", "policyName"),
    ("connectorPolicy", "connectorAllowState"),
    ("support", "owner"),
    ("support", "escalationOwner"),
    ("support", "escalationPath"),
    ("support", "escalationContact"),
)
UPDATE_SECTIONS = ("monitoring", "dlp", "connectorPolicy", "support")
STATUS_BY_PREFIX = {
    ("monitoring", "owner"): "blocked_pending_owner_capture",
    ("monitoring", "failureMetrics"): "blocked_pending_metrics_capture",
    ("dlp",): "blocked_pending_policy_capture",
    ("connectorPolicy",): "blocked_pending_policy_capture",
    ("support",): "blocked_pending_escalation_capture",
}
PLACEHOLDER_BY_PREFIX = {
    ("monitoring", "owner"): "TBD",
    ("monitoring", "failureMetrics"): "required",
    ("dlp",): "TBD",
    ("connectorPolicy",): "TBD",
    ("support",): "TBD",
}


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        flattened: dict[str, Any] = {}
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}" if prefix else key
            flattened.update(_flatten(child, child_prefix))
        return flattened
    return {prefix: value}


def _collect_leaf_paths(data: dict[str, Any], prefix: tuple[str, ...] = ()) -> set[str]:
    paths: set[str] = set()
    for key, value in data.items():
        next_prefix = (*prefix, key)
        if isinstance(value, dict) and value:
            paths.update(_collect_leaf_paths(value, next_prefix))
        else:
            paths.add(".".join(next_prefix))
    return paths


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        candidate = value.strip()
        return candidate not in {"", "TBD", "required"} and not candidate.startswith(
            "blocked_pending"
        )
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def _get_path(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    cursor: Any = data
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            return None
        cursor = cursor[key]
    return cursor


def _set_path(data: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    cursor: dict[str, Any] = data
    for key in path[:-1]:
        next_value = cursor.get(key)
        if not isinstance(next_value, dict):
            next_value = {}
            cursor[key] = next_value
        cursor = next_value
    cursor[path[-1]] = value


def _blocked_status(path: tuple[str, ...]) -> str:
    for prefix, status in STATUS_BY_PREFIX.items():
        if path[: len(prefix)] == prefix:
            return status
    return "blocked_pending_capture"


def _placeholder(path: tuple[str, ...]) -> str:
    for prefix, placeholder in PLACEHOLDER_BY_PREFIX.items():
        if path[: len(prefix)] == prefix:
            return placeholder
    return "TBD"


def _capture_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in REQUIRED_FIELDS:
        field = ".".join(path)
        value = _get_path(data, path)
        present = _is_present(value)
        entries.append(
            {
                "field": field,
                "value": value if present else _placeholder(path),
                "status": "captured" if present else _blocked_status(path),
            }
        )
    return entries


def _validate_supplied_fields(
    supplied: dict[str, Any], allowed_paths: set[str]
) -> list[str]:
    unknown = sorted(set(supplied) - allowed_paths)
    return unknown


def update_evidence(
    template: dict[str, Any], supplied: dict[str, Any]
) -> tuple[dict[str, Any], list[str]]:
    evidence = json.loads(json.dumps(template))
    flattened = _flatten(supplied)
    allowed_paths: set[str] = set()
    for section in UPDATE_SECTIONS:
        section_value = template.get(section)
        if isinstance(section_value, dict):
            allowed_paths.update(_collect_leaf_paths({section: section_value}))
    unknown = _validate_supplied_fields(flattened, allowed_paths)
    if unknown:
        raise ValueError(
            "unsupported monitoring/DLP fields supplied: " + ", ".join(unknown)
        )

    for path_text, value in flattened.items():
        _set_path(evidence, tuple(path_text.split(".")), value)

    evidence["requiredEvidence"] = [".".join(path) for path in REQUIRED_FIELDS]
    evidence["capturedEvidence"] = _capture_entries(evidence)
    evidence.setdefault("claimBoundary", {})["monitoringConfigured"] = False
    evidence["claimBoundary"]["dlpEvidenceCaptured"] = False
    evidence["claimBoundary"]["productionReadinessClaimed"] = False

    missing = [
        ".".join(path)
        for path in REQUIRED_FIELDS
        if not _is_present(_get_path(evidence, path))
    ]
    return evidence, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update Power Platform monitoring/DLP evidence from fields."
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Path to the monitoring/DLP evidence template.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to a JSON file containing supplied monitoring/DLP fields.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to write the updated evidence record.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    template = _json(args.template)
    supplied = _json(args.input)
    if not isinstance(supplied, dict):
        raise SystemExit(f"{args.input}: input must be a JSON object")

    base = _json(args.output) if args.output.exists() else template
    evidence, missing = update_evidence(base, supplied)
    _dump(args.output, evidence)

    summary = {
        "status": evidence["status"],
        "output": str(args.output),
        "complete": not missing,
        "missingFields": missing,
        "capturedFields": [
            item["field"]
            for item in evidence["capturedEvidence"]
            if item["status"] == "captured"
        ],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
