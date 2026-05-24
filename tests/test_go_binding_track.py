from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "go_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "go_binding"
CONTRACT_BUNDLE = FIXTURE_ROOT / "contract_bundle.json"
CONTRACT_ROOT = ROOT / "contracts" / "go-binding"
LIVE_CONTRACT = CONTRACT_ROOT / "go-binding.contract.json"
LIVE_SCHEMA = CONTRACT_ROOT / "go-binding.schema.json"
LIVE_EXAMPLES = CONTRACT_ROOT / "examples"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _squash(text: str) -> str:
    return " ".join(text.split())


def test_go_binding_track_metadata_docs_and_contract_bundle_are_conservative():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        CONTRACT_BUNDLE,
        LIVE_CONTRACT,
        LIVE_SCHEMA,
        LIVE_EXAMPLES / "cli-arrow.pass.json",
        LIVE_EXAMPLES / "service.pass.json",
        LIVE_EXAMPLES / "binding.fail.json",
        ROOT / "bindings" / "go" / "go.mod",
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    tracks = _read_text(TRACKS_REGISTRY)
    bundle = _load_json(CONTRACT_BUNDLE)
    live_contract = _load_json(LIVE_CONTRACT)
    cli_arrow_pass = _load_json(LIVE_EXAMPLES / "cli-arrow.pass.json")
    service_pass = _load_json(LIVE_EXAMPLES / "service.pass.json")
    binding_fail = _load_json(LIVE_EXAMPLES / "binding.fail.json")

    assert metadata["track_id"] == "go_binding_20260512"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "in-progress"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "go-binding-roadmap-complete"
    assert metadata["primary_contract"] == (
        "contracts/go-binding/go-binding.contract.json"
    )
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert "Go binding roadmap" in str(metadata["description"])

    for phrase in [
        "Provide a Go integration path for services, command-line tools, "
        "and data-pipeline systems.",
        "Go should consume the shared Rust core through C ABI, service, or "
        "CLI/file contracts and must not reimplement formulas.",
        "Compare cgo C ABI, service, and CLI/file integration for Go.",
        "Define Go request/response structs aligned to the public contract.",
        "Reuse shared golden fixtures.",
        "Document module publication only after parity gates are stable.",
        "Go roadmap identifies the initial supported integration strategy.",
        "Go examples validate against shared fixtures.",
        "No formula logic is implemented in Go.",
    ]:
        assert phrase in spec or phrase in plan

    for phrase in [
        "Select the lowest-maintenance initial path.",
        "Define packaging and cross-compilation constraints.",
    ]:
        assert phrase in plan

    assert "Track go_binding_20260512 Context" in index
    assert "Go Binding" in tracks
    assert (
        "support Go services and data pipelines through shared-core or "
        "file/service contracts without formula duplication." in tracks
    )

    bundle_map = _as_mapping(bundle)
    diagnostics = _as_mapping(bundle_map["diagnostics"])
    provenance = _as_mapping(bundle_map["provenance"])
    go_module = _as_mapping(bundle_map["go_module"])

    assert bundle_map["schema_version"] == "1.0"
    assert bundle_map["binding_id"] == "go_binding_20260512"
    assert bundle_map["surface"] == "go"
    assert bundle_map["initial_strategy"] == "cli-arrow-file interop"
    assert bundle_map["fallback_strategy"] == "service boundary"
    assert bundle_map["formula_logic_location"] == "rust core"
    assert bundle_map["go_module_status"] == "future-only"
    assert diagnostics["format"] == "json"
    assert diagnostics["includes"] == [
        "contract_id",
        "fixture_id",
        "validation_status",
        "strategy",
        "fallback",
    ]
    assert provenance["checksum_algorithm"] == "sha256"
    assert provenance["preserve_fields"] == [
        "source_basis",
        "fixture_id",
        "notes",
    ]
    assert go_module["status"] == "future-only"
    assert go_module["release_gate"] == "contract and parity stable"
    assert live_contract["schema_version"] == "1.0"
    assert live_contract["privacy"]["classification"] == "synthetic"
    assert live_contract["privacy"]["contains_phi"] is False
    priorities = {
        mode["mode"]: mode["priority"] for mode in live_contract["transport_modes"]
    }
    assert priorities == {
        "arrow-file": "primary",
        "cli": "primary",
        "service": "fallback",
    }
    cli_arrow_checks = cli_arrow_pass["response"]["diagnostics"]["checks"]
    assert {check["status"] for check in cli_arrow_checks} == {"pass"}
    assert service_pass["response"]["mode"] == "service"
    assert "fail" in {
        check["status"] for check in binding_fail["response"]["diagnostics"]["checks"]
    }


def test_go_binding_preserves_provenance_without_formula_logic():
    bundle = _load_json(CONTRACT_BUNDLE)
    diagnostics = _as_mapping(bundle["diagnostics"])
    provenance = _as_mapping(bundle["provenance"])
    go_module = _as_mapping(bundle["go_module"])

    assert bundle["formula_logic_location"] == "rust core"
    assert "go" not in str(bundle["formula_logic_location"]).lower()
    assert diagnostics["format"] == "json"
    assert provenance["checksum_algorithm"] == "sha256"
    assert go_module["status"] == "future-only"
    assert "publication" not in str(go_module["status"]).lower()


def test_go_binding_if_a_scaffold_exists_it_stays_thin_and_non_formula():
    candidate_roots = [
        ROOT / "go-binding",
        ROOT / "bindings" / "go",
        ROOT / "src" / "go",
        ROOT / "go",
        ROOT / "go-binding-scaffold",
        ROOT / "cmd" / "go-binding",
    ]
    scaffold_root = next((path for path in candidate_roots if path.exists()), None)

    if scaffold_root is None:
        return

    scaffold_text = _squash(
        " ".join(
            _read_text(path)
            for path in scaffold_root.rglob("*")
            if path.is_file()
            and "bin" not in path.parts
            and "vendor" not in path.parts
            and "node_modules" not in path.parts
            and "target" not in path.parts
            and path.suffix
            in {".md", ".txt", ".json", ".go", ".mod", ".sum", ".yaml", ".yml"}
        )
    ).lower()

    for forbidden in [
        "formula logic",
        "reimplement formula",
        "duplicate formulas",
        "go module publication",
        "publication-ready",
        "production-ready",
    ]:
        assert forbidden not in scaffold_text
