from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "typescript_wasm_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
PACKAGING_PLANS = ROOT / "conductor" / "downstream-packaging-plans.md"
WASM_BINDING = ROOT / "wasm-binding"
DOCS_SITE_PACKAGING = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "downstream-packaging-plans.md"
)
DOCS_TUTORIAL = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "tutorials"
    / "typescript-wasm-browser-demo.mdx"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def test_typescript_wasm_binding_track_files_and_scaffold_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        PACKAGING_PLANS,
        WASM_BINDING / "README.md",
        WASM_BINDING / "package.json",
        WASM_BINDING / "tsconfig.json",
        WASM_BINDING / "src" / "adapter.ts",
        WASM_BINDING / "src" / "index.ts",
        WASM_BINDING / "src" / "types.ts",
        WASM_BINDING / "test" / "adapter.test.ts",
        DOCS_SITE_PACKAGING,
        DOCS_TUTORIAL,
    ]:
        assert path.exists(), path


def test_typescript_wasm_binding_track_docs_require_synthetic_fixtures_and_parity():
    spec = _read(TRACK / "spec.md").lower()
    plan = _read(TRACK / "plan.md").lower()
    strategy = _read(TRACK / "strategy.md").lower()
    registry = _read(TRACKS_REGISTRY).lower()
    docs_site = _read(DOCS_SITE_PACKAGING).lower()
    tutorial = _read(DOCS_TUTORIAL).lower()
    ci_notes = _read(TRACK / "ci_notes.md").lower()

    for phrase in [
        "provide a typescript/wasm integration for browser-based documentation demos",
        "add browser demo examples using synthetic data only",
        "wasm outputs match shared golden fixtures for validated calculators",
        "add ci build checks for wasm artifacts without publishing sensitive data",
    ]:
        assert phrase in spec

    for phrase in [
        "browser-demo examples and fixtures to be synthetic-data-only",
        "validate included calculators against shared golden fixtures",
        "typescript definitions to be generated from, or hand-maintained "
        "against, the public contract",
        "without publishing sensitive data",
    ]:
        assert phrase in plan

    assert (
        "enable browser docs demos and node workflows from the shared rust core "
        "with synthetic-data-only privacy boundaries" in registry
    )

    for phrase in [
        "synthetic, browser-only, and\n  wrapper-only",
        "do not cache patient-level data",
        "do not duplicate\n  calculator rules in typescript",
    ]:
        assert phrase in docs_site

    for phrase in [
        "browser demos must use synthetic data only",
        "no telemetry, remote logging, analytics, or background upload behavior",
        "the public typescript facade is hand-maintained",
        "shared golden fixture\nparity exists",
    ]:
        assert phrase in strategy

    for phrase in [
        "synthetic fixtures only",
        "do not load or cache patient-level data in the demo",
        "typescript must not duplicate",
        "shared fixtures to verify the browser result matches the canonical",
    ]:
        assert phrase in tutorial

    assert "sensitive-data restrictions" in ci_notes
    assert "do not place phi" in ci_notes


def test_typescript_wasm_binding_track_metadata_stays_roadmap_only():
    metadata = _load_json(TRACK / "metadata.json")

    assert metadata["track_id"] == "typescript_wasm_binding_20260512"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "prototype"
    assert metadata["publication_status"] == "not-ready"


def test_typescript_wasm_browser_scaffold_does_not_duplicate_formula_logic():
    readme = _read(WASM_BINDING / "README.md").lower()
    adapter = _read(WASM_BINDING / "src" / "adapter.ts").lower()
    types = _read(WASM_BINDING / "src" / "types.ts").lower()
    package_json = _load_json(WASM_BINDING / "package.json")

    assert package_json["private"] is True
    assert "strict" in _read(WASM_BINDING / "tsconfig.json").lower()
    assert "adapter shell" in readme
    assert "synthetic data only" in readme
    assert "not publication-ready" in readme
    assert "wasmadaptererror" in adapter
    assert "fails closed" not in adapter
    assert "futurewasmcalculatorexports" in types

    for forbidden in [
        "private_service_adjustment",
        "long_stay_per_diem",
        "same_day_base_weight",
        "icu_rate",
        "nwau25 =",
        "nwau25 <-",
    ]:
        assert forbidden not in adapter
        assert forbidden not in types
