from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"


def _metadata(track_id: str) -> dict[str, object]:
    return json.loads((TRACKS / track_id / "metadata.json").read_text())


def _text(track_id: str, filename: str) -> str:
    return (TRACKS / track_id / filename).read_text()


def test_rust_migration_tracks_have_normalized_metadata() -> None:
    expectations = {
        "rust_cli_core_migration_20260703": {
            "track_class": "binding",
            "current_state": "roadmap-only",
            "publication_status": "published-with-gaps",
        },
        "rust_mcp_core_migration_20260703": {
            "track_class": "binding",
            "current_state": "roadmap-only",
            "publication_status": "published-with-gaps",
        },
        "rust_cli_mcp_promotion_evidence_20260703": {
            "track_class": "validator",
            "current_state": "roadmap-only",
            "publication_status": "future-only",
        },
    }

    for track_id, expected in expectations.items():
        metadata = _metadata(track_id)
        for key, value in expected.items():
            assert metadata.get(key) == value, (track_id, key, metadata.get(key))


def test_rust_migration_governance_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_rust_migration_track_governance.py"],
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout


def test_cli_migration_track_pins_runtime_selection_contract() -> None:
    spec = _text("rust_cli_core_migration_20260703", "spec.md")
    plan = _text("rust_cli_core_migration_20260703", "plan.md")
    combined = f"{spec}\n{plan}"

    assert "--runtime python|rust|auto" in combined
    assert "default runtime remains `python`" in combined
    assert "NWAU_RUNTIME" in combined
    assert "explicit CLI `--runtime` option takes precedence" in combined
    assert "fail closed" in combined
