from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / "conductor" / "workflow.md"


def _track_plan(track_id: str) -> Path:
    for base in (ROOT / "conductor" / "tracks", ROOT / "conductor" / "archive"):
        candidate = base / track_id / "plan.md"
        if candidate.exists():
            return candidate
    raise AssertionError(f"missing Conductor plan: {track_id}")


OPEN_TRACK_PLANS = [
    ROOT
    / "conductor"
    / "archive"
    / "docs_release_publication_readiness_20260510"
    / "plan.md",
    _track_plan("multi_surface_binding_delivery_20260510"),
    ROOT / "conductor" / "archive" / "rust_acute_python_poc_20260510" / "plan.md",
    _track_plan("rust_ci_supply_chain_hardening_20260510"),
    _track_plan("rust_core_architecture_20260510"),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_workflow_uses_conductor_review_and_auto_advances():
    workflow = _read(WORKFLOW)
    normalized = " ".join(workflow.split())

    assert "conductor-review" in workflow
    assert "manual verification" not in workflow.lower()
    assert "user confirmation" not in workflow.lower()
    assert "Do not pause for manual confirmation" in workflow
    assert (
        "automatically continue with the next incomplete task"
        in normalized
    )


def test_open_track_plans_call_out_conductor_review():
    for plan in OPEN_TRACK_PLANS:
        text = _read(plan)
        assert "conductor-review" in text, plan
        assert "auto-fix" in text, plan
        assert "auto-progress" in text, plan
