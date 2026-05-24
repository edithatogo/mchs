from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks.md"
MATRIX = ROOT / "conductor" / "status-matrix.json"


LINK_RE = re.compile(r"\./tracks/([a-z0-9_]+_\d{8})/")


def _incomplete_tracks(text: str) -> set[str]:
    tracks: set[str] = set()
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "[ ]" not in line and "[~]" not in line:
            continue
        window = "\n".join(lines[index : index + 3])
        match = LINK_RE.search(window)
        if match:
            tracks.add(match.group(1))
    return tracks


def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    text = TRACKS.read_text(encoding="utf-8")
    incomplete = _incomplete_tracks(text)
    recorded = set(matrix["incompleteTracksFromIndex"])

    missing = sorted(incomplete - recorded)
    stale = sorted(recorded - incomplete)
    if missing:
        raise SystemExit(f"status matrix missing incomplete tracks: {missing}")
    if stale:
        raise SystemExit(f"status matrix has stale incomplete tracks: {stale}")
    boundary = matrix["portfolioClaimBoundary"]
    if boundary["allTracksImplemented"]:
        raise SystemExit("portfolio overclaims all tracks implemented")
    if boundary["allContractsProductionReady"]:
        raise SystemExit("portfolio overclaims contract production readiness")
    if boundary["allExternalRuntimeOutcomesProven"]:
        raise SystemExit("portfolio overclaims external runtime outcomes")

    print("Conductor status matrix passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
