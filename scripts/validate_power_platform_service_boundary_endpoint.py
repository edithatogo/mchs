#!/usr/bin/env python3
"""Validate a supplied service-boundary HTTPS endpoint configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    ROOT / "power-platform" / "evidence" / "service-boundary-endpoint-template.json"
)
HEALTHZ_PATH = "/healthz"
SERVER_CARD_PATH = "/.well-known/mcp/server-card.json"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def evaluate_configuration(config: dict) -> tuple[int, dict]:
    service_boundary = config.get("serviceBoundary", {})
    base_url = normalize_https_base_url(service_boundary.get("httpsBaseUrl"))
    base_url_env = service_boundary.get(
        "baseUrlEnvironmentVariable",
        "mchs_api_base_url",
    )

    required_inputs = [
        {
            "logicalName": base_url_env,
            "valueStatus": "provided" if base_url is not None else "missing",
            "purpose": "Real public HTTPS base URL for the service boundary",
        }
    ]
    required_checks = [
        {
            "name": "healthz",
            "path": service_boundary.get("healthzPath", HEALTHZ_PATH),
            "expectedStatusCode": 200,
        },
        {
            "name": "serverCard",
            "path": service_boundary.get("serverCardPath", SERVER_CARD_PATH),
            "expectedStatusCode": 200,
            "expectedContentType": "application/json",
        },
    ]

    summary = {
        "status": "blocked_pending_real_https_endpoint",
        "serviceBoundary": {
            "logicalConnectionReference": service_boundary.get(
                "logicalConnectionReference", "mchs_service_boundary"
            ),
            "baseUrlEnvironmentVariable": base_url_env,
            "httpsBaseUrl": base_url,
            "healthzPath": service_boundary.get("healthzPath", HEALTHZ_PATH),
            "serverCardPath": service_boundary.get("serverCardPath", SERVER_CARD_PATH),
            "apiKeySecretConfigured": bool(
                service_boundary.get("apiKeySecretConfigured", False)
            ),
        },
        "handoff": {
            "status": "blocked_pending_real_https_endpoint"
            if base_url is None
            else "ready_for_probe",
            "requiredInputs": required_inputs,
            "requiredChecks": required_checks,
            "nextAction": (
                "Provide a real public HTTPS base URL, publish the healthz and "
                "server-card routes, then rerun this validator with --probe."
            ),
        },
        "checks": [],
    }

    if base_url is None:
        summary["checks"].append(
            {
                "name": "httpsBaseUrl",
                "status": "blocked",
                "reason": "service boundary endpoint has not been supplied",
            }
        )
        return 2, summary

    summary["status"] = "ready_for_probe"
    summary["checks"].append(
        {
            "name": "httpsBaseUrl",
            "status": "passed",
            "value": base_url,
        }
    )
    return 0, summary


def probe_endpoint(base_url: str, timeout: float) -> list[dict]:
    checks: list[dict] = []
    for path, expects_json in [
        (HEALTHZ_PATH, False),
        (SERVER_CARD_PATH, True),
    ]:
        url = f"{base_url}{path}"
        request = Request(url, headers={"Accept": "application/json"})
        try:
            with urlopen(request, timeout=timeout) as response:  # nosec B310
                status_code = getattr(response, "status", response.getcode())
                body = response.read()
                content_type = response.headers.get("Content-Type", "")
        except Exception as error:  # pragma: no cover - network dependent
            checks.append(
                {
                    "name": path,
                    "status": "failed",
                    "error": str(error),
                }
            )
            continue

        check = {
            "name": path,
            "status": "passed" if status_code == 200 else "failed",
            "statusCode": status_code,
            "contentType": content_type,
        }
        if expects_json and status_code == 200:
            try:
                check["json"] = json.loads(body.decode("utf-8"))
            except Exception as error:  # pragma: no cover - network dependent
                check["status"] = "failed"
                check["error"] = f"server-card is not valid JSON: {error}"
        checks.append(check)
    return checks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to a service-boundary endpoint config or template.",
    )
    parser.add_argument(
        "--probe",
        action="store_true",
        help=(
            "Probe /healthz and /.well-known/mcp/server-card.json when "
            "a real URL is supplied."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Network timeout in seconds for endpoint probes.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = _json(args.config)
    exit_code, summary = evaluate_configuration(config)

    if args.probe and summary["status"] == "ready_for_probe":
        base_url = summary["serviceBoundary"]["httpsBaseUrl"]
        probe_results = probe_endpoint(base_url, timeout=args.timeout)
        summary["checks"].extend(probe_results)
        if all(check.get("status") == "passed" for check in probe_results):
            summary["status"] = "probe_passed"
            exit_code = 0
        else:
            summary["status"] = "probe_failed"
            exit_code = 1

    print(json.dumps(summary, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
