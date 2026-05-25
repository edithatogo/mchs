from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "kotlin_native_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
PACKAGING_MATRIX = ROOT / "docs" / "roadmaps" / "polyglot-packaging-release-matrix.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "kotlin-native-binding.md"
GOVERNANCE = ROOT / "docs-site" / "src" / "content" / "docs" / "governance"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "kotlin_native_binding"
CONTRACT_ROOT = ROOT / "contracts" / "kotlin-native-binding"
BINDING_ROOT = ROOT / "bindings" / "kotlin-native"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def test_kotlin_native_track_is_native_first_and_contract_driven():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        PACKAGING_MATRIX,
        ROADMAP,
        GOVERNANCE / "kotlin-native-binding.md",
        CONTRACT_ROOT / "kotlin-native-binding.contract.json",
        CONTRACT_ROOT / "kotlin-native-binding.schema.json",
        FIXTURE_ROOT / "contract_bundle.json",
        FIXTURE_ROOT / "validation.pass.json",
        FIXTURE_ROOT / "validation.fail.json",
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    tracks = _read_text(TRACKS_REGISTRY)
    packaging = _read_text(PACKAGING_MATRIX)
    roadmap = _read_text(ROADMAP)
    governance = _read_text(GOVERNANCE / "kotlin-native-binding.md")
    squashed_spec = " ".join(spec.split())
    squashed_roadmap = " ".join(roadmap.split())
    squashed_governance = " ".join(governance.split())

    assert metadata["track_id"] == "kotlin_native_binding_20260512"
    assert metadata["primary_contract"] == (
        "contracts/kotlin-native-binding/kotlin-native-binding.contract.json"
    )
    assert metadata["publication_status"] == "not-applicable"
    assert "without a JVM runtime dependency" in str(metadata["description"])

    for phrase in [
        "Kotlin/Native is the authored Kotlin surface",
        "Java/JVM support is outside the initial scope",
        "C ABI, service, or Arrow/Parquet file contract",
        "must not duplicate formula logic",
        "No JVM runtime, Maven publication, or Gradle build is required",
    ]:
        assert phrase in squashed_spec

    for phrase in [
        "avoids a JVM runtime dependency",
        "memory ownership, and C ABI considerations",
        "Kotlin/Native prototype and shared-fixture tests",
    ]:
        assert phrase in plan

    assert "Kotlin/Native Binding" in tracks
    assert "no JVM runtime requirement" in tracks
    assert "Native artifact over C ABI, service, or file contract" in packaging
    assert "Go, Kotlin/Native, and other adapters" in packaging
    assert (
        "does not require a JVM runtime, Maven publication, or a Gradle build"
        in squashed_roadmap
    )
    assert "No JVM runtime, Maven publication, or Gradle build" in squashed_governance


def test_kotlin_native_contract_and_fixtures_reject_runtime_overclaiming():
    contract = _load_json(CONTRACT_ROOT / "kotlin-native-binding.contract.json")
    bundle = _load_json(FIXTURE_ROOT / "contract_bundle.json")
    pass_example = _load_json(FIXTURE_ROOT / "validation.pass.json")
    fail_example = _load_json(FIXTURE_ROOT / "validation.fail.json")

    readiness = _as_mapping(contract["build_readiness"])
    kotlin_native = _as_mapping(readiness["kotlin_native"])
    c_abi = _as_mapping(readiness["c_abi"])
    service = _as_mapping(readiness["service"])

    assert contract["binding_bundle_id"] == "kotlin_native_binding_contract_20260513"
    assert _as_mapping(contract["privacy"])["contains_phi"] is False
    assert bundle["binding_id"] == "kotlin_native_binding_20260512"
    assert bundle["surface"] == "kotlin-native"
    assert bundle["formula_logic_location"] == "rust core"
    assert bundle["initial_strategy"] == "arrow/parquet file interop"
    assert bundle["fallback_strategy"] == "service boundary"

    assert kotlin_native["status"] == "private"
    assert kotlin_native["runtime"] == "native"
    assert c_abi["status"] == "private"
    assert service["status"] == "private"

    assert pass_example["result"] == "pass"
    assert pass_example["formula_logic_location"] == "rust core"
    assert pass_example["strategy"] == "arrow/parquet file interop"
    assert fail_example["result"] == "fail"
    assert "artifact publication" in str(fail_example["reason"])
    assert "native adapter boundary" in str(fail_example["reason"])


def test_kotlin_native_scaffold_has_no_jvm_build_or_formula_logic():
    assert BINDING_ROOT.exists()
    assert not (BINDING_ROOT / "build.gradle.kts").exists()
    assert not (BINDING_ROOT / "pom.xml").exists()

    scaffold_files = [
        path
        for path in BINDING_ROOT.rglob("*")
        if path.is_file() and path.suffix in {".md", ".kt", ".json"}
    ]
    assert scaffold_files

    scaffold_text = "\n".join(_read_text(path) for path in scaffold_files).lower()

    for forbidden in [
        "private_service_adjustment",
        "long_stay_per_diem",
        "same_day_base_weight",
        "icu_rate",
        "embedded formula implementation",
        "publication ready",
        "maven central",
        "gradle build",
    ]:
        assert forbidden not in scaffold_text

    assert "jvm runtime dependency" in scaffold_text
    assert "formula logic remains in the rust core" in scaffold_text
