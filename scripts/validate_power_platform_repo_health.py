from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"
MONITORING_DLP = PP / "evidence" / "dlp-monitoring-policy-evidence-20260521.json"
SUBREPO_CLOSURE = PP / "repository" / "subrepo-closure-20260521.json"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _closure_authorized(closure: dict) -> bool:
    return bool(closure["standaloneRemote"].get("remoteUrl")) or bool(
        closure["waiver"].get("approvedBy")
    )


def _require_path(data: dict, path: tuple[str, ...], label: str, source: Path) -> None:
    cursor: object = data
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            joined = ".".join(path)
            raise SystemExit(f"{source}: missing required {label} field {joined}")
        cursor = cursor[key]
    if cursor in (None, "", [], {}):
        joined = ".".join(path)
        raise SystemExit(f"{source}: {label} field {joined} must be populated")


def main() -> int:
    scorecard = _json(PP / "repository" / "repo-health-scorecard.json")
    manifest = _json(PP / "repository" / "subrepo-manifest.json")
    deployment = _json(PP / "evidence" / "deployment-status.json")
    dlp = _json(MONITORING_DLP)
    closure = _json(SUBREPO_CLOSURE)

    if scorecard["score"] < 9.5:
        raise SystemExit("Power Platform repo-health score is below 9.5")
    if scorecard["targetScore"] != 9.5:
        raise SystemExit("Power Platform repo-health target must remain 9.5")
    if scorecard.get("targetScoreCandidate") != 9.9:
        raise SystemExit("Power Platform repo-health 9.9 candidate is not recorded")
    if not (PP / "repository" / "health-9-9" / "contract.json").exists():
        raise SystemExit("Power Platform repo-health 9.9 contract is missing")
    if manifest["mode"] != "in_repository_governed_subrepo_boundary":
        raise SystemExit("Power Platform subrepo mode is not explicitly governed")
    if not manifest["claimBoundary"]["subrepoBoundaryEnforced"]:
        raise SystemExit("Power Platform subrepo boundary is not enforced")
    if manifest["claimBoundary"]["runtimeProductionReady"]:
        raise SystemExit("Power Platform runtime readiness is overclaimed")
    if deployment["productionReadinessClaimed"]:
        raise SystemExit("Deployment status overclaims production readiness")
    if closure["requiredClosureFields"] != {
        "standaloneRemote": ["remoteUrl"],
        "explicitWaiver": ["approvedBy"],
    }:
        raise SystemExit("closure artifact must require remoteUrl or approvedBy")
    if not _closure_authorized(closure):
        if closure["status"] != "blocked_pending_remote_or_explicit_waiver":
            raise SystemExit("closure must stay blocked until remote or waiver exists")
        if closure["claimBoundary"]["subrepoClosureComplete"]:
            raise SystemExit("closure completion is overclaimed")
        if closure["selectedOption"] is not None:
            raise SystemExit("closure must not select an option before evidence exists")
    if scorecard["score"] >= 9.9 and not _closure_authorized(closure):
        raise SystemExit(
            "claiming 9.9 requires standalone remote URL or waiver approver"
        )
    if dlp["status"] != "blocked_pending_nsw_admin_policy_capture":
        raise SystemExit("Monitoring and DLP evidence status must remain blocked")
    for path in (
        ("dlp", "policyId"),
        ("dlp", "policyName"),
        ("dlp", "policyClassification"),
        ("connectorPolicy", "policyId"),
        ("connectorPolicy", "policyName"),
        ("connectorPolicy", "connectorAllowState"),
        ("monitoring", "owner"),
        ("monitoring", "failureMetrics"),
        ("support", "owner"),
        ("support", "escalationOwner"),
        ("support", "escalationPath"),
        ("support", "escalationContact"),
    ):
        _require_path(dlp, path, "monitoring DLP evidence", MONITORING_DLP)
    for path in (
        ("monitoring", "failureMetrics", "connectorFailures"),
        ("monitoring", "failureMetrics", "flowRunFailures"),
        ("monitoring", "failureMetrics", "serviceBoundaryHealth"),
        ("monitoring", "failureMetrics", "appHealthMetrics"),
        ("monitoring", "failureMetrics", "correlationIdsWithoutPatientData"),
    ):
        _require_path(dlp, path, "monitoring failure metric", MONITORING_DLP)

    print("Power Platform repo-health scorecard passed at 9.5 with 9.9 gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
