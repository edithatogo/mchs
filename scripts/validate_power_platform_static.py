#!/usr/bin/env python3
"""Static validation for the Power Platform ALM source tree."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"
REQUIRED_PATHS = [
    PP / "README.md",
    PP / "repository" / "subrepo-contract.md",
    PP / "settings" / "solution-settings.json",
    PP / "connectors" / "service-boundary-contract.md",
    PP / "solution" / "README.md",
    PP / "solution" / "src",
    PP / "pipelines" / "README.md",
    PP / "evidence" / "README.md",
]
FORBIDDEN_TERMS = [
    "patient_name",
    "medicare_number",
    "ihacpa secret",
]
FORMULA_MARKERS = [
    "PW x APaed",
    "AICU x ICU hours",
    "Power Fx formula implementation",
]


def fail(message: str) -> None:
    print(f"[power-platform-static][ERROR] {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    for path in REQUIRED_PATHS:
        if not path.exists():
            fail(f"missing required path: {path.relative_to(ROOT)}")

    settings = json.loads((PP / "settings" / "solution-settings.json").read_text())
    if settings["solutionUniqueName"] != "mchs_alm_orchestration":
        fail("unexpected solutionUniqueName")
    if "mchs_service_boundary" not in settings.get("connectionReferences", []):
        fail("missing mchs_service_boundary connection reference")

    for path in PP.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for term in FORBIDDEN_TERMS:
            if term in text:
                relative = path.relative_to(ROOT)
                fail(f"forbidden private-data marker {term!r} in {relative}")
        raw = path.read_text(encoding="utf-8", errors="ignore")
        for marker in FORMULA_MARKERS:
            if marker in raw:
                fail(f"forbidden formula marker {marker!r} in {path.relative_to(ROOT)}")

    print("Power Platform static validation passed")


if __name__ == "__main__":
    main()
