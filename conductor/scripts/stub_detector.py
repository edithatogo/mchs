#!/usr/bin/env python3
"""Run the workspace-level Conductor stub detector from this repository.

The canonical implementation is shared by projects in the parent Conductor
workspace. This wrapper keeps the documented repository-local command working
for agents and CI tasks that start from the project root.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    workspace_detector = (
        Path(__file__).resolve().parents[3]
        / "conductor"
        / "scripts"
        / "stub_detector.py"
    )
    if not workspace_detector.exists():
        print(
            f"Missing workspace stub detector: {workspace_detector}",
            file=sys.stderr,
        )
        return 2

    sys.argv[0] = str(workspace_detector)
    runpy.run_path(str(workspace_detector), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
