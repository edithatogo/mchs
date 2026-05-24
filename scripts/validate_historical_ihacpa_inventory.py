"""Validate the historical IHACPA coverage audit contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "historical_ihacpa_coverage_20260512"
INVENTORY = TRACK / "historical_source_inventory.md"
MANIFEST = ROOT / "archive" / "ihacpa" / "raw" / "manifest.json"

FOUNDATIONAL_HASHES = {
    "460a69489e2bb4210203d35f5095851f8440d55b6a610afc1d580534c7f1983d",
    "0ef844f901347b13746d9b7cb27ab98f97fb303c93ed497e0f188b0e771c7e9c",
}


def _manifest_years() -> set[int]:
    records = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {
        int(record["year_start"])
        for record in records
        if record.get("status") in {"downloaded", "box-html-only"}
    }


def main() -> None:
    """Raise ``AssertionError`` if the historical audit contract drifts."""
    inventory = INVENTORY.read_text(encoding="utf-8")
    years = _manifest_years()

    if 2012 in years:
        raise AssertionError("2012-13 must remain an explicit calculator gap")
    if not set(range(2013, 2027)).issubset(years):
        raise AssertionError(
            "calculator manifest coverage must span 2013-14 through 2026-27"
        )

    for digest in FOUNDATIONAL_HASHES:
        if digest not in inventory:
            raise AssertionError(f"missing foundational 2012-13 hash {digest}")

    required_phrases = [
        "NEP determination",
        "Technical spec",
        "NWAU calculators",
        "Price weights",
        "NHCDC / cost evidence",
        "gap/unknown; no direct 2012-13 calculator artifact proven",
        "NHCDC materials are recorded as cost evidence only",
        "not calculator parity evidence",
    ]
    for phrase in required_phrases:
        if phrase not in inventory:
            raise AssertionError(f"missing historical audit phrase: {phrase}")


if __name__ == "__main__":
    main()
