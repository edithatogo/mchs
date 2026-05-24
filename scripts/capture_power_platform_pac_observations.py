#!/usr/bin/env python3
"""Capture current PAC observations for app publication and connector connection."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "power-platform" / "evidence"
DEFAULT_TENANT_NAME = "NSW Health Department"
DEFAULT_ENVIRONMENT_NAME = "Dylan Mordaunt (Illawarra Shoalhaven LHD)'s Environment"
DEFAULT_ENVIRONMENT_ID = "611bca65-0b2a-eaa1-9e74-23bbba8eeec4"
DEFAULT_ENVIRONMENT_URL = "https://orgefc9aa3e.crm6.dynamics.com/"
REQUIRED_OBSERVATIONS = ("appId", "playUrl", "connectionId")
UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
PLAY_URL_RE = re.compile(
    r"^https://apps\.powerapps\.com/play/e/"
    r"(?P<environment_id>[0-9a-fA-F-]{36})/"
    r"a/(?P<app_id>[0-9a-fA-F-]{36})"
    r"(?:\?tenantId=(?P<tenant_id>[0-9a-fA-F-]{36}))?$"
)
ZERO_UUID = "00000000-0000-0000-0000-000000000000"
PLACEHOLDER_MARKERS = (
    "placeholder",
    "replace_me",
    "replace-me",
    "todo",
    "tbd",
    "your_",
)


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _is_placeholder_token(value: str) -> bool:
    lowered = value.strip().lower()
    return (
        lowered == ZERO_UUID
        or (lowered.startswith("{") and lowered.endswith("}"))
        or (lowered.startswith("<") and lowered.endswith(">"))
        or any(marker in lowered for marker in PLACEHOLDER_MARKERS)
    )


def _validate_uuid(value: str | None) -> tuple[str | None, str | None]:
    normalized = _clean(value)
    if normalized is None:
        return None, "missing"
    if _is_placeholder_token(normalized):
        return None, "placeholder"
    if not UUID_RE.fullmatch(normalized):
        return None, "invalid_format"
    return normalized, None


def _validate_play_url(
    value: str | None, *, expected_app_id: str | None = None
) -> tuple[str | None, str | None]:
    normalized = _clean(value)
    if normalized is None:
        return None, "missing"
    if _is_placeholder_token(normalized):
        return None, "placeholder"
    match = PLAY_URL_RE.fullmatch(normalized)
    if match is None:
        return None, "invalid_format"
    if any(
        component.lower() == ZERO_UUID
        for component in (
            match.group("environment_id"),
            match.group("app_id"),
            match.group("tenant_id"),
        )
        if component is not None
    ):
        return None, "placeholder"
    if (
        expected_app_id is not None
        and match.group("app_id").lower() != expected_app_id.lower()
    ):
        return None, "mismatch"
    return normalized, None


def _status(missing: list[str]) -> str:
    if missing:
        return "blocked_pending_required_pac_observations"
    return "captured_current_pac_observations"


def build_evidence(
    *,
    as_of: str,
    app_id: str | None,
    play_url: str | None,
    connection_id: str | None,
    app_name: str | None = None,
    connection_display_name: str | None = None,
    connector_api_id: str | None = None,
    tenant_name: str = DEFAULT_TENANT_NAME,
    environment_name: str = DEFAULT_ENVIRONMENT_NAME,
    environment_id: str = DEFAULT_ENVIRONMENT_ID,
    environment_url: str = DEFAULT_ENVIRONMENT_URL,
) -> dict[str, Any]:
    normalized_app_id, app_id_reason = _validate_uuid(app_id)
    normalized_play_url, play_url_reason = _validate_play_url(
        play_url, expected_app_id=normalized_app_id
    )
    normalized_connection_id, connection_id_reason = _validate_uuid(connection_id)

    validation = {
        "appId": {"status": "observed" if app_id_reason is None else "blocked"},
        "playUrl": {"status": "observed" if play_url_reason is None else "blocked"},
        "connectionId": {
            "status": "observed" if connection_id_reason is None else "blocked"
        },
    }
    for field, reason in [
        ("appId", app_id_reason),
        ("playUrl", play_url_reason),
        ("connectionId", connection_id_reason),
    ]:
        if reason is not None:
            validation[field]["reason"] = reason

    missing = [
        field
        for field, reason in [
            ("appId", app_id_reason),
            ("playUrl", play_url_reason),
            ("connectionId", connection_id_reason),
        ]
        if reason is not None
    ]

    app_publication_status = (
        "observed" if app_id_reason is None and play_url_reason is None else "blocked"
    )
    connector_connection_status = (
        "observed" if connection_id_reason is None else "blocked"
    )

    app_publication = {
        "appId": normalized_app_id,
        "playUrl": normalized_play_url,
        "status": app_publication_status,
    }
    if app_name:
        app_publication["appName"] = app_name

    connector_connection = {
        "connectionId": normalized_connection_id,
        "status": connector_connection_status,
    }
    if connection_display_name:
        connector_connection["connectionDisplayName"] = connection_display_name
    if connector_api_id:
        connector_connection["connectorApiId"] = connector_api_id

    evidence = {
        "schemaVersion": 1,
        "evidenceType": "power_platform_pac_observation_capture",
        "status": _status(missing),
        "asOf": as_of,
        "environment": {
            "tenantName": tenant_name,
            "environmentName": environment_name,
            "environmentId": environment_id,
            "environmentUrl": environment_url,
        },
        "requiredEvidence": list(REQUIRED_OBSERVATIONS),
        "currentPacObservations": {
            "appPublication": app_publication,
            "customConnectorConnection": connector_connection,
        },
        "validation": validation,
        "missingRequiredObservations": missing,
        "claimBoundary": {
            "appPublished": False,
            "connectionConfigured": False,
            "productionReadinessClaimed": False,
        },
        "nextAction": (
            "Capture real PAC appId, playUrl, and connectionId values; placeholders "
            "and mismatched play URLs stay blocked until the observed values are real."
        ),
    }
    return evidence


def write_evidence(path: Path, evidence: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Capture PAC observations for app publication and connector connection."
        )
    )
    parser.add_argument("--app-id", default=None, help="Observed Power Apps appId.")
    parser.add_argument(
        "--play-url", default=None, help="Observed Power Apps play URL."
    )
    parser.add_argument(
        "--connection-id",
        default=None,
        help="Observed custom connector connection ID from PAC.",
    )
    parser.add_argument("--app-name", default=None, help="Optional observed app name.")
    parser.add_argument(
        "--connection-display-name",
        default=None,
        help="Optional observed custom connector connection display name.",
    )
    parser.add_argument(
        "--connector-api-id",
        default=None,
        help="Optional observed custom connector API id.",
    )
    parser.add_argument(
        "--tenant-name",
        default=DEFAULT_TENANT_NAME,
        help="Tenant name to record in the evidence.",
    )
    parser.add_argument(
        "--environment-name",
        default=DEFAULT_ENVIRONMENT_NAME,
        help="Environment name to record in the evidence.",
    )
    parser.add_argument(
        "--environment-id",
        default=DEFAULT_ENVIRONMENT_ID,
        help="Environment id to record in the evidence.",
    )
    parser.add_argument(
        "--environment-url",
        default=DEFAULT_ENVIRONMENT_URL,
        help="Environment URL to record in the evidence.",
    )
    parser.add_argument(
        "--as-of",
        default=date.today().isoformat(),
        help="Observation date to stamp into the evidence.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Evidence output path "
            "(default: power-platform/evidence/pac-observation-capture-<as-of>.json)"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evidence = build_evidence(
        as_of=args.as_of,
        app_id=args.app_id,
        play_url=args.play_url,
        connection_id=args.connection_id,
        app_name=args.app_name,
        connection_display_name=args.connection_display_name,
        connector_api_id=args.connector_api_id,
        tenant_name=args.tenant_name,
        environment_name=args.environment_name,
        environment_id=args.environment_id,
        environment_url=args.environment_url,
    )
    output = (
        Path(args.output)
        if args.output
        else DEFAULT_OUTPUT_DIR
        / f"pac-observation-capture-{args.as_of.replace('-', '')}.json"
    )
    write_evidence(output, evidence)
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 2 if evidence["status"].startswith("blocked") else 0


if __name__ == "__main__":
    raise SystemExit(main())
