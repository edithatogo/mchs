from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_power_platform_readiness_checklist.py"


def test_render_power_platform_readiness_checklist_script_exists() -> None:
    assert SCRIPT.exists(), SCRIPT


def test_render_power_platform_readiness_checklist_emits_markdown_sections(
    tmp_path: Path,
) -> None:
    summary = {
        "schemaVersion": 1,
        "status": "blocked_pending_power_platform_readiness_evidence",
        "readinessClaimed": False,
        "allChecksBlocked": False,
        "checkCount": 3,
        "checks": [
            {
                "name": "endpoint",
                "command": [
                    "python",
                    "scripts/validate_power_platform_service_boundary_endpoint.py",
                ],
                "expectedExitCode": 2,
                "observedExitCode": 2,
                "expectedStatus": "blocked_pending_real_https_endpoint",
                "observedStatus": "blocked_pending_real_https_endpoint",
                "blocked": True,
                "ok": True,
                "details": {
                    "payload": {
                        "blocker": {
                            "summary": (
                                "service boundary production endpoint and "
                                "connection reference values"
                            )
                        }
                    }
                },
            },
            {
                "name": "github",
                "command": [
                    "python",
                    "scripts/validate_power_platform_github_live_gate.py",
                ],
                "expectedExitCode": 0,
                "observedExitCode": 0,
                "expectedStatus": "blocked_pending_repository_secrets_and_workflow_run",
                "observedStatus": "blocked_pending_repository_secrets_and_workflow_run",
                "blocked": True,
                "ok": True,
                "details": {
                    "payload": {
                        "summary": "repository secrets and workflow run evidence"
                    }
                },
            },
            {
                "name": "subrepo",
                "command": [
                    "python",
                    "scripts/write_power_platform_subrepo_closure.py",
                ],
                "expectedExitCode": 0,
                "observedExitCode": 0,
                "expectedStatus": "blocked_pending_remote_or_explicit_waiver",
                "observedStatus": "blocked_pending_remote_or_explicit_waiver",
                "blocked": False,
                "ok": True,
                "details": {"payload": {"summary": "not blocked"}},
            },
        ],
    }

    input_path = tmp_path / "preflight.json"
    input_path.write_text(json.dumps(summary), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--input", str(input_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    text = result.stdout
    assert "# Power Platform aggregate readiness operator checklist" in text
    assert (
        "- Source status: `blocked_pending_power_platform_readiness_evidence`" in text
    )
    assert "- Blocked checks: `2` of `3`" in text
    assert "- Readiness claim: not made" in text
    assert "## 1. Endpoint" in text
    assert (
        "service boundary production endpoint and connection reference values" in text
    )
    assert "## 2. GitHub" in text
    assert "repository secrets and workflow run evidence" in text
    assert "## 3. Subrepo" not in text
    assert "Keep readiness unclaimed" in text
