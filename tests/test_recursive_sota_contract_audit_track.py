from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "recursive_sota_contract_audit_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
REQUIREMENTS = ROOT / "conductor" / "requirements.md"
DESIGN = ROOT / "conductor" / "design.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_metadata() -> dict[str, Any]:
    return json.loads(_read(TRACK / "metadata.json"))


def test_recursive_sota_archive_metadata_records_contract_only_scope():
    metadata = _load_metadata()

    assert metadata["track_id"] == "recursive_sota_contract_audit_20260513"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["completion_policy"].startswith("Complete-with-gaps means")
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert metadata["support_scope"]["implemented"] == [
        "recursive SOTA audit requirement in conductor/requirements.md",
        "recursive requirements-design-audit loop in conductor/design.md",
        "governance tests for contract and tooling surfaces",
        "explicit gap register for missing current audit outputs",
    ]
    assert metadata["support_scope"]["not_implemented"] == [
        "completed current SOTA comparison report",
        "finding list with remediation links and owner tracks",
        "external benchmark or publication proof",
        "periodic audit automation",
    ]
    assert {gap["status"] for gap in metadata["gap_register"]} == {
        "deferred",
        "out-of-scope",
    }
    assert metadata["archive_evidence"]["review"] == (
        "conductor/archive/recursive_sota_contract_audit_20260513/review.md"
    )


def test_recursive_sota_plan_records_archive_review_checkpoints():
    plan = _read(TRACK / "plan.md")

    assert "[checkpoint:" in plan
    assert "Archive Repair" in plan
    assert "metadata.json" in plan
    assert "plan.md" in plan
    assert "governance-only complete-with-gaps scope" in plan


def test_recursive_sota_contract_is_present_in_requirements_and_design():
    requirements = _read(REQUIREMENTS)
    design = _read(DESIGN)

    assert "SHOULD-003" in requirements
    assert "Recursive SOTA audits should periodically compare" in requirements
    assert "create remediation tracks" in requirements
    assert "Recursive SOTA audit" in design
    assert "Audit --> Req" in design


def test_recursive_sota_registry_points_to_completed_archive():
    registry = _read(TRACKS)

    assert "- [x] **Track: Recursive SOTA Contract Audit**" in registry
    assert "./archive/recursive_sota_contract_audit_20260513/" in registry
    assert "./tracks/recursive_sota_contract_audit_20260513/" not in registry
