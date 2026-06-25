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


TRACK = _track("release_workflow_validation_20260513")


def test_release_workflow_validation_track_records_concrete_evidence():
    metadata = json.loads((TRACK / "metadata.json").read_text(encoding="utf-8"))

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert ".github/workflows/release-rust.yml" in metadata["completion_evidence"]
    assert ".github/workflows/security.yml" in metadata["completion_evidence"]
    assert ".github/workflows/rust-ci.yml" in metadata["completion_evidence"]
    assert metadata["support_scope"]["runtime_support_claim"].startswith(
        "No runtime support"
    )


def test_release_workflows_wire_metadata_and_evidence_checks():
    release = (ROOT / ".github" / "workflows" / "release.yml").read_text(
        encoding="utf-8"
    )
    publish = (ROOT / ".github" / "workflows" / "publish.yml").read_text(
        encoding="utf-8"
    )
    rust_release = (
        ROOT / ".github" / "workflows" / "release-rust.yml"
    ).read_text(encoding="utf-8")

    assert "uv run python .github/scripts/validate_release_metadata.py" in release
    assert "uv run python .github/scripts/validate_release_metadata.py" in publish
    assert "release-evidence-bundle.json" in rust_release
    assert "Validate release evidence bundle fields" in rust_release
