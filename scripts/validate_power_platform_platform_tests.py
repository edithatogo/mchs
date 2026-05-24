from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    status = _json(PP / "evidence" / "platform-test-status.json")
    plan = _json(PP / "tests" / "platform-test-plan.json")

    checks = {check["name"]: check for check in status["platformChecks"]}
    for required in [
        "pac-auth-and-solution-visibility",
        "solution-checker",
        "custom-connector-registration",
        "generated-canvas-msapp",
        "real-power-app-visual-review",
        "real-power-app-runtime-smoke",
        "real-power-automate-flow-smoke",
    ]:
        if required not in checks:
            raise SystemExit(f"missing platform check: {required}")

    if checks["pac-auth-and-solution-visibility"]["status"] != "passed":
        raise SystemExit("PAC solution visibility must remain evidenced")
    if checks["solution-checker"]["status"] != "passed":
        raise SystemExit("solution checker must remain evidenced")
    if checks["custom-connector-registration"]["status"] != "passed":
        raise SystemExit("custom connector registration must remain evidenced")
    if checks["generated-canvas-msapp"]["status"] != "passed":
        raise SystemExit("generated canvas msapp must remain evidenced")
    if checks["real-power-app-visual-review"]["status"] != "passed":
        raise SystemExit("Power App visual review must be evidenced as passed")
    if checks["real-power-app-runtime-smoke"]["status"] != "partial":
        raise SystemExit("Power App runtime smoke must remain partial")
    if checks["real-power-automate-flow-smoke"]["status"] != "blocked":
        raise SystemExit("Power Automate flow smoke must remain blocked")

    boundary = status["claimBoundary"]
    if boundary["allPlatformTestsPassed"]:
        raise SystemExit("all platform tests are overclaimed")
    visual = status["visualFunction"]
    if boundary["visualFunctionOptimized"]:
        if not visual["optimizedInTenant"]:
            raise SystemExit("visual function is overclaimed without tenant evidence")
        for required in [
            "optimizedAppId",
            "optimizedAppPlayUrl",
            "optimizedScreenshot",
            "optimizedScreenshotSha256",
        ]:
            if not visual.get(required):
                raise SystemExit(f"visual optimization evidence missing: {required}")
    if boundary["productionReadinessClaimed"]:
        if any(
            checks[name]["status"] != "passed"
            for name in [
                "pac-auth-and-solution-visibility",
                "solution-checker",
                "custom-connector-registration",
                "generated-canvas-msapp",
                "real-power-app-visual-review",
            ]
        ):
            raise SystemExit(
                "production readiness claim requires all core platform "
                "checks to be passed"
            )
        if checks["real-power-app-runtime-smoke"]["status"] != "passed":
            raise SystemExit(
                "production readiness claim requires real Power App runtime "
                "smoke evidence"
            )
        if checks["real-power-automate-flow-smoke"]["status"] != "passed":
            raise SystemExit(
                "production readiness claim requires real Power Automate "
                "flow smoke evidence"
            )
        if not visual.get("optimizedInTenant"):
            raise SystemExit(
                "production readiness claim requires tenant visual evidence"
            )
    if "Power App visual review" not in plan["requiredOrder"]:
        raise SystemExit("platform test plan must require visual review")

    print("Power Platform platform-test status passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
