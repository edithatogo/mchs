from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "stata_interop_binding_20260513"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "stata_interop_binding"
CONTRACT_BUNDLE = FIXTURE_ROOT / "contract_bundle.json"
CONTRACT_ROOT = ROOT / "contracts" / "stata-interop-binding"
LIVE_CONTRACT = CONTRACT_ROOT / "stata-interop-binding.contract.json"
LIVE_SCHEMA = CONTRACT_ROOT / "stata-interop-binding.schema.json"
LIVE_EXAMPLES = CONTRACT_ROOT / "examples"
STATA_ROOT = ROOT / "bindings" / "stata"
STATA_ADO = STATA_ROOT / "mchs.ado"


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


def test_stata_interop_track_metadata_docs_and_contract_bundle_are_conservative():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        CONTRACT_BUNDLE,
        LIVE_CONTRACT,
        LIVE_SCHEMA,
        LIVE_EXAMPLES / "csv-parquet.pass.json",
        LIVE_EXAMPLES / "service.pass.json",
        LIVE_EXAMPLES / "binding.fail.json",
        STATA_ADO,
        STATA_ROOT / "mchs.sthlp",
        STATA_ROOT / "README.md",
        STATA_ROOT / "examples" / "file_import_workflow.do",
        STATA_ROOT / "examples" / "nwau_cli_invocation.do",
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    tracks = _read_text(TRACKS_REGISTRY)
    bundle = _load_json(CONTRACT_BUNDLE)
    live_contract = _load_json(LIVE_CONTRACT)
    csv_parquet_pass = _load_json(LIVE_EXAMPLES / "csv-parquet.pass.json")
    service_pass = _load_json(LIVE_EXAMPLES / "service.pass.json")
    binding_fail = _load_json(LIVE_EXAMPLES / "binding.fail.json")

    assert metadata["track_id"] == "stata_interop_binding_20260513"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "file-cli-adapter-ready-with-publication-gates"
    assert metadata["primary_contract"] == (
        "contracts/stata-interop-binding/stata-interop-binding.contract.json"
    )
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["completion_evidence"] == [
        "docs",
        "workflows",
        "tests",
        "bounded-adapter",
    ]
    assert "Stata interoperability" in str(metadata["description"])

    spec_squashed = _squash(spec)
    plan_squashed = _squash(plan)

    for phrase in [
        "Define Stata interoperability for health economics and applied policy users.",
        "Stata should use file, CLI, or service boundaries for costing studies and must not contain a separate formula implementation.",
        "Define CSV/Parquet/DTA exchange and CLI/service invocation patterns.",
        "Preserve diagnostics, provenance, and validation status in Stata-readable outputs.",
        "Document package publication only after fixture and reproducibility gates pass.",
        "Stata interop strategy is selected and documented.",
        "Examples validate against shared fixtures.",
        "Formula logic remains single-sourced outside Stata scripts.",
    ]:
        assert phrase in spec_squashed or phrase in plan_squashed

    for phrase in [
        "Select initial reproducible costing-study boundary.",
        "Define DTA/CSV/Parquet and package gating constraints.",
        "Promote legacy status wording to bounded file/CLI adapter.",
    ]:
        assert phrase in plan_squashed

    assert "Track stata_interop_binding_20260513 Context" in index
    assert "Stata Interoperability" in tracks
    assert "Rust Core GA" in tracks

    bundle_map = _as_mapping(bundle)
    diagnostics = _as_mapping(bundle_map["diagnostics"])
    provenance = _as_mapping(bundle_map["provenance"])
    stata_module = _as_mapping(bundle_map["stata_interop_module"])

    assert bundle_map["schema_version"] == "1.0"
    assert bundle_map["binding_id"] == "stata_interop_binding_20260513"
    assert bundle_map["surface"] == "stata"
    assert bundle_map["initial_strategy"] == "file-import cli-invocation interop"
    assert bundle_map["fallback_strategy"] == "dta-exchange service boundary"
    assert bundle_map["formula_logic_location"] == "rust core"
    assert bundle_map["stata_interop_status"] == "complete-with-gaps"
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
    assert stata_module["status"] == "complete-with-gaps"
    assert stata_module["release_gate"] == "contract and parity stable"
    assert live_contract["schema_version"] == "1.0"
    assert live_contract["privacy"]["classification"] == "synthetic"
    assert live_contract["privacy"]["contains_phi"] is False
    priorities = {
        mode["mode"]: mode["priority"] for mode in live_contract["transport_modes"]
    }
    assert priorities == {
        "file-import": "primary",
        "cli-invocation": "primary",
        "dta-exchange": "fallback",
        "service": "fallback",
    }
    csv_parquet_checks = csv_parquet_pass["response"]["diagnostics"]["checks"]
    assert {check["status"] for check in csv_parquet_checks} == {"pass"}
    assert service_pass["response"]["mode"] == "service"
    assert "fail" in {
        check["status"] for check in binding_fail["response"]["diagnostics"]["checks"]
    }

    readiness = {
        item["id"]: item["state"] for item in live_contract["module_readiness"]
    }
    assert readiness["stata_file_cli_adapter"] == "ready"
    assert readiness["stata_package_publication"] == "deferred"


def test_stata_interop_preserves_provenance_without_formula_logic():
    bundle = _load_json(CONTRACT_BUNDLE)
    diagnostics = _as_mapping(bundle["diagnostics"])
    provenance = _as_mapping(bundle["provenance"])
    stata_module = _as_mapping(bundle["stata_interop_module"])

    assert bundle["formula_logic_location"] == "rust core"
    assert "stata" not in str(bundle["formula_logic_location"]).lower()
    assert diagnostics["format"] == "json"
    assert provenance["checksum_algorithm"] == "sha256"
    assert stata_module["status"] == "complete-with-gaps"
    assert "publication" not in str(stata_module["status"]).lower()


def test_stata_ado_exposes_concrete_transport_adapter_without_formula_logic():
    ado = _read_text(STATA_ADO)
    ado_squashed = _squash(ado).lower()
    docs = _squash(_read_text(STATA_ROOT / "README.md")).lower()
    help_text = _squash(_read_text(STATA_ROOT / "mchs.sthlp")).lower()
    cli_example = _squash(
        _read_text(STATA_ROOT / "examples" / "nwau_cli_invocation.do")
    ).lower()
    import_example = _squash(
        _read_text(STATA_ROOT / "examples" / "file_import_workflow.do")
    ).lower()

    for required in [
        "program define mchs, rclass",
        "program define _mchs_import, rclass",
        "program define _mchs_run, rclass",
        "program define _mchs_validate, rclass",
        "syntax using/ [, clear saveas(string asis) replace]",
        "syntax using/ , calculator(string) year(string) output(string asis)",
        "local cli \"funding-calculator\"",
        "shell `cmd'",
        "import delimited using",
        "confirm file",
        "confirm new file",
        "contract_version calculator_id pricing_year fixture_gate",
    ]:
        assert required in ado_squashed

    for required in [
        "mchs import using",
        "mchs run using",
        "mchs validate",
        "delegating all calculations to the shared core",
    ]:
        assert required in docs or required in help_text

    assert "mchs run using" in cli_example
    assert "mchs validate" in cli_example
    assert "mchs import using" in import_example
    assert "mchs validate" in import_example


def test_stata_interop_scaffold_is_thin_and_non_formula():
    candidate_roots = [
        ROOT / "stata-interop",
        ROOT / "bindings" / "stata",
        ROOT / "src" / "stata",
        ROOT / "stata",
        ROOT / "stata-binding-scaffold",
        ROOT / "cmd" / "stata-binding",
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
            in {".md", ".txt", ".json", ".do", ".ado", ".yaml", ".yml"}
        )
    ).lower()

    for forbidden in [
        "implement formula logic",
        "stata formula implementation",
        "stata package is ready",
        "publication-ready",
        "production-ready",
        "stata code implements",
    ]:
        assert forbidden not in scaffold_text
