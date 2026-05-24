from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_power_platform_toolchain_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_toolchain.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform and Power BI toolchain contract passed." in result.stdout


def test_power_platform_visual_contract_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_visual_contract.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform visual performance contract passed." in result.stdout


def test_github_actions_manifest_uses_official_power_platform_actions() -> None:
    manifest = _json(PP / "tooling" / "github-actions-manifest.json")
    assert manifest["githubActions"]["powerPlatform"]["provider"] == (
        "microsoft/powerplatform-actions"
    )
    assert "pack-solution@v1" in manifest["githubActions"]["powerPlatform"]["actions"]
    assert "checker@v1" in manifest["githubActions"]["powerPlatform"]["actions"]
    assert manifest["localCliTools"]["pbiviz"] == "installed"


def test_visual_contract_records_optimized_msapp_without_runtime_overclaim() -> None:
    contract = _json(
        PP / "apps" / "mchs-orchestration-app" / "visual-performance-contract.json"
    )
    assert contract["optimizedArtifact"]["sha256"] == (
        "9040d1d68f2f9183027cec7b7aa0322add56b437148355227ec66bf77dc3c4e7"
    )
    assert contract["claimBoundary"]["optimizedSourceGenerated"] is True
    assert contract["claimBoundary"]["optimizedMsappPacked"] is True
    assert contract["claimBoundary"]["optimizedAppPublished"] is True
    assert contract["claimBoundary"]["productionRuntimeReady"] is False
    assert contract["publication"]["appId"] == "669d0089-8abe-4e94-ab50-aa69513a6cc4"
