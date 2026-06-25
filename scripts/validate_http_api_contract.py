"""Validate the MCHS HTTP OpenAPI contract."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
OPENAPI = ROOT / "contracts" / "http-api" / "openapi.yaml"


class UniqueKeyLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate mapping keys."""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=False)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=False)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def load_openapi(path: Path = OPENAPI) -> dict[str, Any]:
    """Load the OpenAPI document and reject duplicate YAML keys."""
    data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError("OpenAPI document must be a YAML mapping")
    return data


def validate_openapi(data: dict[str, Any]) -> None:
    """Validate structural contract requirements not covered by plain YAML parsing."""
    if data.get("openapi") != "3.1.0":
        raise ValueError("HTTP API contract must be OpenAPI 3.1.0")

    paths = data.get("paths")
    components = data.get("components")
    if not isinstance(paths, dict) or not isinstance(components, dict):
        raise ValueError("OpenAPI document must contain paths and components mappings")

    required_paths = {
        "/calculators",
        "/calculators/{calculatorId}",
        "/calculators/{calculatorId}/schema",
        "/validate",
        "/calculations",
        "/calculations/async",
        "/calculations/async/{jobId}",
        "/calculations/{calculatorId}/explain",
        "/evidence/{bundleId}",
        "/support/streams",
        "/support/years",
    }
    missing = required_paths - set(paths)
    if missing:
        raise ValueError(f"OpenAPI document is missing paths: {sorted(missing)}")

    schemas = components.get("schemas")
    responses = components.get("responses")
    if not isinstance(schemas, dict) or not isinstance(responses, dict):
        raise ValueError("OpenAPI components must contain schemas and responses")

    for schema_name in [
        "ValidationResponse",
        "CalculationResponse",
        "AsyncJobResponse",
        "AsyncJobStatus",
        "EvidenceBundle",
        "Diagnostics",
        "DiagnosticEntry",
    ]:
        if schema_name not in schemas:
            raise ValueError(f"missing component schema {schema_name}")

    async_status = schemas["AsyncJobStatus"]
    if "properties" not in async_status or "jobId" not in async_status["properties"]:
        raise ValueError("AsyncJobStatus must define job status properties")

    not_found = responses.get("NotFoundResponse")
    if not isinstance(not_found, dict) or "properties" in not_found:
        raise ValueError("NotFoundResponse must be a response object, not a schema")

    calc_responses = paths["/calculations"]["post"]["responses"]
    if "422" not in calc_responses:
        raise ValueError("POST /calculations must expose a validation failure response")


def main() -> int:
    """Run validation as a CLI."""
    try:
        validate_openapi(load_openapi())
    except Exception as exc:  # noqa: BLE001 - CLI should print any validation failure.
        print(f"HTTP API contract validation failed: {exc}", file=sys.stderr)
        return 1
    print("HTTP API contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
