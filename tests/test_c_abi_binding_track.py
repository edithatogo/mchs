from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "c_abi_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
DOWNSTREAM_PACKAGING_PLANS = ROOT / "conductor" / "downstream-packaging-plans.md"
C_ABI_CRATE = ROOT / "rust" / "crates" / "nwau-c-abi"
DOCS_TUTORIAL = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "tutorials"
    / "c-abi-consumers.mdx"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def test_c_abi_binding_track_scaffold_and_docs_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        DOWNSTREAM_PACKAGING_PLANS,
        ROOT / "rust" / "Cargo.toml",
        C_ABI_CRATE / "Cargo.toml",
        C_ABI_CRATE / "src" / "lib.rs",
        C_ABI_CRATE / "include" / "nwau_abi.h",
        DOCS_TUTORIAL,
    ]:
        assert path.exists(), path


def test_c_abi_binding_track_requires_versioned_memory_safe_arrow_contract():
    spec = _read(TRACK / "spec.md").lower()
    plan = _read(TRACK / "plan.md").lower()
    strategy = _read(TRACK / "strategy.md").lower()
    ci_notes = _read(TRACK / "ci_notes.md").lower()
    registry = _read(TRACKS_REGISTRY).lower()
    tutorial = _read(DOCS_TUTORIAL).lower()
    packaging = _read(DOWNSTREAM_PACKAGING_PLANS).lower()

    for phrase in [
        "stable c abi",
        "ffi-safe data structures, memory ownership, and error handling",
        "prefer arrow c data interface or file-based arrow boundaries where practical",
        "abi versioning and compatibility policy are documented.",
        "memory ownership and error semantics are tested.",
        "c abi outputs match shared golden fixtures.",
    ]:
        assert phrase in spec

    for phrase in [
        "conservative abi contract for versioning, ownership, and errors",
        "document arrow c data interface usage and the file-based arrow boundary",
        "abi compatibility checks",
        "shared golden fixture parity as the gate before any readiness claim",
    ]:
        assert phrase in plan

    assert (
        "define a stable institutional embedding abi only after core schemas "
        "and calculator parity are stable." in registry
    )
    assert "c abi wrapper or secured service boundary" in packaging
    assert "arrow c data interface" in strategy
    assert "prefix all exported symbols with `nwau_abi_`" in strategy
    assert "header generation" in ci_notes
    assert "exported symbols" in ci_notes
    assert "null pointer handling" in ci_notes
    assert "thin and explicit" in tutorial
    assert "version the abi independently from implementation internals." in tutorial
    assert "make every output shape deterministic and easy to free" in tutorial
    assert "return structured error codes" in tutorial
    assert "use arrow as the preferred tabular interchange boundary" in tutorial
    assert "byte-for-byte or field-for-field comparable" in tutorial
    assert "do not port calculator formulas into the c wrapper" in tutorial
    assert "do not mirror validation logic in native glue code" in tutorial


def test_c_abi_binding_track_metadata_stays_conservative():
    metadata = _load_json(TRACK / "metadata.json")

    assert metadata["track_id"] == "c_abi_binding_20260512"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "prototype"
    assert metadata["publication_status"] == "not-ready"


def test_c_abi_scaffold_is_versioned_and_fails_closed_without_formula_logic():
    cargo = _read(ROOT / "rust" / "Cargo.toml")
    crate_manifest = _read(C_ABI_CRATE / "Cargo.toml").lower()
    rust_source = _read(C_ABI_CRATE / "src" / "lib.rs").lower()
    header = _read(C_ABI_CRATE / "include" / "nwau_abi.h").lower()

    assert '"crates/nwau-c-abi"' in cargo
    assert 'name = "nwau-c-abi"' in crate_manifest
    assert 'crate-type = ["cdylib", "staticlib", "rlib"]' in crate_manifest
    assert "publish = false" in crate_manifest

    for phrase in [
        "nwau_abi_version_major",
        "nwau_abi_version_minor",
        "nwau_abi_version_patch",
        "nwau_abi_status_unimplemented",
        "nwau_abi_calculate_acute_2025",
    ]:
        assert phrase in rust_source
        assert phrase in header

    assert "borrowed pointer" in header
    assert "caller owns that storage" in header
    assert "returns `nwau_abi_status_unimplemented`" in header
    assert "nwau_abi_status_unimplemented" in rust_source
    assert "nwau25: 999.0" in rust_source

    for forbidden in [
        "nwau25 =",
        "nwau25 +=",
        "private_service_deduction =",
        "gwau =",
    ]:
        assert forbidden not in rust_source
