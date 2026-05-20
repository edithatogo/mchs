from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contracts" / "release" / "evidence-bundle.schema.json"
BUNDLE = (
    ROOT
    / "power-platform"
    / "evidence"
    / "nsw-operational-readiness-bundle-template.json"
)
RUNBOOK = (
    ROOT / "power-platform" / "deployment" / "nsw-managed-solution-promotion-runbook.md"
)
READINESS = (
    ROOT / "power-platform" / "deployment" / "nsw-deployment-readiness-template.md"
)
GOVERNANCE = ROOT / "power-platform" / "governance" / "nsw-power-platform-governance.md"
RUNTIME_SMOKE = (
    ROOT / "power-platform" / "evidence" / "runtime-smoke-evidence-template.json"
)
CONNECTIONS = (
    ROOT / "power-platform" / "evidence" / "connection-reference-evidence-template.json"
)
MONITORING = (
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-evidence-template.json"
)
FLOW_SMOKE_TEMPLATE = (
    ROOT / "power-platform" / "evidence" / "flow-smoke-evidence-template.json"
)
FLOW_SMOKE_EVIDENCE = (
    ROOT / "power-platform" / "evidence" / "power-automate-flow-smoke-20260521.json"
)
ENDPOINT = ROOT / "power-platform" / "evidence" / (
    "service-boundary-endpoint-template.json"
)
GITHUB_LIVE_GATE_TEMPLATE = (
    ROOT
    / "power-platform"
    / "evidence"
    / "official-github-live-gate-evidence-template.json"
)
GITHUB_LIVE_GATE = ROOT / "power-platform" / "evidence" / (
    "github-live-gate-20260521.json"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _required_fields(schema: dict) -> set[str]:
    return set(schema.get("required", []))


def test_power_platform_evidence_bundle_contains_required_fields_and_blockers():
    schema = _json(SCHEMA)
    bundle = _json(BUNDLE)

    for field in _required_fields(schema):
        assert field in bundle, f"Missing required evidence field: {field}"

    bundle_limitations = "\n".join(bundle.get("known_limitations", []))
    for blocker in [
        "service_boundary_production_endpoint_missing",
        "connection_reference_values_missing",
        "real_dataverse_app_component_smoke_missing",
        "real_power_automate_flow_component_smoke_missing",
    ]:
        assert blocker in bundle_limitations

    assert bundle["coverage"]["threshold"] >= 0.0
    assert bundle["coverage"]["actual"] >= 0.0


def test_power_platform_artifacts_state_no_live_nsw_claim():
    for path in [RUNBOOK, READINESS, GOVERNANCE]:
        text = _text(path).lower()
        assert "do not claim" in text


def test_power_platform_evidence_templates_exist():
    for path in [
        RUNBOOK,
        READINESS,
        GOVERNANCE,
        BUNDLE,
        RUNTIME_SMOKE,
        CONNECTIONS,
        MONITORING,
        FLOW_SMOKE_TEMPLATE,
        FLOW_SMOKE_EVIDENCE,
        ENDPOINT,
        GITHUB_LIVE_GATE_TEMPLATE,
        GITHUB_LIVE_GATE,
    ]:
        assert path.exists(), path


def test_power_platform_operational_evidence_contracts_are_precise():
    runtime = _json(RUNTIME_SMOKE)
    connections = _json(CONNECTIONS)
    monitoring = _json(MONITORING)
    flow_smoke = _json(FLOW_SMOKE_TEMPLATE)
    flow_smoke_evidence = _json(FLOW_SMOKE_EVIDENCE)

    assert runtime["claimBoundary"]["runtimeSmokePassed"] is False
    assert runtime["claimBoundary"]["productionReadinessClaimed"] is False
    assert connections["claimBoundary"]["connectionsConfigured"] is False
    assert monitoring["claimBoundary"]["monitoringConfigured"] is False
    assert monitoring["claimBoundary"]["dlpEvidenceCaptured"] is False
    live_gate_template = _json(GITHUB_LIVE_GATE_TEMPLATE)
    live_gate = _json(GITHUB_LIVE_GATE)
    assert live_gate_template["requiredSecrets"] == [
        "POWER_PLATFORM_ENVIRONMENT_URL",
        "POWER_PLATFORM_APPLICATION_ID",
        "POWER_PLATFORM_CLIENT_SECRET",
        "POWER_PLATFORM_TENANT_ID",
    ]
    assert live_gate_template["requiredSecretChecks"] == [
        {
            "name": "POWER_PLATFORM_ENVIRONMENT_URL",
            "source": "repository secret",
            "check": "gh secret list",
            "observed": False,
        },
        {
            "name": "POWER_PLATFORM_APPLICATION_ID",
            "source": "repository secret",
            "check": "gh secret list",
            "observed": False,
        },
        {
            "name": "POWER_PLATFORM_CLIENT_SECRET",
            "source": "repository secret",
            "check": "gh secret list",
            "observed": False,
        },
        {
            "name": "POWER_PLATFORM_TENANT_ID",
            "source": "repository secret",
            "check": "gh secret list",
            "observed": False,
        },
    ]
    assert live_gate_template["workflowDispatchInputs"] == {
        "workflowFile": ".github/workflows/power-platform-official-actions.yml",
        "event": "workflow_dispatch",
        "inputs": {
            "run_live_checks": {
                "type": "boolean",
                "required": True,
                "expected": True,
            },
            "workflow": {
                "type": "string",
                "required": True,
                "expected": "Power Platform Official Actions",
            },
            "trigger": {
                "type": "string",
                "required": True,
                "expected": "workflow_dispatch",
            },
        },
    }
    assert "workflow run URL" in live_gate_template["requiredGateEvidence"]
    assert (
        "who-am-i target environment output"
        in live_gate_template["requiredGateEvidence"]
    )
    assert "solution checker result" in live_gate_template["requiredGateEvidence"]
    assert (
        "packed managed solution artifact hash"
        in live_gate_template["requiredGateEvidence"]
    )
    assert live_gate_template["claimBoundary"]["officialLiveGateCompleted"] is False
    assert live_gate["status"] == "blocked_pending_repository_secrets_and_workflow_run"
    assert live_gate["workflowDispatchInputs"] == {
        "workflowFile": ".github/workflows/power-platform-official-actions.yml",
        "event": "workflow_dispatch",
        "inputs": {
            "run_live_checks": {
                "type": "boolean",
                "required": True,
                "expected": True,
            },
            "workflow": {
                "type": "string",
                "required": True,
                "expected": "Power Platform Official Actions",
            },
            "trigger": {
                "type": "string",
                "required": True,
                "expected": "workflow_dispatch",
            },
        },
    }
    assert live_gate["run"]["status"] == "not_run"
    assert live_gate["run"]["runUrl"] is None
    assert (
        live_gate["run"]["runUrlPattern"]
        == r"^https://github\.com/[^/]+/[^/]+/actions/runs/\d+$"
    )
    assert live_gate["run"]["whoAmI"] == "not_run"
    assert live_gate["run"]["solutionChecker"]["result"] == "not_run"
    assert live_gate["run"]["solutionChecker"]["command"] == "pac solution checker run"
    assert live_gate["run"]["solutionArtifactSha256"] is None
    assert live_gate["run"]["solutionArtifactEvidence"] == {
        "path": "dist/power-platform/mchs_alm_orchestration_managed.zip",
        "hashAlgorithm": "sha256",
        "hashPattern": r"^[a-f0-9]{64}$",
        "hashCommand": (
            "sha256sum dist/power-platform/mchs_alm_orchestration_managed.zip"
        ),
    }
    assert live_gate["claimBoundary"]["officialLiveGatePassed"] is False
    assert live_gate["claimBoundary"]["productionDeploymentSecretsConfigured"] is False
    assert flow_smoke["claimBoundary"]["flowSmokePassed"] is False
    assert flow_smoke_evidence["claimBoundary"]["flowSmokePassed"] is False
    assert all(entry["flowId"] is None for entry in flow_smoke["realNswRunEvidence"])
    assert all(
        entry["runId"] is None for entry in flow_smoke_evidence["realNswRunEvidence"]
    )
    assert all(
        "connectionReference" in item["requiredEvidence"]
        for item in flow_smoke["flowSmokeChecklist"]
    )
    assert all(
        "connectionReferenceId" in item["requiredEvidence"]
        for item in flow_smoke["flowSmokeChecklist"]
    )
    assert monitoring["dlp"]["policyId"]
    assert monitoring["dlp"]["policyName"]
    assert monitoring["dlp"]["policyClassification"]
    assert monitoring["connectorPolicy"]["policyId"]
    assert monitoring["connectorPolicy"]["policyName"]
    assert monitoring["connectorPolicy"]["connectorAllowState"]
    assert monitoring["monitoring"]["owner"]
    assert monitoring["monitoring"]["failureMetrics"]["connectorFailures"]
    assert monitoring["support"]["owner"]
    assert monitoring["support"]["escalationOwner"]
    assert monitoring["support"]["escalationPath"]
    assert monitoring["support"]["escalationContact"]


def test_power_platform_operational_evidence_validator_passes():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_operational_evidence.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform operational evidence contracts passed." in result.stdout


def test_power_platform_repo_health_9_9_gate_validator_passes():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_repo_health.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert (
        "Power Platform repo-health scorecard passed at 9.5 with 9.9 gate."
        in result.stdout
    )


def test_power_platform_github_live_gate_validator_passes():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_github_live_gate.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform official GitHub live-gate evidence contract passed." in (
        result.stdout
    )
