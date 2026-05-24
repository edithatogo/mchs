from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

from click.testing import CliRunner

from nwau_py.cli.main import cli
from nwau_py.pricing_year_diff import (
    compare_pricing_year_manifests,
    format_pricing_year_diff_report,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "pricing_year_diff_tooling_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = ROOT / "contracts" / "pricing-year-diff"
DOCS_PAGE = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "pricing-year-diff-tooling.mdx"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def test_pricing_year_diff_tooling_track_and_contract_are_complete():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        TRACK / "review.md",
        CONTRACT / "pricing-year-diff.contract.json",
        CONTRACT / "pricing-year-diff.schema.json",
        CONTRACT / "examples" / "diff-year.json",
        CONTRACT / "examples" / "diff-year.markdown.md",
        DOCS_PAGE,
    ]:
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    registry = _read_text(TRACKS)
    docs = _read_text(DOCS_PAGE)

    assert metadata["track_id"] == "pricing_year_diff_tooling_20260512"
    assert metadata["status"] == "complete"
    assert metadata["current_state"] == "implemented-with-manifest-backed-diffs"
    assert metadata["publication_status"] == "not-ready"
    assert (
        "funding-calculator diff-year <from-year> <to-year>"
        in (metadata["primary_contract"])
    )
    assert "- [x] **Track: Pricing-Year Diff Tooling**" in registry
    assert "source changes" in docs
    assert "implementation changes" in docs


def test_pricing_year_diff_report_covers_changed_missing_new_and_unchanged_cases():
    report = compare_pricing_year_manifests("2025", "2026", repo_root=ROOT)

    assert report.from_year == "2025"
    assert report.to_year == "2026"
    assert report.summary == {
        "constants_changed": 1,
        "coding_sets_changed": 5,
        "source_artifacts_changed": 2,
        "validation_changed": 1,
        "gaps_added": 1,
        "gaps_removed": 2,
        "gaps_changed": 2,
    }

    constants = report.constants[0]
    assert constants.key == "constants"
    assert any(change.path == "nep.value" for change in constants.changes)
    assert any(change.path == "nec.value" for change in constants.changes)

    coding_sets = {item.key: item for item in report.coding_sets}
    assert coding_sets["AR-DRG"].change_type == "changed"
    assert any(
        change.path == "version"
        and change.before == "v11.0"
        and change.after == "v12.0"
        for change in coding_sets["AR-DRG"].changes
    )
    assert coding_sets["AECC"].change_type == "changed"
    assert not any(change.path == "version" for change in coding_sets["AECC"].changes)

    gap_types = {item.change_type for item in report.gaps}
    assert {"added", "removed", "changed"} <= gap_types
    assert any(item.key == "constants.nec :: value_unpublished" for item in report.gaps)
    assert any(
        item.key == "source_artifacts.published_on :: scope_unknown"
        for item in report.gaps
    )

    validation_paths = {change.path for change in report.validation}
    assert "current_pricing_year" in validation_paths
    assert "validation_status" not in validation_paths


def test_pricing_year_diff_cli_json_and_markdown_are_reviewable():
    runner = CliRunner()

    json_result = runner.invoke(
        cast(Any, cli),
        ["diff-year", "2025", "2026", "--json"],
    )
    assert json_result.exit_code == 0, json_result.output
    payload = json.loads(json_result.output)
    assert payload["from_year"] == "2025"
    assert payload["to_year"] == "2026"
    assert payload["summary"]["constants_changed"] == 1
    assert payload["summary"]["gaps_added"] == 1

    markdown_result = runner.invoke(cast(Any, cli), ["diff-year", "2025", "2026"])
    assert markdown_result.exit_code == 0, markdown_result.output
    for phrase in [
        "# Pricing-year diff: 2025 -> 2026",
        "## Constants",
        "`nep.value`: `7434` -> `7418`",
        "`AR-DRG`",
        "source_artifacts.published_on :: scope_unknown",
    ]:
        assert phrase in markdown_result.output


def test_pricing_year_diff_contract_examples_match_manifest_backed_years():
    contract = _read_json(CONTRACT / "pricing-year-diff.contract.json")
    example = _read_json(CONTRACT / "examples" / "diff-year.json")
    markdown = _read_text(CONTRACT / "examples" / "diff-year.markdown.md")

    assert contract["tool"]["name"] == "funding-calculator"
    assert contract["commands"][0]["syntax"] == (
        "funding-calculator diff-year <from-year> <to-year>"
    )
    assert example["command"] == "funding-calculator diff-year 2025 2026 --json"
    assert example["from_year"] == "2025"
    assert example["to_year"] == "2026"
    assert example["summary"]["state"] == "changed"
    assert "# Pricing-year diff: 2025 -> 2026" in markdown


def test_pricing_year_diff_markdown_renderer_is_stable():
    report = compare_pricing_year_manifests("2025", "2026", repo_root=ROOT)
    rendered = format_pricing_year_diff_report(report)

    assert rendered.startswith("# Pricing-year diff: 2025 -> 2026")
    assert "## Summary" in rendered
    assert rendered.count("## ") == 6
