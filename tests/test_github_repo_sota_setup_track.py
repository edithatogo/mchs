from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "github_repo_sota_setup_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_metadata() -> dict[str, Any]:
    return json.loads(_read(TRACK / "metadata.json"))


def test_github_repo_sota_archive_metadata_records_remote_evidence_boundary():
    metadata = _load_metadata()

    assert metadata["track_id"] == "github_repo_sota_setup_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")

    support_scope = metadata["support_scope"]
    assert support_scope["state"] == "complete-with-gaps"
    assert support_scope["implemented"] == [
        "remote repository metadata and homepage verified through gh",
        "labels verified through gh",
        "GitHub Pages configuration verified through gh",
        "master branch protection verified through gh",
        (
            "release, tag, workflow, and github-pages environment evidence "
            "verified through gh"
        ),
        "local workflow and tooling configuration evidence retained",
    ]
    assert support_scope["not_implemented"] == [
        "enabled Dependabot vulnerability alerts",
        "enabled GitHub secret scanning and push protection",
        "complete package registry publication proof for every planned ecosystem",
        "manual repository settings that GitHub does not expose to this token",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "deferred",
        "external-gate",
    }
    assert metadata["remote_evidence"]["repo"]["nameWithOwner"] == "edithatogo/mchs"
    assert metadata["remote_evidence"]["repo"]["homepageUrl"] == (
        "https://edithatogo.github.io/mchs/"
    )
    assert metadata["remote_evidence"]["pages"]["https_enforced"] is True
    assert metadata["remote_evidence"]["branch_protection"]["branch"] == "master"
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/github_repo_sota_setup_20260513/review.md"
    )


def test_github_repo_sota_plan_records_archive_review_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "metadata.json" in plan
    assert "plan.md" in plan
    assert "security and package publication gaps remain explicit" in plan


def test_github_repo_sota_registry_points_to_completed_archive():
    registry = _read(TRACKS)

    assert "- [x] **Track: GitHub Repository SOTA Setup**" in registry
    assert "./archive/github_repo_sota_setup_20260513/" in registry
    assert "./tracks/github_repo_sota_setup_20260513/" not in registry
