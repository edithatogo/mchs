from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "power-platform" / "tooling" / "github-actions-manifest.json"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    power_platform = manifest["githubActions"]["powerPlatform"]
    power_bi = manifest["githubActions"]["powerBI"]
    boundary = manifest["claimBoundary"]

    if power_platform["provider"] != "microsoft/powerplatform-actions":
        raise SystemExit("official Microsoft Power Platform Actions are required")
    for action in [
        "actions-install@v1",
        "pack-solution@v1",
        "who-am-i@v1",
        "checker@v1",
    ]:
        if action not in power_platform["actions"]:
            raise SystemExit(f"missing Power Platform GitHub action: {action}")
    for tool in ["powerbi CLI", "powerbi-visuals-tools pbiviz"]:
        if tool not in power_bi["tooling"]:
            raise SystemExit(f"missing Power BI tooling: {tool}")
    if not boundary["githubWorkflowReferencesInstalled"]:
        raise SystemExit("GitHub workflow references are not installed")
    if not boundary["localRequiredCliToolsInstalled"]:
        raise SystemExit("local required CLI tools are not installed")
    if boundary["productionDeploymentSecretsConfigured"]:
        raise SystemExit("production deployment secrets are not evidenced")

    print("Power Platform and Power BI toolchain contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
