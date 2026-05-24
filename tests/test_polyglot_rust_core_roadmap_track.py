from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "polyglot_rust_core_roadmap_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
TECH_STACK = ROOT / "conductor" / "tech-stack.md"
CONTRACT_ROOT = ROOT / "contracts" / "polyglot-rust-core-roadmap"
CONTRACT = CONTRACT_ROOT / "polyglot-rust-core-roadmap.contract.json"
SCHEMA = CONTRACT_ROOT / "polyglot-rust-core-roadmap.schema.json"
EXAMPLES = CONTRACT_ROOT / "examples"
ROADMAP_DOCS = [
    ROOT / "docs" / "roadmaps" / "polyglot-rust-core.md",
    ROOT / "docs" / "roadmaps" / "polyglot-rust-core-architecture.md",
    ROOT / "docs" / "roadmaps" / "polyglot-packaging-release-matrix.md",
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "polyglot-rust-core-roadmap.md",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _single_line(text: str) -> str:
    return " ".join(text.split())


def test_polyglot_rust_core_roadmap_track_metadata_contract_and_docs_are_present():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS,
        TECH_STACK,
        CONTRACT,
        SCHEMA,
        EXAMPLES / "validation.pass.json",
        EXAMPLES / "validation.fail.json",
        *ROADMAP_DOCS,
    ]:
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    tracks = _read_text(TRACKS)
    tech_stack = _read_text(TECH_STACK)
    contract = _read_json(CONTRACT)
    schema = _read_json(SCHEMA)
    pass_example = _read_json(EXAMPLES / "validation.pass.json")
    fail_example = _read_json(EXAMPLES / "validation.fail.json")

    assert metadata["track_id"] == "polyglot_rust_core_roadmap_20260512"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "in-progress"
    assert metadata["track_class"] == "roadmap-governance"
    assert metadata["current_state"] == "polyglot-roadmap-complete"
    assert metadata["primary_contract"] == (
        "contracts/polyglot-rust-core-roadmap/polyglot-rust-core-roadmap.contract.json"
    )
    assert metadata["dependencies"] == [
        "abstraction_doctrine_enforcement_20260512",
        "reference_data_manifest_schema_20260512",
        "formula_parameter_bundle_pipeline_20260512",
        "pricing_year_validation_gates_20260512",
        "python_rust_binding_stabilization_20260512",
    ]
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert metadata["publication_status"] == "not-applicable"
    assert "shared Rust calculator core" in str(metadata["description"])

    assert contract["schema_version"] == "1.0"
    assert contract["privacy"]["classification"] == "synthetic"
    assert contract["privacy"]["contains_phi"] is False
    assert sorted(contract["contract_versions"]) == [
        "abi_boundary",
        "batch_io",
        "binding_conformance",
        "diagnostics",
        "fixture_gates",
        "provenance",
        "validation_status",
    ]
    assert schema["title"] == "Polyglot Rust Core roadmap contract"
    assert pass_example["state"] == "pass"
    assert pass_example["batch_io"]["format"] == "arrow-ipc"
    assert fail_example["state"] == "fail"
    assert fail_example["fixture_gates"]["state"] == "block"

    assert "# Specification: Polyglot Rust Core Roadmap" in spec
    assert "Python remains the current validated public runtime" in spec
    assert "Rust becomes the default only when fixture parity, packaging," in (
        _single_line(spec)
    )
    assert (
        "TypeScript/WASM, Java/JVM, C ABI, SQL/DuckDB, SAS interoperability"
        in _single_line(spec)
    )
    assert "Power Platform managed solutions" in spec
    assert "Rust-core promotion lifecycle" in plan
    assert "Python baseline, Rust canary, Rust opt-in, and Rust default gates" in plan
    assert "Arrow-compatible batch schemas, diagnostics, errors, provenance" in plan
    assert "Python wheels, Rust crates, R packages, Julia packages" in plan
    assert "Power Platform managed solutions" in plan
    assert "- [x] Task: Define the polyglot architecture" in plan
    assert "- [x] Task: Define shared cross-language contracts" in plan
    assert "- [x] Task: Define packaging and release expectations" in plan
    assert "- [x] Task: Publish the polyglot roadmap" in plan
    assert "- [Specification](./spec.md)" in index
    assert "- [Implementation Plan](./plan.md)" in index
    assert "- [Metadata](./metadata.json)" in index
    assert "Polyglot Rust Core Roadmap" in tracks
    assert "shared Rust calculator core" in tracks
    assert "Rust Core Roadmap" in tracks
    assert "Rust is the intended future calculator core" in tech_stack
    assert "Python remains the current validated runtime path" in tech_stack
    assert "fixture-gated" in tech_stack
    assert "governance/polyglot-rust-core-roadmap" in _read_text(
        ROOT / "docs-site" / "astro.config.mjs"
    )


def test_polyglot_rust_core_roadmap_does_not_overclaim_rust_default():
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    tech_stack = _read_text(TECH_STACK)

    for text in [spec, plan, tech_stack]:
        assert "implemented Rust default" not in text
        assert "Rust default is implemented" not in text
        assert "Rust default is already implemented" not in text
        assert "Rust is the default runtime today" not in text

    assert "Python remains the current validated public runtime" in spec
    assert "Rust becomes the default only when fixture parity, packaging," in (
        _single_line(spec)
    )
    assert (
        "Rust promotion must preserve traceability to IHACPA source materials" in spec
    )
