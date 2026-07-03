from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"
ARCHIVE = ROOT / "conductor" / "archive"

EXPECTED_METADATA = {
    "rust_cli_core_migration_20260703": {
        "track_class": "binding",
        "current_state": {"roadmap-only", "implemented-awaiting-review", "archived"},
        "publication_status": "published-with-gaps",
    },
    "rust_mcp_core_migration_20260703": {
        "track_class": "binding",
        "current_state": {"roadmap-only", "implemented-awaiting-review", "archived"},
        "publication_status": "published-with-gaps",
    },
    "rust_cli_mcp_promotion_evidence_20260703": {
        "track_class": "validator",
        "current_state": {"roadmap-only", "implemented-awaiting-review", "archived"},
        "publication_status": "future-only",
    },
}

REQUIRED_TEXT = {
    "rust_cli_core_migration_20260703": {
        "spec.md": (
            "--runtime python|rust|auto",
            "default runtime remains `python`",
            "NWAU_RUNTIME",
            "first Rust-backed implementation slice",
            "existing Rust canary/kernel evidence",
        ),
        "plan.md": (
            "Contract Hardening Pre-Phase",
            "numeric tolerance and rounding policy",
            "schema parity source",
            "unsupported diagnostic codes",
            "support-status wording",
        ),
    },
    "rust_mcp_core_migration_20260703": {
        "spec.md": (
            "Python stdio transport",
            "formula runtime",
            "Rust-backed dispatcher",
            "must not shell out to the CLI",
            "first Rust-backed implementation slice",
            "existing Rust canary/kernel evidence",
        ),
        "plan.md": (
            "Contract Hardening Pre-Phase",
            "numeric tolerance and rounding policy",
            "schema parity source",
            "unsupported diagnostic codes",
            "support-status wording",
            "must not shell out to the CLI",
        ),
    },
}


def _track_root(track_id: str) -> Path:
    active = TRACKS / track_id
    if active.exists():
        return active
    return ARCHIVE / track_id


def _metadata(track_id: str) -> dict[str, object]:
    path = _track_root(track_id) / "metadata.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _track_text(track_id: str, filename: str) -> str:
    return (_track_root(track_id) / filename).read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    for track_id, expected in EXPECTED_METADATA.items():
        metadata = _metadata(track_id)
        for key, expected_value in expected.items():
            actual = metadata.get(key)
            if isinstance(expected_value, set):
                matches = actual in expected_value
            else:
                matches = actual == expected_value
            if not matches:
                failures.append(
                    f"{track_id}: expected {key}={expected_value!r}, got {actual!r}"
                )

    for track_id, files in REQUIRED_TEXT.items():
        for filename, snippets in files.items():
            text = _track_text(track_id, filename)
            failures.extend(
                f"{track_id}/{filename}: missing required text {snippet!r}"
                for snippet in snippets
                if snippet not in text
            )

    if failures:
        raise SystemExit("\n".join(failures))

    print("Rust migration track governance passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
