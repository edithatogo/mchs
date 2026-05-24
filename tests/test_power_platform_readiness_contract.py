from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (
    ROOT / "power-platform" / "evidence" / "aggregate-readiness-preflight.schema.json"
)
README = ROOT / "power-platform" / "evidence" / "README.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "power-platform-deployment-readiness.md"


def test_aggregate_readiness_preflight_schema_requires_actionable_checks() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    check_schema = schema["properties"]["checks"]["items"]

    assert check_schema["required"] == [
        "name",
        "command",
        "expectedExitCode",
        "observedExitCode",
        "expectedStatus",
        "observedStatus",
        "blocked",
        "ok",
        "help",
        "nextAction",
        "details",
    ]
    assert check_schema["properties"]["help"]["minLength"] == 1
    assert check_schema["properties"]["nextAction"]["minLength"] == 1


def test_aggregate_readiness_docs_spell_out_each_check_next_step() -> None:
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")

    for label, phrase in [
        ("endpoint", "Provide a real public HTTPS base URL"),
        ("github", "Configure the required repository secrets"),
        ("pac", "Run PAC auth and recapture real `appId`"),
        (
            "flow_smoke",
            "Provide real `flowId`, `runId`, `runStatus`, and HTTPS `runUrl` values",
        ),
        ("dlp", "Supply real monitoring and DLP evidence fields"),
        ("subrepo", "Supply either a standalone remote or an explicit waiver record"),
    ]:
        assert label in readme, label
        assert phrase in readme, phrase

    assert "help" in roadmap
    assert "nextAction" in roadmap
