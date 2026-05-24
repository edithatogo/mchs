#!/usr/bin/env python3
"""Preflight the service-boundary endpoint operator package JSON artifacts."""

from __future__ import annotations

import argparse
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OPERATOR_INPUT = (
    ROOT
    / "power-platform"
    / "evidence"
    / "examples"
    / "service-boundary-endpoint-operator-input.example.json"
)
DEFAULT_PROBE_RESULT = (
    ROOT
    / "power-platform"
    / "evidence"
    / "examples"
    / "service-boundary-probe-result.example.json"
)
HEALTHZ_PATH = "/healthz"
SERVER_CARD_PATH = "/.well-known/mcp/server-card.json"


def _json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def _placeholder_reason(hostname: str) -> str | None:
    if not hostname:
        return "baseUrl must include a host"

    lowered = hostname.strip().lower()
    if lowered in {"localhost", "example.invalid"}:
        return "baseUrl must not use a placeholder host"
    if lowered.endswith((".example", ".invalid", ".localhost", ".test")):
        return "baseUrl must not use a placeholder host"

    try:
        address = ipaddress.ip_address(lowered)
    except ValueError:
        return None

    if address.is_private or address.is_loopback or address.is_link_local:
        return "baseUrl must not use a private or loopback address"
    if address.is_multicast or address.is_reserved:
        return "baseUrl must not use a reserved address"
    return None


def _is_placeholder_reason(reason: str) -> bool:
    lowered = reason.lower()
    return (
        "placeholder" in lowered
        or "private or loopback" in lowered
        or "reserved address" in lowered
        or "baseurl must not use a reserved address" in lowered
        or "baseurl must not use a private or loopback address" in lowered
    )


def normalize_https_base_url(base_url: str | None) -> str | None:
    if base_url is None:
        return None

    candidate = base_url.strip()
    if not candidate:
        return None

    parsed = urlparse(candidate)
    if parsed.scheme != "https":
        raise ValueError("baseUrl must use https")
    if not parsed.netloc:
        raise ValueError("baseUrl must include a host")
    if parsed.path not in ("", "/"):
        raise ValueError("baseUrl must not include a path")
    if parsed.query or parsed.fragment:
        raise ValueError("baseUrl must not include a query string or fragment")

    hostname = parsed.hostname or ""
    reason = _placeholder_reason(hostname)
    if reason is not None:
        raise ValueError(reason)
    return candidate.rstrip("/")


def _operator_boundary(operator_input: dict) -> dict:
    nested = operator_input.get("serviceBoundary")
    if isinstance(nested, dict):
        return nested
    return operator_input


def _coerce_checks(probe_payload: dict | list) -> tuple[str | None, list[dict]]:
    if isinstance(probe_payload, list):
        return None, [check for check in probe_payload if isinstance(check, dict)]

    if isinstance(probe_payload, dict):
        checks = probe_payload.get("checks")
        if isinstance(checks, list):
            return probe_payload.get("status"), [
                check for check in checks if isinstance(check, dict)
            ]

        if "status" in probe_payload and "name" in probe_payload:
            return probe_payload.get("status"), [probe_payload]

    raise ValueError("probe result must be a JSON list or an object with checks")


def _check_key(check: dict) -> str:
    return str(check.get("name") or check.get("path") or "").strip().lower()


def _placeholder_probe_reason(check: dict) -> str | None:
    error_text = str(check.get("error") or check.get("reason") or "").lower()
    if "example only" in error_text or "placeholder" in error_text:
        return "probe result still contains example-only placeholder text"
    return None


def summarize_probe(probe_payload: dict | list) -> dict:
    source_status, checks = _coerce_checks(probe_payload)
    healthz = None
    server_card = None
    placeholder_detected = False
    placeholder_reasons: list[str] = []

    for check in checks:
        key = _check_key(check)
        if key in {"healthz", "/healthz"}:
            healthz = check
        elif key in {"servercard", "server-card", "/.well-known/mcp/server-card.json"}:
            server_card = check

        reason = _placeholder_probe_reason(check)
        if reason is not None:
            placeholder_detected = True
            if reason not in placeholder_reasons:
                placeholder_reasons.append(reason)

    required_checks_present = healthz is not None and server_card is not None
    required_checks_passed = (
        required_checks_present
        and healthz.get("status") == "passed"
        and server_card.get("status") == "passed"
    )

    derived_status = "operator_package_ready"
    if placeholder_detected:
        derived_status = "blocked_placeholder_detected"
    elif not required_checks_present:
        derived_status = "blocked_missing_required_probe_checks"
    elif not required_checks_passed:
        derived_status = "blocked_probe_not_ready"

    return {
        "sourceStatus": source_status,
        "status": derived_status,
        "checks": checks,
        "requiredChecksPresent": required_checks_present,
        "requiredChecksPassed": required_checks_passed,
        "placeholderDetected": placeholder_detected,
        "placeholderReasons": placeholder_reasons,
        "healthzAttempted": healthz is not None,
        "serverCardAttempted": server_card is not None,
        "healthzPassed": bool(healthz and healthz.get("status") == "passed"),
        "serverCardPassed": bool(server_card and server_card.get("status") == "passed"),
        "selectedChecks": {
            "healthz": healthz,
            "serverCard": server_card,
        },
    }


def evaluate_package(
    operator_input: dict,
    probe_payload: dict | list,
) -> tuple[int, dict]:
    boundary = _operator_boundary(operator_input)
    raw_base_url = boundary.get("httpsBaseUrl")
    base_url_env = boundary.get("baseUrlEnvironmentVariable", "mchs_api_base_url")
    logical_connection_reference = boundary.get(
        "logicalConnectionReference", "mchs_service_boundary"
    )
    api_key_secret_configured = bool(boundary.get("apiKeySecretConfigured", False))

    base_url = None
    operator_reasons: list[str] = []
    placeholder_detected = False
    try:
        base_url = normalize_https_base_url(raw_base_url)
    except ValueError as error:
        operator_reasons.append(str(error))
        placeholder_detected = _is_placeholder_reason(str(error))

    probe_summary = summarize_probe(probe_payload)

    operator_status = "provided" if base_url is not None else "missing"
    if base_url is None:
        operator_status = "blocked"
        if not operator_reasons:
            operator_reasons.append("service boundary base URL is missing")
    if not api_key_secret_configured:
        operator_status = "blocked"
        operator_reasons.append("service boundary API key secret is not configured")

    overall_status = "operator_package_ready"
    if operator_status == "blocked":
        overall_status = "blocked_operator_input_invalid"
    if probe_summary["status"].startswith("blocked_"):
        overall_status = probe_summary["status"]
    if placeholder_detected or probe_summary["placeholderDetected"]:
        overall_status = "blocked_placeholder_detected"

    summary = {
        "status": overall_status,
        "operatorInput": {
            "logicalConnectionReference": logical_connection_reference,
            "baseUrlEnvironmentVariable": base_url_env,
            "httpsBaseUrl": raw_base_url,
            "apiKeySecretConfigured": api_key_secret_configured,
            "healthzPath": boundary.get("healthzPath", HEALTHZ_PATH),
            "serverCardPath": boundary.get("serverCardPath", SERVER_CARD_PATH),
            "valueStatus": operator_status,
            "reasons": operator_reasons,
        },
        "probe": probe_summary,
        "checks": [],
    }

    if overall_status == "operator_package_ready":
        summary["checks"].append(
            {
                "name": "operatorInput",
                "status": "passed",
                "value": raw_base_url,
            }
        )
        summary["checks"].append(
            {
                "name": "probeResult",
                "status": "passed",
                "requiredChecksPresent": probe_summary["requiredChecksPresent"],
                "requiredChecksPassed": probe_summary["requiredChecksPassed"],
            }
        )
        return 0, summary

    summary["checks"].append(
        {
            "name": "operatorInput",
            "status": "blocked",
            "value": raw_base_url,
            "reasons": operator_reasons,
        }
    )
    summary["checks"].append(
        {
            "name": "probeResult",
            "status": "blocked"
            if not probe_summary["requiredChecksPassed"]
            or probe_summary["placeholderDetected"]
            else "passed",
            "placeholderDetected": probe_summary["placeholderDetected"],
            "requiredChecksPresent": probe_summary["requiredChecksPresent"],
            "requiredChecksPassed": probe_summary["requiredChecksPassed"],
            "placeholderReasons": probe_summary["placeholderReasons"],
        }
    )
    return 2, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--operator-input",
        type=Path,
        default=DEFAULT_OPERATOR_INPUT,
        help="Path to the operator input JSON file.",
    )
    parser.add_argument(
        "--probe-result",
        type=Path,
        default=DEFAULT_PROBE_RESULT,
        help="Path to the probe result JSON file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    operator_input = _json(args.operator_input)
    probe_payload = _json(args.probe_result)
    if not isinstance(operator_input, dict):
        raise ValueError("operator input must be a JSON object")

    exit_code, summary = evaluate_package(operator_input, probe_payload)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
