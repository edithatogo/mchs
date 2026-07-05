from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "release_evidence_bundle_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
WORKFLOW = ROOT / ".github" / "workflows" / "release-rust.yml"
ROADMAP = ROOT / "docs" / "roadmaps" / "release" / "evidence-bundle-format.md"
GENERATOR = ROOT / "scripts" / "generate_release_evidence.py"

spec = importlib.util.spec_from_file_location("generate_release_evidence", GENERATOR)
assert spec is not None
generate_release_evidence = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = generate_release_evidence
spec.loader.exec_module(generate_release_evidence)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def test_release_evidence_bundle_archive_metadata_records_runtime_scope() -> None:
    metadata = _json(TRACK / "metadata.json")

    assert metadata["track_id"] == "release_evidence_bundle_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["local_completion"].startswith(
        "The evidence bundle schema"
    )
    assert metadata["support_scope"]["external_gate"].startswith("not applicable")
    assert metadata["support_scope"]["runtime_support_claim"].startswith(
        "No release-candidate"
    )
    assert {block["id"] for block in metadata["gap_blockers"]} == {
        "registry-evidence-required",
        "rc-ga-validation-integration",
    }


def test_release_evidence_bundle_archive_plan_review_and_registry_are_complete() -> (
    None
):
    plan = _read(TRACK / "plan.md")
    review = _read(TRACK / "review.md")
    registry = _read(TRACKS)
    roadmap = _read(ROADMAP)
    workflow = _read(WORKFLOW)

    assert "Bundle Format" in plan
    assert "[checkpoint:" in plan
    assert "archive-ready" in review
    assert "- [x] **Track: Release Evidence Bundle**" in registry
    assert "release evidence bundle" in roadmap.lower()
    assert "Generate release evidence bundle" in workflow


def test_release_evidence_runtime_generator_matches_archive_scope() -> None:
    report = generate_release_evidence.build_report(
        generated_at="2026-06-25T00:00:00Z",
        version="9.9.9",
        registries=[
            generate_release_evidence.RegistryEvidence(
                "pypi",
                "published",
                "9.9.9",
                "https://pypi.example.test/project/nwau-py/9.9.9/",
            ),
            generate_release_evidence.RegistryEvidence(
                "conda-forge",
                "recipe-only",
                None,
                "https://github.example.test/pr/1",
                "mocked recipe-only response",
            ),
        ],
    )
    markdown = generate_release_evidence.render_markdown(report)

    assert report["report_version"] == "1.0"
    assert report["source"]["version"] == "9.9.9"
    assert report["registries"][0]["status"] == "published"
    assert report["registries"][1]["status"] == "recipe-only"
    assert "conda-forge is recipe-only" in report["consistency_checks"]["warnings"]
    assert "# Release Evidence Report" in markdown
    assert "| pypi | published | 9.9.9 |" in markdown
