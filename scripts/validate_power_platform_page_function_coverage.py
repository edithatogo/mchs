from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"
COVERAGE = PP / "apps" / "mchs-orchestration-app" / "page-function-coverage.json"
HEALTH99 = PP / "repository" / "health-9-9" / "contract.json"
OPENAPI = PP / "connectors" / "mchs-service-boundary" / "openapi.json"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    coverage = _json(COVERAGE)
    health99 = _json(HEALTH99)
    openapi = _json(OPENAPI)

    connector_operations = {
        operation["operationId"]
        for path_item in openapi["paths"].values()
        for operation in path_item.values()
    }
    covered_operations = {
        operation["operationId"] for operation in coverage["operationCoverage"]
    }
    if connector_operations != covered_operations:
        missing = sorted(connector_operations - covered_operations)
        extra = sorted(covered_operations - connector_operations)
        raise SystemExit(
            f"operation coverage mismatch; missing={missing}; extra={extra}"
        )

    for operation in coverage["operationCoverage"]:
        source = ROOT / operation["source"]
        if not source.exists():
            raise SystemExit(f"missing operation screen source: {operation['source']}")
        text = source.read_text(encoding="utf-8")
        if operation["screen"] not in text:
            raise SystemExit(f"screen source does not declare {operation['screen']}")
        if operation["complete"]:
            raise SystemExit("operation pages must not be marked complete before smoke")
        if operation["runtimeSmokeStatus"] != (
            "blocked_pending_service_endpoint_and_connection_reference"
        ):
            raise SystemExit(
                "runtime smoke status must remain blocked for operation pages"
            )

    gate = coverage["completionGate"]
    if not gate["allOperationPagesSourceControlled"]:
        raise SystemExit("operation page source control gate is not recorded")
    if gate["allOperationPagesUxComplete"]:
        raise SystemExit("operation page UX completion is overclaimed")
    if gate["allOperationRuntimeSmokePassed"]:
        raise SystemExit("operation runtime smoke is overclaimed")
    if gate["allCalculationsFullyImplementedInApp"]:
        raise SystemExit("calculation implementation is overclaimed inside Power Apps")

    boundary = coverage["claimBoundary"]
    if boundary["operationPagesComplete"]:
        raise SystemExit("operation page completion is overclaimed")
    if boundary["everyCalculationFunctionFullyProven"]:
        raise SystemExit("calculation/function proof is overclaimed")
    if boundary["repoHealth99Eligible"]:
        raise SystemExit("repo-health 9.9 eligibility is overclaimed")

    if health99["currentScore"] != 9.5:
        raise SystemExit("9.9 contract must preserve current score at 9.5")
    if health99["targetScore"] != 9.9:
        raise SystemExit("9.9 contract target is not 9.9")
    if health99["claimBoundary"]["score99Claimed"]:
        raise SystemExit("9.9 score is overclaimed")
    if not all(gate["status"] == "blocked" for gate in health99["requiredGates"]):
        raise SystemExit("9.9 gates must remain blocked until live evidence exists")

    print("Power Platform page/function coverage and 9.9 contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
