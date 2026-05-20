from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "preflight_power_platform_readiness.py"


def test_power_platform_readiness_preflight_script_exists() -> None:
    assert SCRIPT.exists(), SCRIPT


def test_power_platform_readiness_preflight_emits_blocked_summary() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    summary = json.loads(result.stdout)
    assert summary["schemaVersion"] == 1
    assert summary["status"] == "blocked_pending_power_platform_readiness_evidence"
    assert summary["readinessClaimed"] is False
    assert summary["allChecksBlocked"] is True
    assert summary["checkCount"] == 6

    names = [check["name"] for check in summary["checks"]]
    assert names == ["endpoint", "github", "pac", "flow_smoke", "dlp", "subrepo"]

    expected_statuses = {
        "endpoint": "blocked_pending_real_https_endpoint",
        "github": "blocked_pending_repository_secrets_and_workflow_run",
        "pac": "blocked_pending_required_pac_observations",
        "flow_smoke": "blocked_pending_sample_capture",
        "dlp": "blocked_pending_shape_or_placeholder_validation",
        "subrepo": "blocked_pending_remote_or_explicit_waiver",
    }
    expected_exits = {
        "endpoint": 2,
        "github": 0,
        "pac": 2,
        "flow_smoke": 2,
        "dlp": 2,
        "subrepo": 0,
    }

    for check in summary["checks"]:
        name = check["name"]
        assert check["ok"] is True
        assert check["blocked"] is True
        assert check["observedStatus"] == expected_statuses[name]
        assert check["expectedStatus"] == expected_statuses[name]
        assert check["observedExitCode"] == expected_exits[name]
        assert check["expectedExitCode"] == expected_exits[name]

