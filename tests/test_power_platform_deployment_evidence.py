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
PAC_RUNBOOK = ROOT / "power-platform" / "deployment" / "pac-operator-runbook.md"
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
PAC_OPERATOR_PACKAGE = (
    ROOT / "power-platform" / "evidence" / "pac-operator-package-20260521.json"
)
MONITORING = (
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-evidence-template.json"
)
MONITORING_RUNBOOK = (
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-operator-runbook.md"
)
MONITORING_SAMPLE = (
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-capture-sample.json"
)
FLOW_SMOKE_TEMPLATE = (
    ROOT / "power-platform" / "evidence" / "flow-smoke-evidence-template.json"
)
FLOW_SMOKE_RUNBOOK = (
    ROOT / "power-platform" / "evidence" / "flow-smoke-capture-runbook.md"
)
FLOW_SMOKE_SAMPLE_CAPTURE = (
    ROOT / "power-platform" / "evidence" / "flow-smoke-capture-sample.json"
)
FLOW_SMOKE_EVIDENCE = (
    ROOT / "power-platform" / "evidence" / "power-automate-flow-smoke-20260521.json"
)
ENDPOINT = (
    ROOT / "power-platform" / "evidence" / ("service-boundary-endpoint-template.json")
)
GITHUB_LIVE_GATE_TEMPLATE = (
    ROOT
    / "power-platform"
    / "evidence"
    / "official-github-live-gate-evidence-template.json"
)
GITHUB_LIVE_GATE = (
    ROOT / "power-platform" / "evidence" / ("github-live-gate-20260521.json")
)
REMAINING_BLOCKERS = (
    ROOT / "power-platform" / "evidence" / "remaining-blockers-20260521.json"
)
EVIDENCE_README = ROOT / "power-platform" / "evidence" / "README.md"
REPO_HEALTH_SCORECARD = (
    ROOT / "power-platform" / "repository" / "repo-health-scorecard.json"
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
    for path in [RUNBOOK, PAC_RUNBOOK, READINESS, GOVERNANCE]:
        text = _text(path).lower()
        assert "do not claim" in text


def test_power_platform_remaining_blocker_ids_are_documented():
    remaining = _json(REMAINING_BLOCKERS)
    blocker_ids = [blocker["id"] for blocker in remaining["remainingBlockers"]]

    documented_surfaces = [_text(EVIDENCE_README)]
    for directory in [
        ROOT / "docs" / "runbooks",
        ROOT / "power-platform" / "deployment",
    ]:
        documented_surfaces.extend(
            _text(path) for path in sorted(directory.glob("*.md"))
        )

    documented_text = "\n".join(documented_surfaces)
    for blocker_id in blocker_ids:
        assert blocker_id in documented_text, blocker_id


def test_power_platform_deployment_readiness_roadmap_documents_local_only_preflight():
    text = _text(ROOT / "docs" / "roadmaps" / "power-platform-deployment-readiness.md")
    lowered = text.lower()

    assert "aggregate-readiness-preflight" in lowered
    assert "local-only" in lowered
    assert "validate_power_platform_repo_health.py" in lowered
    assert "validate_power_platform_github_live_gate.py" in lowered
    assert "dispatch live workflows" in lowered


def test_power_platform_evidence_templates_exist():
    for path in [
        RUNBOOK,
        PAC_RUNBOOK,
        READINESS,
        GOVERNANCE,
        BUNDLE,
        RUNTIME_SMOKE,
        CONNECTIONS,
        PAC_OPERATOR_PACKAGE,
        MONITORING,
        MONITORING_RUNBOOK,
        MONITORING_SAMPLE,
        FLOW_SMOKE_TEMPLATE,
        FLOW_SMOKE_RUNBOOK,
        FLOW_SMOKE_SAMPLE_CAPTURE,
        FLOW_SMOKE_EVIDENCE,
        ENDPOINT,
        GITHUB_LIVE_GATE_TEMPLATE,
        GITHUB_LIVE_GATE,
    ]:
        assert path.exists(), path


def test_power_platform_operational_evidence_contracts_are_precise():
    runtime = _json(RUNTIME_SMOKE)
    connections = _json(CONNECTIONS)
    pac_package = _json(PAC_OPERATOR_PACKAGE)
    monitoring = _json(MONITORING)
    flow_smoke = _json(FLOW_SMOKE_TEMPLATE)
    flow_smoke_runbook = _text(FLOW_SMOKE_RUNBOOK)
    flow_smoke_sample = _json(FLOW_SMOKE_SAMPLE_CAPTURE)
    flow_smoke_evidence = _json(FLOW_SMOKE_EVIDENCE)

    assert runtime["claimBoundary"]["runtimeSmokePassed"] is False
    assert runtime["claimBoundary"]["productionReadinessClaimed"] is False
    assert connections["claimBoundary"]["connectionsConfigured"] is False
    assert pac_package["status"] == "blocked_pending_required_pac_observations"
    assert pac_package["requiredEvidence"] == [
        "appId",
        "playUrl",
        "connectionId",
    ]
    assert pac_package["currentAuthBlocker"]["missingRequiredObservations"] == [
        "appId",
        "playUrl",
        "connectionId",
    ]
    assert pac_package["currentAuthBlocker"]["claimBoundary"] == {
        "appPublished": False,
        "connectionConfigured": False,
        "productionReadinessClaimed": False,
    }
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
    assert "do not claim" in flow_smoke_runbook.lower()
    assert "flow-smoke-capture-sample.json" in flow_smoke_runbook
    assert "update_power_platform_flow_smoke_evidence.py" in flow_smoke_runbook
    assert flow_smoke_sample["status"] == "template_placeholder_only"
    assert flow_smoke_sample["captureType"] == "power_automate_flow_smoke_capture"
    assert len(flow_smoke_sample["flowRuns"]) == 4
    assert all(entry["flowId"] is None for entry in flow_smoke_sample["flowRuns"])
    assert all(entry["runId"] is None for entry in flow_smoke_sample["flowRuns"])
    assert all(entry["runStatus"] is None for entry in flow_smoke_sample["flowRuns"])
    assert all(entry["runUrl"] is None for entry in flow_smoke_sample["flowRuns"])
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
    assert "monitoring.owner" in monitoring["requiredEvidence"]
    assert any(
        entry["field"] == "support.escalationContact"
        for entry in monitoring["capturedEvidence"]
    )


def test_power_platform_monitoring_dlp_operator_package_is_placeholder_only():
    runbook = _text(MONITORING_RUNBOOK).lower()
    assert "do not claim real admin evidence exists" in runbook
    assert "monitoring-dlp-capture-sample.json" in runbook

    sample = _json(MONITORING_SAMPLE)
    assert sample == {
        "monitoring": {
            "owner": "TBD",
            "failureMetrics": {
                "connectorFailures": "required",
                "flowRunFailures": "required",
                "serviceBoundaryHealth": "required",
                "appHealthMetrics": "required",
                "correlationIdsWithoutPatientData": "required",
            },
        },
        "dlp": {
            "policyId": "TBD",
            "policyName": "TBD",
            "policyClassification": "TBD",
            "policyCaptureState": "blocked_pending_policy_capture",
        },
        "connectorPolicy": {
            "policyId": "TBD",
            "policyName": "TBD",
            "connectorAllowState": "blocked_pending_policy_capture",
        },
        "support": {
            "owner": "TBD",
            "escalationOwner": "TBD",
            "escalationPath": "TBD",
            "escalationContact": "TBD",
        },
    }


def test_power_platform_monitoring_dlp_preflight_gate_rejects_placeholder_sample(
    tmp_path,
):
    import subprocess
    import sys

    output_path = tmp_path / "unused-preflight-output.json"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/update_power_platform_monitoring_dlp_evidence.py",
            "--preflight",
            "--input",
            str(MONITORING_SAMPLE),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    summary = json.loads(result.stdout)
    assert summary["complete"] is False
    assert summary["missingFields"] == []
    assert summary["extraFields"] == []
    assert len(summary["placeholderFields"]) == 17
    assert "monitoring.owner" in summary["placeholderFields"]
    assert "support.escalationContact" in summary["placeholderFields"]
    assert not output_path.exists()


def test_power_platform_monitoring_dlp_preflight_gate_accepts_complete_capture(
    tmp_path,
):
    import subprocess
    import sys

    input_path = tmp_path / "complete-monitoring-dlp.json"
    input_path.write_text(
        json.dumps(
            {
                "monitoring": {
                    "owner": "Platform Operations",
                    "failureMetrics": {
                        "connectorFailures": "captured connector failures",
                        "flowRunFailures": "captured flow run failures",
                        "serviceBoundaryHealth": "captured service boundary health",
                        "appHealthMetrics": "captured app health metrics",
                        "correlationIdsWithoutPatientData": (
                            "captured sanitized correlation identifiers"
                        ),
                    },
                },
                "dlp": {
                    "policyId": "policy-123",
                    "policyName": "NSW Health DLP Policy",
                    "policyClassification": "business",
                    "policyCaptureState": "captured",
                },
                "connectorPolicy": {
                    "policyId": "policy-123",
                    "policyName": "NSW Health DLP Policy",
                    "connectorAllowState": "captured",
                },
                "support": {
                    "owner": "Platform Support",
                    "escalationOwner": "Duty Manager",
                    "escalationPath": "24x7 on-call",
                    "escalationContact": "oncall@example.invalid",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/update_power_platform_monitoring_dlp_evidence.py",
            "--preflight",
            "--input",
            str(input_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["complete"] is True
    assert summary["missingFields"] == []
    assert summary["extraFields"] == []
    assert summary["placeholderFields"] == []


def test_power_platform_monitoring_dlp_updater_stays_blocked_until_complete(
    tmp_path,
):
    import subprocess
    import sys

    input_path = tmp_path / "partial-monitoring-dlp.json"
    output_path = tmp_path / "updated-monitoring-dlp.json"
    input_path.write_text(
        json.dumps(
            {
                "monitoring": {
                    "owner": "Platform Operations",
                },
                "dlp": {
                    "policyId": "policy-123",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/update_power_platform_monitoring_dlp_evidence.py",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    summary = json.loads(result.stdout)
    assert summary["complete"] is False
    assert "dlp.policyName" in summary["missingFields"]
    assert "monitoring.failureMetrics.connectorFailures" in summary["missingFields"]

    updated = _json(output_path)
    assert updated["status"].startswith("blocked")
    assert updated["claimBoundary"]["monitoringConfigured"] is False
    captured = {item["field"]: item for item in updated["capturedEvidence"]}
    assert captured["monitoring.owner"]["status"] == "captured"
    assert captured["dlp.policyId"]["status"] == "captured"
    assert captured["dlp.policyName"]["status"].startswith("blocked")


def test_power_platform_monitoring_dlp_updater_populates_complete_capture(
    tmp_path,
):
    import subprocess
    import sys

    input_path = tmp_path / "complete-monitoring-dlp.json"
    output_path = tmp_path / "complete-monitoring-dlp-evidence.json"
    input_path.write_text(
        json.dumps(
            {
                "monitoring": {
                    "owner": "Platform Operations",
                    "failureMetrics": {
                        "connectorFailures": "captured connector failures",
                        "flowRunFailures": "captured flow run failures",
                        "serviceBoundaryHealth": "captured service boundary health",
                        "appHealthMetrics": "captured app health metrics",
                        "correlationIdsWithoutPatientData": (
                            "captured sanitized correlation identifiers"
                        ),
                    },
                },
                "dlp": {
                    "policyId": "policy-123",
                    "policyName": "NSW Health DLP Policy",
                    "policyClassification": "business",
                    "policyCaptureState": "captured",
                },
                "connectorPolicy": {
                    "policyId": "policy-123",
                    "policyName": "NSW Health DLP Policy",
                    "connectorAllowState": "captured",
                },
                "support": {
                    "owner": "Platform Support",
                    "escalationOwner": "Duty Manager",
                    "escalationPath": "24x7 on-call",
                    "escalationContact": "oncall@example.invalid",
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/update_power_platform_monitoring_dlp_evidence.py",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    summary = json.loads(result.stdout)
    assert summary["complete"] is True
    assert summary["missingFields"] == []

    updated = _json(output_path)
    assert updated["status"].startswith("blocked")
    assert updated["dlp"]["policyName"] == "NSW Health DLP Policy"
    assert updated["connectorPolicy"]["connectorAllowState"] == "captured"
    assert updated["support"]["escalationContact"] == "oncall@example.invalid"
    assert all(item["status"] == "captured" for item in updated["capturedEvidence"])


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


def test_repo_health_production_claim_requires_evidence_before_true_claim():
    import scripts.validate_power_platform_repo_health as validator

    scorecard = _json(REPO_HEALTH_SCORECARD)
    manifest = _json(ROOT / "power-platform" / "repository" / "subrepo-manifest.json")
    deployment = _json(ROOT / "power-platform" / "evidence" / "deployment-status.json")
    closure = _json(
        ROOT / "power-platform" / "repository" / "subrepo-closure-20260521.json"
    )
    deployment["productionReadinessClaimed"] = True
    scorecard["score"] = 9.9
    deployment["missing"] = []
    deployment["repoHealth"]["score"] = 9.9
    closure["standaloneRemote"].update(
        {
            "remoteUrl": "https://example.invalid/repo.git",
            "defaultBranch": "main",
            "syncProcedure": "documented",
            "importOwner": "owner@example.invalid",
        }
    )
    closure["claimBoundary"]["subrepoClosureComplete"] = True
    closure["selectedOption"] = "standalone_remote"

    try:
        validator._require_production_claim_evidence(
            deployment,
            manifest,
            scorecard,
            closure,
            ROOT / "power-platform" / "evidence" / "deployment-status.json",
        )
    except SystemExit as exc:
        assert "production readiness claim requires" in str(exc)
    else:
        raise AssertionError(
            "expected a SystemExit for an unsupported production claim"
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


def test_power_platform_remaining_blockers_are_machine_readable_and_unresolved():
    scorecard = _json(REPO_HEALTH_SCORECARD)
    remaining = _json(REMAINING_BLOCKERS)

    assert remaining["evidenceType"] == "power_platform_remaining_blockers"
    assert remaining["status"] == "blocked_with_remaining_blockers"
    assert remaining["claimBoundary"] == {
        "productionReadinessClaimed": False,
        "blockersResolvedClaimed": False,
        "externalBlockersResolvedClaimed": False,
    }
    assert remaining["generatedFrom"] == {
        "repoHealthScorecard": "power-platform/repository/repo-health-scorecard.json",
        "deploymentStatus": "power-platform/evidence/deployment-status.json",
    }

    assert [blocker["summary"] for blocker in remaining["remainingBlockers"]] == (
        scorecard["hardBlockers"]
    )
    for blocker in remaining["remainingBlockers"]:
        assert blocker["resolved"] is False
        assert blocker["source"] == (
            "power-platform/repository/repo-health-scorecard.json"
        )
        assert blocker["supportingEvidence"]
