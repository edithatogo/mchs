from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "power-platform"
    / "apps"
    / "mchs-orchestration-app"
    / "visual-performance-contract.json"
)
SOURCE = (
    ROOT
    / "power-platform"
    / "apps"
    / "mchs-orchestration-app"
    / "source"
    / "Src"
    / "HomeScreen_Screen.fx.yaml"
)


def main() -> int:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    source = SOURCE.read_text(encoding="utf-8")

    for required in [
        "MCHS Orchestration",
        "NSW dylan",
        "Synthetic data only",
        "Connector",
        "Endpoint pending",
        "Launch passed",
        "Operational checks",
        "Readiness guardrails",
        "copy the Power Apps session ID",
    ]:
        if required not in source:
            raise SystemExit(f"optimized home screen missing copy: {required}")

    if "OnVisible" in source and "MCHSServiceBoundary" in source:
        raise SystemExit("home screen must not call the connector on visible")
    connector_budget = contract["performanceBudget"][
        "homeScreenExternalConnectorCallsOnVisibleMax"
    ]
    if connector_budget != 0:
        raise SystemExit("home screen connector-call budget must be zero")
    if not contract["claimBoundary"]["optimizedSourceGenerated"]:
        raise SystemExit("optimized source generation is not recorded")
    if not contract["claimBoundary"]["optimizedMsappPacked"]:
        raise SystemExit("optimized msapp package is not recorded")
    if not contract["claimBoundary"]["optimizedAppPublished"]:
        raise SystemExit("optimized app publication is not recorded")
    publication = contract.get("publication", {})
    for required in ["appId", "playUrl", "screenshot", "screenshotSha256"]:
        if not publication.get(required):
            raise SystemExit(f"optimized app publication missing: {required}")
    if contract["claimBoundary"]["productionRuntimeReady"]:
        if not publication.get("publishedInTenant"):
            raise SystemExit(
                "production runtime readiness claim requires tenant "
                "publication evidence"
            )
        if not contract["claimBoundary"]["optimizedSourceGenerated"]:
            raise SystemExit(
                "production runtime readiness claim requires optimized source evidence"
            )
        if not contract["claimBoundary"]["optimizedMsappPacked"]:
            raise SystemExit(
                "production runtime readiness claim requires packed "
                "optimized msapp evidence"
            )
        if not contract["claimBoundary"]["optimizedAppPublished"]:
            raise SystemExit(
                "production runtime readiness claim requires optimized app "
                "publication evidence"
            )

    print("Power Platform visual performance contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
