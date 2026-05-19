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
    for blocked in [
        "real-power-app-visual-review",
        "real-power-app-runtime-smoke",
        "real-power-automate-flow-smoke",
    ]:
        if checks[blocked]["status"] != "blocked":
            raise SystemExit(f"{blocked} cannot be unblocked without live evidence")

    boundary = status["claimBoundary"]
    if boundary["allPlatformTestsPassed"]:
        raise SystemExit("all platform tests are overclaimed")
    if boundary["visualFunctionOptimized"]:
        raise SystemExit("visual function is overclaimed")
    if boundary["productionReadinessClaimed"]:
        raise SystemExit("production readiness is overclaimed")
    if "Power App visual review" not in plan["requiredOrder"]:
        raise SystemExit("platform test plan must require visual review")

    print("Power Platform platform-test status passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
