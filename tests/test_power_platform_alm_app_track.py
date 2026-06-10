from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "power_platform_alm_app_20260510"
TRACKS = ROOT / "conductor" / "tracks.md"
POWER_PLATFORM = ROOT / "power-platform"
CONTRACT_ROOT = ROOT / "contracts" / "power-platform"
WORKFLOW = ROOT / ".github" / "workflows" / "power-platform-alm.yml"
VALIDATOR = ROOT / "scripts" / "validate_power_platform_capabilities.py"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_power_platform_alm_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        ROOT / "power-platform" / "solution" / "README.md",
        ROOT / "power-platform" / "solution" / "solution-manifest.md",
        ROOT / "power-platform" / "solution" / "environment-variables.md",
        ROOT / "power-platform" / "solution" / "connection-references.md",
        ROOT / "power-platform" / "solution" / "alm-workflow.md",
        ROOT / "power-platform" / "solution" / "app-surface.md",
        ROOT / "power-platform" / "solution" / "app-surface.json",
        ROOT / "power-platform" / "connectors" / "service-boundary-contract.md",
        ROOT / "power-platform" / "pipelines" / "README.md",
        WORKFLOW,
        CONTRACT_ROOT / "power-platform-binding.contract.json",
        CONTRACT_ROOT / "power-platform-binding.schema.json",
        CONTRACT_ROOT / "custom-connector.openapi.yaml",
        CONTRACT_ROOT / "calculator-capability-matrix.json",
        CONTRACT_ROOT / "examples" / "capabilities.pass.json",
        VALIDATOR,
    ]:
        assert path.exists(), path


def test_power_platform_alm_track_records_scope_and_requirements():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    track_index = _read_text(TRACK / "index.md")
    registry = _read_text(TRACKS)
    workflow = _read_text(WORKFLOW)
    alm_workflow = _read_text(POWER_PLATFORM / "solution" / "alm-workflow.md")
    pipelines_readme = _read_text(POWER_PLATFORM / "pipelines" / "README.md")
    app_surface = json.loads(_read_text(POWER_PLATFORM / "solution" / "app-surface.json"))

    assert metadata["track_id"] == "power_platform_alm_app_20260510"
    assert metadata["status"] in {"complete", "completed"}
    assert "Power Platform ALM app setup" in metadata["description"]

    for phrase in [
        "SOTA requirements review",
        "solution-based Power Platform ALM app",
        "orchestration-only",
        "managed environments",
        "Source control should remain the single source of truth",
        "Azure DevOps-oriented",
        "deprecated ALM Accelerator",
        "pac",
        "az",
        "pacx",
        "solution scaffold",
        "service-boundary contract",
        "Phase 3 Scaffold Contract",
    ]:
        assert phrase in spec

    for phrase in [
        "SOTA Requirements and ALM Architecture",
        "Toolchain and Environment Bootstrap",
        "Power Platform Solution and Orchestration App",
        "ALM Automation and Delivery",
        "Conductor - Automated Review and Checkpoint",
        (
            "via conductor-review, auto-fix, and auto-progress "
            "'Power Platform Solution and Orchestration App'"
        ),
        (
            "via conductor-review, auto-fix, and auto-progress "
            "'ALM Automation and Delivery'"
        ),
    ]:
        assert phrase in plan

    assert "power_platform_alm_app_20260510" in track_index
    assert "Power Platform ALM App Setup and Delivery" in registry
    assert "Power Platform Solution Scaffold" in track_index
    assert "ALM Workflow" in track_index

    for phrase in [
        "power-platform/solution/app-surface.json",
        "contracts/power-platform/calculator-capability-matrix.json",
        "scripts/validate_power_platform_capabilities.py",
        "tests/test_power_platform_binding_track.py",
    ]:
        assert phrase in workflow

    for phrase in [
        "capability matrix",
        "app-surface model",
        "connector contract",
        "pac solution checker",
        "external tenant gate",
    ]:
        assert phrase in alm_workflow
        assert phrase in pipelines_readme

    assert app_surface["data_sources"][0]["operations"] == [
        "listMchsCalculatorCapabilities",
        "validateMchsCalculatorInput",
        "runMchsCalculation",
    ]
