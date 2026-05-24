from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "cli_file_interop_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
INTEROP_ROOT = ROOT / "contracts" / "interop"
INTEROP_SCHEMA = INTEROP_ROOT / "cli-file-interop.schema.json"
INTEROP_CONTRACT = INTEROP_ROOT / "cli-file-interop.contract.json"
INTEROP_JOB = INTEROP_ROOT / "examples" / "acute-batch.job.json"
INTEROP_RESULT = INTEROP_ROOT / "examples" / "acute-batch.result.json"
CSV_GOLDEN_MANIFEST = (
    ROOT / "tests" / "fixtures" / "golden" / "acute_2025" / "manifest.json"
)
ARROW_BUNDLE_MANIFEST = (
    ROOT / "tests" / "fixtures" / "bundles" / "acute_2025" / "manifest.json"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read_text(path))


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _as_sequence(value: object) -> list[Any]:
    assert isinstance(value, list)
    return value


def test_cli_file_interop_track_scaffold_and_registry_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        INTEROP_SCHEMA,
        INTEROP_CONTRACT,
        INTEROP_JOB,
        INTEROP_RESULT,
        INTEROP_ROOT / "README.md",
        CSV_GOLDEN_MANIFEST,
        ARROW_BUNDLE_MANIFEST,
    ]:
        assert path.exists(), path

    track_index = _read_text(TRACK / "index.md")
    registry = _read_text(TRACKS_REGISTRY)

    assert "cli_file_interop_binding_20260512" in track_index
    assert "CLI and File Interoperability Binding" in registry
    assert (
        "Gate: provide a language-neutral Arrow/Parquet/CSV and CLI contract"
        in registry
    )


def test_cli_file_interop_docs_cover_versioned_contracts_round_trips_and_privacy():
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    strategy = _read_text(TRACK / "strategy.md")
    ci_notes = _read_text(TRACK / "ci_notes.md")
    registry = _read_text(TRACKS_REGISTRY)
    spec_lower = spec.lower()
    plan_lower = plan.lower()

    for phrase in [
        "CLI input/output contracts are versioned and documented.",
        "Support Arrow/Parquet as preferred interchange and CSV as "
        "compatibility input/output.",
        "Emit structured diagnostics and provenance metadata.",
        "Golden fixtures validate file-based round trips.",
        "Docs explain when to use file interop instead of native bindings.",
    ]:
        assert phrase in spec

    for phrase in [
        "versioned CLI commands and file contract",
        "Arrow/Parquet as the target interchange format",
        "schema requirements, diagnostics, provenance",
        "machine-readable contract bundle",
        "schema/version regression tests",
        "synthetic-data and privacy guardrail tests",
        "file round-trip tests and language-neutral examples",
        "golden fixtures for Arrow/Parquet",
    ]:
        assert phrase in plan

    assert "language-neutral Arrow/Parquet/CSV and CLI contract" in registry
    assert "structured diagnostics" in spec_lower
    assert "provenance metadata" in spec_lower
    assert "synthetic-data and privacy guardrail tests" in plan_lower
    assert "synthetic-data and privacy" in plan_lower
    assert "versioned CLI plus file-interchange contract" in strategy
    assert "Arrow/Parquet as the target interchange format" in strategy
    assert "CSV is a bridge" in strategy
    assert "uv run funding-calculator interop contract" in ci_notes
    assert "./target/debug/<cli-binary>" in ci_notes
    assert "unless a Rust CLI binary has actually" in ci_notes


def test_cli_file_interop_contract_bundle_is_versioned_and_privacy_safe():
    schema = _load_json(INTEROP_SCHEMA)
    contract = _load_json(INTEROP_CONTRACT)
    job = _load_json(INTEROP_JOB)
    result = _load_json(INTEROP_RESULT)
    schema_properties = _as_mapping(schema["properties"])
    schema_privacy = _as_mapping(schema_properties["privacy"])
    schema_privacy_properties = _as_mapping(schema_privacy["properties"])
    schema_contains_phi = _as_mapping(schema_privacy_properties["contains_phi"])

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "privacy" in _as_sequence(schema["required"])
    assert schema_contains_phi["const"] is False

    assert contract["schema_version"] == "1.0"
    assert contract["interop_id"] == "cli_file_interop_binding_20260512"
    contract_tool = _as_mapping(contract["tool"])
    contract_schema = _as_mapping(contract["schema"])
    contract_privacy = _as_mapping(contract["privacy"])
    contract_diagnostics = _as_mapping(contract["diagnostics"])
    contract_provenance = _as_mapping(contract["provenance"])
    assert contract_tool["entry_point"] == "nwau_py.cli.main:cli"
    assert contract_schema["path"] == str(INTEROP_SCHEMA.relative_to(ROOT))
    assert contract_privacy["classification"] == "synthetic"
    assert contract_privacy["contains_phi"] is False
    assert contract_diagnostics["format"] == "json"
    assert contract_diagnostics["location"] == "stderr"
    assert contract_provenance["checksum_algorithm"] == "sha256"
    assert {"csv", "parquet", "arrow"} <= set(_as_sequence(contract["file_formats"]))

    command_items = [_as_mapping(item) for item in _as_sequence(contract["commands"])]
    commands = {str(command["name"]): command for command in command_items}
    assert {"acute", "ed", "non-admitted", "interop contract"} <= set(commands)
    assert "csv" in _as_sequence(commands["acute"]["input_formats"])
    assert "parquet" in _as_sequence(commands["acute"]["output_formats"])

    for manifest in [job, result]:
        assert manifest["schema_version"] == "1.0"
        privacy = _as_mapping(manifest["privacy"])
        provenance = _as_mapping(manifest["provenance"])
        assert privacy["classification"] == "synthetic"
        assert privacy["contains_phi"] is False
        assert "synthetic" in str(provenance["notes"]).lower()


def test_cli_file_interop_fixture_manifests_require_round_trip_and_synthetic_data():
    csv_manifest = _load_json(CSV_GOLDEN_MANIFEST)
    arrow_manifest = _load_json(ARROW_BUNDLE_MANIFEST)

    assert csv_manifest["schema_version"] == "1.0"
    assert csv_manifest["fixture_id"] == "acute_2025"
    assert csv_manifest["privacy_classification"] == "synthetic"
    assert csv_manifest["cross_language_ready"] is True
    csv_payloads = _as_mapping(csv_manifest["payloads"])
    csv_input = _as_mapping(csv_payloads["input"])
    csv_expected = _as_mapping(csv_payloads["expected_output"])
    csv_source_basis = _as_mapping(csv_manifest["source_basis"])
    csv_provenance = _as_mapping(csv_manifest["provenance"])
    csv_notes = _as_sequence(csv_provenance["notes"])
    assert csv_input["format"] == "csv"
    assert csv_expected["format"] == "csv"
    assert csv_input["path"] == "input.csv"
    assert csv_expected["path"] == "expected.csv"
    assert csv_source_basis["kind"] == "synthetic_sample"
    assert "synthetic fixture pack for cross-language parity checks." in (
        str(csv_notes[0]).lower()
    )
    assert "no patient-level or production data included." in (
        str(csv_notes[1]).lower()
    )

    assert arrow_manifest["schema_version"] == "1.0"
    assert arrow_manifest["bundle_id"] == "acute_2025"
    assert arrow_manifest["backend_neutral"] is True
    arrow_payloads = _as_mapping(arrow_manifest["payloads"])
    arrow_input = _as_mapping(arrow_payloads["input"])
    arrow_expected = _as_mapping(arrow_payloads["expected_output"])
    arrow_provenance = _as_mapping(arrow_manifest["provenance"])
    arrow_notes = _as_sequence(arrow_provenance["notes"])
    assert arrow_input["format"] == "parquet"
    assert arrow_expected["format"] == "parquet"
    assert arrow_input["path"] == "input.parquet"
    assert arrow_expected["path"] == "expected_output.parquet"
    assert "synthetic arrow/parquet bundle for bundle-contract tests" in (
        str(arrow_notes[0]).lower()
    )
    assert "no patient-level data included" in (str(arrow_notes[1]).lower())


def test_cli_file_interop_track_metadata_stays_roadmap_only():
    metadata = _load_json(TRACK / "metadata.json")
    index = _read_text(TRACK / "index.md")

    assert metadata["track_id"] == "cli_file_interop_binding_20260512"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "complete"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "prototype"
    assert metadata["publication_status"] == "not-ready"
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert "CLI and file interoperability contract scaffold" in str(
        metadata["description"]
    )
    assert "Complete." in index
