from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"


def _metadata(track_id: str) -> dict[str, object]:
    return json.loads((TRACKS / track_id / "metadata.json").read_text())


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
