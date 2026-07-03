from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENOVATE_FILE = ROOT / "renovate.json"
VALE_STYLE_FILE = ROOT / ".vale" / "styles" / "Project" / "ValidationClaims.yml"
TECH_STACK_FILE = ROOT / "conductor" / "tech-stack.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_renovate_package_rules_pin_the_phase_4_maintenance_contract():
    renovate = json.loads(_read_text(RENOVATE_FILE))

    assert "cargo" in renovate["enabledManagers"]
    assert "npm" in renovate["enabledManagers"]
    assert "gomod" in renovate["enabledManagers"]
    assert "gradle" in renovate["enabledManagers"]
    assert "nuget" in renovate["enabledManagers"]
    assert "dockerfile" in renovate["enabledManagers"]

    expected_package_rules = [
        {
            "matchManagers": ["pep621", "pip_requirements"],
            "matchPackageNames": [
                "click",
                "lightgbm",
                "numpy",
                "pandas",
                "pyarrow",
                "pydantic",
                "polars",
                "pyreadstat",
                "pyxlsb",
            ],
            "groupName": "Runtime calculator dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["pep621", "pip_requirements"],
            "matchPackageNames": [
                "hypothesis",
                "mutmut",
                "pytest",
                "pytest-cov",
                "ruff",
                "scalene",
                "ty",
                "vale",
            ],
            "groupName": "Toolchain and validation dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["github-actions"],
            "groupName": "GitHub Actions",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["cargo"],
            "groupName": "Rust dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["npm"],
            "groupName": "Node package dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["gomod"],
            "groupName": "Go module dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["gradle"],
            "groupName": "Gradle package dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["nuget"],
            "groupName": "NuGet package dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
        {
            "matchManagers": ["dockerfile"],
            "groupName": "Dockerfile dependencies",
            "dependencyDashboardApproval": True,
            "separateMinorPatch": True,
        },
    ]

    assert renovate["packageRules"] == expected_package_rules


def test_vale_validation_claims_style_pins_the_expected_tokens_and_message():
    style = _read_text(VALE_STYLE_FILE)
    lines = style.splitlines()

    expected_tokens = [
        r"\bfully\s+validated\b",
        r"\bcompletely\s+validated\b",
        r"\bcomplete\s+validation\b",
        r"\bproject[-\s]+wide\s+validation\b",
        r"\brepo[-\s]+wide\s+validation\b",
        r"\bend[-\s]+to[-\s]+end\s+validation\b",
        r"\ball\s+calculators\b",
        r"\ball\s+years\b",
        r"\ball\s+years\s+validated\b",
        r"\ball\s+years\s+supported\b",
        r"\bsupports\s+\d{4}\b",
        r"\bvalidated\s+across\s+the\s+board\b",
        r"\bvalidated\s+for\s+all\s+years\b",
        r"\bvalidated\s+against\s+official\s+SAS\s+results\b",
        r"\bmatches\s+the\s+official\s+SAS\s+results\b",
    ]

    assert "extends: existence" in lines
    assert (
        "message: Use a precise calculator/year claim with supporting evidence "
        "instead of a broad validation statement."
    ) in lines
    assert "level: warning" in lines
    assert "ignorecase: true" in lines
    tokens = [
        line.split("- ", 1)[1].strip().strip("'")
        for line in lines
        if line.startswith("  - ")
    ]
    assert tokens == expected_tokens


def test_tech_stack_documents_the_starlight_docs_site_contract():
    tech_stack = _read_text(TECH_STACK_FILE)

    assert "## Starlight Documentation Site" in tech_stack
    assert "@astrojs/starlight" in tech_stack
    assert "0.39.2" in tech_stack
    assert "starlight-links-validator" in tech_stack
    assert "starlight-openapi" in tech_stack
