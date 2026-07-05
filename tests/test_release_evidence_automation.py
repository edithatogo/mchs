from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _track(track_id: str) -> Path:
    for base in (ROOT / "conductor" / "tracks", ROOT / "conductor" / "archive"):
        candidate = base / track_id
        if candidate.exists():
            return candidate
    raise AssertionError(f"missing Conductor track or archive: {track_id}")


TRACK = _track("release_evidence_automation_20260512")
RELEASE_BUNDLE_TRACK = _track("release_evidence_bundle_20260513")
RELEASE_BUNDLE_SCHEMA = ROOT / "contracts" / "release" / "evidence-bundle.schema.json"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
GENERATOR = ROOT / "scripts" / "generate_release_evidence.py"

spec = importlib.util.spec_from_file_location("generate_release_evidence", GENERATOR)
assert spec is not None
release_evidence = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = release_evidence
spec.loader.exec_module(release_evidence)

SAMPLE_REPORT: dict[str, Any] = {
    "report_version": "1.0",
    "generated_at": "2026-05-12T12:00:00Z",
    "source": {
        "version": "0.5.0",
        "git_tag": "v0.5.0",
        "commit": "abc1234",
        "repository": "github.com/owner/microcosting_healthservices",
    },
    "registries": [
        {
            "name": "pypi",
            "status": "published",
            "version": "0.5.0",
            "url": "https://pypi.org/project/nwau-py/",
            "checked_at": "2026-05-12T12:00:00Z",
        },
        {
            "name": "conda-forge",
            "status": "recipe-only",
            "version": None,
            "url": None,
            "checked_at": "2026-05-12T12:00:00Z",
            "notes": "Recipe exists, package not yet uploaded",
        },
        {
            "name": "github_release",
            "status": "published-with-gaps",
            "version": "0.5.0",
            "url": "https://github.com/owner/microcosting_healthservices/releases/tag/v0.5.0",
            "checked_at": "2026-05-12T12:00:00Z",
        },
        {
            "name": "github_pages",
            "status": "published",
            "url": "https://owner.github.io/microcosting_healthservices/",
            "checked_at": "2026-05-12T12:00:00Z",
        },
        {
            "name": "private_mirror",
            "status": "private",
            "version": "0.5.0",
            "url": "https://internal.example.invalid/packages/nwau-py/",
            "checked_at": "2026-05-12T12:00:00Z",
        },
        {
            "name": "crates_io",
            "status": "future-only",
            "version": None,
            "url": None,
            "checked_at": "2026-05-12T12:00:00Z",
            "notes": "Rust core not yet stable",
        },
    ],
    "workflows": [
        {
            "name": "release",
            "status": "passing",
            "latest_run": "2026-05-11T10:00:00Z",
        },
        {
            "name": "publish",
            "status": "passing",
            "latest_run": "2026-05-11T10:00:00Z",
        },
        {
            "name": "docs",
            "status": "passing",
            "latest_run": "2026-05-12T08:00:00Z",
        },
        {
            "name": "ci",
            "status": "passing",
            "latest_run": "2026-05-12T09:00:00Z",
        },
        {
            "name": "conda_recipe",
            "status": "future-only",
            "latest_run": None,
        },
    ],
    "consistency_checks": {
        "version_tag_match": True,
        "readme_badges_current": True,
        "homepage_links_valid": True,
        "warnings": [],
    },
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_release_evidence_automation_spec_defines_json_schema():
    spec = _read_text(TRACK / "release_evidence_automation_spec.md")
    assert "Evidence Schema" in spec
    assert "JSON Report Schema" in spec
    assert "registries" in spec
    assert "workflows" in spec
    assert "consistency_checks" in spec


def test_release_evidence_automation_spec_defines_markdown_schema():
    spec = _read_text(TRACK / "release_evidence_automation_spec.md")
    assert "Markdown Report Schema" in spec
    assert "Registry Status" in spec
    assert "Workflow Status" in spec
    assert "Consistency Checks" in spec


def test_release_evidence_automation_spec_defines_evidence_states():
    spec = _read_text(TRACK / "release_evidence_automation_spec.md")
    assert "published" in spec
    assert "unpublished" in spec
    assert "future-only" in spec
    assert "published-with-gaps" in spec
    assert "recipe-only" in spec
    assert "private" in spec


def test_sample_report_is_valid_json():
    report_json = json.dumps(SAMPLE_REPORT, indent=2)
    parsed = json.loads(report_json)
    assert parsed["report_version"] == "1.0"
    assert parsed["source"]["version"] == "0.5.0"
    assert len(parsed["registries"]) == 6
    assert len(parsed["workflows"]) == 5


def test_sample_report_schema_is_stable():
    report_json = json.dumps(SAMPLE_REPORT, indent=2, sort_keys=True)
    parsed = json.loads(report_json)
    second_json = json.dumps(parsed, indent=2, sort_keys=True)
    assert report_json == second_json


def test_sample_report_detects_future_only_registries():
    future = [r for r in SAMPLE_REPORT["registries"] if r["status"] == "future-only"]
    assert len(future) == 1
    assert {r["name"] for r in future} == {"crates_io"}
    assert any(r["status"] == "recipe-only" for r in SAMPLE_REPORT["registries"])
    assert any(r["status"] == "private" for r in SAMPLE_REPORT["registries"])


def test_sample_report_consistency_checks_default_to_passing():
    assert SAMPLE_REPORT["consistency_checks"]["version_tag_match"] is True
    assert SAMPLE_REPORT["consistency_checks"]["warnings"] == []


def test_release_evidence_generator_builds_json_and_markdown_from_mocked_registries():
    report = release_evidence.build_report(
        generated_at="2026-06-25T00:00:00Z",
        version="9.9.9",
        registries=[
            release_evidence.RegistryEvidence(
                "pypi",
                "published",
                "9.9.9",
                "https://pypi.example.test/project/nwau-py/9.9.9/",
            ),
            release_evidence.RegistryEvidence(
                "conda-forge",
                "recipe-only",
                None,
                "https://github.example.test/pr/1",
                "mocked recipe-only response",
            ),
        ],
    )
    markdown = release_evidence.render_markdown(report)

    assert report["report_version"] == "1.0"
    assert report["source"]["version"] == "9.9.9"
    assert report["source"]["git_tag"] == "v9.9.9"
    assert report["registries"][0]["status"] == "published"
    assert report["registries"][1]["status"] == "recipe-only"
    assert "conda-forge is recipe-only" in report["consistency_checks"]["warnings"]
    assert "# Release Evidence Report" in markdown
    assert "| pypi | published | 9.9.9 |" in markdown
    assert "| conda-forge | recipe-only | - |" in markdown


def test_release_evidence_generator_cli_writes_json_and_markdown(
    tmp_path: Path, monkeypatch
):
    json_out = tmp_path / "release-evidence.json"
    markdown_out = tmp_path / "release-evidence.md"

    monkeypatch.setattr(
        "sys.argv",
        [
            "generate_release_evidence.py",
            "--json-out",
            str(json_out),
            "--markdown-out",
            str(markdown_out),
            "--version",
            "8.8.8",
        ],
    )

    assert release_evidence.main() == 0
    report = json.loads(json_out.read_text(encoding="utf-8"))
    markdown = markdown_out.read_text(encoding="utf-8")

    assert report["source"]["version"] == "8.8.8"
    assert report["registries"]
    assert "## Registry Status" in markdown
    assert "## Workflow Status" in markdown


def test_release_evidence_automation_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACK / "release_evidence_automation_spec.md",
    ]:
        assert path.exists(), path


def test_release_evidence_automation_track_metadata():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    assert metadata["track_id"] == "release_evidence_automation_20260512"
    assert metadata["track_class"] == "publication"


def test_release_evidence_bundle_complete_with_gaps_is_blocked_explicitly():
    metadata = json.loads(_read_text(RELEASE_BUNDLE_TRACK / "metadata.json"))
    schema = json.loads(_read_text(RELEASE_BUNDLE_SCHEMA))

    assert metadata["track_id"] == "release_evidence_bundle_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["gap_blockers"]
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert "registries" in schema["required"]
    registry_statuses = schema["properties"]["registries"]["items"]["properties"][
        "status"
    ]["enum"]
    assert set(registry_statuses) == {
        "published",
        "unpublished",
        "future-only",
        "published-with-gaps",
        "recipe-only",
        "private",
    }


def test_release_evidence_automation_in_tracks_registry():
    registry = _read_text(TRACKS_REGISTRY)
    assert "Release Evidence Automation" in registry
    assert "release_evidence_automation_20260512" in registry
