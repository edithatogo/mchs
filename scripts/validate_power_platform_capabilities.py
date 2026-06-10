"""Validate Power Platform capability discovery artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ROOT = ROOT / "contracts" / "power-platform"
CONTRACT = CONTRACT_ROOT / "power-platform-binding.contract.json"
OPENAPI = CONTRACT_ROOT / "custom-connector.openapi.yaml"
CAPABILITY_MATRIX = CONTRACT_ROOT / "calculator-capability-matrix.json"
APP_SURFACE = ROOT / "power-platform" / "solution" / "app-surface.json"
CAPABILITIES_EXAMPLE = CONTRACT_ROOT / "examples" / "capabilities.pass.json"

EXPECTED_CALCULATORS = {
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
EXPECTED_YEARS = {str(year) for year in range(2013, 2027)}
ENABLED_STATES = {"implemented", "helper"}
DISABLED_STATES = {
    "source_available",
    "shadow",
    "planned",
    "blocked",
    "not_available",
}
ALL_STATES = ENABLED_STATES | DISABLED_STATES
OPERATIONS = {
    "listMchsCalculatorCapabilities",
    "validateMchsCalculatorInput",
    "runMchsCalculation",
}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a JSON object")
    return payload


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path} must contain a YAML object")
    return payload


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate() -> None:
    contract = load_json(CONTRACT)
    openapi = load_yaml(OPENAPI)
    matrix = load_json(CAPABILITY_MATRIX)
    app_surface = load_json(APP_SURFACE)
    capabilities_example = load_json(CAPABILITIES_EXAMPLE)

    contract_operations = set(contract["openapi"]["operation_ids"])
    openapi_operations = {
        operation["operationId"]
        for path_item in openapi["paths"].values()
        for operation in path_item.values()
        if isinstance(operation, dict) and "operationId" in operation
    }
    app_operations = set(app_surface["data_sources"][0]["operations"])

    require(contract_operations == OPERATIONS, "contract operation IDs drifted")
    require(openapi_operations == OPERATIONS, "OpenAPI operation IDs drifted")
    require(app_operations == OPERATIONS, "app surface connector operations drifted")

    capability = contract["capability_matrix"]
    require(
        capability["path"] == "contracts/power-platform/calculator-capability-matrix.json",
        "contract capability matrix path is not canonical",
    )
    require(
        capability["operation_id"] == "listMchsCalculatorCapabilities",
        "contract capability operation is not listMchsCalculatorCapabilities",
    )
    require(
        set(capability["enabled_states"]) == ENABLED_STATES,
        "contract enabled states drifted",
    )
    require(
        set(capability["disabled_states"]) == DISABLED_STATES,
        "contract disabled states drifted",
    )

    years = set(matrix["pricing_years"])
    require(years == EXPECTED_YEARS, "capability pricing years drifted")
    require(
        matrix["pricing_years"] == sorted(EXPECTED_YEARS),
        "capability pricing years must be sorted",
    )
    calculators = {row["calculator_id"]: row for row in matrix["calculators"]}
    require(set(calculators) == EXPECTED_CALCULATORS, "calculator selector set drifted")

    for calculator_id, row in calculators.items():
        year_states = row["year_states"]
        require(
            set(year_states) == EXPECTED_YEARS,
            f"{calculator_id} does not declare every expected year",
        )
        invalid_states = set(year_states.values()) - ALL_STATES
        require(
            not invalid_states,
            f"{calculator_id} contains invalid states: {sorted(invalid_states)}",
        )
        default_year = row["default_enabled_year"]
        require(default_year in year_states, f"{calculator_id} default year is absent")
        require(
            year_states[default_year] in ENABLED_STATES,
            f"{calculator_id} default year is not enabled",
        )
        source_evidence = row.get("source_evidence")
        require(
            isinstance(source_evidence, dict),
            f"{calculator_id} must declare source_evidence",
        )
        for pricing_year, source_path in source_evidence.items():
            require(
                pricing_year in EXPECTED_YEARS,
                f"{calculator_id} source_evidence has unexpected year {pricing_year}",
            )
            require(
                isinstance(source_path, str) and source_path,
                f"{calculator_id} {pricing_year} source_evidence path is empty",
            )
            require(
                (ROOT / source_path).exists(),
                f"{calculator_id} {pricing_year} source evidence missing: {source_path}",
            )
            require(
                year_states[pricing_year]
                in {"source_available", "shadow", "implemented", "helper"},
                (
                    f"{calculator_id} {pricing_year} has evidence but hidden "
                    f"state {year_states[pricing_year]}"
                ),
            )
        for variant in row.get("variant_surfaces", []):
            variant_years = set(variant["pricing_years"])
            require(
                variant_years <= EXPECTED_YEARS,
                f"{calculator_id} variant {variant['variant_id']} has unexpected years",
            )
            require(
                variant["state"] in DISABLED_STATES,
                f"{calculator_id} variant {variant['variant_id']} is not disabled",
            )
            variant_evidence = variant["source_evidence"]
            require(
                set(variant_evidence) == variant_years,
                f"{calculator_id} variant {variant['variant_id']} evidence/year drift",
            )
            for pricing_year, source_path in variant_evidence.items():
                require(
                    (ROOT / source_path).exists(),
                    (
                        f"{calculator_id} variant {variant['variant_id']} "
                        f"{pricing_year} evidence missing: {source_path}"
                    ),
                )

    for calculator_id in {
        "acute",
        "ed",
        "mh",
        "subacute",
        "outpatients",
        "adjustment",
    }:
        row = calculators[calculator_id]
        for pricing_year in {"2021", "2022", "2023", "2024"}:
            require(
                row["year_states"][pricing_year] == "source_available",
                f"{calculator_id} {pricing_year} must be visible as source_available",
            )
            require(
                pricing_year in row["source_evidence"],
                f"{calculator_id} {pricing_year} source evidence is missing",
            )

    for calculator_id in {"acute", "ed", "subacute", "outpatients"}:
        row = calculators[calculator_id]
        for pricing_year in {str(year) for year in range(2013, 2026)}:
            require(
                row["year_states"][pricing_year] in {"source_available", "implemented"},
                f"{calculator_id} {pricing_year} must be visible across the archive horizon",
            )
            require(
                pricing_year in row["source_evidence"],
                f"{calculator_id} {pricing_year} source evidence is missing",
            )

    ed_variants = {
        variant["variant_id"]: variant for variant in calculators["ed"]["variant_surfaces"]
    }
    require(
        set(ed_variants) == {"ed_udg", "ed_aecc", "emergency_service_urg"},
        "ED historical variant surfaces drifted",
    )
    require(
        set(ed_variants["emergency_service_urg"]["pricing_years"])
        == {str(year) for year in range(2013, 2021)},
        "emergency service URG/ES variant coverage drifted",
    )

    for calculator_id in {"adjustment", "hac"}:
        row = calculators[calculator_id]
        for pricing_year in {str(year) for year in range(2018, 2026)}:
            require(
                row["year_states"][pricing_year] in {"source_available", "implemented", "helper"},
                f"{calculator_id} {pricing_year} must be visible across the archive horizon",
            )
            require(
                pricing_year in row["source_evidence"],
                f"{calculator_id} {pricing_year} source evidence is missing",
            )

    for calculator_id in {
        "acute",
        "ed",
        "mh",
        "community_mh",
        "subacute",
        "outpatients",
    }:
        row = calculators[calculator_id]
        for pricing_year in {"2026"}:
            require(
                row["year_states"][pricing_year] == "source_available",
                f"{calculator_id} {pricing_year} must be visible as source_available",
            )
            require(
                pricing_year in row["source_evidence"],
                f"{calculator_id} {pricing_year} source evidence is missing",
            )
    for calculator_id in {"hac", "ahr"}:
        row = calculators[calculator_id]
        for pricing_year in {"2021", "2022", "2023", "2024"}:
            require(
                row["year_states"][pricing_year] == "source_available",
                f"{calculator_id} {pricing_year} must be visible as source_available",
            )
            require(
                pricing_year in row["source_evidence"],
                f"{calculator_id} {pricing_year} source evidence is missing",
            )

    app_state = app_surface["state"]
    require(
        set(app_state["enabled_states"]) == ENABLED_STATES,
        "app surface enabled states drifted",
    )
    require(
        set(app_state["disabled_states"]) == DISABLED_STATES,
        "app surface disabled states drifted",
    )
    screens = {screen["name"]: screen for screen in app_surface["screens"]}
    selector = screens["CalculatorSelector"]
    request_review = screens["RequestReview"]
    require(
        "listMchsCalculatorCapabilities" in " ".join(selector["on_visible"]),
        "selector does not load capabilities from connector",
    )
    require(
        "colMchsPricingYears" in " ".join(selector["on_visible"]),
        "selector does not load pricing years from capability response",
    )
    require(
        "colMchsCalculatorYearGrid" in " ".join(selector["on_visible"]),
        "selector does not build a calculator/year coverage grid",
    )
    controls = {control["name"]: control for control in selector["controls"]}
    require(
        "CalculatorYearCoverageGrid" in controls,
        "selector does not expose the all-calculator/all-year grid",
    )
    require(
        "source_available" in controls["CalculatorYearCoverageGrid"]["disabled_rule"],
        "coverage grid does not disable source_available cells",
    )
    require(
        request_review["submit_guard"] == 'varMchsSelectedYearState in ["implemented", "helper"]',
        "request submit guard does not match enabled states",
    )
    require(
        app_surface["formula_logic_policy"]["allowed_in_power_platform"] is False,
        "Power Platform formula logic policy must remain false",
    )
    require(
        "pricing-year support inference"
        in app_surface["formula_logic_policy"]["blocked_formula_usage"],
        "app surface must block pricing-year support inference",
    )

    require(
        capabilities_example["operation_id"] == "listMchsCalculatorCapabilities",
        "capabilities example operation drifted",
    )
    require(
        capabilities_example["response_fixture"]
        == "contracts/power-platform/calculator-capability-matrix.json",
        "capabilities example does not point at the matrix",
    )
    example_messages = " ".join(
        assertion["message"] for assertion in capabilities_example["assertions"]
    )
    require(
        "2013 through 2026" in example_messages,
        "capabilities example does not assert the full archive horizon",
    )
    require(
        "Source-available" in example_messages,
        "capabilities example does not preserve source-available disabled state wording",
    )
    require(
        "historical variant surfaces" in example_messages,
        "capabilities example does not record ED historical variant surfaces",
    )


def main() -> int:
    validate()
    print("Power Platform capability artifacts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
