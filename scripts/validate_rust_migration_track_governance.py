from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"

EXPECTED_METADATA = {
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


def _metadata(track_id: str) -> dict[str, object]:
    path = TRACKS / track_id / "metadata.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    for track_id, expected in EXPECTED_METADATA.items():
        metadata = _metadata(track_id)
        for key, expected_value in expected.items():
            actual = metadata.get(key)
            if actual != expected_value:
                failures.append(
                    f"{track_id}: expected {key}={expected_value!r}, got {actual!r}"
                )

    if failures:
        raise SystemExit("\n".join(failures))

    print("Rust migration track governance passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
