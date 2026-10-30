#!/usr/bin/env python
"""Validate release metadata consistency across project version sources."""

from __future__ import annotations

import os
import re
import tomllib
from pathlib import Path
from typing import Final

REF_NAME_ENV: Final[str] = "GITHUB_REF_NAME"
REF_NAME_OVERRIDE: Final[str] = "RELEASE_REF_NAME"
REF_TYPE_ENV: Final[str] = "GITHUB_REF_TYPE"
REF_TYPE_OVERRIDE: Final[str] = "RELEASE_REF_TYPE"


def parse_pyproject_version(pyproject_path: Path = Path("pyproject.toml")) -> str:
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    version = pyproject["project"]["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        raise RuntimeError(f"Pyproject version '{version}' must be SemVer-compatible")
    return version


def parse_conda_version(recipe_path: Path = Path("conda/recipe/meta.yaml")) -> str:
    match = re.search(
        r'{%\s*set\s+version\s*=\s*"([^"]+)"\s*%}',
        recipe_path.read_text(encoding="utf-8"),
    )
    if not match:
        raise RuntimeError("Could not parse conda version from conda/recipe/meta.yaml")
    version = match.group(1)
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        raise RuntimeError(
            f"Conda recipe version '{version}' must be SemVer-compatible"
        )
    return version


def parse_tag_version() -> str:
    ref_name = os.environ.get(REF_NAME_OVERRIDE) or os.environ.get(REF_NAME_ENV, "")
    ref_type = os.environ.get(REF_TYPE_OVERRIDE) or os.environ.get(REF_TYPE_ENV, "")
    if not ref_name:
        raise RuntimeError(
            "Could not resolve release ref name from workflow environment"
        )
    if ref_type != "tag":
        raise RuntimeError(
            "Version validation only applies to tag-based release events"
        )
    match = re.fullmatch(
        r"v(?P<version>\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)",
        ref_name,
    )
    if not match:
        raise RuntimeError(
            f"Invalid release ref '{ref_name}' "
            "(expected SemVer-compatible tag vMAJOR.MINOR.PATCH)"
        )
    return match.group("version")


def validate_mcp_registry_metadata(project_version: str) -> None:
    server_json_path = Path("contracts/mcp/registry/server.json")
    package_readme_path = Path("nwau_py/README.md")
    if not server_json_path.exists():
        raise RuntimeError(
            "Missing MCP Registry metadata at contracts/mcp/registry/server.json"
        )
    if not package_readme_path.exists():
        raise RuntimeError(
            "Missing package README required for PyPI MCP ownership verification"
        )

    import json

    metadata = json.loads(server_json_path.read_text(encoding="utf-8"))
    server_name = metadata.get("name")
    if server_name != "io.github.edithatogo/mchs":
        raise RuntimeError("MCP Registry server name must be io.github.edithatogo/mchs")
    if metadata.get("version") != project_version:
        raise RuntimeError(
            f"MCP Registry server version {metadata.get('version')} "
            f"does not match pyproject version {project_version}"
        )
    marker = f"mcp-name: {server_name}"
    if marker not in package_readme_path.read_text(encoding="utf-8"):
        raise RuntimeError(
            f"Package README must contain MCP Registry verification marker '{marker}'"
        )

    packages = metadata.get("packages") or []
    pypi_packages = [
        package for package in packages if package.get("registryType") == "pypi"
    ]
    if not pypi_packages:
        raise RuntimeError("MCP Registry metadata must include a PyPI package entry")
    package = pypi_packages[0]
    if package.get("identifier") != "nwau-py":
        raise RuntimeError("MCP Registry PyPI identifier must be nwau-py")
    if package.get("version") != project_version:
        raise RuntimeError(
            f"MCP Registry package version {package.get('version')} "
            f"does not match pyproject version {project_version}"
        )
    if package.get("transport", {}).get("type") != "stdio":
        raise RuntimeError("MCP Registry package transport must be stdio")


def main() -> int:
    project_version = parse_pyproject_version()
    conda_version = parse_conda_version()
    tag_version = parse_tag_version()

    if tag_version != project_version:
        raise RuntimeError(
            f"Tag version {tag_version} does not match "
            f"pyproject version {project_version}"
        )
    if conda_version != project_version:
        raise RuntimeError(
            f"Conda recipe version {conda_version} does not match "
            f"pyproject version {project_version}"
        )
    validate_mcp_registry_metadata(project_version)

    print(f"Release metadata validated for v{project_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
