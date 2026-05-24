from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_sota_capability_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_sota_capabilities.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform SOTA capability contracts passed." in result.stdout


def test_preview_capabilities_are_guarded_until_nsw_enablement() -> None:
    paths = [
        PP / "pipelines" / "native-pipelines-manifest.json",
        PP / "tests" / "playwright-smoke" / "manifest.json",
        PP / "apps" / "code-apps" / "evaluation-manifest.json",
        PP / "copilot" / "real-time-connector-knowledge.json",
        PP / "dataverse" / "mcp-server-readiness.json",
    ]
    for path in paths:
        manifest = _json(path)
        assert manifest["featureEnabled"] is False
        assert manifest["claimBoundary"]["productionReadinessClaimed"] is False


def test_agentic_observability_contract_covers_runtime_evidence() -> None:
    manifest = _json(PP / "governance" / "agentic-observability.json")
    fields = set(manifest["requiredEvidenceFields"])
    assert {
        "dlpPolicy",
        "connectorPolicy",
        "managedEnvironmentState",
        "solutionCheckerResult",
        "managedImportResult",
        "connectionReferenceMappings",
        "environmentVariableValues",
        "appHealthMetrics",
        "flowRunOutcomes",
        "agentIdentity",
        "leastPrivilegeRoleAssignment",
        "auditLogReference",
        "rollbackReference",
    } <= fields
    assert manifest["featureEnabled"] is True
    assert manifest["claimBoundary"]["tenantEvidenceCaptured"] is False


def test_code_apps_and_copilot_do_not_move_formula_logic_into_power_platform() -> None:
    code_apps = _json(PP / "apps" / "code-apps" / "evaluation-manifest.json")
    copilot = _json(PP / "copilot" / "real-time-connector-knowledge.json")
    assert "no calculator formulas in client code" in code_apps["guardrails"]
    assert "store calculator formulas in prompts" in " ".join(
        copilot["disallowedPatterns"]
    )
    assert copilot["knowledgeMode"] == "real_time_no_replication"
