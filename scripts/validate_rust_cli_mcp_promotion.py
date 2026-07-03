from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "contracts" / "runtime" / "rust-cli-mcp-promotion-matrix.json"
REQUIRED_STATUSES = {
    "rust-default",
    "rust-opt-in",
    "python-only",
    "unsupported",
    "blocked",
}


def _load_matrix() -> dict[str, Any]:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def validate() -> tuple[dict[str, Any], list[str]]:
    matrix = _load_matrix()
    failures: list[str] = []
    surfaces = matrix.get("surfaces", {})
    if not isinstance(surfaces, dict) or not surfaces:
        failures.append("matrix must contain non-empty surfaces")
        surfaces = {}

    if matrix.get("defaultRuntimeDecision") != "remain-python-default-rust-opt-in":
        failures.append("defaultRuntimeDecision must remain fail-closed")
    if matrix.get("rustDefaultAllowed") is not False:
        failures.append("rustDefaultAllowed must be false until all evidence exists")

    counts = Counter()
    for surface_id, surface in surfaces.items():
        status = surface.get("status")
        counts[str(status)] += 1
        if status not in REQUIRED_STATUSES:
            failures.append(f"{surface_id}: unsupported status {status!r}")
        if surface.get("rustDefault") is not False:
            failures.append(f"{surface_id}: rustDefault must be false")
        if surface.get("defaultRuntime") not in {"python", "none"}:
            failures.append(f"{surface_id}: defaultRuntime must be python or none")
        evidence = surface.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            failures.append(f"{surface_id}: missing evidence list")
        else:
            failures.extend(
                f"{surface_id}: evidence path does not exist: {evidence_path}"
                for evidence_path in evidence
                if not (ROOT / str(evidence_path)).exists()
            )

    required = matrix.get("requiredEvidenceForRustDefault", {})
    required_keys = (
        "rust_core_tests",
        "python_compatibility_tests",
        "cli_parity_tests",
        "mcp_parity_tests",
        "unsupported_surface_inventory",
    )
    failures.extend(
        f"missing required evidence key {key}"
        for key in required_keys
        if key not in required
    )
    unsupported_inventory = required.get("unsupported_surface_inventory")
    if unsupported_inventory and not (ROOT / str(unsupported_inventory)).exists():
        failures.append(
            "requiredEvidenceForRustDefault.unsupported_surface_inventory "
            f"does not exist: {unsupported_inventory}"
        )

    payload = {
        "passed": not failures,
        "matrix": str(MATRIX.relative_to(ROOT)),
        "defaultRuntimeDecision": matrix.get("defaultRuntimeDecision"),
        "rustDefaultAllowed": matrix.get("rustDefaultAllowed"),
        "surfaceCounts": dict(sorted(counts.items())),
        "failures": failures,
    }
    return payload, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON summary")
    args = parser.parse_args()
    payload, failures = validate()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            "Rust CLI/MCP promotion gate: "
            + ("passed" if payload["passed"] else "failed")
        )
        print(json.dumps(payload["surfaceCounts"], sort_keys=True))
        for failure in failures:
            print(f"- {failure}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
