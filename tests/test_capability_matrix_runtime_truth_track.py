from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from click.testing import CliRunner

from nwau_py import mcp_server
from nwau_py.capability_matrix import build_capability_matrix, capability_matrix_path
from nwau_py.cli.main import cli

ROOT = Path(__file__).resolve().parents[1]


def _row(matrix: dict[str, Any], row_id: str) -> dict[str, Any]:
    return next(row for row in matrix["rows"] if row["id"] == row_id)


def test_capability_matrix_is_generated_from_reference_manifests() -> None:
    matrix = build_capability_matrix(repo_root=ROOT)

    assert matrix["schema_version"] == "1.0"
    assert matrix["source_manifests"] == [
        "reference-data/2025/manifest.yaml",
        "reference-data/2026/manifest.yaml",
    ]
    assert _row(matrix, "year.2025")["status"] == "source_available"
    assert _row(matrix, "year.2025")["metadata"]["nep"] == 7258
    assert _row(matrix, "year.2026")["metadata"]["nep"] == 7418
    assert _row(matrix, "stream.acute.2025")["status"] == "validated"
    assert _row(matrix, "stream.acute.2026")["status"] == "executable"
    assert _row(matrix, "classifier.ar_drg.2025")["status"] == "blocked_licensed"
    assert _row(matrix, "surface.mcp")["status"] == "validated"


def test_committed_capability_matrix_matches_generator() -> None:
    expected = build_capability_matrix(repo_root=ROOT)
    committed = json.loads(capability_matrix_path(ROOT).read_text(encoding="utf-8"))

    assert committed == expected


def test_cli_reports_the_generated_matrix() -> None:
    runner = CliRunner()
    result = runner.invoke(cast(Any, cli), ["capability-matrix", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert _row(payload, "surface.cli")["status"] == "executable"
    assert _row(payload, "surface.mcp")["status"] == "validated"


def test_mcp_support_resource_uses_the_same_matrix() -> None:
    payload = json.loads(
        mcp_server.read_resource("mchs://support/capability-matrix")["contents"][0][
            "text"
        ]
    )

    assert _row(payload, "classifier.ar_drg.2026")["status"] == "blocked_licensed"
    assert _row(payload, "surface.mcp")["status"] == "validated"


def test_docs_reference_the_generated_matrix() -> None:
    calculators_doc = (ROOT / "nwau_py" / "docs" / "calculators.md").read_text(
        encoding="utf-8"
    )
    coverage_doc = (
        ROOT
        / "docs-site"
        / "src"
        / "content"
        / "docs"
        / "governance"
        / "calculator-coverage.mdx"
    ).read_text(encoding="utf-8")
    versioned_coverage_doc = (
        ROOT
        / "docs-site"
        / "src"
        / "content"
        / "docs"
        / "2026"
        / "governance"
        / "calculator-coverage.mdx"
    ).read_text(encoding="utf-8")
    versioned_reference_doc = (
        ROOT
        / "docs-site"
        / "src"
        / "content"
        / "docs"
        / "2026"
        / "reference"
        / "calculators.mdx"
    ).read_text(encoding="utf-8")

    assert "calculator-capability-matrix.json" in calculators_doc
    assert "calculator-capability-matrix.json" in coverage_doc
    assert "calculator-capability-matrix.json" in versioned_coverage_doc
    assert "calculator-capability-matrix.json" in versioned_reference_doc
    assert "blocked_licensed" in coverage_doc
    assert "source_available" in coverage_doc
