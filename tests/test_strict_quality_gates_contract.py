from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "quality-gates" / "strict-quality-gates.contract.json"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_strict_quality_gate_contract_covers_required_gate_classes() -> None:
    contract = _contract()
    required = set(contract["requiredGateClasses"])

    assert contract["minimumCoveragePercent"] == 90
    assert required == {
        "format",
        "lint",
        "docstring",
        "typing",
        "unit",
        "integration",
        "wheel_smoke",
        "rust_format",
        "rust_lint",
        "rust_unit",
        "coverage",
        "property_based",
        "mutation",
        "profiling",
        "security",
        "dependency_review",
        "dependency_automation",
        "release_metadata",
        "versioning",
    }


def test_strict_quality_gate_contract_references_existing_artifacts() -> None:
    contract = _contract()

    workflow_evidence = contract["workflowEvidence"]
    assert isinstance(workflow_evidence, dict)
    for evidence_path in workflow_evidence.values():
        assert isinstance(evidence_path, str)
        assert (ROOT / evidence_path).exists(), evidence_path

    surfaces = contract["surfaces"]
    assert isinstance(surfaces, list)
    surface_ids = {surface["id"] for surface in surfaces}
    assert {
        "python",
        "rust",
        "r",
        "typescript_wasm",
        "go",
        "dotnet",
        "jvm",
        "julia",
        "matlab",
        "stata",
        "kotlin_native",
    }.issubset(surface_ids)

    for surface in surfaces:
        assert surface["package"], surface["id"]
        assert surface["versionField"], surface["id"]
        artifacts = surface["artifacts"]
        assert isinstance(artifacts, list)
        assert artifacts, surface["id"]
        for artifact in artifacts:
            assert (ROOT / artifact).exists(), f"{surface['id']} -> {artifact}"


def test_current_workflows_enforce_strict_quality_security_and_coverage() -> None:
    pr_ci = _read(".github/workflows/pr-ci.yml")
    slow_validation = _read(".github/workflows/slow-validation.yml")
    slow_validation_reusable = _read(".github/workflows/slow-validation-reusable.yml")
    codeql = _read(".github/workflows/codeql.yml")
    dependency_review = _read(".github/dependency-review-config.yml")

    assert "uv run ruff format --check ." in pr_ci
    assert "uv run ruff check ." in pr_ci
    assert "uv run ruff check --select D2" in pr_ci
    assert "uv run ty check --error all" in pr_ci
    assert "uv run ruff check --select S ." in pr_ci
    assert "uv run bandit -r nwau_py scripts -x tests" in pr_ci
    assert "uv run --with pip-audit --with pip==26.1.2 pip-audit" in pr_ci
    assert "cargo fmt --all --check" in pr_ci
    assert "cargo audit" in pr_ci
    assert "cargo clippy --all-targets --all-features -- -D warnings" in pr_ci
    assert "cargo test" in pr_ci
    assert "--cov-fail-under=90" in pr_ci
    assert "--cov-fail-under=80" not in pr_ci
    assert "fail_ci_if_error: true" in pr_ci
    assert "maturin build --release" in pr_ci
    assert "Smoke test Rust binding from the installed wheel" in pr_ci

    for workflow in (slow_validation, slow_validation_reusable):
        assert "Property checks" in workflow
        assert "Mutation checks" in workflow
        assert "Profiling checks" in workflow
        assert "uv run mutmut run" in workflow
        assert "uv run scalene" in workflow

    assert "github/codeql-action/analyze@v4" in codeql
    assert "fail-on-severity: moderate" in dependency_review
    assert "fail-on-severity: high" in pr_ci


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
