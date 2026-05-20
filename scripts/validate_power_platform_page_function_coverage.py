from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"
COVERAGE = PP / "apps" / "mchs-orchestration-app" / "page-function-coverage.json"
HEALTH99 = PP / "repository" / "health-9-9" / "contract.json"
SUBREPO_CLOSURE = PP / "repository" / "subrepo-closure-20260521.json"
OPENAPI = PP / "connectors" / "mchs-service-boundary" / "openapi.json"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _closure_authorized(closure: dict) -> bool:
    return bool(closure["standaloneRemote"].get("remoteUrl")) or bool(
        closure["waiver"].get("approvedBy")
    )


def main() -> int:
    coverage = _json(COVERAGE)
    health99 = _json(HEALTH99)
    closure = _json(SUBREPO_CLOSURE)
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
        for required_copy in [
            "Synthetic data only",
            "loading, success, validation error, connector error",
            "Trace ID:",
            "No connector error recorded",
            "Power Apps session ID",
        ]:
            if required_copy not in text:
                raise SystemExit(
                    f"operation page missing required UX copy: {required_copy}"
                )
        if not operation.get("sourceUxComplete"):
            raise SystemExit("operation page source UX must be complete")
        if operation["complete"]:
            raise SystemExit("operation pages must not be fully complete before smoke")
        if operation["runtimeSmokeStatus"] != (
            "blocked_pending_service_endpoint_and_connection_reference"
        ):
            raise SystemExit(
                "runtime smoke status must remain blocked for operation pages"
            )

    gate = coverage["completionGate"]
    if not gate["allOperationPagesSourceControlled"]:
        raise SystemExit("operation page source control gate is not recorded")
    if not gate["allOperationPagesUxComplete"]:
        raise SystemExit("operation page UX source completion is not recorded")
    if gate["allOperationRuntimeSmokePassed"]:
        raise SystemExit("operation runtime smoke is overclaimed")
    if gate["allCalculationsFullyImplementedInApp"]:
        raise SystemExit("calculation implementation is overclaimed inside Power Apps")

    boundary = coverage["claimBoundary"]
    if not boundary["operationPagesSourceUxComplete"]:
        raise SystemExit("operation page source UX boundary is not recorded")
    if boundary["operationPagesComplete"]:
        raise SystemExit("operation page runtime completion is overclaimed")
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
    for item in health99["requiredGates"]:
        if not (ROOT / item["evidence"]).exists():
            raise SystemExit(f"9.9 gate evidence target missing: {item['evidence']}")
    statuses = {item["gate"]: item["status"] for item in health99["requiredGates"]}
    if statuses["all_connector_operation_pages_source_ux_complete"] != (
        "passed_source_evidence"
    ):
        raise SystemExit("operation page source UX gate must be passed")
    for gate_name, status in statuses.items():
        if gate_name == "all_connector_operation_pages_source_ux_complete":
            continue
        if status != "blocked":
            raise SystemExit("live 9.9 gates must remain blocked until evidence exists")

    closure_gate = next(
        item
        for item in health99["requiredGates"]
        if item["gate"] == "standalone_power_platform_subrepo_remote_or_explicit_waiver"
    )
    if closure_gate.get("requiredClosureEvidence") != {
        "standaloneRemote": ["remoteUrl"],
        "explicitWaiver": ["approvedBy"],
    }:
        raise SystemExit("subrepo closure gate must require remoteUrl or approvedBy")
    if closure["requiredClosureFields"] != {
        "standaloneRemote": ["remoteUrl"],
        "explicitWaiver": ["approvedBy"],
    }:
        raise SystemExit("subrepo closure must declare remoteUrl or approvedBy as required")
    if not _closure_authorized(closure):
        if closure["status"] != "blocked_pending_remote_or_explicit_waiver":
            raise SystemExit(
                "subrepo closure must stay blocked until remote or waiver exists"
            )
        if closure["claimBoundary"]["subrepoClosureComplete"]:
            raise SystemExit("subrepo closure completion is overclaimed")
        if closure["selectedOption"] is not None:
            raise SystemExit(
                "subrepo closure must not pick an option before evidence exists"
            )
    if health99["claimBoundary"]["score99Claimed"] and not _closure_authorized(closure):
        raise SystemExit("9.9 claim requires standalone remote URL or waiver approver")

    print("Power Platform page/function coverage and 9.9 contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
