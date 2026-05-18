#!/usr/bin/env python3
"""Validate Power Platform service-boundary connector artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _ensure(
    condition: bool, message: str, *, errors: list[str], warnings: list[str]
) -> None:
    if condition:
        return
    if "optional" in message:
        warnings.append(message)
    else:
        errors.append(message)


def validate_openapi(
    path: Path, *, errors: list[str], warnings: list[str]
) -> dict[str, Any]:
    openapi = _load_json(path)

    required_top = [
        "openapi",
        "info",
        "paths",
        "components",
    ]
    for key in required_top:
        _ensure(
            key in openapi,
            f"openapi missing required top-level key: {key}",
            errors=errors,
            warnings=warnings,
        )

    if "openapi" in openapi:
        version = str(openapi["openapi"])
        _ensure(
            version.startswith("3."),
            f"openapi must be 3.x, got {version}",
            errors=errors,
            warnings=warnings,
        )

    for endpoint, methods in {
        "/healthz": {"get"},
        "/v1/calculators": {"get"},
        "/v1/calculators/{calculator_id}": {"get"},
        "/v1/schemas/{schema_name}": {"get"},
        "/v1/validate": {"post"},
        "/v1/calculations": {"post"},
        "/v1/evidence/{bundle_id}": {"get"},
        "/calculators/run": {"post"},
    }.items():
        path_value = openapi.get("paths", {}).get(endpoint)
        _ensure(
            path_value is not None,
            f"openapi missing required path: {endpoint}",
            errors=errors,
            warnings=warnings,
        )
        if path_value is not None:
            for method in methods:
                _ensure(
                    method in path_value,
                    f"openapi missing {method.upper()} for {endpoint}",
                    errors=errors,
                    warnings=warnings,
                )

    schema_names = set((openapi.get("components", {}).get("schemas") or {}).keys())
    for required_schema in {
        "ServiceBoundaryRequest",
        "ServiceBoundaryResponse",
        "HealthResponse",
    }:
        _ensure(
            required_schema in schema_names,
            f"openapi missing required schema: {required_schema}",
            errors=errors,
            warnings=warnings,
        )

    return openapi


def validate_metadata(
    path: Path, expected_openapi: Path, *, errors: list[str], warnings: list[str]
) -> dict[str, Any]:
    metadata = _load_json(path)
    for key in ["name", "displayName", "publisher", "version"]:
        _ensure(
            key in metadata,
            f"metadata missing required field: {key}",
            errors=errors,
            warnings=warnings,
        )

    api_definition = metadata.get("apiDefinition")
    if isinstance(api_definition, str):
        _ensure(
            (path.parent / api_definition).exists(),
            f"metadata apiDefinition {api_definition!r} does not exist",
            errors=errors,
            warnings=warnings,
        )
    else:
        errors.append("metadata missing string field apiDefinition")

    connection_parameters = metadata.get("properties", {}).get("connectionParameters")
    if not isinstance(connection_parameters, dict):
        errors.append("metadata properties.connectionParameters must be an object")
    else:
        for key in ["baseUrl", "api_key"]:
            param = connection_parameters.get(key)
            _ensure(
                isinstance(param, dict),
                f"metadata missing connection parameter: {key}",
                errors=errors,
                warnings=warnings,
            )

    if api_definition and api_definition == expected_openapi.name:
        _ensure(
            True,
            "metadata apiDefinition matches expected connector OpenAPI filename",
            errors=errors,
            warnings=warnings,
        )
    return metadata


def validate_assets(
    *,
    openapi_path: Path | None = None,
    metadata_path: Path | None = None,
) -> tuple[int, list[str], list[str]]:
    chosen_openapi = (
        openapi_path
        or ROOT
        / "power-platform"
        / "connectors"
        / "mchs-service-boundary"
        / "apiDefinition.swagger.json"
    )
    chosen_metadata = (
        metadata_path
        or ROOT
        / "power-platform"
        / "connectors"
        / "mchs-service-boundary"
        / "apiProperties.json"
    )

    errors: list[str] = []
    warnings: list[str] = []

    if not chosen_openapi.exists():
        errors.append(f"missing openapi file: {chosen_openapi}")
    if not chosen_metadata.exists():
        errors.append(f"missing metadata file: {chosen_metadata}")

    if errors:
        return 1, errors, warnings

    validate_openapi(chosen_openapi, errors=errors, warnings=warnings)
    validate_metadata(chosen_metadata, chosen_openapi, errors=errors, warnings=warnings)

    return (1 if errors else 0, errors, warnings)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Power Platform connector artifacts."
    )
    parser.add_argument(
        "--openapi",
        default=None,
        help=(
            "Connector OpenAPI file "
            "(default: connectors/mchs-service-boundary/apiDefinition.swagger.json)"
        ),
    )
    parser.add_argument(
        "--metadata",
        default=None,
        help=(
            "Connector metadata file "
            "(default: connectors/mchs-service-boundary/apiProperties.json)"
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return_code, errors, warnings = validate_assets(
        openapi_path=Path(args.openapi) if args.openapi else None,
        metadata_path=Path(args.metadata) if args.metadata else None,
    )

    for item in warnings:
        print(f"[warn] {item}")
    for item in errors:
        print(f"[error] {item}", file=sys.stderr)

    if return_code != 0:
        print("Connector artifact validation failed.", file=sys.stderr)
    elif args.json:
        payload = {
            "status": "pass",
            "errors": errors,
            "warnings": warnings,
        }
        print(json.dumps(payload, sort_keys=True, indent=2))
    else:
        print("Connector artifact validation passed.")
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
