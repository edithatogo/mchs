from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_every_connector_operation_has_source_controlled_page() -> None:
    coverage = _json(
        PP / "apps" / "mchs-orchestration-app" / "page-function-coverage.json"
    )
    operations = {
        operation["operationId"]: operation
        for operation in coverage["operationCoverage"]
    }
    assert set(operations) == {
        "Health",
        "ListCalculators",
        "GetCalculatorSchema",
        "ValidateInput",
        "Calculate",
        "GetEvidence",
    }
    for operation in operations.values():
        assert (ROOT / operation["source"]).exists()
        assert operation["sourceControlled"] is True
        assert operation["complete"] is False
        assert operation["runtimeSmokeStatus"] == (
            "blocked_pending_service_endpoint_and_connection_reference"
        )


def test_page_function_coverage_does_not_overclaim_completion() -> None:
    coverage = _json(
        PP / "apps" / "mchs-orchestration-app" / "page-function-coverage.json"
    )
    assert coverage["homeScreen"]["complete"] is True
    assert coverage["completionGate"]["allOperationPagesSourceControlled"] is True
    assert coverage["completionGate"]["allOperationPagesUxComplete"] is False
    assert coverage["completionGate"]["allOperationRuntimeSmokePassed"] is False
    assert coverage["completionGate"]["allCalculationsFullyImplementedInApp"] is False
    assert coverage["claimBoundary"]["repoHealth99Eligible"] is False
    assert coverage["claimBoundary"]["productionReadinessClaimed"] is False


def test_repo_health_99_contract_is_blocked_until_live_evidence() -> None:
    contract = _json(PP / "repository" / "health-9-9" / "contract.json")
    assert contract["targetScore"] == 9.9
    assert contract["currentScore"] == 9.5
    assert contract["status"] == "not_eligible_runtime_and_page_completion_blocked"
    assert {gate["gate"] for gate in contract["requiredGates"]} == {
        "all_connector_operation_pages_complete",
        "live_service_boundary_health_validate_calculate_evidence",
        "real_power_automate_flow_smoke",
        "dlp_monitoring_and_connector_policy_evidence",
        "official_github_actions_live_gate_run",
        "standalone_power_platform_subrepo_remote_or_explicit_waiver",
    }
    assert all(gate["status"] == "blocked" for gate in contract["requiredGates"])
    assert contract["claimBoundary"]["score99Claimed"] is False


def test_page_function_coverage_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_page_function_coverage.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        "Power Platform page/function coverage and 9.9 contract passed."
        in result.stdout
    )
