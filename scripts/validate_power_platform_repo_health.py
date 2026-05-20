from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    scorecard = _json(PP / "repository" / "repo-health-scorecard.json")
    manifest = _json(PP / "repository" / "subrepo-manifest.json")
    deployment = _json(PP / "evidence" / "deployment-status.json")

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

    print("Power Platform repo-health scorecard passed at 9.5 with 9.9 gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
