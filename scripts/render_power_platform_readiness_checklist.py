#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

DISPLAY_NAMES = {
    "endpoint": "Endpoint",
    "github": "GitHub",
    "pac": "PAC",
    "flow_smoke": "Flow smoke",
    "dlp": "DLP",
    "subrepo": "Subrepo",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Render aggregate readiness preflight JSON as a Markdown operator "
            "checklist."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        help=(
            "Path to the aggregate readiness preflight JSON. Reads stdin when omitted."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Optional path to write the Markdown checklist. "
            "Prints to stdout when omitted."
        ),
    )
    return parser.parse_args()


def _load_summary(path: Path | None) -> dict[str, Any]:
    if path is None:
        raw = sys.stdin.read()
        source = "stdin"
    else:
        raw = path.read_text(encoding="utf-8")
        source = str(path)
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise SystemExit(f"{source}: invalid JSON: {error}") from error
    if not isinstance(payload, dict):
        raise SystemExit(f"{source}: aggregate preflight JSON must be an object")
    return payload


def _as_text(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _extract_payload_text(check: dict[str, Any], *path: str) -> str | None:
    details = check.get("details")
    if not isinstance(details, dict):
        return None
    payload = details.get("payload")
    if not isinstance(payload, dict):
        return None

    current: Any = payload
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return _as_text(current)


def _display_name(name: str) -> str:
    return DISPLAY_NAMES.get(name, name.replace("_", " ").strip().title())


def _format_command(command: Any) -> str:
    if isinstance(command, list) and all(isinstance(item, str) for item in command):
        return shlex.join(command)
    return str(command)


def _render_blocker_section(index: int, check: dict[str, Any]) -> str:
    name = _display_name(str(check.get("name", "blocker")))
    observed_status = _as_text(check.get("observedStatus")) or "unknown"
    expected_status = _as_text(check.get("expectedStatus")) or "unknown"
    expected_exit = check.get("expectedExitCode")
    command = _format_command(check.get("command"))
    blocker_summary = (
        _extract_payload_text(check, "blocker", "summary")
        or _extract_payload_text(check, "summary")
        or _extract_payload_text(check, "nextAction", "step")
        or observed_status
    )
    support_items: list[str] = []
    supporting_evidence = _extract_payload_text(check, "supportingEvidence")
    if supporting_evidence:
        support_items.append(supporting_evidence)

    lines = [
        f"## {index}. {name}",
        "",
        f"- [ ] Address the blocker: {blocker_summary}.",
        f"- [ ] Re-run `{command}`.",
        (
            f"- [ ] Confirm the check reports `{expected_status}` "
            f"with exit code `{expected_exit}` or a cleared blocker state."
        ),
    ]
    if support_items:
        lines.append(f"- [ ] Review supporting evidence: {support_items[0]}.")
    lines.append(
        "- [ ] Keep readiness unclaimed until the aggregate preflight is no "
        "longer blocked."
    )
    return "\n".join(lines)


def render_checklist(summary: dict[str, Any]) -> str:
    checks = summary.get("checks")
    if not isinstance(checks, list):
        raise SystemExit("aggregate preflight JSON must contain a checks array")

    blocked_checks = [
        check
        for check in checks
        if isinstance(check, dict) and check.get("blocked") is True
    ]
    total_checks = len([check for check in checks if isinstance(check, dict)])

    lines = [
        "# Power Platform aggregate readiness operator checklist",
        "",
        f"- Source status: `{_as_text(summary.get('status')) or 'unknown'}`",
        f"- Blocked checks: `{len(blocked_checks)}` of `{total_checks}`",
        "- Readiness claim: not made",
    ]

    if not blocked_checks:
        lines.extend(
            [
                "",
                "No blocked checks were present in the supplied summary.",
            ]
        )
        return "\n".join(lines)

    for index, check in enumerate(blocked_checks, start=1):
        lines.extend(["", _render_blocker_section(index, check)])
    return "\n".join(lines)


def main() -> int:
    args = _parse_args()
    summary = _load_summary(args.input)
    markdown = render_checklist(summary)
    if args.output is None:
        sys.stdout.write(markdown)
        sys.stdout.write("\n")
    else:
        args.output.write_text(markdown + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
