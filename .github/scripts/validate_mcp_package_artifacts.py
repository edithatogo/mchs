#!/usr/bin/env python
"""Validate MCP-related package artifact contents before publishing."""

from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path


def _single_artifact(pattern: str) -> Path:
    matches = sorted(Path("dist").glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one artifact matching {pattern}, found {len(matches)}"
        )
    return matches[0]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def validate_wheel(wheel_path: Path) -> None:
    """Validate the wheel contains MCP runtime metadata and no test/archive tree."""
    with zipfile.ZipFile(wheel_path) as wheel:
        names = set(wheel.namelist())
        dist_info = next(
            name.rsplit("/", maxsplit=1)[0]
            for name in names
            if name.endswith(".dist-info/METADATA")
        )
        entry_points = wheel.read(f"{dist_info}/entry_points.txt").decode()
        metadata = wheel.read(f"{dist_info}/METADATA").decode()
        package_readme = wheel.read("nwau_py/README.md").decode()

    _assert("nwau_py/mcp_server.py" in names, "wheel is missing nwau_py/mcp_server.py")
    _assert(
        "nwau_py/mcp_http_server.py" in names,
        "wheel is missing nwau_py/mcp_http_server.py",
    )
    _assert("mchs-mcp" in entry_points, "wheel is missing mchs-mcp entry point")
    _assert(
        "mchs-mcp-http" in entry_points,
        "wheel is missing mchs-mcp-http entry point",
    )
    _assert(
        "mcp-name: io.github.edithatogo/mchs" in package_readme,
        "wheel package README is missing MCP Registry verification marker",
    )
    _assert("License-Expression: MIT" in metadata, "wheel metadata lacks SPDX license")
    _assert(
        not any(name.startswith("tests/") for name in names),
        "wheel must not include tests/",
    )
    _assert(
        not any(name.startswith("archive/") for name in names),
        "wheel must not include archive/",
    )
    for package_data in [
        "nwau_py/data/complexitygroups_2025.csv",
        "nwau_py/data/indigenous_distribution.json",
        "nwau_py/data/remoteness_distribution.json",
        "nwau_py/mcp_assets/canonical/calculator.schema.json",
        "nwau_py/mcp_assets/canonical/diagnostics.schema.json",
        "nwau_py/mcp_assets/canonical/evidence.schema.json",
        "nwau_py/mcp_assets/canonical/provenance.schema.json",
        "nwau_py/mcp_assets/canonical/support-status.schema.json",
    ]:
        _assert(package_data in names, f"wheel is missing {package_data}")


def validate_sdist(sdist_path: Path) -> None:
    """Validate the source distribution contains MCP runtime metadata only."""
    with tarfile.open(sdist_path) as sdist:
        names = set(sdist.getnames())
        prefix = sdist_path.name.removesuffix(".tar.gz")
        package_readme = sdist.extractfile(f"{prefix}/nwau_py/README.md")
        _assert(package_readme is not None, "sdist is missing nwau_py/README.md")
        readme_text = package_readme.read().decode()

    _assert(
        f"{prefix}/nwau_py/mcp_server.py" in names,
        "sdist is missing nwau_py/mcp_server.py",
    )
    _assert(
        f"{prefix}/nwau_py/mcp_http_server.py" in names,
        "sdist is missing nwau_py/mcp_http_server.py",
    )
    _assert(
        f"{prefix}/nwau_py/mcp_assets/canonical/calculator.schema.json" in names,
        "sdist is missing packaged canonical MCP schemas",
    )
    _assert(
        "mcp-name: io.github.edithatogo/mchs" in readme_text,
        "sdist package README is missing MCP Registry verification marker",
    )
    _assert(
        not any(name.startswith(f"{prefix}/tests/") for name in names),
        "sdist must not include tests/",
    )
    _assert(
        not any(name.startswith(f"{prefix}/archive/") for name in names),
        "sdist must not include archive/",
    )


def main() -> int:
    validate_wheel(_single_artifact("*.whl"))
    validate_sdist(_single_artifact("*.tar.gz"))
    print("MCP package artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
