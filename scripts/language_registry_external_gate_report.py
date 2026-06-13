#!/usr/bin/env python3
"""Report language registry publication gates without overclaiming.

The default mode reads the checked-in language registry contract. ``--live`` adds
small public HTTP probes for known registry/submission URLs, but it does not
promote a registry to complete unless the public response contains the expected
package version.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)

COMPLETE_STATUSES = {"published_verified", "complete", "completed", "verified"}
SUBMITTED_MARKERS = ("submitted", "open", "pending_review", "review")
BLOCK_MARKERS = ("blocked", "pending", "required", "credential", "cla", "agreement")

PUBLIC_PROBES = {
    "python_pypi": "https://pypi.org/pypi/nwau-py/0.2.2/json",
    "rust_crates_io": "https://crates.io/api/v1/crates/nwau-core/0.1.0",
    "typescript_npm": "https://registry.npmjs.org/@edithatogo%2fmchs-wasm-binding/0.1.0",
    "dotnet_nuget": "https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/0.1.0/mchs.bindings.dotnet.0.1.0.nupkg",
    "go_module_proxy": "https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/v0.1.0.info",
    "conda_forge": "https://api.anaconda.org/package/conda-forge/nwau-py",
    "julia_general": "https://juliahub.com/ui/Packages/General/NationalWeightedActivityUnitWrapper",
}

OPEN_VSX_API = "https://open-vsx.org/api/edithatogo/mchs-tools"
VSCODE_MARKETPLACE_QUERY_URL = (
    "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
    "?api-version=7.2-preview.1"
)
VSCODE_MARKETPLACE_EXTENSION_ID = "edithatogo.mchs-tools"


def fetch(url: str) -> dict[str, Any]:
    if urlparse(url).scheme != "https":
        return {"url": url, "error": "unsupported_scheme"}
    request = urllib.request.Request(
        url, headers={"User-Agent": "mchs-registry-gate-report/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310
            body = response.read(2_000_000).decode("utf-8", errors="replace")
            return {"url": url, "http_status": response.status, "body": body[:10_000]}
    except urllib.error.HTTPError as exc:
        body = exc.read(2_000).decode("utf-8", errors="replace")
        return {"url": url, "http_status": exc.code, "body": body}
    except Exception as exc:
        return {"url": url, "error": type(exc).__name__, "message": str(exc)}


def fetch_post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    if urlparse(url).scheme != "https":
        return {"url": url, "error": "unsupported_scheme"}
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "mchs-registry-gate-report/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310
            response_body = response.read(2_000_000).decode("utf-8", errors="replace")
            return {
                "url": url,
                "http_status": response.status,
                "body": response_body[:100_000],
            }
    except urllib.error.HTTPError as exc:
        response_body = exc.read(2_000).decode("utf-8", errors="replace")
        return {"url": url, "http_status": exc.code, "body": response_body}
    except Exception as exc:
        return {"url": url, "error": type(exc).__name__, "message": str(exc)}


def version_visible(registry: dict[str, Any], probe: dict[str, Any]) -> bool:
    if probe.get("http_status") != 200:
        return False
    version = str(registry.get("version") or "")
    body = str(probe.get("body") or "")
    return bool(version and version in body)


def vscode_marketplace_payload() -> dict[str, Any]:
    return {
        "filters": [
            {
                "criteria": [
                    {
                        "filterType": 7,
                        "value": VSCODE_MARKETPLACE_EXTENSION_ID,
                    }
                ],
                "pageNumber": 1,
                "pageSize": 1,
                "sortBy": 0,
                "sortOrder": 0,
            }
        ],
        "assetTypes": [],
        "flags": 914,
    }


def vscode_target_version_visible(
    registry: dict[str, Any], observation: dict[str, Any]
) -> bool:
    return version_visible(registry, observation.get("openvsx_probe", {})) and (
        version_visible(registry, observation.get("marketplace_probe", {}))
    )


def classify(registry: dict[str, Any], live: dict[str, Any] | None = None) -> str:
    status = str(registry.get("current_status") or "").lower()
    blocker = registry.get("blocker")
    if status in COMPLETE_STATUSES or status.endswith("published_verified"):
        return "completed"
    if live and (
        live.get("target_version_visible") is True
        or version_visible(registry, live.get("public_probe", {}))
    ):
        return "completion_candidates"
    if registry.get("publicationEvidence"):
        return "partial_publications"
    if registry.get("submission_url") or any(
        marker in status for marker in SUBMITTED_MARKERS
    ):
        return "submitted_review_items"
    if blocker or any(marker in status for marker in BLOCK_MARKERS):
        return "external_blocks"
    return "publication_follow_up_items"


def build_report(contract: dict[str, Any], live: bool) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {
        "completed": [],
        "completion_candidates": [],
        "partial_publications": [],
        "submitted_review_items": [],
        "publication_follow_up_items": [],
        "external_blocks": [],
    }
    live_observations: dict[str, Any] = {}

    for registry in contract.get("registries", []):
        registry_id = registry.get("id")
        observation: dict[str, Any] = {}
        if live:
            if registry_id == "vscode_openvsx":
                observation["openvsx_probe"] = fetch(OPEN_VSX_API)
                observation["marketplace_probe"] = fetch_post_json(
                    VSCODE_MARKETPLACE_QUERY_URL,
                    vscode_marketplace_payload(),
                )
                observation["target_version_visible"] = vscode_target_version_visible(
                    registry, observation
                )
            elif registry_id in PUBLIC_PROBES:
                observation["public_probe"] = fetch(PUBLIC_PROBES[registry_id])
                observation["target_version_visible"] = version_visible(
                    registry, observation["public_probe"]
                )
            submission_url = registry.get("submission_url")
            if isinstance(submission_url, str) and submission_url.startswith(
                "https://github.com/"
            ):
                observation["submission_probe"] = fetch(submission_url)
            if observation:
                live_observations[str(registry_id)] = observation

        group = classify(registry, observation if live else None)
        groups[group].append(
            {
                "id": registry_id,
                "registry": registry.get("registry"),
                "package": registry.get("package"),
                "version": registry.get("version"),
                "status": registry.get("current_status"),
                "submission_url": registry.get("submission_url"),
                "blocker": registry.get("blocker"),
            }
        )

    return {
        "schemaVersion": 1,
        "source": str(CONTRACT.relative_to(ROOT)),
        "contractAsOf": contract.get("asOf"),
        "claimBoundary": contract.get("claimBoundary", {}),
        "groups": groups,
        "liveObservations": live_observations if live else None,
    }


def print_text(report: dict[str, Any]) -> None:
    print(
        f"Language registry gate report (contract as of {report.get('contractAsOf')})"
    )
    print(f"Source: {report.get('source')}")
    print()
    for name, items in report["groups"].items():
        print(f"## {name} ({len(items)})")
        for item in items:
            blocker = f" blocker={item['blocker']}" if item.get("blocker") else ""
            url = f" url={item['submission_url']}" if item.get("submission_url") else ""
            line = f"- {item['id']}: {item['package']} {item['version']}"
            line += f" status={item['status']}{url}{blocker}"
            print(line)
        print()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--promotion",
        action="store_true",
        help="Group registries by promotion state. Kept for runbook compatibility.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Add public HTTP probes for known registries and submission URLs.",
    )
    parser.add_argument("--output", type=Path, help="Write JSON report to this path.")
    parser.add_argument(
        "--json", action="store_true", help="Print JSON instead of text."
    )
    args = parser.parse_args(argv)

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    report = build_report(contract, live=args.live)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    if args.json or args.output:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
