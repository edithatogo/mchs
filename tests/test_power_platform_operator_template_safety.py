from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OPERATOR_TEMPLATE_FILES = [
    ROOT / "docs" / "runbooks" / "github-live-gate.env.example",
    ROOT / "power-platform" / "deployment" / "nsw-deployment-readiness-template.md",
    ROOT
    / "power-platform"
    / "evidence"
    / "connection-reference-evidence-template.json",
    ROOT / "power-platform" / "evidence" / "explicit-waiver-input-template.json",
    ROOT / "power-platform" / "evidence" / "flow-smoke-capture-sample.json",
    ROOT / "power-platform" / "evidence" / "flow-smoke-evidence-template.json",
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-capture-sample.json",
    ROOT / "power-platform" / "evidence" / "monitoring-dlp-evidence-template.json",
    ROOT
    / "power-platform"
    / "evidence"
    / "nsw-operational-readiness-bundle-template.json",
    ROOT
    / "power-platform"
    / "evidence"
    / "official-github-live-gate-evidence-template.json",
    ROOT / "power-platform" / "evidence" / "runtime-smoke-evidence-template.json",
    ROOT / "power-platform" / "evidence" / "service-boundary-endpoint-template.json",
    ROOT
    / "power-platform"
    / "evidence"
    / "standalone-subrepo-remote-input-template.json",
]

SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ASIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
)

LIVE_CLAIM_PATTERNS = (
    re.compile(r'(?i)"productionReadinessClaimed"\s*:\s*true'),
    re.compile(r'(?i)"officialLiveGateCompleted"\s*:\s*true'),
    re.compile(r'(?i)"tenantRuntimeClaimsAllowed"\s*:\s*true'),
    re.compile(r'(?i)"nsw_real_deployment_claim"\s*:\s*true'),
    re.compile(r"(?i)\bproduction ready\b"),
    re.compile(r"(?i)\bproduction readiness complete\b"),
    re.compile(r"(?i)\bactive NSW production deployment\b"),
    re.compile(r"(?i)\bdeployed to production\b"),
    re.compile(r"(?i)\balready live\b"),
    re.compile(r"(?i)\blive production\b"),
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict:
    return json.loads(_read_text(path))


def _assert_no_patterns(
    path: Path,
    text: str,
    patterns: tuple[re.Pattern[str], ...],
) -> None:
    for pattern in patterns:
        assert not pattern.search(text), (
            f"{path}: matched forbidden pattern {pattern.pattern!r}"
        )


def test_operator_sample_and_template_files_stay_placeholder_only() -> None:
    for path in OPERATOR_TEMPLATE_FILES:
        text = _read_text(path)
        _assert_no_patterns(path, text, SECRET_PATTERNS)

        if path.suffix == ".md":
            lowered = text.lower()
            assert "do not claim" in lowered or "does not claim" in lowered
        else:
            _assert_no_patterns(path, text, LIVE_CLAIM_PATTERNS)

        if path.name == "github-live-gate.env.example":
            values = {}
            for line in text.splitlines():
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", maxsplit=1)
                values[key] = value

            assert values["GITHUB_TOKEN"] == "provided_by_github_actions"
            assert values["GH_TOKEN"] == "provided_by_github_actions"


def test_operator_template_claims_remain_blocked() -> None:
    readiness_bundle = _read_json(
        ROOT
        / "power-platform"
        / "evidence"
        / "nsw-operational-readiness-bundle-template.json"
    )
    service_boundary_template = _read_json(
        ROOT / "power-platform" / "evidence" / "service-boundary-endpoint-template.json"
    )
    live_gate_template = _read_json(
        ROOT
        / "power-platform"
        / "evidence"
        / "official-github-live-gate-evidence-template.json"
    )

    assert readiness_bundle["governance"]["nsw_real_deployment_claim"] is False
    assert readiness_bundle["governance"]["managed_solution_import_claim"] is True
    assert (
        service_boundary_template["claimBoundary"]["productionReadinessClaimed"]
        is False
    )
    assert live_gate_template["claimBoundary"]["productionReadinessClaimed"] is False
