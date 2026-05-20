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
    "whoAmI": "not_run",
    "solutionArtifact": "dist/power-platform/mchs_alm_orchestration_managed.zip",
    "solutionArtifactSha256": None,
    "solutionArtifactPackStatus": "not_run",
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
            data.get("requiredGateEvidence") == EXPECTED_GATE_EVIDENCE,
            f"{path}: requiredGateEvidence must stay aligned with live-gate evidence",
        )
        return

    _require(
        data.get("requiredSecrets") == EXPECTED_SECRETS,
        f"{path}: requiredSecrets must remain the four repository secrets",
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

    solution_checker = run.get("solutionChecker")
    _require(
        isinstance(solution_checker, dict),
        f"{path}: run.solutionChecker must be a mapping",
    )
    _require(
        solution_checker.get("result") == "not_run",
        f"{path}: run.solutionChecker.result must remain not_run",
    )
    _require(
        solution_checker.get("findings") is None,
        f"{path}: run.solutionChecker.findings must remain null",
    )


def _validate_claim_boundary(data: dict, path: Path) -> None:
    claim_boundary = data.get("claimBoundary")
    _require(
        isinstance(claim_boundary, dict),
        f"{path}: missing claimBoundary block",
    )
    _require(
        claim_boundary.get("officialLiveGateCompleted") is False,
        f"{path}: officialLiveGateCompleted must remain false",
    )
    _require(
        claim_boundary.get("tenantRuntimeClaimsAllowed") is False,
        f"{path}: tenantRuntimeClaimsAllowed must remain false",
    )
    _require(
        claim_boundary.get("productionReadinessClaimed") is False,
        f"{path}: productionReadinessClaimed must remain false",
    )
    if path == CURRENT:
        _require(
            claim_boundary.get("officialLiveGatePassed") is False,
            f"{path}: officialLiveGatePassed must remain false",
        )
        _require(
            claim_boundary.get("productionDeploymentSecretsConfigured") is False,
            f"{path}: productionDeploymentSecretsConfigured must remain false",
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
