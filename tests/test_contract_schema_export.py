from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "contract_schema_export_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"

SAMPLE_CALCULATOR_INPUT_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CalculatorInput",
    "type": "object",
    "properties": {
        "pricing_year": {"type": "string", "pattern": "^\\d{4}$"},
        "stream": {
            "type": "string",
            "enum": [
                "acute",
                "subacute",
                "mental_health",
                "emergency",
                "outpatient",
                "community_mental_health",
            ],
        },
        "admission_date": {"type": "string", "format": "date"},
        "separation_date": {"type": "string", "format": "date"},
        "care_type": {"type": "string"},
        "ar_drg": {"type": "string"},
        "days_in_care": {"type": "integer", "minimum": 0},
        "same_day_flag": {"type": "boolean"},
    },
    "required": ["pricing_year", "stream"],
}

SAMPLE_CALCULATOR_OUTPUT_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CalculatorOutput",
    "type": "object",
    "properties": {
        "nwau": {"type": "number"},
        "nwau_components": {"type": "object"},
        "adjustments": {"type": "object"},
        "diagnostics": {"type": "object"},
        "pricing_year": {"type": "string"},
        "stream": {"type": "string"},
    },
    "required": ["nwau", "pricing_year", "stream"],
}

SAMPLE_PROVENANCE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ProvenanceRecord",
    "type": "object",
    "properties": {
        "source_id": {"type": "string"},
        "source_url": {"type": "string", "format": "uri"},
        "retrieved_at": {"type": "string", "format": "date-time"},
        "checksum_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "source_authority": {"type": "string"},
        "notes": {"type": "string"},
    },
    "required": ["source_id", "source_url", "retrieved_at", "checksum_sha256"],
}

SAMPLE_DIAGNOSTIC_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "DiagnosticRecord",
    "type": "object",
    "properties": {
        "run_id": {"type": "string"},
        "run_timestamp": {"type": "string", "format": "date-time"},
        "validator": {"type": "string"},
        "pricing_year": {"type": "string"},
        "stream": {"type": "string"},
        "fixture_pack_id": {"type": "string"},
        "result": {"type": "string", "enum": ["pass", "fail", "error", "skip"]},
        "details": {"type": "string"},
    },
    "required": ["run_id", "run_timestamp", "validator", "result"],
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_contract_schema_export_spec_defines_schema_inventory():
    spec = _read_text(TRACK / "contract_schema_export_spec.md")
    assert "Required Schemas" in spec
    assert "Calculator Input" in spec
    assert "Calculator Output" in spec
    assert "Pricing-Year Manifest" in spec
    assert "Formula Bundle" in spec


def test_contract_schema_export_spec_defines_versioning_policy():
    spec = _read_text(TRACK / "contract_schema_export_spec.md")
    assert "Versioning Policy" in spec
    assert "Schema versions are independent" in spec
    assert "semantic versioning" in spec


def test_contract_schema_export_spec_defines_determinism_requirement():
    spec = _read_text(TRACK / "contract_schema_export_spec.md")
    assert "Determinism Requirement" in spec
    assert "byte-identical" in spec


def test_contract_schema_export_spec_defines_output_locations():
    spec = _read_text(TRACK / "contract_schema_export_spec.md")
    assert "contracts/schemas/" in spec
    assert "Output Locations" in spec


def test_sample_calculator_input_schema_is_valid_json():
    schema_json = json.dumps(SAMPLE_CALCULATOR_INPUT_SCHEMA, indent=2)
    parsed = json.loads(schema_json)
    assert parsed["title"] == "CalculatorInput"
    assert "pricing_year" in parsed["properties"]
    assert "stream" in parsed["properties"]
    assert parsed["required"] == ["pricing_year", "stream"]


def test_sample_calculator_output_schema_is_valid_json():
    schema_json = json.dumps(SAMPLE_CALCULATOR_OUTPUT_SCHEMA, indent=2)
    parsed = json.loads(schema_json)
    assert parsed["title"] == "CalculatorOutput"
    assert "nwau" in parsed["properties"]
    assert parsed["required"] == ["nwau", "pricing_year", "stream"]


def test_sample_provenance_schema_is_valid_json():
    schema_json = json.dumps(SAMPLE_PROVENANCE_SCHEMA, indent=2)
    parsed = json.loads(schema_json)
    assert parsed["title"] == "ProvenanceRecord"
    assert "checksum_sha256" in parsed["properties"]
    assert "source_url" in parsed["properties"]


def test_sample_diagnostic_schema_is_valid_json():
    schema_json = json.dumps(SAMPLE_DIAGNOSTIC_SCHEMA, indent=2)
    parsed = json.loads(schema_json)
    assert parsed["title"] == "DiagnosticRecord"
    assert parsed["properties"]["result"]["enum"] == ["pass", "fail", "error", "skip"]


def test_schema_export_is_deterministic():
    schemas = [
        SAMPLE_CALCULATOR_INPUT_SCHEMA,
        SAMPLE_CALCULATOR_OUTPUT_SCHEMA,
        SAMPLE_PROVENANCE_SCHEMA,
        SAMPLE_DIAGNOSTIC_SCHEMA,
    ]
    for schema in schemas:
        first = json.dumps(schema, indent=2, sort_keys=True)
        second = json.dumps(json.loads(first), indent=2, sort_keys=True)
        assert first == second


def test_contract_schema_export_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACK / "review.md",
        TRACK / "contract_schema_export_spec.md",
    ]:
        assert path.exists(), path


def test_contract_schema_export_track_metadata():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    assert metadata["track_id"] == "contract_schema_export_20260512"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "data-contract"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "contracts/canonical/calculator.schema.json" in metadata[
        "completion_evidence"
    ]


def test_contract_schema_export_in_tracks_registry():
    registry = _read_text(TRACKS_REGISTRY)
    assert "Contract Schema Export" in registry
    assert "./archive/contract_schema_export_20260512/" in registry
