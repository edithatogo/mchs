from __future__ import annotations

import os
import subprocess
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bootstrap-power-platform-github-live-gate.sh"


def _write_fake_gh(path: Path, log: Path) -> None:
    repo_json = (
        '{"nameWithOwner":"octo/example",'
        '"defaultBranchRef":{"name":"main"}}'
    )
    secret_json = (
        '[{"name":"POWER_PLATFORM_ENVIRONMENT_URL"},'
        '{"name":"POWER_PLATFORM_APPLICATION_ID"},'
        '{"name":"POWER_PLATFORM_CLIENT_SECRET"},'
        '{"name":"POWER_PLATFORM_TENANT_ID"}]'
    )
    path.write_text(
        dedent(
            f"""\
            #!/usr/bin/env bash
            set -euo pipefail
            printf '%s\n' "$*" >> "{log!s}"
            case "$1 $2" in
              "repo view")
                printf '%s\n' '{repo_json}'
                ;;
              "secret list")
                printf '%s\n' '{secret_json}'
                ;;
              "workflow run")
                exit 0
                ;;
              *)
                printf 'unexpected gh invocation: %s\n' "$*" >&2
                exit 1
                ;;
            esac
            """
        ),
        encoding="utf-8",
    )
    path.chmod(0o755)


def _run_bootstrap(
    env_file: Path,
    tmp_path: Path,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    gh_log = tmp_path / "gh.log"
    gh = tmp_path / "gh"
    _write_fake_gh(gh, gh_log)

    env = os.environ.copy()
    env["PATH"] = f"{tmp_path}:{env['PATH']}"

    return subprocess.run(
        [str(SCRIPT), "--inputs-file", str(env_file), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_bootstrap_rejects_placeholder_operator_inputs_before_dispatch(tmp_path: Path):
    env_file = tmp_path / "github-live-gate.env"
    env_file.write_text(
        dedent(
            """\
            LIVE_GATE_WORKFLOW=publish.yml
            LIVE_GATE_TAG=v0.0.0
            NSW_OPERATOR_NAME=NSW operator name
            NSW_OPERATOR_EMAIL=operator@example.nsw.gov.au
            NSW_APPROVER_NAME=NSW approver name
            NSW_APPROVER_EMAIL=approver@example.nsw.gov.au
            NSW_RELEASE_REASON=Manual live-gate dispatch for GitHub release
            NSW_RELEASE_NOTES=Document the evidence bundle and approval reference
            GITHUB_TOKEN=provided_by_github_actions
            GH_TOKEN=provided_by_github_actions
            """
        ),
        encoding="utf-8",
    )

    result = _run_bootstrap(env_file, tmp_path)

    assert result.returncode != 0
    assert "placeholder value" in result.stderr
    assert "LIVE_GATE_TAG" in result.stderr


def test_bootstrap_dispatches_after_sanitized_inputs_and_secret_checks(tmp_path: Path):
    env_file = tmp_path / "github-live-gate.env"
    env_file.write_text(
        dedent(
            """\
            LIVE_GATE_WORKFLOW=publish.yml
            LIVE_GATE_TAG=v1.2.3
            NSW_OPERATOR_NAME=Alex Example
            NSW_OPERATOR_EMAIL=alex.example@nsw.gov.au
            NSW_APPROVER_NAME=Jordan Example
            NSW_APPROVER_EMAIL=jordan.example@nsw.gov.au
            NSW_RELEASE_REASON=Manual live-gate dispatch for release verification
            NSW_RELEASE_NOTES=Evidence bundle stored in the live-gate JSON
            GITHUB_TOKEN=provided_by_github_actions
            GH_TOKEN=provided_by_github_actions
            """
        ),
        encoding="utf-8",
    )

    result = _run_bootstrap(env_file, tmp_path, "--dispatch")

    assert result.returncode == 0
    assert "Operator inputs preflight passed." in result.stdout
    assert "All required repository secrets are present." in result.stdout
    assert "Workflow dispatch requested." in result.stdout
