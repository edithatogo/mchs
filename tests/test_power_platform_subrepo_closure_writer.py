from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "write_power_platform_subrepo_closure.py"


def _run_writer(
    *args: str, output: Path
) -> tuple[dict, subprocess.CompletedProcess[str]]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output", str(output), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(output.read_text(encoding="utf-8")), result


def test_writer_defaults_to_blocked_record(tmp_path: Path) -> None:
    output = tmp_path / "subrepo-closure.json"
    record, result = _run_writer(output=output)

    assert record["status"] == "blocked_pending_remote_or_explicit_waiver"
    assert record["selectedOption"] is None
    assert record["claimBoundary"]["subrepoClosureComplete"] is False
    assert record["standaloneRemote"]["remoteUrl"] is None
    assert record["waiver"]["approvedBy"] is None
    assert "blocked_pending_remote_or_explicit_waiver" in result.stdout


def test_writer_can_write_complete_standalone_remote_record(tmp_path: Path) -> None:
    output = tmp_path / "subrepo-closure.json"
    record, result = _run_writer(
        "standalone-remote",
        "--remote-url",
        "https://github.com/example/power-platform-subrepo.git",
        "--default-branch",
        "main",
        "--sync-procedure",
        "git pull --ff-only; git push",
        "--import-owner",
        "NSW import owner",
        output=output,
    )

    assert record["status"] == "standalone_remote_recorded"
    assert record["selectedOption"] == "standalone_remote"
    assert record["claimBoundary"] == {
        "standaloneRemoteProvisioned": True,
        "explicitWaiverRecorded": False,
        "subrepoClosureComplete": True,
    }
    assert record["standaloneRemote"] == {
        "provisioned": True,
        "remoteUrl": "https://github.com/example/power-platform-subrepo.git",
        "defaultBranch": "main",
        "syncProcedure": "git pull --ff-only; git push",
        "importOwner": "NSW import owner",
        "provisioningStatus": "provisioned",
    }
    assert record["waiver"]["required"] is False
    assert record["waiver"]["status"] == "not_required"
    assert record["waiver"]["approvedBy"] is None
    assert "standalone_remote_recorded" in result.stdout


def test_writer_can_write_complete_explicit_waiver_record(tmp_path: Path) -> None:
    output = tmp_path / "subrepo-closure.json"
    record, result = _run_writer(
        "explicit-waiver",
        "--approved-by",
        "NSW platform governance",
        "--approval-record",
        "GOV-2026-05-21-001",
        "--reason",
        "Standalone remote is deferred pending repository split approval.",
        "--review-date",
        "2026-05-21",
        "--risk-acceptance",
        "Accepted by product owner for current governed boundary.",
        output=output,
    )

    assert record["status"] == "explicit_waiver_recorded"
    assert record["selectedOption"] == "explicit_waiver"
    assert record["claimBoundary"] == {
        "standaloneRemoteProvisioned": False,
        "explicitWaiverRecorded": True,
        "subrepoClosureComplete": True,
    }
    assert record["standaloneRemote"]["remoteUrl"] is None
    assert record["standaloneRemote"]["provisioningStatus"] == "not_provisioned"
    assert record["waiver"] == {
        "required": True,
        "status": "recorded",
        "reason": "Standalone remote is deferred pending repository split approval.",
        "approvedBy": "NSW platform governance",
        "approvalRecord": "GOV-2026-05-21-001",
        "reviewDate": "2026-05-21",
        "riskAcceptance": "Accepted by product owner for current governed boundary.",
    }
    assert "explicit_waiver_recorded" in result.stdout


def test_writer_rejects_incomplete_explicit_waiver_input(tmp_path: Path) -> None:
    output = tmp_path / "subrepo-closure.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output",
            str(output),
            "explicit-waiver",
            "--approved-by",
            "NSW platform governance",
            "--approval-record",
            "GOV-2026-05-21-001",
            "--reason",
            "Standalone remote is deferred pending repository split approval.",
            "--review-date",
            "2026-05-21",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "--risk-acceptance" in result.stderr
    assert not output.exists()


def test_writer_rejects_placeholder_standalone_remote_input(tmp_path: Path) -> None:
    output = tmp_path / "subrepo-closure.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output",
            str(output),
            "standalone-remote",
            "--remote-url",
            "<remote-url>",
            "--default-branch",
            "main",
            "--sync-procedure",
            "git pull --ff-only; git push",
            "--import-owner",
            "NSW import owner",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "remote-url must be a complete value, not a placeholder" in result.stderr
    assert not output.exists()


def test_writer_rejects_placeholder_explicit_waiver_input(tmp_path: Path) -> None:
    output = tmp_path / "subrepo-closure.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output",
            str(output),
            "explicit-waiver",
            "--approved-by",
            "<approver>",
            "--approval-record",
            "GOV-2026-05-21-001",
            "--reason",
            "Standalone remote is deferred pending repository split approval.",
            "--review-date",
            "2026-05-21",
            "--risk-acceptance",
            "Accepted by product owner for current governed boundary.",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "approved-by must be a complete value, not a placeholder" in result.stderr
    assert not output.exists()
