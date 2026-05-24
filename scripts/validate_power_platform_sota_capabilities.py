from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PP = ROOT / "power-platform"


CAPABILITY_FILES = [
    PP / "pipelines" / "native-pipelines-manifest.json",
    PP / "tests" / "playwright-smoke" / "manifest.json",
    PP / "apps" / "code-apps" / "evaluation-manifest.json",
    PP / "copilot" / "real-time-connector-knowledge.json",
    PP / "dataverse" / "mcp-server-readiness.json",
    PP / "governance" / "agentic-observability.json",
]


PREVIEW_OR_EXTERNAL_CAPABILITIES = {
    "native_power_platform_pipelines",
    "playwright_power_apps_runtime_smoke",
    "power_apps_code_apps",
    "copilot_studio_real_time_connector_knowledge",
    "dataverse_mcp_server",
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _validate_capability(path: Path) -> None:
    data = _read_json(path)
    capability = data["capability"]
    claim_boundary = data["claimBoundary"]

    if data["schemaVersion"] != 1:
        raise SystemExit(f"{path}: unsupported schemaVersion")
    if "status" not in data:
        raise SystemExit(f"{path}: missing status")
    if "featureFlag" not in data:
        raise SystemExit(f"{path}: missing featureFlag")
    if claim_boundary.get("productionReadinessClaimed") is True:
        _require(
            data.get("featureEnabled") is True,
            f"{path}: production readiness claim requires the feature to be enabled",
        )
        _require(
            bool(data.get("status")) and not str(data["status"]).startswith("blocked"),
            (
                f"{path}: production readiness claim requires a non-blocked "
                "capability status"
            ),
        )
    elif claim_boundary.get("productionReadinessClaimed") is not False:
        raise SystemExit(f"{path}: productionReadinessClaimed must be a boolean")
    if capability in PREVIEW_OR_EXTERNAL_CAPABILITIES and data["featureEnabled"]:
        raise SystemExit(f"{path}: preview/external capability enabled too early")


def main() -> int:
    for path in CAPABILITY_FILES:
        if not path.exists():
            raise SystemExit(f"missing Power Platform SOTA capability file: {path}")
        _validate_capability(path)

    observability = _read_json(PP / "governance" / "agentic-observability.json")
    required = set(observability["requiredEvidenceFields"])
    for field in {
        "dlpPolicy",
        "connectorPolicy",
        "managedEnvironmentState",
        "appHealthMetrics",
        "flowRunOutcomes",
        "agentIdentity",
        "auditLogReference",
    }:
        if field not in required:
            raise SystemExit(f"missing observability evidence field: {field}")

    print("Power Platform SOTA capability contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
