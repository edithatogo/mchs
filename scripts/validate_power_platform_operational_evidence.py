from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "power-platform" / "evidence"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_false(data: dict, key: str, path: Path) -> None:
    if data["claimBoundary"].get(key) is not False:
        raise SystemExit(f"{path}: {key} must remain false until live evidence exists")


def main() -> int:
    deployment = _json(EVIDENCE / "deployment-status.json")
    bundle = _json(EVIDENCE / "nsw-operational-readiness-bundle-template.json")
    runtime = _json(EVIDENCE / "runtime-smoke-evidence-template.json")
    connections = _json(EVIDENCE / "connection-reference-evidence-template.json")
    monitoring = _json(EVIDENCE / "monitoring-dlp-evidence-template.json")

    if not deployment["managedSolutionImported"]:
        raise SystemExit("managed solution import evidence is required")
    if deployment["productionReadinessClaimed"]:
        raise SystemExit("deployment status overclaims production readiness")

    known_limitations = "\n".join(bundle["known_limitations"])
    for blocker in [
        "service_boundary_production_endpoint_missing",
        "connection_reference_values_missing",
        "real_dataverse_app_component_smoke_missing",
        "real_power_automate_flow_component_smoke_missing",
    ]:
        if blocker not in known_limitations:
            raise SystemExit(f"missing operational blocker: {blocker}")

    if bundle["governance"]["runtime_production_readiness_claim"]:
        raise SystemExit("readiness bundle overclaims runtime production readiness")
    _require_false(runtime, "runtimeSmokePassed", EVIDENCE)
    _require_false(runtime, "productionReadinessClaimed", EVIDENCE)
    _require_false(connections, "connectionsConfigured", EVIDENCE)
    _require_false(connections, "productionReadinessClaimed", EVIDENCE)
    _require_false(monitoring, "monitoringConfigured", EVIDENCE)
    _require_false(monitoring, "dlpEvidenceCaptured", EVIDENCE)
    _require_false(monitoring, "productionReadinessClaimed", EVIDENCE)

    print("Power Platform operational evidence contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
