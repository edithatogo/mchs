from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "swift_binding_20260513"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "swift_binding"
CONTRACT_BUNDLE = FIXTURE_ROOT / "contract_bundle.json"
CONTRACT_ROOT = ROOT / "contracts" / "swift-binding"
LIVE_CONTRACT = CONTRACT_ROOT / "swift-binding.contract.json"
LIVE_SCHEMA = CONTRACT_ROOT / "swift-binding.schema.json"
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


class TestSwiftBindingTrack:

    def test_swift_binding_track_metadata_docs_and_contract_bundle_are_conservative(self):
        for path in [
            TRACK / "spec.md",
            TRACK / "plan.md",
            TRACK / "index.md",
            TRACK / "metadata.json",
            TRACKS_REGISTRY,
            CONTRACT_BUNDLE,
            LIVE_CONTRACT,
            LIVE_SCHEMA,
            LIVE_EXAMPLES / "file-exchange.pass.json",
            LIVE_EXAMPLES / "service.pass.json",
            LIVE_EXAMPLES / "binding.fail.json",
        ]:
            assert path.exists(), path

        metadata = _load_json(TRACK / "metadata.json")
        spec = _read_text(TRACK / "spec.md")
        plan = _read_text(TRACK / "plan.md")
        index = _read_text(TRACK / "index.md")
        tracks = _read_text(TRACKS_REGISTRY)
        bundle = _load_json(CONTRACT_BUNDLE)
        live_contract = _load_json(LIVE_CONTRACT)

        assert metadata["track_id"] == "swift_binding_20260513"
        assert metadata["type"] == "feature"
        assert metadata["status"] == "completed"
        assert metadata["track_class"] == "binding"
        assert metadata["current_state"] == "complete-with-gaps"
        assert metadata["primary_contract"] == (
            "contracts/swift-binding/swift-binding.contract.json"
        )
        assert metadata["publication_status"] == "not-applicable"
        assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
        assert "Swift roadmap" in str(metadata["description"])

        for phrase in [
            "Define a Swift integration roadmap for Apple-platform and native client",
            "Swift should consume the shared core through C ABI, service, or",
            "must not duplicate formula logic",
            "Compare Swift C ABI, service, and file/Arrow interop.",
            "Define Swift request/response models, diagnostics, provenance, and fixture gates.",
            "Document Swift Package Manager publication only after parity and platform gates pass.",
            "Swift strategy is selected and documented.",
            "Swift examples validate against shared fixtures.",
            "Formula logic remains single-sourced outside Swift adapters.",
        ]:
            assert phrase in spec or phrase in plan

        for phrase in [
            "Select initial native/client-safe boundary.",
            "Define SPM and Apple-platform gating constraints.",
        ]:
            assert phrase in plan

        assert "Track swift_binding_20260513 Context" in index
        assert "Swift Binding" in tracks
        assert (
            "Swift Binding"
            in tracks
        )
        assert "audience/owner evidence gate" in tracks

        bundle_map = _as_mapping(bundle)
        diagnostics = _as_mapping(bundle_map["diagnostics"])
        provenance = _as_mapping(bundle_map["provenance"])
        swift_module = _as_mapping(bundle_map["swift_module"])

        assert bundle_map["schema_version"] == "1.0"
        assert bundle_map["binding_id"] == "swift_binding_20260513"
        assert bundle_map["surface"] == "swift"
        assert bundle_map["initial_strategy"] == "file-arrow exchange and CLI invocation"
        assert bundle_map["fallback_strategy"] == "service boundary"
        assert bundle_map["future_strategy"] == "c-abi integration"
        assert bundle_map["formula_logic_location"] == "rust core"
        assert bundle_map["swift_module_status"] == "transport-adapter-ready"
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
        assert swift_module["status"] == "transport-adapter-ready"
        assert swift_module["release_gate"] == "audience and owner evidence recorded"
        assert swift_module["platform_gate"] == "apple-platform ci matrix"
        assert live_contract["schema_version"] == "1.0"
        assert live_contract["privacy"]["classification"] == "synthetic"
        assert live_contract["privacy"]["contains_phi"] is False
        readiness = {
            item["id"]: item["state"]
            for item in cast(list[dict[str, str]], live_contract["module_readiness"])
        }
        assert readiness["swift_transport_adapter"] == "ready"
        assert readiness["file_exchange_boundary"] == "ready"
        assert readiness["cli_boundary"] == "ready"
        assert readiness["c_abi_path"] == "blocked"
        priorities = {
            mode["mode"]: mode["priority"] for mode in live_contract["transport_modes"]
        }
        assert priorities == {
            "file-exchange": "primary",
            "cli": "primary",
            "service": "fallback",
            "c-abi": "future",
        }

    def test_swift_binding_preserves_provenance_without_formula_logic(self):
        bundle = _load_json(CONTRACT_BUNDLE)
        diagnostics = _as_mapping(bundle["diagnostics"])
        provenance = _as_mapping(bundle["provenance"])
        swift_module = _as_mapping(bundle["swift_module"])

        assert bundle["formula_logic_location"] == "rust core"
        assert "swift" not in str(bundle["formula_logic_location"]).lower()
        assert diagnostics["format"] == "json"
        assert provenance["checksum_algorithm"] == "sha256"
        assert swift_module["status"] == "transport-adapter-ready"
        assert "publication" not in str(swift_module["status"]).lower()

    def test_swift_binding_if_a_scaffold_exists_it_stays_thin_and_non_formula(self):
        scaffold_root = ROOT / "bindings" / "swift"
        assert scaffold_root.exists(), scaffold_root

        scaffold_text = _squash(
            " ".join(
                _read_text(path)
                for path in scaffold_root.rglob("*")
                if path.is_file()
                and "bin" not in path.parts
                and "vendor" not in path.parts
                and "node_modules" not in path.parts
                and "target" not in path.parts
                and ".build" not in path.parts
                and path.suffix
                in {".md", ".txt", ".json", ".swift", ".c", ".h", ".modulemap", ".yaml", ".yml"}
            )
        ).lower()

        for forbidden in [
            "formula logic",
            "reimplement formula",
            "duplicate formulas",
            "swift module publication",
            "publication-ready",
            "production-ready",
        ]:
            assert forbidden not in scaffold_text

        assert "fileboundarybindingadapter" in scaffold_text
        assert "cliprocessbindingadapter" in scaffold_text
        assert "foundation.process" in scaffold_text or "process()" in scaffold_text
        assert "nwau_py.cli.main" in scaffold_text
