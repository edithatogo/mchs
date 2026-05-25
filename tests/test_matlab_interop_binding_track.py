from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "matlab_interop_binding_20260513"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "matlab_interop_binding"
CONTRACT_BUNDLE = FIXTURE_ROOT / "contract_bundle.json"
CONTRACT_ROOT = ROOT / "contracts" / "matlab-interop-binding"
LIVE_CONTRACT = CONTRACT_ROOT / "matlab-interop-binding.contract.json"
LIVE_SCHEMA = CONTRACT_ROOT / "matlab-interop-binding.schema.json"
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


def test_matlab_interop_binding_metadata_docs_and_contract_bundle_are_conservative():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        CONTRACT_BUNDLE,
        LIVE_CONTRACT,
        LIVE_SCHEMA,
        LIVE_EXAMPLES / "file-import.pass.json",
        LIVE_EXAMPLES / "cli-invocation.pass.json",
        LIVE_EXAMPLES / "binding.fail.json",
        LIVE_EXAMPLES / "diagnostics.pass.json",
        LIVE_EXAMPLES / "diagnostics.fail.json",
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    tracks = _read_text(TRACKS_REGISTRY)
    bundle = _load_json(CONTRACT_BUNDLE)
    live_contract = _load_json(LIVE_CONTRACT)
    file_import_pass = _load_json(LIVE_EXAMPLES / "file-import.pass.json")
    cli_invocation_pass = _load_json(LIVE_EXAMPLES / "cli-invocation.pass.json")
    binding_fail = _load_json(LIVE_EXAMPLES / "binding.fail.json")

    assert metadata["track_id"] == "matlab_interop_binding_20260513"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "adapter-ready-with-deferred-release-gates"
    assert metadata["primary_contract"] == (
        "contracts/matlab-interop-binding/matlab-interop-binding.contract.json"
    )
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert "MATLAB interoperability" in str(metadata["description"])

    for phrase in [
        "Define MATLAB interoperability for numerical, simulation, teaching, "
        "and legacy",
        "MATLAB should consume file, CLI, service, or C ABI",
        "must not duplicate formula logic",
        "Compare MAT/CSV/Parquet, CLI/service, and C ABI interop",
        "Document toolbox publication only after fixture and platform gates pass",
        "Define MATLAB file, CLI/service, and C ABI interop strategy",
        "Select initial reproducible analytics boundary",
        "Define toolbox and platform gating constraints",
        "Validate diagnostics and provenance against the shared contract",
        "Document numerical analytics workflow patterns",
    ]:
        assert phrase in spec or phrase in plan

    assert "Track matlab_interop_binding_20260513 Context" in index
    assert "MATLAB Interoperability" in tracks
    assert "audience/owner evidence gate" in tracks

    bundle_map = _as_mapping(bundle)
    diagnostics = _as_mapping(bundle_map["diagnostics"])
    provenance = _as_mapping(bundle_map["provenance"])
    matlab_module = _as_mapping(bundle_map["matlab_module"])

    assert bundle_map["schema_version"] == "1.0"
    assert bundle_map["binding_id"] == "matlab_interop_binding_20260513"
    assert bundle_map["surface"] == "matlab"
    assert bundle_map["initial_strategy"] == "file-import and cli-invocation interop"
    assert bundle_map["fallback_strategy"] == "mat-exchange and c-abi-mex boundary"
    assert bundle_map["formula_logic_location"] == "rust core"
    assert bundle_map["matlab_module_status"] == "adapter-ready"
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
    assert matlab_module["status"] == "adapter-ready"
    assert matlab_module["release_gate"] == (
        "toolbox publication, platform parity, and audience owner gates still deferred"
    )
    assert live_contract["schema_version"] == "1.0"
    assert live_contract["privacy"]["classification"] == "synthetic"
    assert live_contract["privacy"]["contains_phi"] is False
    priorities = {
        mode["mode"]: mode["priority"] for mode in live_contract["transport_modes"]
    }
    assert priorities == {
        "file-import": "primary",
        "cli-invocation": "primary",
        "mat-exchange": "fallback",
        "c-abi-mex": "fallback",
    }
    readiness = {
        item["id"]: item["state"] for item in live_contract["module_readiness"]
    }
    assert readiness["matlab_file_cli_adapter"] == "adapter_ready"
    assert readiness["file_import_boundary"] == "adapter_ready"
    assert readiness["cli_invocation_boundary"] == "adapter_ready"
    file_import_checks = file_import_pass["response"]["diagnostics"]["checks"]
    assert {check["status"] for check in file_import_checks} == {"pass"}
    assert file_import_pass["response"]["module_readiness_state"] == "adapter_ready"
    assert cli_invocation_pass["response"]["mode"] == "cli-invocation"
    assert cli_invocation_pass["response"]["module_readiness_state"] == "adapter_ready"
    assert "fail" in {
        check["status"] for check in binding_fail["response"]["diagnostics"]["checks"]
    }


def test_matlab_interop_binding_preserves_provenance_without_formula_logic():
    bundle = _load_json(CONTRACT_BUNDLE)
    diagnostics = _as_mapping(bundle["diagnostics"])
    provenance = _as_mapping(bundle["provenance"])
    matlab_module = _as_mapping(bundle["matlab_module"])

    assert bundle["formula_logic_location"] == "rust core"
    assert "matlab" not in str(bundle["formula_logic_location"]).lower()
    assert diagnostics["format"] == "json"
    assert provenance["checksum_algorithm"] == "sha256"
    assert matlab_module["status"] == "adapter-ready"
    assert "publication" not in str(matlab_module["status"]).lower()


def test_matlab_interop_binding_adapter_is_concrete_file_cli_boundary_only():
    candidate_roots = [
        ROOT / "matlab-binding",
        ROOT / "bindings" / "matlab",
        ROOT / "src" / "matlab",
        ROOT / "matlab",
        ROOT / "matlab-binding-scaffold",
    ]
    scaffold_root = next((path for path in candidate_roots if path.exists()), None)

    if scaffold_root is None:
        return

    matlab_root = ROOT / "bindings" / "matlab" / "mchs"
    expected_adapter_files = [
        matlab_root / "validateInput.m",
        matlab_root / "importResultTable.m",
        matlab_root / "invokeCli.m",
    ]
    for path in expected_adapter_files:
        assert path.exists(), path

    validate_input = _read_text(matlab_root / "validateInput.m")
    import_result_table = _read_text(matlab_root / "importResultTable.m")
    invoke_cli = _read_text(matlab_root / "invokeCli.m")
    assert "isfile(inputPath)" in validate_input
    assert "RequiredColumns" in validate_input
    assert "readtable(outputPath)" in import_result_table
    assert "parquetread(outputPath)" in import_result_table
    assert "[exitCode, stdoutText] = system(command)" in invoke_cli
    assert "output_file_created" in invoke_cli

    scaffold_text = _squash(
        " ".join(
            _read_text(path)
            for path in scaffold_root.rglob("*")
            if path.is_file()
            and "bin" not in path.parts
            and "vendor" not in path.parts
            and "node_modules" not in path.parts
            and "target" not in path.parts
            and path.suffix in {".md", ".txt", ".json", ".m", ".mat", ".yaml", ".yml"}
        )
    ).lower()

    for forbidden in [
        "formula logic",
        "reimplement formula",
        "duplicate formulas",
        "matlab toolbox publication",
        "publication-ready",
        "production-ready",
        "acute weight",
        "nwau weight",
        "funding adjustment",
    ]:
        assert forbidden not in scaffold_text
