from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_conductor_status_matrix_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_conductor_status_matrix.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Conductor status matrix passed." in result.stdout


def test_conductor_status_matrix_does_not_overclaim_completion() -> None:
    matrix = json.loads((ROOT / "conductor" / "status-matrix.json").read_text())
    boundary = matrix["portfolioClaimBoundary"]
    assert boundary["allTracksImplemented"] is False
    assert boundary["allContractsProductionReady"] is False
    assert boundary["allExternalRuntimeOutcomesProven"] is False
    assert (
        "power_platform_operational_evidence_20260518"
        in matrix["incompleteTracksFromIndex"]
    )
