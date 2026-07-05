from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from nwau_py.hwau import normalize_hwau_result

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "hwau_terminology_migration_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "pricing-and-hwau-strategy.md"
HTTP_RESPONSE = (
    ROOT / "contracts" / "http-api" / "examples" / "calculation-response.json"
)
OPENAPI = ROOT / "contracts" / "http-api" / "openapi.yaml"
OPENAI_EXAMPLES = ROOT / "contracts" / "openai-adapter" / "examples.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_hwau_result_normalizer_preserves_nwau_alias_for_compatibility():
    result = normalize_hwau_result({"nwau": 4.85, "totalCost": 4520.75})

    assert result == {"nwau": 4.85, "totalCost": 4520.75, "hwau": 4.85}


def test_hwau_result_normalizer_rejects_conflicting_alias_values():
    try:
        normalize_hwau_result({"hwau": 4.8, "nwau": 4.9})
    except ValueError as exc:
        assert "conflicting HWAU/NWAU aliases" in str(exc)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("expected conflicting HWAU/NWAU alias values to fail")


def test_public_contract_examples_expose_hwau_with_nwau_compatibility_alias():
    response = _json(HTTP_RESPONSE)
    result = response["result"]
    normalized = normalize_hwau_result(result)

    assert result["hwau"] == result["nwau"]
    assert normalized["hwau"] == normalized["nwau"]
    assert "generic HWAU" in _read(OPENAI_EXAMPLES)
    assert '"hwau": 4.85' in _read(OPENAI_EXAMPLES)
    assert '"nwau": 4.85' in _read(OPENAI_EXAMPLES)


def test_openapi_documents_hwau_and_nwau_aliases_for_calculation_result():
    openapi = yaml.safe_load(_read(OPENAPI))
    result_schema = openapi["components"]["schemas"]["CalculationResult"]
    properties = result_schema["properties"]

    assert properties["hwau"]["description"].startswith("Generic healthcare")
    assert properties["nwau"]["description"].startswith("Australian")
    assert set(result_schema["required"]) >= {"totalCost", "hwau", "currency"}


def test_hwau_archive_metadata_and_registry_are_complete_with_alias_evidence():
    metadata = _json(TRACK / "metadata.json")
    plan = _read(TRACK / "plan.md")
    registry = _read(TRACKS)
    roadmap = _read(ROADMAP)

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert "tests/test_hwau_terminology_migration_archive_track.py" in (
        metadata["completion_evidence"]
    )
    assert metadata["gap_register"][0]["status"] == "partially-resolved"
    assert "[checkpoint:" in plan
    assert "Runtime and Schema Alias Evidence" in plan
    assert "- [x] **Track: HWAU Terminology Migration**" in registry
    assert "healthcare weighted activity unit" in roadmap
