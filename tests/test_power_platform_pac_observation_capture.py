from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "capture_power_platform_pac_observations.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("pac_observation_capture", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pac_observation_capture_blocks_without_required_values(tmp_path: Path) -> None:
    module = _load_module()
    output = tmp_path / "blocked.json"

    evidence = module.build_evidence(
        as_of="2026-05-21",
        app_id=None,
        play_url=None,
        connection_id=None,
    )
    module.write_evidence(output, evidence)

    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["status"] == "blocked_pending_required_pac_observations"
    assert saved["missingRequiredObservations"] == [
        "appId",
        "playUrl",
        "connectionId",
    ]
    assert saved["currentPacObservations"]["appPublication"]["status"] == "blocked"
    assert (
        saved["currentPacObservations"]["customConnectorConnection"]["status"]
        == "blocked"
    )
    assert saved["claimBoundary"]["appPublished"] is False
    assert saved["claimBoundary"]["productionReadinessClaimed"] is False


def test_pac_observation_capture_records_current_observations(tmp_path: Path) -> None:
    module = _load_module()
    output = tmp_path / "capture.json"

    evidence = module.build_evidence(
        as_of="2026-05-21",
        app_id="ff64f58a-73de-42ee-b92d-f65503619c49",
        play_url=(
            "https://apps.powerapps.com/play/e/611bca65-0b2a-eaa1-9e74-23bbba8eeec4/"
            "a/ff64f58a-73de-42ee-b92d-f65503619c49?tenantId=a687a7bf-02db-43df-"
            "bcbb-e7a8bda611a2"
        ),
        connection_id="0f3d6edc-9653-f111-bec6-00224893a0e1",
        app_name="MCHS Orchestration",
        connection_display_name="MCHS Service Boundary",
        connector_api_id="/providers/Microsoft.PowerApps/apis/new_mchs-20service-20boundary",
    )
    module.write_evidence(output, evidence)

    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["status"] == "captured_current_pac_observations"
    assert saved["missingRequiredObservations"] == []
    assert saved["currentPacObservations"]["appPublication"]["appId"] == (
        "ff64f58a-73de-42ee-b92d-f65503619c49"
    )
    assert saved["currentPacObservations"]["appPublication"]["status"] == "observed"
    assert (
        saved["currentPacObservations"]["customConnectorConnection"]["connectionId"]
        == "0f3d6edc-9653-f111-bec6-00224893a0e1"
    )
    assert (
        saved["currentPacObservations"]["customConnectorConnection"]["status"]
        == "observed"
    )
    assert saved["claimBoundary"]["appPublished"] is False
    assert saved["claimBoundary"]["connectionConfigured"] is False
    assert saved["claimBoundary"]["productionReadinessClaimed"] is False


def test_pac_observation_capture_cli_writes_output_file(tmp_path: Path) -> None:
    output = tmp_path / "cli.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--as-of",
            "2026-05-21",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["status"] == "blocked_pending_required_pac_observations"
    assert "appId" in saved["missingRequiredObservations"]
