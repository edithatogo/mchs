from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _track(track_id: str) -> Path:
    for base in (ROOT / "conductor" / "tracks", ROOT / "conductor" / "archive"):
        candidate = base / track_id
        if candidate.exists():
            return candidate
    raise AssertionError(f"missing Conductor track or archive: {track_id}")


TRACK = _track("track_archive_integrity_20260513")


def test_track_archive_policy_defines_eligibility_and_required_record():
    policy = (ROOT / "conductor" / "track-archive-policy.md").read_text(
        encoding="utf-8"
    )

    assert "Archive Eligibility" in policy
    assert "Do Not Archive" in policy
    assert "Required Archive Record" in policy
    assert "final review or verification report" in policy
    assert "conductor/tracks.md" in policy
    assert "archive path" in policy


def test_track_archive_integrity_metadata_points_to_policy_and_review():
    metadata = json.loads((TRACK / "metadata.json").read_text(encoding="utf-8"))

    assert metadata["track_id"] == "track_archive_integrity_20260513"
    assert metadata["primary_contract"] == "conductor/track-archive-policy.md"
    assert "conductor/track-archive-policy.md" in metadata["completion_evidence"]
    assert metadata["support_scope"]["local_completion"].startswith(
        "The archive policy"
    )
    assert (TRACK / "review.md").exists()
