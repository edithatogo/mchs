from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "julia_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
PACKAGING_PLANS = ROOT / "conductor" / "downstream-packaging-plans.md"
JULIA_BINDING = ROOT / "julia-binding"
DOCS_TUTORIAL = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "tutorials"
    / "julia-dataframes-arrow-costing-study.mdx"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def test_julia_binding_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        JULIA_BINDING / "Project.toml",
        JULIA_BINDING / "README.md",
        JULIA_BINDING / "src" / "NWAUJulia.jl",
        JULIA_BINDING / "test" / "runtests.jl",
        DOCS_TUTORIAL,
    ]:
        assert path.exists(), path


def test_julia_binding_records_the_selected_cli_file_strategy():
    strategy = _read(TRACK / "strategy.md").lower()
    plan = _read(TRACK / "plan.md").lower()
    registry = _read(TRACKS_REGISTRY).lower()

    assert (
        "start with **cli/file integration** as the initial julia binding path."
        in strategy
    )
    assert "csv is\nthe executable prototype" in strategy
    assert "arrow remains the target interchange format" in strategy
    assert "the julia package acting as a thin\norchestration layer" in strategy
    assert "single-sourced outside julia" in strategy
    assert "avoid pythoncall as the primary integration path" in strategy
    assert "promote to c abi only after the core contract is stable" in strategy
    assert "selected path: cli/file integration" in plan
    assert (
        "support julia analytics through c abi or arrow/cli interop while "
        "preserving single-sourced calculator logic" in registry
    )


def test_julia_binding_reuses_shared_golden_fixtures_and_examples_docs():
    spec = _read(TRACK / "spec.md").lower()
    plan = _read(TRACK / "plan.md").lower()

    for phrase in [
        "reuse shared golden fixtures",
        "julia examples validate against shared fixtures",
        "document dataframe/arrow workflow examples",
    ]:
        assert phrase in spec

    for phrase in [
        "fixture-readiness claims",
        "repository tests that enforce no julia formula duplication",
        "add dataframes.jl and arrow-target documentation examples",
    ]:
        assert phrase in plan


def test_julia_binding_package_and_binary_claims_stay_conservative():
    strategy = _read(TRACK / "strategy.md").lower()
    packaging = _read(PACKAGING_PLANS).lower()
    metadata = _load_json(TRACK / "metadata.json")

    for phrase in [
        "package/binary distribution: good for performance, but versioned "
        "native artifacts increase release complexity across platforms.",
        "package/binary distribution: weakest of the three for a clean "
        "julia-first distribution story because python becomes a required "
        "runtime dependency.",
        "package/binary distribution: conservative for an initial rollout because",
        "release readiness is claimable only after fixture-backed parity is recorded",
        "packaging wrappers must not duplicate calculator formulas",
    ]:
        assert phrase in strategy or phrase in packaging

    assert metadata["current_state"] == "prototype"
    assert metadata["publication_status"] == "not-ready"


def test_julia_package_is_wrapper_only_and_uses_the_shared_cli_boundary():
    source = _read(JULIA_BINDING / "src" / "NWAUJulia.jl").lower()
    readme = _read(JULIA_BINDING / "README.md").lower()
    tests = _read(JULIA_BINDING / "test" / "runtests.jl").lower()

    for forbidden in [
        "nwau25 =",
        "nwau25 <-",
        "private_service_adjustment",
        "long_stay_per_diem",
        "same_day_base_weight",
        "icu_rate",
    ]:
        assert forbidden not in source

    assert "nwau_py.cli.main" in source
    assert "run(cmd(argv))" in source
    assert "formula logic stays in python" in readme
    assert "csv-only because that is the active shared cli contract" in readme
    assert "command assembly" in tests
    assert "missing input guard" in tests


def test_julia_docs_keep_arrow_as_target_not_current_release_claim():
    tutorial = _read(DOCS_TUTORIAL).lower()
    packaging = _read(PACKAGING_PLANS).lower()
    ci_notes = _read(TRACK / "ci_notes.md").lower()

    assert (
        "thin cli/file wrapper with csv as the\ncurrent executable prototype"
        in tutorial
    )
    assert "arrow.jl` is the target" in tutorial
    assert "registry-ready package claim" in tutorial.replace("\n", " ")
    assert "recommended evaluation path: cli/file wrapper first" in packaging
    normalized_packaging = " ".join(packaging.split())
    assert "csv as the executable prototype" in normalized_packaging
    assert "arrow as the target batch interchange format" in normalized_packaging
    assert "do not claim general registry readiness" in packaging
    assert "avoids adding a required github actions julia matrix" in (
        " ".join(ci_notes.split())
    )
