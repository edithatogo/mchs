from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from click.testing import CliRunner

from nwau_py.cli.main import cli
from nwau_py.source_scanner import (
    build_source_audit_package,
    scan_sources_dry_run,
    source_audit_package_to_json,
)

FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "source_scanner"
TRACK_ID = "ihacpa_source_license_audit_automation_20260703"
ISSUE_URL = "https://github.com/edithatogo/mchs/issues/209"
CONTRACT = Path("contracts/source-scanner/source-scanner.contract.json")


def _scan_manifest():
    return scan_sources_dry_run(
        html_documents=(FIXTURE_DIR / "nwau_scanner_listing.html",),
        source_page_url="https://www.ihacpa.gov.au/",
        pricing_year="2027",
    ).manifest


def test_source_audit_package_renders_review_only_drafts() -> None:
    package = build_source_audit_package(
        _scan_manifest(),
        track_id=TRACK_ID,
        github_issue_number=209,
        github_issue_url=ISSUE_URL,
    )
    rendered = json.loads(source_audit_package_to_json(package))

    assert rendered["track"]["metadata"]["track_class"] == "audit"
    assert rendered["track"]["metadata"]["github_issue_number"] == 209
    assert rendered["track"]["metadata"]["github_issue_url"] == ISSUE_URL
    assert f"[GitHub Issue]({ISSUE_URL})" in rendered["track"]["index"]
    assert rendered["github_issue"]["title"].startswith("chore:")
    body = rendered["github_issue"]["body"].lower()
    assert "restricted assets must never be copied" in body
    assert "box.com" not in body
    assert rendered["scan_manifest"]["pricing_year"] == "2027"


def test_source_audit_package_uses_custom_track_title() -> None:
    package = build_source_audit_package(
        _scan_manifest(),
        track_id=TRACK_ID,
        github_issue_url=ISSUE_URL,
        track_title="Custom Audit Track",
    )
    rendered = json.loads(source_audit_package_to_json(package))

    assert rendered["track"]["metadata"]["track_title"] == "Custom Audit Track"
    assert rendered["track"]["spec"].startswith("# Specification: Custom Audit Track")
    assert rendered["track"]["plan"].startswith("# Plan: Custom Audit Track")
    assert "Track title: Custom Audit Track" in rendered["github_issue"]["body"]


def test_sources_audit_cli_writes_drafts_and_emits_json(tmp_path) -> None:
    runner = CliRunner()
    output_dir = tmp_path / "audit"
    fixture = FIXTURE_DIR / "nwau_scanner_listing.html"

    result = runner.invoke(
        cast(Any, cli),
        [
            "sources",
            "audit",
            "--html-file",
            str(fixture),
            "--source-page-url",
            "https://www.ihacpa.gov.au/",
            "--year",
            "2027",
            "--track-id",
            TRACK_ID,
            "--issue-number",
            "209",
            "--issue-url",
            ISSUE_URL,
            "--write-dir",
            str(output_dir),
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["track"]["metadata"]["track_id"] == TRACK_ID
    assert (output_dir / "draft-manifest.json").exists()
    assert (output_dir / "conductor" / "tracks" / TRACK_ID / "metadata.json").exists()
    assert (output_dir / "conductor" / "tracks" / TRACK_ID / "spec.md").exists()
    assert (output_dir / "github-issue.md").exists()


def test_source_scanner_contract_includes_audit_command() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    commands = {command["name"]: command for command in contract["commands"]}

    assert "sources audit" in commands
    assert commands["sources audit"]["mode"] == "audit"
    assert "audit_package_format" in contract["outputs"]
