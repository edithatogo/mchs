from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOLUTION_DIR = ROOT / "power-platform" / "solution"
APPS_DIR = ROOT / "power-platform" / "apps"
FLOWS_DIR = ROOT / "power-platform" / "flows"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_power_platform_solution_slice_has_source_control_assets() -> None:
    solution_manifest = _read_json(SOLUTION_DIR / "source-controlled-metadata.json")
    app_manifest = _read_json(
        APPS_DIR / "mchs-orchestrator" / "app-surface-manifest.json"
    )
    flow_definition = _read_json(FLOWS_DIR / "mchs-submit-calculation.json")

    assert solution_manifest["solution"]["id"] == "mchs_alm_orchestration"
    assert (SOLUTION_DIR / "solution-manifest.md").exists()
    assert (SOLUTION_DIR / "app-surface.md").exists()
    assert (SOLUTION_DIR / "alm-workflow.md").exists()

    components = solution_manifest["solution"]["components"]
    assert components["apps"][0]["path"] == "power-platform/apps/mchs-orchestrator"
    assert (
        components["flows"][0]["path"]
        == "power-platform/flows/mchs-submit-calculation.json"
    )
    assert (
        components["environmentVariables"]["path"]
        == "power-platform/solution/environment-variables.json"
    )
    assert (
        components["connectionReferences"]["path"]
        == "power-platform/solution/connection-references.json"
    )

    assert app_manifest["app"]["appType"] in {"model-driven", "canvas"}
    assert app_manifest["app"]["flowBindings"] == ["mchs-submit-calculation"]
    assert flow_definition["flow"]["name"] == "mchs-submit-calculation"
    assert flow_definition["flow"]["connections"] == [
        "mchs_service_boundary",
        "mchs_solution_checker",
    ]


def test_power_platform_app_flow_contract_is_end_to_end() -> None:
    env_vars = _read_json(SOLUTION_DIR / "environment-variables.json")[
        "environmentVariables"
    ]
    env_names = {entry["name"] for entry in env_vars}
    connection_refs = {
        entry["name"]
        for entry in _read_json(SOLUTION_DIR / "connection-references.json")[
            "connectionReferences"
        ]
    }
    app_manifest = _read_json(
        APPS_DIR / "mchs-orchestrator" / "app-surface-manifest.json"
    )
    flow_definition = _read_json(FLOWS_DIR / "mchs-submit-calculation.json")

    assert {
        "mchs_api_base_url",
        "mchs_api_contract_version",
        "mchs_api_calculator_id",
        "mchs_api_pricing_year",
    }.issubset(env_names)

    assert {
        "mchs_service_boundary",
        "mchs_solution_checker",
    }.issubset(connection_refs)

    assert set(app_manifest["app"]["environmentVariableRefs"]) == {
        "mchs_api_base_url",
        "mchs_api_contract_version",
        "mchs_api_calculator_id",
        "mchs_api_pricing_year",
    }
    assert set(app_manifest["app"]["connectionReferenceRefs"]) == connection_refs

    assert flow_definition["flow"]["contract"]["requiredFields"] == [
        "status",
        "result",
        "warnings",
        "trace_id",
    ]
