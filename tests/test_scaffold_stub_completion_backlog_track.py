from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "scaffold_stub_completion_backlog_20260524"
TRACK = ROOT / "conductor" / "tracks" / TRACK_ID
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / TRACK_ID
TRACKS = ROOT / "conductor" / "tracks.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_scaffold_stub_completion_backlog_tracks_overclaimed_completion_work():
    for path in [
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
        ROOT / "conductor" / "scripts" / "stub_detector.py",
    ]:
        assert path.exists(), path

    metadata = json.loads(_read(TRACK / "metadata.json"))
    tracks = _read(TRACKS)
    spec = _read(TRACK / "spec.md")
    plan = _read(TRACK / "plan.md")

    assert metadata["track_id"] == "scaffold_stub_completion_backlog_20260524"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["no_stub_enforce"] is True
    assert metadata["primary_contract"] == "conductor/no-stub-policy.md"

    assert "**Track: Scaffold and Stub Completion Backlog**" in tracks
    assert "Bring scaffold-only, stub-only, complete-with-gaps" in tracks

    for phrase in [
        "complete-with-gaps",
        "state mismatches",
        "implementation files",
        "validation command",
        "publication evidence",
    ]:
        assert phrase in spec

    for phrase in [
        "Capture the current no-stub detector baseline",
        "Fix current detector findings",
        "Create or update follow-on implementation tracks",
        "Wire the no-stub detector into the strict quality gate",
    ]:
        assert phrase in plan


def test_scaffold_stub_completion_backlog_names_current_detector_findings():
    plan = _read(TRACK / "plan.md")

    for track_id in [
        "mcp_server_registry_submission_20260516",
        "rust_core_ga_20260513",
        "rust_core_ga_post_cline_review_20260513",
    ]:
        assert track_id in plan
