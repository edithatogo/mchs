#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOLUTION_ROOT = ROOT / "power-platform" / "solution"
PIPELINE_ROOT = ROOT / "power-platform" / "pipelines"
SCRIPTS_ROOT = ROOT / "scripts"
WORKFLOW_ROOT = ROOT / ".github" / "workflows"


REQUIRED_FILES = [
    SOLUTION_ROOT / "README.md",
    SOLUTION_ROOT / "solution-manifest.md",
    SOLUTION_ROOT / "environment-variables.md",
    SOLUTION_ROOT / "connection-references.md",
    SOLUTION_ROOT / "alm-workflow.md",
    SOLUTION_ROOT / "app-surface.md",
    ROOT / "power-platform" / "connectors" / "service-boundary-contract.md",
    PIPELINE_ROOT / "README.md",
    PIPELINE_ROOT / "pack-check-import-gates.md",
    SCRIPTS_ROOT / "bootstrap-power-platform-alm.sh",
    SCRIPTS_ROOT / "power-platform-alm-lifecycle-gates.sh",
    WORKFLOW_ROOT / "power-platform-alm.yml",
]


COMMAND_SURFACES = [
    "pac solution pack",
    "pac solution unpack",
    "pac solution import",
    "pac solution checker run",
]


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]


def require_files(results: ValidationResult) -> None:
    for path in REQUIRED_FILES:
        if not path.exists():
            results.errors.append(f"missing required file: {path}")


def check_markdown_contracts(results: ValidationResult) -> None:
    manifest = (
        (SOLUTION_ROOT / "solution-manifest.md").read_text(encoding="utf-8").lower()
    )
    workflow = (
        (WORKFLOW_ROOT / "power-platform-alm.yml").read_text(encoding="utf-8").lower()
    )
    pipeline = (
        (PIPELINE_ROOT / "pack-check-import-gates.md")
        .read_text(encoding="utf-8")
        .lower()
    )
    gates_doc = (PIPELINE_ROOT / "README.md").read_text(encoding="utf-8").lower()

    for term in [
        "pack",
        "check",
        "import",
        "solution checker",
        "managed solution",
    ]:
        if term not in pipeline and term not in gates_doc:
            results.errors.append(f"missing gate term in pipeline docs: {term}")

    for term in [
        "solution",
        "packaging contract",
        "build format",
        "managed",
    ]:
        if term not in manifest:
            results.errors.append(f"manifest missing term: {term}")

    if "power-platform-alm-lifecycle-gates.sh" not in workflow:
        results.errors.append(
            "workflow does not invoke power-platform-alm-lifecycle-gates.sh"
        )


def command_available(name: str) -> bool:
    return (
        subprocess.run(
            ["bash", "-lc", f"command -v {name}"],
            check=False,
            capture_output=True,
        ).returncode
        == 0
    )


def check_command_surface(results: ValidationResult, require_tools: bool) -> None:
    if not require_tools:
        if command_available("pac"):
            results.warnings.append(
                "pac present but --require-tools not set; skipping live command checks"
            )
        else:
            results.warnings.append(
                "pac missing and --require-tools not set; skipping live command checks"
            )
        return

    if not command_available("pac"):
        results.errors.append("pac is required for live command surface checks")
        return

    for command in COMMAND_SURFACES:
        proc = subprocess.run(
            ["bash", "-lc", f"{command} --help"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if proc.returncode != 0:
            results.errors.append(f"command surface regression: {command} --help")
            continue
        if not proc.stdout.strip():
            results.warnings.append(
                f"command surface returned empty output: {command} --help"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-tools",
        action="store_true",
        help="Fail when pac is missing instead of skipping surface checks.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a JSON summary and command surface evidence.",
    )
    return parser.parse_args()


def summarize(results: ValidationResult, emit_json: bool = False) -> int:
    if emit_json:
        import json

        payload = {
            "errors": results.errors,
            "warnings": results.warnings,
            "status": "pass" if not results.errors else "fail",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for warning in results.warnings:
            print(f"[warn] {warning}")
        if results.warnings:
            print(f"[warn] observed {len(results.warnings)} warning(s)")
    if results.errors:
        for error in results.errors:
            print(f"[error] {error}")
        print(f"Validation failed: {len(results.errors)} error(s)")
        return 1
    print("Validation complete: Power Platform ALM gate contract is valid.")
    return 0


def run_validation(require_tools: bool) -> ValidationResult:
    results = ValidationResult(errors=[], warnings=[])
    require_files(results)
    check_markdown_contracts(results)
    check_command_surface(results, require_tools=require_tools)
    return results


def main() -> int:
    args = parse_args()
    results = run_validation(require_tools=args.require_tools)
    return summarize(results, emit_json=args.json)


if __name__ == "__main__":
    raise SystemExit(main())
