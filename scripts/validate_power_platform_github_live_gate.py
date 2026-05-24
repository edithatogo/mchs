from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "power-platform" / "evidence"
TEMPLATE = EVIDENCE / "official-github-live-gate-evidence-template.json"
CURRENT = EVIDENCE / "github-live-gate-20260521.json"

EXPECTED_SECRETS = [
    "POWER_PLATFORM_ENVIRONMENT_URL",
    "POWER_PLATFORM_APPLICATION_ID",
    "POWER_PLATFORM_CLIENT_SECRET",
    "POWER_PLATFORM_TENANT_ID",
]

EXPECTED_SECRET_CHECKS = [
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

EXPECTED_WORKFLOW_DISPATCH = {
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

EXPECTED_RUN_WORKFLOW_DISPATCH = {
    "workflowFile": ".github/workflows/power-platform-official-actions.yml",
    "event": "workflow_dispatch",
    "inputs": {
        "run_live_checks": True,
        "workflow": "Power Platform Official Actions",
        "trigger": "workflow_dispatch",
    },
}

EXPECTED_GATE_EVIDENCE = [
    "workflow run URL",
    "who-am-i target environment output",
    "solution checker result",
    "packed managed solution artifact hash",
    "managed import/visibility checks from pac",
    "runtime smoke command evidence",
]

EXPECTED_CURRENT_EVIDENCE = [
    "workflow run URL",
    "who-am-i target environment output",
    "packed managed solution artifact hash",
    "solution checker result",
    "approval environment record if required",
]

EXPECTED_NOT_RUN = {
    "status": "not_run",
    "runId": None,
    "runUrl": None,
    "runUrlPattern": r"^https://github\.com/[^/]+/[^/]+/actions/runs/\d+$",
    "whoAmI": "not_run",
    "solutionArtifact": "dist/power-platform/mchs_alm_orchestration_managed.zip",
    "solutionArtifactSha256": None,
    "solutionArtifactPackStatus": "not_run",
}

EXPECTED_SOLUTION_CHECKER = {
    "result": "not_run",
    "findings": None,
    "command": "pac solution checker run",
    "reportPath": None,
}

EXPECTED_ARTIFACT_EVIDENCE = {
    "path": "dist/power-platform/mchs_alm_orchestration_managed.zip",
    "hashAlgorithm": "sha256",
    "hashPattern": r"^[a-f0-9]{64}$",
    "hashCommand": "sha256sum dist/power-platform/mchs_alm_orchestration_managed.zip",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _validate_required_lists(data: dict, path: Path) -> None:
    if path == TEMPLATE:
        _require(
            data.get("requiredSecrets") == EXPECTED_SECRETS,
            f"{path}: requiredSecrets must remain the four repository secrets",
        )
        _require(
            data.get("requiredSecretChecks") == EXPECTED_SECRET_CHECKS,
            (
                f"{path}: requiredSecretChecks must stay aligned with "
                "the blocked secret inventory"
            ),
        )
        _require(
            data.get("workflowDispatchInputs") == EXPECTED_WORKFLOW_DISPATCH,
            f"{path}: workflowDispatchInputs must remain the dispatch contract",
        )
        _require(
            data.get("requiredGateEvidence") == EXPECTED_GATE_EVIDENCE,
            f"{path}: requiredGateEvidence must stay aligned with live-gate evidence",
        )
        return

    _require(
        data.get("requiredSecrets") == EXPECTED_SECRETS,
        f"{path}: requiredSecrets must remain the four repository secrets",
    )
    _require(
        data.get("requiredSecretChecks") == EXPECTED_SECRET_CHECKS,
        (
            f"{path}: requiredSecretChecks must stay aligned with "
            "the blocked secret inventory"
        ),
    )
    _require(
        data.get("workflowDispatchInputs") == EXPECTED_WORKFLOW_DISPATCH,
        f"{path}: workflowDispatchInputs must remain the dispatch contract",
    )
    _require(
        data.get("requiredEvidence") == EXPECTED_CURRENT_EVIDENCE,
        f"{path}: requiredEvidence must stay aligned with the current live-gate record",
    )


def _validate_run_block(data: dict, path: Path) -> None:
    run = data.get("run")
    _require(isinstance(run, dict), f"{path}: missing run evidence block")
    for key, expected in EXPECTED_NOT_RUN.items():
        _require(
            run.get(key) == expected,
            f"{path}: run.{key} must remain {expected!r} until live evidence exists",
        )

    _require(
        run["runUrlPattern"] == EXPECTED_NOT_RUN["runUrlPattern"],
        f"{path}: run.runUrlPattern must be the GitHub Actions run URL pattern",
    )

    workflow_dispatch = run.get("workflowDispatchInputs")
    _require(
        workflow_dispatch == EXPECTED_RUN_WORKFLOW_DISPATCH,
        (
            f"{path}: run.workflowDispatchInputs must stay aligned with "
            "the concrete dispatch values"
        ),
    )

    solution_checker = run.get("solutionChecker")
    _require(
        isinstance(solution_checker, dict),
        f"{path}: run.solutionChecker must be a mapping",
    )
    for key, expected in EXPECTED_SOLUTION_CHECKER.items():
        _require(
            solution_checker.get(key) == expected,
            f"{path}: run.solutionChecker.{key} must remain {expected!r}",
        )

    solution_artifact = run.get("solutionArtifactEvidence")
    _require(
        isinstance(solution_artifact, dict),
        f"{path}: run.solutionArtifactEvidence must be a mapping",
    )
    for key, expected in EXPECTED_ARTIFACT_EVIDENCE.items():
        _require(
            solution_artifact.get(key) == expected,
            f"{path}: run.solutionArtifactEvidence.{key} must remain {expected!r}",
        )


def _validate_live_gate_production_claim(data: dict, path: Path) -> None:
    claim_boundary = data.get("claimBoundary", {})
    if claim_boundary.get("productionReadinessClaimed") is not True:
        return

    _require(
        claim_boundary.get("officialLiveGateCompleted") is True,
        f"{path}: production readiness claim requires officialLiveGateCompleted evidence",
    )
    _require(
        claim_boundary.get("tenantRuntimeClaimsAllowed") is True,
        f"{path}: production readiness claim requires tenant runtime evidence",
    )
    _require(
        claim_boundary.get("productionDeploymentSecretsConfigured") is True,
        f"{path}: production readiness claim requires deployment secrets evidence",
    )

    run = data.get("run", {})
    _require(
        run.get("status") != "not_run",
        f"{path}: production readiness claim requires a workflow run",
    )
    _require(
        bool(run.get("runUrl")),
        f"{path}: production readiness claim requires a workflow run URL",
    )
    _require(
        run.get("solutionChecker", {}).get("result") not in (None, "not_run"),
        f"{path}: production readiness claim requires solution checker evidence",
    )
    _require(
        bool(run.get("solutionArtifactSha256")),
        f"{path}: production readiness claim requires a packed managed solution artifact hash",
    )
    _require(
        data.get("repositorySecretsObserved", {}).get("requiredSecretsPresent") is True,
        f"{path}: production readiness claim requires repository secrets evidence",
    )
    _require(
        all(
            check.get("observed") is True
            for check in data.get("requiredSecretChecks", [])
        ),
        f"{path}: production readiness claim requires all repository secrets to be observed",
    )
    _require(
        claim_boundary.get("officialLiveGatePassed") is True,
        f"{path}: production readiness claim requires the official live gate to be passed",
    )
    _require(
        claim_boundary.get("officialLiveGateCompleted") is True,
        f"{path}: production readiness claim requires official live gate completion",
    )
    _require(
        claim_boundary.get("tenantRuntimeClaimsAllowed") is True,
        f"{path}: production readiness claim requires tenant runtime claims to be allowed",
    )
    _require(
        claim_boundary.get("productionDeploymentSecretsConfigured") is True,
        f"{path}: production readiness claim requires deployment secrets to be configured",
    )


def _validate_claim_boundary(data: dict, path: Path) -> None:
    claim_boundary = data.get("claimBoundary")
    _require(
        isinstance(claim_boundary, dict),
        f"{path}: missing claimBoundary block",
    )
    _require(
        claim_boundary.get("officialLiveGateCompleted") in (False, True),
        f"{path}: officialLiveGateCompleted must be a boolean",
    )
    _require(
        claim_boundary.get("tenantRuntimeClaimsAllowed") in (False, True),
        f"{path}: tenantRuntimeClaimsAllowed must be a boolean",
    )
    _require(
        claim_boundary.get("productionReadinessClaimed") in (False, True),
        f"{path}: productionReadinessClaimed must be a boolean",
    )
    _validate_live_gate_production_claim(data, path)
    if path == CURRENT:
        _require(
            claim_boundary.get("officialLiveGatePassed") in (False, True),
            f"{path}: officialLiveGatePassed must be a boolean",
        )
        _require(
            claim_boundary.get("productionDeploymentSecretsConfigured")
            in (False, True),
            f"{path}: productionDeploymentSecretsConfigured must be a boolean",
        )


def main() -> int:
    template = _json(TEMPLATE)
    current = _json(CURRENT)

    _require(
        template["evidenceType"] == "power_platform_official_github_actions_live_gate",
        f"{TEMPLATE}: evidenceType changed unexpectedly",
    )
    _require(
        current["evidenceType"] == "github_power_platform_live_gate",
        f"{CURRENT}: evidenceType changed unexpectedly",
    )
    _require(
        template["status"] == "blocked_pending_repository_secrets_and_workflow_run",
        (
            f"{TEMPLATE}: status must remain "
            "blocked_pending_repository_secrets_and_workflow_run"
        ),
    )
    _require(
        current["status"] == "blocked_pending_repository_secrets_and_workflow_run",
        (
            f"{CURRENT}: status must remain "
            "blocked_pending_repository_secrets_and_workflow_run"
        ),
    )
    _require(
        template["targetWorkflow"]
        == ".github/workflows/power-platform-official-actions.yml",
        f"{TEMPLATE}: targetWorkflow must remain the official actions workflow",
    )
    _require(
        current["workflow"] == ".github/workflows/power-platform-official-actions.yml",
        f"{CURRENT}: workflow must remain the official actions workflow",
    )
    _validate_required_lists(template, TEMPLATE)
    _validate_required_lists(current, CURRENT)
    _validate_run_block(template, TEMPLATE)
    _validate_run_block(current, CURRENT)
    _validate_claim_boundary(template, TEMPLATE)
    _validate_claim_boundary(current, CURRENT)

    print("Power Platform official GitHub live-gate evidence contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
