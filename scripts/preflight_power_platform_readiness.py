#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
EVIDENCE = ROOT / "power-platform" / "evidence"

ENDPOINT_VALIDATOR = SCRIPTS / "validate_power_platform_service_boundary_endpoint.py"
GITHUB_VALIDATOR = SCRIPTS / "validate_power_platform_github_live_gate.py"
PAC_CAPTURE = SCRIPTS / "capture_power_platform_pac_observations.py"
FLOW_SMOKE_PRECHECK = SCRIPTS / "update_power_platform_flow_smoke_evidence.py"
DLP_PRECHECK = SCRIPTS / "update_power_platform_monitoring_dlp_evidence.py"
SUBREPO_WRITER = SCRIPTS / "write_power_platform_subrepo_closure.py"

FLOW_SMOKE_TEMPLATE = EVIDENCE / "flow-smoke-evidence-template.json"
FLOW_SMOKE_SAMPLE = EVIDENCE / "flow-smoke-capture-sample.json"
DLP_SAMPLE = EVIDENCE / "monitoring-dlp-capture-sample.json"
GITHUB_EVIDENCE = EVIDENCE / "github-live-gate-20260521.json"


def _run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _load_json_text(text: str, label: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        return None, f"{label}: invalid JSON output: {error}"
    if not isinstance(payload, dict):
        return None, f"{label}: JSON output must be an object"
    return payload, None


def _load_json_file(path: Path, label: str) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        return None, f"{label}: unable to read JSON output: {error}"
    except json.JSONDecodeError as error:
        return None, f"{label}: invalid JSON output: {error}"
    if not isinstance(payload, dict):
        return None, f"{label}: JSON output must be an object"
    return payload, None


def _check_result(
    *,
    name: str,
    command: list[str],
    expected_exit_code: int,
    observed_exit_code: int,
    expected_status: str,
    observed_status: str | None,
    payload: dict[str, Any] | None,
    parse_error: str | None,
    stdout: str,
    stderr: str,
) -> dict[str, Any]:
    ok = (
        observed_exit_code == expected_exit_code
        and observed_status == expected_status
        and parse_error is None
    )
    blocked = bool(observed_status and observed_status.startswith("blocked"))
    result = {
        "name": name,
        "command": command,
        "expectedExitCode": expected_exit_code,
        "observedExitCode": observed_exit_code,
        "expectedStatus": expected_status,
        "observedStatus": observed_status,
        "blocked": blocked,
        "ok": ok,
        "details": {
            "stdout": stdout,
            "stderr": stderr,
        },
    }
    if payload is not None:
        result["details"]["payload"] = payload
    if parse_error is not None:
        result["details"]["parseError"] = parse_error
    return result


def _endpoint_check() -> dict[str, Any]:
    command = [sys.executable, str(ENDPOINT_VALIDATOR)]
    proc = _run(command)
    payload, parse_error = _load_json_text(proc.stdout, "endpoint validator")
    observed_status = payload.get("status") if payload is not None else None
    return _check_result(
        name="endpoint",
        command=command,
        expected_exit_code=2,
        observed_exit_code=proc.returncode,
        expected_status="blocked_pending_real_https_endpoint",
        observed_status=observed_status,
        payload=payload,
        parse_error=parse_error,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _github_check() -> dict[str, Any]:
    command = [sys.executable, str(GITHUB_VALIDATOR)]
    proc = _run(command)
    evidence, parse_error = _load_json_file(GITHUB_EVIDENCE, "GitHub live-gate")
    observed_status = evidence.get("status") if evidence is not None else None
    return _check_result(
        name="github",
        command=command,
        expected_exit_code=0,
        observed_exit_code=proc.returncode,
        expected_status="blocked_pending_repository_secrets_and_workflow_run",
        observed_status=observed_status,
        payload=evidence,
        parse_error=parse_error,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _pac_check(tmpdir: Path) -> dict[str, Any]:
    output = tmpdir / "pac-observation-capture.json"
    command = [
        sys.executable,
        str(PAC_CAPTURE),
        "--output",
        str(output),
    ]
    proc = _run(command)
    payload, parse_error = _load_json_text(proc.stdout, "PAC observation capture")
    if payload is None:
        file_payload, file_error = _load_json_file(output, "PAC observation capture")
        if file_payload is not None:
            payload = file_payload
            parse_error = file_error
    observed_status = payload.get("status") if payload is not None else None
    return _check_result(
        name="pac",
        command=command,
        expected_exit_code=2,
        observed_exit_code=proc.returncode,
        expected_status="blocked_pending_required_pac_observations",
        observed_status=observed_status,
        payload=payload,
        parse_error=parse_error,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _flow_smoke_check(tmpdir: Path) -> dict[str, Any]:
    output = tmpdir / "flow-smoke.json"
    command = [
        sys.executable,
        str(FLOW_SMOKE_PRECHECK),
        "--preflight",
        "--template",
        str(FLOW_SMOKE_TEMPLATE),
        "--capture",
        str(FLOW_SMOKE_SAMPLE),
        "--output",
        str(output),
    ]
    proc = _run(command)
    payload, parse_error = _load_json_text(proc.stdout, "flow smoke preflight")
    observed_status = payload.get("status") if payload is not None else None
    return _check_result(
        name="flow_smoke",
        command=command,
        expected_exit_code=2,
        observed_exit_code=proc.returncode,
        expected_status="blocked_pending_sample_capture",
        observed_status=observed_status,
        payload=payload,
        parse_error=parse_error,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _dlp_check(tmpdir: Path) -> dict[str, Any]:
    output = tmpdir / "monitoring-dlp.json"
    command = [
        sys.executable,
        str(DLP_PRECHECK),
        "--preflight",
        "--input",
        str(DLP_SAMPLE),
        "--output",
        str(output),
    ]
    proc = _run(command)
    payload, parse_error = _load_json_text(proc.stdout, "monitoring/DLP preflight")
    observed_status = payload.get("status") if payload is not None else None
    return _check_result(
        name="dlp",
        command=command,
        expected_exit_code=2,
        observed_exit_code=proc.returncode,
        expected_status="blocked_pending_shape_or_placeholder_validation",
        observed_status=observed_status,
        payload=payload,
        parse_error=parse_error,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def _subrepo_check(tmpdir: Path) -> dict[str, Any]:
    output = tmpdir / "subrepo-closure.json"
    command = [
        sys.executable,
        str(SUBREPO_WRITER),
        "--output",
        str(output),
    ]
    proc = _run(command)
    payload, parse_error = _load_json_file(output, "subrepo closure")
    observed_status = payload.get("status") if payload is not None else None
    return _check_result(
        name="subrepo",
        command=command,
        expected_exit_code=0,
        observed_exit_code=proc.returncode,
        expected_status="blocked_pending_remote_or_explicit_waiver",
        observed_status=observed_status,
        payload=payload,
        parse_error=parse_error,
        stdout=proc.stdout,
        stderr=proc.stderr,
    )


def run_preflight() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="mchs-power-platform-preflight-") as tmp:
        tmpdir = Path(tmp)
        checks = [
            _endpoint_check(),
            _github_check(),
            _pac_check(tmpdir),
            _flow_smoke_check(tmpdir),
            _dlp_check(tmpdir),
            _subrepo_check(tmpdir),
        ]

    all_checks_ok = all(check["ok"] for check in checks)
    all_checks_blocked = all(check["blocked"] for check in checks)
    status = (
        "blocked_pending_power_platform_readiness_evidence"
        if all_checks_ok and all_checks_blocked
        else "failed_power_platform_readiness_preflight"
    )
    return {
        "schemaVersion": 1,
        "status": status,
        "readinessClaimed": False,
        "allChecksBlocked": all_checks_blocked,
        "checkCount": len(checks),
        "checks": checks,
    }


def main() -> int:
    summary = run_preflight()
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"].startswith("blocked_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
