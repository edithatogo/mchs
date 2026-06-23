from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "power_platform_binding_20260512"
CONTRACT_ROOT = ROOT / "contracts" / "power-platform"
CONTRACT = CONTRACT_ROOT / "power-platform-binding.contract.json"
SCHEMA = CONTRACT_ROOT / "power-platform-binding.schema.json"
OPENAPI = CONTRACT_ROOT / "custom-connector.openapi.yaml"
CAPABILITY_MATRIX = CONTRACT_ROOT / "calculator-capability-matrix.json"
POWER_PLATFORM_ROOT = ROOT / "power-platform"
APP_SURFACE = POWER_PLATFORM_ROOT / "solution" / "app-surface.json"
CAPABILITIES_EXAMPLE = CONTRACT_ROOT / "examples" / "capabilities.pass.json"
PASS_EXAMPLE = CONTRACT_ROOT / "examples" / "validation.pass.json"
FAIL_EXAMPLE = CONTRACT_ROOT / "examples" / "validation.fail.json"
RAW_ARCHIVE_MANIFEST = ROOT / "archive" / "ihacpa" / "raw" / "manifest.json"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return cast(dict[str, Any], payload)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(_read_text(path))
    assert isinstance(payload, dict)
    return cast(dict[str, Any], payload)


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _as_sequence(value: object) -> list[Any]:
    assert isinstance(value, list)
    return value


def _source_evidence_exists(source_path: str) -> bool:
    raw_manifest = _as_sequence(json.loads(_read_text(RAW_ARCHIVE_MANIFEST)))
    manifest_paths = {
        entry["path"]
        for entry in raw_manifest
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    return (ROOT / source_path).exists() or source_path in manifest_paths


def test_power_platform_binding_contract_artifacts_exist_and_are_parseable():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "binding_strategy.md",
        TRACK / "metadata.json",
        POWER_PLATFORM_ROOT / "connectors" / "service-boundary-contract.md",
        POWER_PLATFORM_ROOT / "solution" / "app-surface.md",
        APP_SURFACE,
        POWER_PLATFORM_ROOT / "solution" / "environment-variables.md",
        POWER_PLATFORM_ROOT / "solution" / "solution-manifest.md",
        CONTRACT_ROOT / "README.md",
        CONTRACT,
        SCHEMA,
        OPENAPI,
        CAPABILITY_MATRIX,
        CAPABILITIES_EXAMPLE,
        PASS_EXAMPLE,
        FAIL_EXAMPLE,
    ]:
        assert path.exists(), path

    schema = _load_json(SCHEMA)
    contract = _load_json(CONTRACT)
    openapi = _load_yaml(OPENAPI)
    capability_matrix = _load_json(CAPABILITY_MATRIX)
    app_surface = _load_json(APP_SURFACE)
    capabilities_example = _load_json(CAPABILITIES_EXAMPLE)
    pass_example = _load_json(PASS_EXAMPLE)
    fail_example = _load_json(FAIL_EXAMPLE)

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["title"] == "Power Platform binding contract"
    assert contract["schema_version"] == "1.0"
    assert contract["contract_id"] == "power_platform_binding_20260512"
    assert openapi["openapi"] == "3.0.1"
    assert capability_matrix["schema_version"] == "1.0"
    assert capability_matrix["pricing_years"] == [
        str(year) for year in range(2013, 2027)
    ]
    assert app_surface["mode"] == "orchestration-only"
    assert capabilities_example["operation_id"] == "listMchsCalculatorCapabilities"
    capability_messages = " ".join(
        assertion["message"] for assertion in capabilities_example["assertions"]
    )
    assert "2013 through 2026" in capability_messages
    assert "Source-available" in capability_messages
    assert "historical variant surfaces" in capability_messages
    assert pass_example["result"] == "pass"
    assert fail_example["result"] == "fail"


def test_power_platform_binding_declares_service_api_boundary_not_formula_logic():
    metadata = _load_json(TRACK / "metadata.json")
    contract = _load_json(CONTRACT)
    pass_example = _load_json(PASS_EXAMPLE)
    fail_example = _load_json(FAIL_EXAMPLE)
    surface = _as_mapping(contract["surface"])
    policy = _as_mapping(contract["formula_logic_policy"])
    public_contract = _as_mapping(contract["public_calculator_contract"])

    assert metadata["track_id"] == "power_platform_binding_20260512"
    assert metadata["primary_contract"] == (
        "contracts/power-platform/power-platform-binding.contract.json"
    )
    assert metadata["current_state"] == "runtime-evidence-recorded-with-blockers"
    assert "remaining endpoint/connection/runtime blockers" in metadata["description"]

    assert surface["platform"] == "Power Platform"
    assert surface["mode"] == "orchestration-only"
    assert surface["formula_logic_location"] == "shared-service-boundary"
    assert public_contract["source"] == "conductor/public-api-contract.md"
    assert public_contract["alignment_mode"] == "request-response-compatible"
    assert policy["allowed_in_power_platform"] is False
    assert policy["runtime_owner"] == "shared calculator service"
    assert "Power Automate expressions" in policy["blocked_assets"]
    assert "NWAU formula constants" in policy["blocked_terms"]
    assert pass_example["power_platform_formula_logic"] is False
    assert pass_example["formula_logic_location"] == "shared-service-boundary"
    assert "Power Platform-owned calculation logic" in fail_example["rejected_pattern"]


def test_power_platform_openapi_matches_contract_operations_and_request_envelope():
    contract = _load_json(CONTRACT)
    openapi = _load_yaml(OPENAPI)
    paths = _as_mapping(openapi["paths"])
    components = _as_mapping(openapi["components"])
    schemas = _as_mapping(components["schemas"])
    request_schema = _as_mapping(schemas["PowerPlatformCalculationRequest"])

    operation_ids = set(_as_sequence(_as_mapping(contract["openapi"])["operation_ids"]))
    discovered_operation_ids = {
        _as_mapping(_as_mapping(paths["/capabilities"])["get"])["operationId"],
        _as_mapping(_as_mapping(paths["/validate"])["post"])["operationId"],
        _as_mapping(_as_mapping(paths["/calculations"])["post"])["operationId"],
    }

    assert operation_ids == {
        "listMchsCalculatorCapabilities",
        "validateMchsCalculatorInput",
        "runMchsCalculation",
    }
    assert discovered_operation_ids == operation_ids
    assert request_schema["additionalProperties"] is False
    capability_schema = _as_mapping(schemas["PowerPlatformCalculatorCapability"])
    year_state_schema = _as_mapping(
        _as_mapping(_as_mapping(capability_schema["properties"])["year_states"])[
            "additionalProperties"
        ]
    )
    assert "source_evidence" in capability_schema["required"]
    assert "variant_surfaces" in capability_schema["properties"]
    assert "PowerPlatformCalculatorVariant" in schemas
    assert "source_available" in year_state_schema["enum"]
    assert set(_as_sequence(request_schema["required"])) == {
        "contract_version",
        "calculator_id",
        "pricing_year",
        "fixture_gate",
        "correlation_id",
        "input",
    }

    operations = {
        operation["operation_id"]: operation
        for operation in _as_sequence(contract["operations"])
    }
    capabilities = _as_mapping(operations["listMchsCalculatorCapabilities"])
    validate = _as_mapping(operations["validateMchsCalculatorInput"])
    calculate = _as_mapping(operations["runMchsCalculation"])
    assert capabilities["executes_calculation"] is False
    assert capabilities["path"] == "/capabilities"
    assert validate["executes_calculation"] is False
    assert calculate["executes_calculation"] is True
    assert calculate["execution_owner"] == "shared calculator service"
    assert validate["path"] == "/validate"
    assert calculate["path"] == "/calculations"


def test_power_platform_capability_matrix_covers_all_app_calculators_and_years():
    contract = _load_json(CONTRACT)
    matrix = _load_json(CAPABILITY_MATRIX)
    capability = _as_mapping(contract["capability_matrix"])
    years = set(_as_sequence(matrix["pricing_years"]))
    calculators = {
        row["calculator_id"]: _as_mapping(row)
        for row in _as_sequence(matrix["calculators"])
    }

    assert (
        capability["path"]
        == "contracts/power-platform/calculator-capability-matrix.json"
    )
    assert capability["operation_id"] == "listMchsCalculatorCapabilities"
    assert set(_as_sequence(capability["enabled_states"])) == {"implemented", "helper"}
    assert set(_as_sequence(capability["disabled_states"])) == {
        "source_available",
        "shadow",
        "planned",
        "blocked",
        "not_available",
    }
    assert years == {str(year) for year in range(2013, 2027)}
    assert matrix["pricing_years"] == [str(year) for year in range(2013, 2027)]
    assert set(calculators) == {
        "acute",
        "ed",
        "mh",
        "community_mh",
        "subacute",
        "outpatients",
        "adjustment",
        "hac",
        "ahr",
    }

    for calculator in calculators.values():
        year_states = _as_mapping(calculator["year_states"])
        source_evidence = _as_mapping(calculator["source_evidence"])
        assert set(year_states) == years
        assert calculator["service_operation"] == "runMchsCalculation"
        assert year_states["2026"] in {"planned", "source_available"}
        assert year_states["2024"] in {"source_available", "shadow"}
        assert isinstance(source_evidence, dict)
        for evidence_path in source_evidence.values():
            assert _source_evidence_exists(evidence_path), evidence_path

    for calculator_id in {"acute", "ed", "subacute", "outpatients"}:
        year_states = _as_mapping(calculators[calculator_id]["year_states"])
        source_evidence = _as_mapping(calculators[calculator_id]["source_evidence"])
        for pricing_year in {str(year) for year in range(2013, 2026)}:
            assert year_states[pricing_year] in {"source_available", "implemented"}
            assert pricing_year in source_evidence

    ed_variants = {
        variant["variant_id"]: _as_mapping(variant)
        for variant in _as_sequence(calculators["ed"]["variant_surfaces"])
    }
    assert set(ed_variants) == {"ed_udg", "ed_aecc", "emergency_service_urg"}
    assert set(ed_variants["emergency_service_urg"]["pricing_years"]) == {
        str(year) for year in range(2013, 2021)
    }
    for variant in ed_variants.values():
        assert variant["state"] == "source_available"
        variant_evidence = _as_mapping(variant["source_evidence"])
        assert set(variant_evidence) == set(variant["pricing_years"])
        for evidence_path in variant_evidence.values():
            assert _source_evidence_exists(evidence_path), evidence_path

    for calculator_id in {
        "acute",
        "ed",
        "mh",
        "subacute",
        "outpatients",
        "adjustment",
    }:
        year_states = _as_mapping(calculators[calculator_id]["year_states"])
        source_evidence = _as_mapping(calculators[calculator_id]["source_evidence"])
        for pricing_year in {"2021", "2022", "2023", "2024"}:
            assert year_states[pricing_year] == "source_available"
            assert pricing_year in source_evidence

    for calculator_id in {"adjustment", "hac"}:
        year_states = _as_mapping(calculators[calculator_id]["year_states"])
        source_evidence = _as_mapping(calculators[calculator_id]["source_evidence"])
        for pricing_year in {str(year) for year in range(2018, 2026)}:
            assert year_states[pricing_year] in {
                "source_available",
                "implemented",
                "helper",
            }
            assert pricing_year in source_evidence

    for calculator_id in {
        "acute",
        "ed",
        "mh",
        "community_mh",
        "subacute",
        "outpatients",
    }:
        year_states = _as_mapping(calculators[calculator_id]["year_states"])
        source_evidence = _as_mapping(calculators[calculator_id]["source_evidence"])
        assert year_states["2026"] == "source_available"
        assert "2026" in source_evidence

    for calculator_id in {"hac", "ahr"}:
        year_states = _as_mapping(calculators[calculator_id]["year_states"])
        source_evidence = _as_mapping(calculators[calculator_id]["source_evidence"])
        for pricing_year in {"2021", "2022", "2023", "2024", "2025"}:
            assert pricing_year in source_evidence
        for pricing_year in {"2021", "2022", "2023", "2024"}:
            assert year_states[pricing_year] == "source_available"

    assert calculators["acute"]["year_states"]["2025"] == "implemented"
    assert calculators["community_mh"]["year_states"]["2021"] == "shadow"
    assert calculators["community_mh"]["year_states"]["2025"] == "implemented"
    assert calculators["hac"]["app_surface"] == "helper"
    assert calculators["hac"]["year_states"]["2025"] == "helper"
    assert calculators["ahr"]["app_surface"] == "helper"
    assert calculators["ahr"]["year_states"]["2025"] == "helper"


def test_power_platform_app_surface_uses_capability_matrix_for_selectors():
    matrix = _load_json(CAPABILITY_MATRIX)
    app_surface = _load_json(APP_SURFACE)
    calculators = {
        row["calculator_id"]: _as_mapping(row)
        for row in _as_sequence(matrix["calculators"])
    }
    state = _as_mapping(app_surface["state"])
    screens = {
        screen["name"]: _as_mapping(screen)
        for screen in _as_sequence(app_surface["screens"])
    }
    data_source = _as_mapping(_as_sequence(app_surface["data_sources"])[0])

    assert "listMchsCalculatorCapabilities" in data_source["operations"]
    assert "validateMchsCalculatorInput" in data_source["operations"]
    assert "runMchsCalculation" in data_source["operations"]
    assert set(_as_sequence(state["enabled_states"])) == {"implemented", "helper"}
    assert set(_as_sequence(state["disabled_states"])) == {
        "source_available",
        "shadow",
        "planned",
        "blocked",
        "not_available",
    }

    selector = screens["CalculatorSelector"]
    request_review = screens["RequestReview"]
    selector_text = json.dumps(selector)
    request_text = json.dumps(request_review)
    assert "listMchsCalculatorCapabilities" in selector_text
    assert "colMchsPricingYears" in selector_text
    assert "colMchsCalculatorYearGrid" in selector_text
    assert "CalculatorYearCoverageGrid" in selector_text
    assert "variant_surfaces" in selector_text
    assert "SelectedCalculator.year_states" in selector_text
    assert 'state in [\\"implemented\\", \\"helper\\"]' in selector_text
    assert "source_available" in selector_text
    assert (
        'varMchsSelectedYearState in [\\"implemented\\", \\"helper\\"]' in request_text
    )
    assert set(calculators) == {
        "acute",
        "ed",
        "mh",
        "community_mh",
        "subacute",
        "outpatients",
        "adjustment",
        "hac",
        "ahr",
    }

    policy = _as_mapping(app_surface["formula_logic_policy"])
    assert policy["allowed_in_power_platform"] is False
    assert "pricing-year support inference" in policy["blocked_formula_usage"]
    assert "NWAU arithmetic" in policy["blocked_formula_usage"]


def test_power_platform_env_vars_connection_refs_and_alm_gates_are_local_safe():
    contract = _load_json(CONTRACT)
    env_vars = {
        env_var["name"]: env_var
        for env_var in _as_sequence(contract["environment_variables"])
    }
    connection_refs = _as_sequence(contract["connection_references"])
    alm_gates = {gate["name"]: gate for gate in _as_sequence(contract["alm_gates"])}

    assert set(env_vars) == {
        "mchs_api_base_url",
        "mchs_api_contract_version",
        "mchs_api_calculator_id",
        "mchs_api_pricing_year",
    }
    assert all(env_var["required"] is True for env_var in env_vars.values())
    assert all(env_var["secret"] is False for env_var in env_vars.values())

    connection = _as_mapping(connection_refs[0])
    assert connection["logical_name"] == "mchs_shared_calculator_connector"
    assert connection["authentication"] == "apiKey"
    assert connection["secret_in_source_control"] is False

    assert alm_gates["contract-validation"]["requires_credentials"] is False
    assert alm_gates["solution-checker"]["requires_credentials"] is True
    assert (
        "pytest tests/test_power_platform_binding_track.py"
        in alm_gates["contract-validation"]["tool"]
    )
    assert (
        "scripts/validate_power_platform_capabilities.py"
        in alm_gates["contract-validation"]["tool"]
    )


def test_power_platform_capability_validator_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_power_platform_capabilities.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "Power Platform capability artifacts passed." in result.stdout


def test_power_platform_docs_point_to_concrete_contract_artifacts():
    service_boundary = _read_text(
        POWER_PLATFORM_ROOT / "connectors" / "service-boundary-contract.md"
    )
    app_surface = _read_text(POWER_PLATFORM_ROOT / "solution" / "app-surface.md")
    env_vars = _read_text(POWER_PLATFORM_ROOT / "solution" / "environment-variables.md")
    solution_manifest = _read_text(
        POWER_PLATFORM_ROOT / "solution" / "solution-manifest.md"
    )
    strategy = _read_text(TRACK / "binding_strategy.md")
    plan = _read_text(TRACK / "plan.md")

    for text in [service_boundary, solution_manifest, strategy]:
        assert "contracts/power-platform/power-platform-binding.contract.json" in text
        assert "contracts/power-platform/custom-connector.openapi.yaml" in text

    for text in [service_boundary, app_surface, strategy]:
        assert "listMchsCalculatorCapabilities" in text
        assert "validateMchsCalculatorInput" in text
        assert "runMchsCalculation" in text
        assert "correlation_id" in text

    assert "mchs_api_calculator_id" in env_vars
    assert "mchs_api_pricing_year" in env_vars
    assert "power-platform/solution/app-surface.json" in app_surface
    assert "power-platform/solution/app-surface.json" in solution_manifest
    assert "source-available" in service_boundary
    assert "source-available" in app_surface
    assert "source-available" in strategy
    assert "scripts/validate_power_platform_capabilities.py" in solution_manifest
    assert "tests/test_power_platform_binding_track.py" in plan
    assert "no tenant-exported managed solution zip" in strategy
