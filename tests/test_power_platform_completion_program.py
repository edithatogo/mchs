from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def test_power_platform_static_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_static.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform static validation passed" in result.stdout


def test_solution_source_tree_has_real_solution_metadata() -> None:
    solution = PP / "solution" / "src" / "Other" / "Solution.xml"
    customizations = PP / "solution" / "src" / "customizations.xml"
    assert solution.exists()
    assert customizations.exists()
    root = ET.parse(solution).getroot()
    unique = root.find("./SolutionManifest/UniqueName")
    version = root.find("./SolutionManifest/Version")
    assert unique is not None
    assert unique.text == "mchs_alm_orchestration"
    assert version is not None
    assert version.text == "0.2.2.0"


def test_custom_connector_openapi_has_required_operations_and_security() -> None:
    spec = json.loads(
        (PP / "connectors" / "mchs-service-boundary" / "openapi.json").read_text()
    )
    operations = {
        operation["operationId"]
        for path in spec["paths"].values()
        for operation in path.values()
    }
    assert {
        "Health",
        "ListCalculators",
        "GetCalculatorSchema",
        "ValidateInput",
        "Calculate",
        "GetEvidence",
    } <= operations
    assert "apiKey" in spec["components"]["securitySchemes"]


def test_app_and_flows_are_orchestration_only() -> None:
    app = json.loads((PP / "apps" / "mchs-orchestration-app" / "app.json").read_text())
    assert app["type"] == "canvas-app-source-manifest"
    assert "No calculator formulas" in app["formulaLogicPolicy"]
    for flow_path in (PP / "flows").glob("*/flow.json"):
        flow = json.loads(flow_path.read_text())
        assert flow["connectionReference"] == "mchs_service_boundary"
        assert flow["storesPatientData"] is False
        assert flow["containsFormulaLogic"] is False


def test_deployment_evidence_claim_boundary_is_precise() -> None:
    status = json.loads((PP / "evidence" / "deployment-status.json").read_text())
    assert status["sourceReady"] is True
    assert status["managedSolutionImported"] is True
    assert status["nswDeploymentClaimed"] is True
    assert status["managedPromotionClaimed"] is True
    assert status["productionReadinessClaimed"] is False
    assert status["status"] == (
        "managed_solution_imported_optimized_app_and_pages_source_ready_pending_runtime_smoke"
    )
    assert "production service-boundary execution evidence" in status["missing"]
    assert "real Power App visual optimization evidence" not in status["missing"]
    page_runtime_blocker = (
        "Power App operation pages are source-UX complete but not live runtime-proven"
    )
    assert page_runtime_blocker in status["missing"]
    assert status["repoHealth"]["score"] == 9.5
    assert status["repoHealth"]["targetScoreCandidate"] == 9.9
    assert status["repoHealth"]["status"] == "healthy_with_runtime_smoke_blocker"
    assert status["subrepo"]["mode"] == "in_repository_governed_subrepo_boundary"


def test_power_platform_repo_health_and_subrepo_boundary() -> None:
    scorecard = json.loads(
        (PP / "repository" / "repo-health-scorecard.json").read_text()
    )
    manifest = json.loads((PP / "repository" / "subrepo-manifest.json").read_text())
    closure_path = PP / "repository" / "subrepo-closure-20260521.json"
    closure = json.loads(closure_path.read_text())
    roadmap = PP / "roadmap" / "sota-bleeding-edge-capabilities-20260520.md"

    assert scorecard["targetScore"] == 9.5
    assert scorecard["targetScoreCandidate"] == 9.9
    assert scorecard["score"] >= 9.5
    assert scorecard["status"] == "healthy_with_runtime_smoke_blocker"
    assert scorecard["health99Contract"] == (
        "power-platform/repository/health-9-9/contract.json"
    )
    assert manifest["claimBoundary"]["subrepoBoundaryEnforced"] is True
    assert manifest["claimBoundary"]["standaloneRemoteProvisioned"] is False
    assert manifest["claimBoundary"]["runtimeProductionReady"] is False
    assert manifest["closureRequirements"] == {
        "standaloneRemote": [
            "remoteUrl",
            "defaultBranch",
            "syncProcedure",
            "importOwner",
        ],
        "explicitWaiver": [
            "approvedBy",
            "approvalRecord",
            "reason",
            "reviewDate",
            "riskAcceptance",
        ],
    }
    assert (
        "record a fully populated standaloneRemote or explicitWaiver "
        "closure record before any 9.9 claim" in manifest["standaloneSplitRequirements"]
    )
    assert closure["status"] == "blocked_pending_remote_or_explicit_waiver"
    assert closure["claimBoundary"]["subrepoClosureComplete"] is False
    assert closure["standaloneRemote"]["remoteUrl"] is None
    assert closure["standaloneRemote"]["defaultBranch"] is None
    assert closure["standaloneRemote"]["syncProcedure"] is None
    assert closure["standaloneRemote"]["importOwner"] is None
    assert closure["waiver"]["approvedBy"] is None
    assert closure["waiver"]["approvalRecord"] is None
    assert closure["waiver"]["reviewDate"] is None
    assert closure["waiver"]["riskAcceptance"] is None
    assert roadmap.exists()


def test_power_platform_repo_health_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_repo_health.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform repo-health scorecard passed at 9.5 with 9.9 gate." in (
        result.stdout
    )
