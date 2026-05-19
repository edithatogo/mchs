from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_power_platform_platform_test_status_is_truthful() -> None:
    status = _json(PP / "evidence" / "platform-test-status.json")
    checks = {check["name"]: check["status"] for check in status["platformChecks"]}
    assert checks["pac-auth-and-solution-visibility"] == "passed"
    assert checks["solution-checker"] == "passed"
    assert checks["real-power-app-visual-review"] == "blocked"
    assert checks["real-power-app-runtime-smoke"] == "blocked"
    assert checks["real-power-automate-flow-smoke"] == "blocked"
    assert status["visualFunction"]["viewedInTenant"] is False
    assert status["visualFunction"]["optimizedInTenant"] is False
    assert status["claimBoundary"]["allPlatformTestsPassed"] is False


def test_power_platform_platform_test_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_platform_tests.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform platform-test status passed." in result.stdout


def test_power_platform_visual_optimization_plan_exists() -> None:
    plan = _json(PP / "tests" / "platform-test-plan.json")
    checklist = set(plan["visualOptimizationChecklist"])
    assert {
        "loading state during connector calls",
        "human-readable validation errors",
        "copyable correlation ID for support",
        "responsive layout at desktop and tablet widths",
        "keyboard navigability",
        "sufficient color contrast",
    } <= checklist
