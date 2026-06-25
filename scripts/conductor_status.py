#!/usr/bin/env python3
"""
Conductor Status - MCHS project track status report.

Reads all track metadata.json files and the tracks.md ledger to produce
a summary of every conductor track, its current state, status, class,
publication readiness, and last-updated timestamp.

Usage:
    python scripts/conductor_status.py
    python scripts/conductor_status.py --verbose
    python scripts/conductor_status.py --json
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONDUCTOR = ROOT / "conductor"
TRACKS_DIR = CONDUCTOR / "tracks"
TRACKS_MD = CONDUCTOR / "tracks.md"
ARCHIVE_DIR = CONDUCTOR / "archive"


def read_metadata(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def parse_tracks_md(path: Path) -> dict[str, bool]:
    ledger: dict[str, bool] = {}
    if not path.exists():
        return ledger
    text = path.read_text()
    p = re.compile(
        r"- \[([ x])\]\s+\*\*Track:\s*.+?\*\*\s*\n.*?\[\./tracks/([^/]+)/?\]",
        re.MULTILINE,
    )
    for m in p.finditer(text):
        ledger[m.group(2)] = m.group(1) == "x"
    ap = re.compile(
        r"- \[([ x])\]\s+\*\*Track:\s*.+?\*\*\s*\n.*?\[\./archive/([^/]+)/?\]",
        re.MULTILINE,
    )
    for m in ap.finditer(text):
        ledger[m.group(2)] = m.group(1) == "x"
    return ledger


def collect_tracks() -> list[dict]:
    ledger = parse_tracks_md(TRACKS_MD)
    rows: list[dict] = []
    for base, archived in [(TRACKS_DIR, False), (ARCHIVE_DIR, True)]:
        if not base.exists():
            continue
        for track_dir in sorted(path for path in base.iterdir() if path.is_dir()):
            metadata = read_metadata(track_dir / "metadata.json")
            track_id = metadata.get("track_id", track_dir.name)
            rows.append(
                {
                    "track_id": track_id,
                    "archived": archived,
                    "ledger_complete": ledger.get(track_id),
                    "status": metadata.get("status"),
                    "current_state": metadata.get("current_state"),
                    "track_class": metadata.get("track_class"),
                    "publication_status": metadata.get("publication_status"),
                    "updated_at": metadata.get("updated_at"),
                    "path": track_dir.relative_to(ROOT).as_posix(),
                }
            )
    return rows


def summarize(rows: list[dict]) -> dict:
    summary: dict[str, int] = {
        "total": len(rows),
        "archived": sum(1 for row in rows if row["archived"]),
        "active": sum(1 for row in rows if not row["archived"]),
    }
    for field in ["status", "current_state", "track_class", "publication_status"]:
        for row in rows:
            value = row.get(field) or "unset"
            key = f"{field}:{value}"
            summary[key] = summary.get(key, 0) + 1
    return summary


def print_table(rows: list[dict], verbose: bool) -> None:
    print(f"{'track_id':58} {'loc':8} {'status':14} {'state':24} {'class':14} publication")
    print("-" * 132)
    for row in rows:
        loc = "archive" if row["archived"] else "active"
        print(
            f"{row['track_id'][:58]:58} "
            f"{loc:8} "
            f"{str(row.get('status') or 'unset')[:14]:14} "
            f"{str(row.get('current_state') or 'unset')[:24]:24} "
            f"{str(row.get('track_class') or 'unset')[:14]:14} "
            f"{row.get('publication_status') or 'unset'}"
        )
        if verbose:
            print(f"  path: {row['path']}")
            print(f"  ledger_complete: {row['ledger_complete']}")


def main(argv: list[str]) -> int:
    emit_json = "--json" in argv
    verbose = "--verbose" in argv
    unknown = [
        arg for arg in argv if arg not in {"--json", "--verbose", "-h", "--help"}
    ]
    if "-h" in argv or "--help" in argv:
        print(__doc__.strip())
        return 0
    if unknown:
        print(f"Unknown argument(s): {', '.join(unknown)}", file=sys.stderr)
        return 2

    rows = collect_tracks()
    payload = {"summary": summarize(rows), "tracks": rows}
    if emit_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_table(rows, verbose=verbose)
        print()
        print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
