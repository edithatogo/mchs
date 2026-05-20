from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


BLOCKER_TEMPLATES = [
    (
        ROOT
        / ".github"
        / "ISSUE_TEMPLATE"
        / (
            "power-platform-blocker-service-boundary-production-endpoint-and-"
            "connection-reference-values.yml"
        ),
        "service_boundary_production_endpoint_and_connection_reference_values",
        "service boundary production endpoint and connection reference values",
        [
            "power-platform/evidence/connection-reference-evidence-template.json",
            "power-platform/evidence/runtime-smoke-evidence-template.json",
        ],
    ),
    (
        ROOT
        / ".github"
        / "ISSUE_TEMPLATE"
        / (
            "power-platform-blocker-real-power-automate-flow-component-smoke-"
            "evidence.yml"
        ),
        "real_power_automate_flow_component_smoke_evidence",
        "real Power Automate flow component smoke evidence",
        [
            "power-platform/evidence/flow-smoke-evidence-template.json",
            "power-platform/evidence/power-automate-flow-smoke-20260521.json",
        ],
    ),
    (
        ROOT
        / ".github"
        / "ISSUE_TEMPLATE"
        / "power-platform-blocker-production-service-boundary-execution-evidence.yml",
        "production_service_boundary_execution_evidence",
        "production service-boundary execution evidence",
        [
            "power-platform/evidence/live-service-boundary-smoke-20260521.json",
            "power-platform/evidence/runtime-smoke-evidence-template.json",
        ],
    ),
    (
        ROOT
        / ".github"
        / "ISSUE_TEMPLATE"
        / (
            "power-platform-blocker-power-app-operation-pages-are-source-ux-"
            "complete-but-not-live-runtime-proven.yml"
        ),
        "power_app_operation_pages_are_source_ux_complete_but_not_live_runtime_proven",
        "Power App operation pages are source-UX complete but not live runtime-proven",
        [
            "power-platform/evidence/canvas-app-publication-20260520.json",
            "power-platform/evidence/deployment-status.json",
        ],
    ),
]


def test_power_platform_blocker_issue_templates_cover_all_remaining_blockers() -> None:
    for path, blocker_id, summary, evidence_paths in BLOCKER_TEMPLATES:
        text = path.read_text()

        assert path.exists()
        assert blocker_id in text
        assert summary in text
        assert "Local issue-generation template" in text
        assert "I have not claimed production readiness or blocker resolution." in text

        for evidence_path in evidence_paths:
            assert evidence_path in text
