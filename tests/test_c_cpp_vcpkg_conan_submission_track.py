from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "c_cpp_vcpkg_conan_submission_20260524"
TRACK_INDEX = TRACK / "index.md"
TRACK_CHECKLIST = TRACK / "upstream_pr_checklist.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
VCPKG_JSON = ROOT / "packaging" / "vcpkg" / "ports" / "nwau-c-abi" / "vcpkg.json"
VCPKG_PORTFILE = (
    ROOT / "packaging" / "vcpkg" / "ports" / "nwau-c-abi" / "portfile.cmake"
)
CONANFILE = ROOT / "packaging" / "conan" / "conanfile.py"
PACKAGING_README = ROOT / "packaging" / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry
        for registry in data["registries"]
        if registry["id"] == "c_cpp_vcpkg_conan"
    )


def test_c_cpp_track_records_cancelled_not_publication():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _registry()

    assert (TRACK / "review.md").exists()
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["current_status"] == "deprecated_cancelled_not_published"
    assert metadata["publication_claimed"] is False
    assert metadata["publication_status"] == "cancelled_not_published"
    assert metadata["cancelled_at"] == "2026-07-03"
    assert "Deprecated and cancelled" in metadata["blocker"]
    assert "historical evidence only" in metadata["blocker"]
    assert (
        metadata["package_evidence"]["publication_claim"]
        == "No public vcpkg or ConanCenter publication is claimed; the surface is "
        "deprecated and cancelled."
    )
    assert registry["current_status"] == "deprecated_cancelled_not_published"
    assert "Deprecated and cancelled" in registry["blocker"]
    assert registry["cancelled_at"] == "2026-07-03"
    assert "historical evidence only" in registry["blocker"]
    assert "cargoPackageResult" in registry["preparationEvidence"]
    assert registry["preparationEvidence"]["archivedTrack"].endswith(
        "conductor/archive/c_cpp_vcpkg_conan_submission_20260524/"
    )
    assert (
        "compiled nwau-c-abi v0.1.0 successfully"
        in registry["preparationEvidence"]["cargoPackageResult"]
    )
    assert registry["preparationEvidence"]["vcpkgPortfile"].endswith("portfile.cmake")
    assert (
        registry["preparationEvidence"]["conanCenterSubmissionState"]
        == "open_cla_resolved_pending_scheduler_review"
    )
    assert (
        "license/cla status context is SUCCESS"
        in registry["preparationEvidence"]["latestConanCenterReviewUpdate"]
    )
    assert (
        "2026-06-25" in registry["preparationEvidence"]["latestConanCenterReviewUpdate"]
    )
    assert (
        "mergeStateStatus=BLOCKED"
        in registry["preparationEvidence"]["latestConanCenterReviewUpdate"]
    )
    assert (
        "Job scheduler is ACTION_REQUIRED"
        in registry["preparationEvidence"]["latestConanCenterReviewUpdate"]
    )
    assert "conanRecipeReadiness" in registry["preparationEvidence"]
    assert "conanCreateCommand" in registry["preparationEvidence"]
    assert "conanPackageReference" in registry["preparationEvidence"]
    assert "vcpkgOverlayInstallCommand" in registry["preparationEvidence"]
    expected_overlay_result = (
        "Installed nwau-c-abi:arm64-osx@0.1.0 successfully from the local overlay "
        "port with release and debug static libraries, header, copyright, and SPDX "
        "metadata."
    )
    assert (
        registry["preparationEvidence"]["vcpkgOverlayInstallResult"]
        == expected_overlay_result
    )


def test_c_cpp_packaging_wording_preserves_private_preview_and_upstream_gates():
    readme = _read(PACKAGING_README)
    plan = _read(TRACK / "plan.md")
    spec = _read(TRACK / "spec.md")
    index = _read(TRACK_INDEX)
    checklist = _read(TRACK_CHECKLIST)

    assert "local/private preview readiness" in readme
    assert "not evidence of public vcpkg" in readme
    assert "no public vcpkg or conancenter publication is claimed." in spec.lower()
    assert "deprecated and cancelled" in spec.lower()
    assert "conan create packaging/conan --build=missing" in readme
    assert "Conan create and vcpkg overlay-port validation pass locally" in plan
    assert "Upstream PR Checklist" in index
    assert "vcpkg outcome" in checklist.lower()
    assert "closed unmerged" in checklist
    assert "conandata.yml" in checklist
    assert "does not currently support building Rust libraries" in checklist
    assert "open a pr to `conan-io/conan-center-index`" in checklist.lower()
    assert "https://github.com/conan-io/conan-center-index/pull/30262" in plan
    assert "Capture ConanCenter CLA/recheck resolution" in plan
    assert "deprecated and cancelled" in checklist.lower()
    assert "historical evidence only" in checklist.lower()


def test_vcpkg_port_has_manifest_and_build_portfile():
    manifest = json.loads(_read(VCPKG_JSON))
    portfile = _read(VCPKG_PORTFILE)

    assert manifest["name"] == "nwau-c-abi"
    assert manifest["version"] == "0.1.0"
    assert "scaffold" not in manifest["description"].lower()
    assert "find_program(CARGO NAMES cargo REQUIRED)" in portfile
    assert "nwau_build_and_install(release release)" in portfile
    assert "nwau_build_and_install(debug debug)" in portfile
    assert "--manifest-path" in portfile
    assert "rust/crates/nwau-c-abi/Cargo.toml" in portfile
    assert "nwau_abi.h" in portfile
    assert "vcpkg_install_copyright" in portfile


def test_conan_recipe_builds_and_packages_c_abi_metadata():
    recipe = _read(CONANFILE)

    assert 'settings = "os", "arch", "compiler", "build_type"' in recipe
    assert '"shared": [True, False]' in recipe
    assert '"fPIC": [True, False]' in recipe
    assert "def export_sources(self):" in recipe
    assert "self.export_sources_folder" in recipe
    assert '"crates", "nwau-c-abi"' in recipe
    assert '"crates", "nwau-core"' in recipe
    assert '"crates", "nwau-py"' in recipe
    assert "../../rust" not in recipe
    assert "cargo build --release --locked" in recipe
    assert '"nwau_abi.h"' in recipe
    assert 'dst=os.path.join(self.package_folder, "include")' in recipe
    assert '"libnwau_c_abi.a"' in recipe
    assert '"libnwau_c_abi.dylib"' in recipe
    assert '"*.dylib"' not in recipe
    assert '"*.a"' not in recipe
    assert 'self.cpp_info.libs = ["nwau_c_abi"]' in recipe
    assert "cmake_target_name" in recipe
    assert "pkg_config_name" in recipe
