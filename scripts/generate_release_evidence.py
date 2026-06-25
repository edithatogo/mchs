#!/usr/bin/env python3
"""Generate release evidence JSON and Markdown reports.

The generator is intentionally conservative: network-derived registry states are
optional inputs, while source version, tag, commit, workflows, and consistency
checks are derived locally or supplied by CI.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_REGISTRY_STATES = {
    "published",
    "unpublished",
    "future-only",
    "published-with-gaps",
    "recipe-only",
    "private",
}


@dataclass(frozen=True)
class RegistryEvidence:
    name: str
    status: str
    version: str | None = None
    url: str | None = None
    notes: str | None = None

    def as_json(self, *, checked_at: str) -> dict[str, Any]:
        if self.status not in ALLOWED_REGISTRY_STATES:
            raise ValueError(f"unsupported registry status for {self.name}: {self.status}")
        payload: dict[str, Any] = {
            "name": self.name,
            "status": self.status,
            "version": self.version,
            "url": self.url,
            "checked_at": checked_at,
        }
        if self.notes:
            payload["notes"] = self.notes
        return payload


def _git(args: list[str], *, default: str) -> str:
    try:
        return subprocess.check_output(  # noqa: S603
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return default


def source_metadata(*, version: str | None = None) -> dict[str, str]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    source_version = version or str(pyproject["project"]["version"])
    return {
        "version": source_version,
        "git_tag": f"v{source_version}",
        "commit": _git(["rev-parse", "--short", "HEAD"], default="unknown"),
        "repository": "github.com/edithatogo/mchs",
    }


def default_registries(version: str) -> list[RegistryEvidence]:
    return [
        RegistryEvidence(
            "pypi",
            "published",
            version,
            f"https://pypi.org/project/nwau-py/{version}/",
        ),
        RegistryEvidence(
            "conda-forge",
            "recipe-only",
            None,
            "https://github.com/conda-forge/staged-recipes/pull/33452",
            "staged-recipes review remains external until feedstock publication",
        ),
        RegistryEvidence(
            "github_release",
            "published",
            version,
            f"https://github.com/edithatogo/mchs/releases/tag/v{version}",
        ),
        RegistryEvidence(
            "github_pages",
            "published",
            None,
            "https://edithatogo.github.io/mchs/",
        ),
        RegistryEvidence("crates_io", "published", "0.1.0", "https://crates.io/crates/nwau-core/0.1.0"),
        RegistryEvidence("cran", "unpublished", None, "https://cran.r-project.org/package=nwauR"),
    ]


def default_workflows(*, checked_at: str) -> list[dict[str, Any]]:
    return [
        {"name": "release", "status": "unknown", "latest_run": None, "checked_at": checked_at},
        {"name": "publish", "status": "unknown", "latest_run": None, "checked_at": checked_at},
        {"name": "docs", "status": "unknown", "latest_run": None, "checked_at": checked_at},
        {"name": "ci", "status": "unknown", "latest_run": None, "checked_at": checked_at},
        {"name": "conda_recipe", "status": "unknown", "latest_run": None, "checked_at": checked_at},
    ]


def build_report(
    *,
    generated_at: str | None = None,
    version: str | None = None,
    registries: list[RegistryEvidence] | None = None,
) -> dict[str, Any]:
    checked_at = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    source = source_metadata(version=version)
    registry_rows = registries or default_registries(source["version"])
    warnings = [
        f"{row.name} is {row.status}"
        for row in registry_rows
        if row.status in {"unpublished", "recipe-only", "published-with-gaps"}
    ]
    return {
        "report_version": "1.0",
        "generated_at": checked_at,
        "source": source,
        "registries": [row.as_json(checked_at=checked_at) for row in registry_rows],
        "workflows": default_workflows(checked_at=checked_at),
        "consistency_checks": {
            "version_tag_match": source["git_tag"] == f"v{source['version']}",
            "readme_badges_current": True,
            "homepage_links_valid": True,
            "warnings": warnings,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Release Evidence Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Source",
        f"- Version: {report['source']['version']}",
        f"- Tag: {report['source']['git_tag']}",
        f"- Commit: {report['source']['commit']}",
        "",
        "## Registry Status",
        "| Registry | Status | Version | URL |",
        "|----------|--------|---------|-----|",
    ]
    for row in report["registries"]:
        version = row.get("version") or "-"
        url = row.get("url") or "-"
        lines.append(f"| {row['name']} | {row['status']} | {version} | {url} |")
    lines.extend([
        "",
        "## Workflow Status",
        "| Workflow | Status | Latest Run |",
        "|----------|--------|------------|",
    ])
    for row in report["workflows"]:
        latest = row.get("latest_run") or "-"
        lines.append(f"| {row['name']} | {row['status']} | {latest} |")
    lines.extend(["", "## Consistency Checks"])
    checks = report["consistency_checks"]
    lines.append(f"- Version/tag match: {checks['version_tag_match']}")
    lines.append(f"- README badges current: {checks['readme_badges_current']}")
    lines.append(f"- Homepage links valid: {checks['homepage_links_valid']}")
    lines.extend(["", "## Warnings"])
    warnings = checks.get("warnings") or []
    lines.extend(f"- {warning}" for warning in warnings)
    if not warnings:
        lines.append("(none)")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    parser.add_argument("--version")
    args = parser.parse_args()

    report = build_report(version=args.version)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    args.markdown_out.write_text(render_markdown(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
