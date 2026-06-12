from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "quality-gates" / "strict-quality-gates.contract.json"


def test_strict_quality_gate_contract_covers_all_gate_classes() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    required = set(contract["requiredGateClasses"])

    assert contract["minimumCoveragePercent"] >= 90
    assert required == {
        "unit",
        "integration",
        "end_to_end",
        "smoke",
        "edge",
        "property_based",
        "mutation",
        "profiling",
        "load_or_load_balancing",
        "security",
        "versioning",
    }

    surfaces = contract["surfaces"]
    assert surfaces
    for surface in surfaces:
        assert set(surface["requiredGateClasses"]) == required, surface["id"]
        assert surface["manifest"], surface["id"]
        assert surface["versionField"], surface["id"]
        assert surface["gateEvidence"], surface["id"]


def test_strict_coverage_thresholds_are_enforced_in_workflows() -> None:
    pr_ci = (ROOT / ".github" / "workflows" / "pr-ci.yml").read_text(
        encoding="utf-8"
    )
    coverage = (ROOT / ".github" / "workflows" / "coverage.yml").read_text(
        encoding="utf-8"
    )
    rust_ci = (ROOT / ".github" / "workflows" / "rust-ci.yml").read_text(
        encoding="utf-8"
    )

    assert "--cov-fail-under=90" in pr_ci
    assert "--cov-fail-under=80" not in pr_ci
    assert "threshold 90.0%" in coverage
    assert "threshold 90.0%" in rust_ci
    assert "PASS: Coverage ${coverage_pct}% meets threshold 90.0%" in rust_ci


def test_dependency_automation_covers_public_package_managers() -> None:
    renovate = json.loads((ROOT / "renovate.json").read_text(encoding="utf-8"))
    managers = set(renovate["enabledManagers"])

    assert {
        "pep621",
        "pip_requirements",
        "github-actions",
        "cargo",
        "npm",
        "gomod",
        "gradle",
        "nuget",
        "dockerfile",
    }.issubset(managers)
