"""Validate repository topology and package-surface ownership."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SURFACES = ROOT / "contracts" / "repository-topology" / "package-surfaces.json"

MANIFEST_NAMES = {
    "Cargo.toml",
    "DESCRIPTION",
    "DotNetBinding.csproj",
    "Package.swift",
    "Project.toml",
    "build.gradle.kts",
    "build.sbt",
    "conanfile.py",
    "go.mod",
    "meta.yaml",
    "package.json",
    "portfile.cmake",
    "pyproject.toml",
    "settings.gradle.kts",
    "vcpkg.json",
}

PRUNE_DIRS = {
    ".cache",
    ".git",
    ".gradle",
    ".hypothesis",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".build",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "target",
}

GENERATED_PATH_PARTS = {
    ".build",
    ".cache",
    ".gradle",
    ".hypothesis",
    ".mypy_cache",
    ".playwright-mcp",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "target",
}

GENERATED_PREFIXES = (
    "build/",
    "dist/",
)

GENERATED_FILE_SUFFIXES = (
    ".tar.gz",
    ".vsix",
    ".whl",
    ".zip",
)

EVIDENCE_ARTIFACT_PATTERNS = (
    re.compile(r"^archive/sas/.+/base_library\.zip$"),
    re.compile(r"^bindings/matlab/mchs-matlab-interop-[0-9][^/]*\.zip$"),
    re.compile(r"^bindings/stata/mchs-stata-interop-[0-9][^/]*\.zip$"),
    re.compile(r"^integrations/vscode/mchs-tools-[0-9][^/]*\.vsix$"),
)

GITMODULE_PATH_RE = re.compile(r"^\s*path\s*=\s*(?P<path>.+?)\s*$")


@dataclass(frozen=True)
class Diagnostic:
    """A topology validation diagnostic."""

    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        """Return a JSON-serializable representation."""
        return {"code": self.code, "message": self.message, "path": self.path}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return payload


def _relative(path: Path, root: Path = ROOT) -> str:
    return path.relative_to(root).as_posix()


def _run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def _gitmodules_paths(root: Path) -> set[str]:
    gitmodules = root / ".gitmodules"
    if not gitmodules.exists():
        return set()
    paths: set[str] = set()
    for line in gitmodules.read_text(encoding="utf-8").splitlines():
        match = GITMODULE_PATH_RE.match(line)
        if match:
            paths.add(match.group("path"))
    return paths


def _gitlinks(root: Path) -> set[str]:
    output = _run_git(root, "ls-files", "-s")
    links: set[str] = set()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "160000":
            links.add(parts[3])
    return links


def _tracked_files(root: Path) -> list[str]:
    output = _run_git(root, "ls-files")
    return [line for line in output.splitlines() if line]


def _find_nested_git_dirs(root: Path) -> list[str]:
    nested: list[str] = []
    for current, dirs, _files in os.walk(root):
        current_path = Path(current)
        dirs[:] = [name for name in dirs if name not in PRUNE_DIRS or name == ".git"]
        if current_path == root:
            if ".git" in dirs:
                dirs.remove(".git")
            continue
        if current_path.name == ".git":
            nested.append(_relative(current_path, root))
            dirs[:] = []
    return nested


def _discover_manifests(root: Path) -> set[str]:
    manifests: set[str] = set()
    for current, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in PRUNE_DIRS]
        current_path = Path(current)
        for filename in files:
            if filename in MANIFEST_NAMES:
                manifests.add(
                    current_path.joinpath(filename).relative_to(root).as_posix()
                )
    return manifests


def _is_generated_path(path: str) -> bool:
    parts = set(Path(path).parts)
    if parts & GENERATED_PATH_PARTS:
        return True
    return any(path.startswith(prefix) for prefix in GENERATED_PREFIXES) or any(
        path.endswith(suffix) for suffix in GENERATED_FILE_SUFFIXES
    )


def _is_evidence_artifact(path: str) -> bool:
    return any(pattern.match(path) for pattern in EVIDENCE_ARTIFACT_PATTERNS)


def _validate_gitlinks(root: Path) -> list[Diagnostic]:
    mapped = _gitmodules_paths(root)
    return [
        Diagnostic(
            code="unmanaged_gitlink",
            path=link,
            message="Gitlink is present without a matching .gitmodules path.",
        )
        for link in sorted(_gitlinks(root))
        if link not in mapped
    ]


def _validate_current_repo(data: dict[str, Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if data.get("canonical_root") != "microcosting_healthservices":
        diagnostics.append(
            Diagnostic(
                code="invalid_canonical_root",
                message=(
                    "package-surfaces.json must declare microcosting_healthservices."
                ),
                path=str(SURFACES.relative_to(ROOT)),
            )
        )

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        return [
            Diagnostic(
                code="missing_surfaces",
                message="package-surfaces.json must contain a non-empty surfaces list.",
                path=str(SURFACES.relative_to(ROOT)),
            )
        ]

    registered_manifests: dict[str, list[str]] = {}
    seen_surface_ids: set[str] = set()

    for surface in surfaces:
        if not isinstance(surface, dict):
            diagnostics.append(
                Diagnostic(
                    code="invalid_surface",
                    message="Surface entry is not an object.",
                )
            )
            continue
        surface_id = str(surface.get("id", ""))
        if not surface_id or surface_id in seen_surface_ids:
            diagnostics.append(
                Diagnostic(
                    code="duplicate_surface_id",
                    message=f"Surface id is missing or duplicated: {surface_id}",
                    path=surface_id or None,
                )
            )
        seen_surface_ids.add(surface_id)

        owner_track = surface.get("owner_track")
        if not isinstance(owner_track, str) or not owner_track:
            diagnostics.append(
                Diagnostic(
                    code="missing_owner_track",
                    message=f"Surface {surface_id} lacks an owner track.",
                    path=surface_id,
                )
            )
        elif not (
            (ROOT / "conductor" / "tracks" / owner_track).exists()
            or (ROOT / "conductor" / "archive" / owner_track).exists()
        ):
            diagnostics.append(
                Diagnostic(
                    code="missing_owner_track",
                    message=f"Owner track does not exist for surface {surface_id}.",
                    path=owner_track,
                )
            )

        manifests = surface.get("manifests")
        if not isinstance(manifests, list):
            diagnostics.append(
                Diagnostic(
                    code="invalid_manifests",
                    message=f"Surface {surface_id} manifests must be a list.",
                    path=surface_id,
                )
            )
            continue

        for manifest in manifests:
            if not isinstance(manifest, str) or not manifest:
                diagnostics.append(
                    Diagnostic(
                        code="invalid_manifest",
                        message=f"Surface {surface_id} has an invalid manifest.",
                        path=surface_id,
                    )
                )
                continue
            registered_manifests.setdefault(manifest, []).append(surface_id)
            if not (ROOT / manifest).exists():
                diagnostics.append(
                    Diagnostic(
                        code="missing_manifest",
                        message=f"Manifest for surface {surface_id} does not exist.",
                        path=manifest,
                    )
                )

        release = surface.get("release")
        if not isinstance(release, dict):
            diagnostics.append(
                Diagnostic(
                    code="missing_release_boundary",
                    message=f"Surface {surface_id} lacks release boundary data.",
                    path=surface_id,
                )
            )
            continue
        state = release.get("registry_state")
        evidence = release.get("evidence")
        external_gate = release.get("external_gate")
        if state == "published_verified" and not evidence:
            diagnostics.append(
                Diagnostic(
                    code="missing_publication_evidence",
                    message=(
                        f"Surface {surface_id} claims publication without evidence."
                    ),
                    path=surface_id,
                )
            )
        if state in {"submitted", "blocked"} and not external_gate:
            diagnostics.append(
                Diagnostic(
                    code="missing_external_gate",
                    message=f"Surface {surface_id} must name its external gate.",
                    path=surface_id,
                )
            )

    discovered = _discover_manifests(ROOT)
    diagnostics.extend(
        [
            Diagnostic(
                code="unregistered_manifest",
                message="Package manifest is not registered to a package surface.",
                path=manifest,
            )
            for manifest in sorted(discovered - set(registered_manifests))
        ]
    )

    for manifest, owners in sorted(registered_manifests.items()):
        if len(owners) > 1:
            categories = {
                str(surface.get("category"))
                for surface in surfaces
                if isinstance(surface, dict) and surface.get("id") in owners
            }
            if "registry" not in categories:
                diagnostics.append(
                    Diagnostic(
                        code="duplicate_manifest_owner",
                        message=f"Manifest has multiple non-registry owners: {owners}",
                        path=manifest,
                    )
                )

    diagnostics.extend(
        [
            Diagnostic(
                code="nested_git_dir",
                message=(
                    "Nested .git directory is not allowed below the canonical root."
                ),
                path=nested,
            )
            for nested in _find_nested_git_dirs(ROOT)
        ]
    )

    diagnostics.extend(_validate_gitlinks(ROOT))

    diagnostics.extend(
        [
            Diagnostic(
                code="tracked_generated_artifact",
                message="Generated artifact path is tracked as source.",
                path=path,
            )
            for path in _tracked_files(ROOT)
            if _is_generated_path(path) and not _is_evidence_artifact(path)
        ]
    )

    return diagnostics


def _validate_outer_root(outer_root: Path) -> list[Diagnostic]:
    diagnostics = _validate_gitlinks(outer_root)
    for nested in _find_nested_git_dirs(outer_root):
        if nested == "microcosting_healthservices/.git":
            diagnostics.append(
                Diagnostic(
                    code="outer_wrapper_contains_nested_repo",
                    message=(
                        "Outer wrapper contains the canonical repo as a "
                        "nested Git repo."
                    ),
                    path=nested,
                )
            )
    return diagnostics


def _print_text(diagnostics: list[Diagnostic]) -> None:
    if not diagnostics:
        print("Repository topology validation passed.")
        return
    print("Repository topology validation failed:")
    for diagnostic in diagnostics:
        location = f" ({diagnostic.path})" if diagnostic.path else ""
        print(f"- {diagnostic.code}{location}: {diagnostic.message}")


def main(argv: list[str] | None = None) -> int:
    """Run repository topology validation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable output",
    )
    parser.add_argument(
        "--outer-root",
        type=Path,
        help="Explicitly validate a wrapper/superproject root",
    )
    args = parser.parse_args(argv)

    data = _load_json(SURFACES)
    diagnostics = _validate_current_repo(data)
    if args.outer_root is not None:
        diagnostics.extend(_validate_outer_root(args.outer_root.resolve()))

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not diagnostics,
                    "diagnostics": [diagnostic.as_dict() for diagnostic in diagnostics],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        _print_text(diagnostics)
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
