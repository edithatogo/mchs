from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"
TRACKS_MD = ROOT / "conductor" / "tracks.md"
SURFACES = ROOT / "contracts" / "repository-topology" / "package-surfaces.json"
VALIDATOR = ROOT / "scripts" / "validate_repository_topology.py"

TRACK_IDS = [
    "repository_topology_authority_20260624",
    "outer_wrapper_retirement_migration_20260624",
    "package_surface_ownership_registry_20260624",
    "repository_topology_ci_gate_20260624",
    "release_boundary_control_plane_20260624",
    "generated_artifact_retention_policy_20260624",
    "worktree_branch_pr_hygiene_20260624",
    "future_repo_split_playbook_20260624",
]

REQUIRED_SURFACES = {
    "python-runtime",
    "rust-workspace",
    "docs-site",
    "r-binding",
    "julia-binding",
    "go-binding",
    "dotnet-binding",
    "swift-binding",
    "jvm-binding",
    "scala-spark-binding",
    "wasm-npm-binding",
    "vscode-extension",
    "power-platform-app",
    "stata-binding",
    "matlab-binding",
    "conda-forge-recipe",
    "homebrew-formula",
    "conan-recipe",
    "vcpkg-port",
    "cran-registry",
    "maven-central-registry",
    "smithery-mcpb-package",
}

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


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict:
    return json.loads(_read(path))


def _discover_manifests() -> set[str]:
    manifests: set[str] = set()
    for current, dirs, files in os.walk(ROOT):
        dirs[:] = [name for name in dirs if name not in PRUNE_DIRS]
        current_path = Path(current)
        for filename in files:
            if filename in MANIFEST_NAMES:
                manifests.add(
                    current_path.joinpath(filename).relative_to(ROOT).as_posix()
                )
    return manifests


def test_repository_topology_track_family_is_registered() -> None:
    tracks_md = _read(TRACKS_MD)
    for track_id in TRACK_IDS:
        track_dir = TRACKS / track_id
        archived = False
        if not track_dir.exists():
            track_dir = ROOT / "conductor" / "archive" / track_id
            archived = True
        assert track_dir.exists(), track_id
        for filename in ["metadata.json", "spec.md", "plan.md", "index.md"]:
            assert (track_dir / filename).exists(), f"{track_id}/{filename}"

        metadata = _load_json(track_dir / "metadata.json")
        assert metadata["track_id"] == track_id
        assert metadata["no_stub_enforce"] is True
        if archived:
            assert metadata["status"] == "completed"
            assert metadata["current_state"] == "complete"
            assert (track_dir / "review.md").exists(), track_id
            assert f"./archive/{track_id}/" in tracks_md
        else:
            assert metadata["status"] == "new"
            assert metadata["current_state"] == "in-progress"
            assert f"./tracks/{track_id}/" in tracks_md

        plan = _read(track_dir / "plan.md")
        assert "Conductor - User Manual Verification" in plan
        assert "(Protocol in workflow.md)" in plan


def test_conductor_track_short_names_are_unique() -> None:
    by_short_name: dict[str, list[str]] = {}
    for track_dir in TRACKS.iterdir():
        if not track_dir.is_dir():
            continue
        parts = track_dir.name.rsplit("_", 1)
        short_name = (
            parts[0]
            if len(parts) == 2 and len(parts[1]) == 8 and parts[1].isdigit()
            else track_dir.name
        )
        by_short_name.setdefault(short_name, []).append(track_dir.name)

    duplicates = {
        short_name: sorted(track_ids)
        for short_name, track_ids in by_short_name.items()
        if len(track_ids) > 1
    }
    assert duplicates == {}


def test_topology_policy_declares_canonical_root_and_bans_git_sprawl() -> None:
    topology = _read(ROOT / "conductor" / "repository-topology.md")
    wrapper = _read(ROOT / "conductor" / "outer-wrapper-retirement.md")
    artifacts = _read(ROOT / "conductor" / "generated-artifact-retention-policy.md")
    hygiene = _read(ROOT / "conductor" / "worktree-branch-pr-hygiene.md")
    split = _read(ROOT / "conductor" / "future-repo-split-playbook.md")
    release = _read(ROOT / "conductor" / "release-boundary-control-plane.md")

    assert "`microcosting_healthservices` is the canonical implementation" in topology
    assert "Nested `.git` directories" in topology
    assert "Gitlinks without a matching `.gitmodules`" in topology
    assert "package surface registry" in topology
    assert "migrate" in wrapper and "archive" in wrapper and "delete" in wrapper
    assert "generated-ignore" in artifacts
    assert "--force-with-lease" in hygiene
    assert "clean temporary worktree" in hygiene
    assert "git subtree split" in split
    assert "published_verified" in release
    assert "external registry, reviewer, account, or maintainer gates" in hygiene


def test_package_surface_registry_covers_required_surfaces_and_manifests() -> None:
    registry = _load_json(SURFACES)
    assert registry["canonical_root"] == "microcosting_healthservices"

    surfaces = {surface["id"]: surface for surface in registry["surfaces"]}
    assert set(surfaces) >= REQUIRED_SURFACES

    registered_manifests = {
        manifest
        for surface in registry["surfaces"]
        for manifest in surface["manifests"]
    }
    assert _discover_manifests() <= registered_manifests

    for surface in registry["surfaces"]:
        assert surface["owner_track"]
        owner_track = surface["owner_track"]
        assert (TRACKS / owner_track).exists() or (
            ROOT / "conductor" / "archive" / owner_track
        ).exists(), surface["id"]
        for manifest in surface["manifests"]:
            assert (ROOT / manifest).exists(), manifest
        release = surface["release"]
        if release["registry_state"] == "published_verified":
            assert release["evidence"], surface["id"]
        if release["registry_state"] in {"submitted", "blocked"}:
            assert release["external_gate"], surface["id"]
        assert surface["formula_logic"] != "shared-core" or surface["id"] in {
            "python-runtime",
            "rust-workspace",
        }


def test_repository_topology_validator_passes_for_current_canonical_repo() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--json"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["diagnostics"] == []


def test_repository_topology_validator_detects_unmanaged_outer_gitlink(
    tmp_path: Path,
) -> None:
    outer = tmp_path / "outer"
    outer.mkdir()
    subprocess.run(["git", "init"], cwd=outer, check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "update-index",
            "--add",
            "--cacheinfo",
            "160000,d7a0790b2617c9b7b1211e3d95dc8497818246f5,microcosting_healthservices",
        ],
        cwd=outer,
        check=True,
        capture_output=True,
    )

    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--json", "--outer-root", str(outer)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    codes = {diagnostic["code"] for diagnostic in payload["diagnostics"]}
    assert "unmanaged_gitlink" in codes


def test_pr_ci_runs_repository_topology_validator() -> None:
    workflow = _read(ROOT / ".github" / "workflows" / "pr-ci.yml")
    assert "Validate repository topology" in workflow
    assert "uv run python scripts/validate_repository_topology.py" in workflow
