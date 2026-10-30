from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs-site"
WORKFLOW = ROOT / ".github" / "workflows" / "docs-site.yml"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_starlight_scaffold_files_exist():
    expected_paths = [
        SITE / "package.json",
        SITE / "package-lock.json",
        SITE / "astro.config.mjs",
        SITE / "src" / "content" / "versions" / "2025.json",
        SITE / "src" / "content" / "docs" / "index.mdx",
        SITE / "src" / "content" / "docs" / "versions" / "index.mdx",
        SITE / "src" / "content" / "docs" / "governance" / "index.mdx",
        SITE / "src" / "content" / "docs" / "governance" / "calculator-coverage.mdx",
        SITE
        / "src"
        / "content"
        / "docs"
        / "governance"
        / "public-calculator-contract.mdx",
        SITE / "public" / "contracts" / "public-calculator-contract.v1.schema.json",
        SITE / "src" / "content" / "docs" / "governance" / "starlight-extensions.mdx",
        SITE / "src" / "content" / "docs" / "versions" / "2025.md",
        SITE / "src" / "content" / "docs" / "migration" / "legacy-docs.md",
        WORKFLOW,
    ]

    for path in expected_paths:
        assert path.exists(), path


def test_starlight_package_declares_required_plugins_and_scripts():
    package_json = json.loads(_read_text(SITE / "package.json"))

    assert package_json["private"] is True
    assert package_json["name"] == "docs-site"
    assert package_json["scripts"] == {
        "dev": "astro dev",
        "build": "astro build",
        "preview": "astro preview",
        "linkcheck": "astro build",
    }

    dependencies = package_json["dependencies"]
    assert dependencies["@astrojs/starlight"] == "0.42.8"
    assert dependencies["astro"] == "7.4.4"
    assert "starlight-links-validator" in dependencies
    assert "starlight-versions" in dependencies
    assert package_json["dependencies"]["starlight-versions"] == "0.10.1"


def test_starlight_config_documents_the_static_docs_site_contract():
    config = _read_text(SITE / "astro.config.mjs")

    assert "@astrojs/starlight" in config
    assert "starlightLinksValidator" in config
    assert "starlightVersions" in config
    assert "GITHUB_REPOSITORY" in config
    assert "SITE_URL" in config
    assert "SITE_BASE" in config
    assert "editLink" in config
    assert "customCss" in config
    assert "versions" in config


def test_docs_site_workflow_builds_and_deploys_the_site():
    workflow = _read_text(WORKFLOW)

    assert "docs-site" in workflow
    assert "branches: [master]" in workflow
    assert '      - "docs-site/**"' in workflow
    assert '      - "conductor/**"' in workflow
    assert "npm ci" in workflow
    assert "npm run build" in workflow
    assert "linkcheck" in workflow
    assert "pages" in workflow
