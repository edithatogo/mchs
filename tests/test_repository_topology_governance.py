from __future__ import annotations

import json
import os
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"
TRACKS_MD = ROOT / "conductor" / "tracks.md"
SURFACES = ROOT / "contracts" / "repository-topology" / "package-surfaces.json"
VALIDATOR = ROOT / "scripts" / "validate_repository_topology.py"
OUTER_MANIFEST = ROOT / "conductor" / "outer-wrapper-migration-manifest.json"

_validator_spec = spec_from_file_location("validate_repository_topology", VALIDATOR)
assert _validator_spec is not None and _validator_spec.loader is not None
_validator = module_from_spec(_validator_spec)
sys.modules[_validator_spec.name] = _validator
_validator_spec.loader.exec_module(_validator)

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


def test_package_surface_registry_conforms_to_declared_schema_shape() -> None:
    schema = _load_json(
        ROOT / "contracts" / "repository-topology" / "package-surfaces.schema.json"
    )
    registry = _load_json(SURFACES)

    assert set(schema["required"]) <= set(registry)
    surface_schema = schema["$defs"]["surface"]
    release_schema = schema["$defs"]["release"]
    surface_keys = set(surface_schema["properties"])
    release_keys = set(release_schema["properties"])

    for surface in registry["surfaces"]:
        assert set(surface_schema["required"]) <= set(surface), surface["id"]
        assert set(surface) <= surface_keys, surface["id"]
        for field in [
            "category",
            "lifecycle",
            "support_status",
            "artifact_policy",
            "formula_logic",
        ]:
            assert surface[field] in surface_schema["properties"][field]["enum"], (
                surface["id"],
                field,
            )

        release = surface["release"]
        assert set(release_schema["required"]) <= set(release), surface["id"]
        assert set(release) <= release_keys, surface["id"]
        assert (
            release["registry_state"]
            in release_schema["properties"]["registry_state"]["enum"]
        )


def test_readme_registry_claims_match_release_boundary_states() -> None:
    readme = _read(ROOT / "README.md")
    registry = _load_json(SURFACES)

    states = {
        surface["id"]: surface["release"]["registry_state"]
        for surface in registry["surfaces"]
    }
    assert states["cran-registry"] == "submitted"
    assert states["maven-central-registry"] == "published_verified"
    assert states["vscode-extension"] == "deprecated_cancelled_publication_retained"
    assert states["vcpkg-port"] == "deprecated_cancelled_not_published"
    assert states["swift-binding"] == "deprecated_cancelled_publication_retained"

    for phrase in [
        "CRAN maintainer submission/review remains external",
        "**Deprecated and cancelled** as of 2026-07-03",
        "Swift Package Index (`MCHSBind`)",
        "no further Swift Package Index work is planned unless re-chartered",
        "No support claim beyond the specific registry states above",
    ]:
        assert phrase in readme


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


def test_generated_artifact_policy_detects_package_artifacts() -> None:
    assert _validator._is_generated_path("dist/nwau_py-0.1.0.tar.gz")
    assert _validator._is_generated_path("integrations/vscode/mchs-tools-0.1.1.vsix")
    assert _validator._is_generated_path(
        "archive/sas/NWAU24_SAS_Calculator/calculators/Scorer_v4/base_library.zip"
    )
    assert _validator._is_generated_path(
        "bindings/matlab/mchs-matlab-interop-0.1.0.zip"
    )
    assert _validator._is_generated_path(
        "bindings/stata/mchs-stata-interop-0.1.0.zip"
    )
    assert not _validator._is_evidence_artifact("dist/nwau_py-0.1.0.tar.gz")
    assert _validator._is_evidence_artifact("integrations/vscode/mchs-tools-0.1.1.vsix")
    assert _validator._is_evidence_artifact(
        "archive/sas/NWAU24_SAS_Calculator/calculators/Scorer_v4/base_library.zip"
    )
    assert _validator._is_evidence_artifact(
        "bindings/matlab/mchs-matlab-interop-0.1.0.zip"
    )
    assert _validator._is_evidence_artifact(
        "bindings/stata/mchs-stata-interop-0.1.0.zip"
    )


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


def test_outer_wrapper_migration_manifest_records_phase_one_inventory() -> None:
    manifest = _load_json(OUTER_MANIFEST)
    assert manifest["track_id"] == "outer_wrapper_retirement_migration_20260624"
    assert manifest["recommended_option"] == "retire-wrapper-after-preservation"
    assert (
        manifest["decision_boundary"]
        == "Inventory and manifest only; no outer-wrapper files are deleted by "
        "this phase."
    )

    entries = {entry["path"]: entry for entry in manifest["entries"]}
    gitlink = entries["microcosting_healthservices"]
    assert gitlink["classification"] == "gitlink"
    assert gitlink["disposition"] == "retire-or-formalize"
    assert gitlink["git_mode"] == "160000"
    assert gitlink["sha256"] is None

    tracked_logs = [
        entry
        for entry in manifest["entries"]
        if entry["state"] == "tracked"
        and entry["classification"] == "generated-log"
        and entry["path"].startswith(".playwright-mcp/")
    ]
    assert len(tracked_logs) >= 40
    assert all(
        entry["sha256"] for entry in tracked_logs if entry["git_mode"] != "160000"
    )

    power_platform_evidence = [
        entry
        for entry in manifest["entries"]
        if entry["state"] == "untracked"
        and entry["classification"] == "evidence"
        and entry["path"].startswith("power-platform/evidence/")
    ]
    assert len(power_platform_evidence) >= 100
    assert all(entry["sha256"] for entry in power_platform_evidence)

    source_slices = [
        entry
        for entry in manifest["entries"]
        if entry["state"] == "untracked"
        and entry["classification"] == "source-or-governance"
    ]
    assert any(entry["path"].startswith("scripts/") for entry in source_slices)
    assert any(entry["path"].startswith("tests/") for entry in source_slices)
    assert any(entry["path"].startswith("power-platform/") for entry in source_slices)


def test_pr_ci_runs_repository_topology_validator() -> None:
    workflow = _read(ROOT / ".github" / "workflows" / "pr-ci.yml")
    assert "Validate repository topology" in workflow
    assert "uv run python scripts/validate_repository_topology.py" in workflow
