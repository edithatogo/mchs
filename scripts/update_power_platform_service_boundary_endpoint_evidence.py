#!/usr/bin/env python3
"""Update service-boundary endpoint evidence from a supplied URL and probe result."""

from __future__ import annotations

import argparse
import copy
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT / "power-platform" / "evidence" / "service-boundary-endpoint-template.json"
)


def _json(path: Path) -> dict | list:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
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
    if hostname == "example.invalid" or hostname.endswith(".invalid"):
        raise ValueError("baseUrl must not use a placeholder host")
    return candidate.rstrip("/")


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


def summarize_probe(probe_payload: dict | list) -> dict:
    source_status, checks = _coerce_checks(probe_payload)
    healthz = None
    server_card = None

    for check in checks:
        key = _check_key(check)
        if key in {"healthz", "/healthz"}:
            healthz = check
        elif key in {
            "servercard",
            "server-card",
            "/.well-known/mcp/server-card.json",
        }:
            server_card = check

    required_checks_present = healthz is not None and server_card is not None
    required_checks_passed = (
        required_checks_present
        and healthz.get("status") == "passed"
        and server_card.get("status") == "passed"
    )
    any_failed = any(check.get("status") != "passed" for check in checks)

    derived_status = "probe_passed" if required_checks_passed else "probe_failed"
    if not checks:
        derived_status = "blocked_pending_real_https_endpoint"

    return {
        "sourceStatus": source_status,
        "status": derived_status,
        "checks": checks,
        "requiredChecksPresent": required_checks_present,
        "requiredChecksPassed": required_checks_passed,
        "anyFailed": any_failed,
        "healthzAttempted": healthz is not None,
        "serverCardAttempted": server_card is not None,
        "healthzPassed": bool(healthz and healthz.get("status") == "passed"),
        "serverCardPassed": bool(server_card and server_card.get("status") == "passed"),
        "selectedChecks": {
            "healthz": healthz,
            "serverCard": server_card,
        },
    }


def render_evidence(
    source: dict,
    base_url: str,
    probe_summary: dict,
    as_of: str,
) -> dict:
    evidence = copy.deepcopy(source)

    evidence["asOf"] = as_of
    evidence["status"] = probe_summary["status"]

    service_boundary = evidence.setdefault("serviceBoundary", {})
    service_boundary["httpsBaseUrl"] = base_url
    if probe_summary["requiredChecksPassed"]:
        service_boundary["publiclyReachableFromPowerPlatform"] = True
    service_boundary.setdefault("publiclyReachableFromPowerPlatform", False)
    service_boundary.setdefault("tlsTrusted", False)

    validation = evidence.setdefault("validation", {})
    validation["endpointSyntaxValidated"] = True
    validation["healthzProbed"] = probe_summary["healthzAttempted"]
    validation["serverCardProbed"] = probe_summary["serverCardAttempted"]
    validation["probeRequired"] = True
    validation["probe"] = {
        "status": probe_summary["status"],
        "sourceStatus": probe_summary["sourceStatus"],
        "checks": probe_summary["checks"],
    }

    claim_boundary = evidence.setdefault("claimBoundary", {})
    claim_boundary["endpointConfigured"] = True
    claim_boundary["endpointValidated"] = probe_summary["requiredChecksPassed"]
    claim_boundary["productionReadinessClaimed"] = False

    handoff = evidence.setdefault("handoff", {})
    handoff["status"] = probe_summary["status"]
    handoff["nextAction"] = (
        "Keep production readiness unclaimed; record the generated artifact as "
        "endpoint evidence only."
        if probe_summary["requiredChecksPassed"]
        else (
            "Provide a real public HTTPS base URL, publish the healthz and "
            "server-card routes, then rerun "
            "scripts/validate_power_platform_service_boundary_endpoint.py "
            "with --probe."
        )
    )
    required_inputs = handoff.setdefault("requiredInputs", [])
    if required_inputs:
        required_inputs[0]["valueStatus"] = "provided"

    return evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Blocked endpoint evidence template or a prior evidence record.",
    )
    parser.add_argument(
        "--https-base-url",
        required=True,
        help="Real public HTTPS base URL to record in the evidence.",
    )
    parser.add_argument(
        "--probe-result",
        type=Path,
        required=True,
        help="JSON probe result, typically the output from the endpoint validator.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the updated evidence JSON here instead of stdout.",
    )
    parser.add_argument(
        "--as-of",
        default=date.today().isoformat(),
        help="Evidence date to record (defaults to today).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = _json(args.source)
    if not isinstance(source, dict):
        raise ValueError("source evidence must be a JSON object")

    base_url = normalize_https_base_url(args.https_base_url)
    if base_url is None:
        raise ValueError("https-base-url must not be empty")

    probe_payload = _json(args.probe_result)
    probe_summary = summarize_probe(probe_payload)
    evidence = render_evidence(source, base_url, probe_summary, args.as_of)

    if args.output is None:
        print(json.dumps(evidence, indent=2, sort_keys=True))
    else:
        _write_json(args.output, evidence)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
