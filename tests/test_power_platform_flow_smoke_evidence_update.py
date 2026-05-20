from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_power_platform_flow_smoke_evidence.py"
TEMPLATE = ROOT / "power-platform" / "evidence" / "flow-smoke-evidence-template.json"


def _load_module():
    spec = importlib.util.spec_from_file_location("flow_smoke_update", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _template() -> dict:
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def _complete_capture() -> dict:
    return {
        "asOf": "2026-05-21",
        "flowRuns": [
            {
                "flowLogicalName": "mchs-validate-input",
                "flowId": "11111111-1111-1111-1111-111111111111",
                "runId": "run-validate-input-001",
                "runStatus": "succeeded",
                "runUrl": "https://example.com/runs/validate-input-001",
            },
            {
                "flowLogicalName": "mchs-calculate-request",
                "flowId": "22222222-2222-2222-2222-222222222222",
                "runId": "run-calculate-request-001",
                "runStatus": "succeeded",
                "runUrl": "https://example.com/runs/calculate-request-001",
            },
            {
                "flowLogicalName": "mchs-evidence-export",
                "flowId": "33333333-3333-3333-3333-333333333333",
                "runId": "run-evidence-export-001",
                "runStatus": "succeeded",
                "runUrl": "https://example.com/runs/evidence-export-001",
            },
            {
                "flowLogicalName": "mchs-deployment-smoke",
                "flowId": "44444444-4444-4444-4444-444444444444",
                "runId": "run-deployment-smoke-001",
                "runStatus": "succeeded",
                "runUrl": "https://example.com/runs/deployment-smoke-001",
            },
        ],
    }


def test_flow_smoke_evidence_update_refuses_incomplete_capture(tmp_path) -> None:
    module = _load_module()
    output = tmp_path / "power-automate-flow-smoke.json"
    capture = _complete_capture()
    capture["flowRuns"][0].pop("runUrl")

    exit_code, summary, merged = module.build_flow_smoke_evidence(
        _template(), capture, output_path=output
    )

    assert exit_code == 2
    assert merged is None
    assert summary["status"] == "blocked_pending_real_flow_run_capture"
    assert summary["missingFields"]["mchs-validate-input"] == ["runUrl"]
    assert not output.exists()


def test_flow_smoke_evidence_update_merges_complete_capture(
    tmp_path, monkeypatch
) -> None:
    module = _load_module()
    capture_file = tmp_path / "capture.json"
    output = tmp_path / "power-automate-flow-smoke.json"
    capture_file.write_text(
        json.dumps(_complete_capture(), indent=2) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: SimpleNamespace(
            template=TEMPLATE,
            capture=capture_file,
            output=output,
        ),
    )

    exit_code = module.main()

    assert exit_code == 0
    merged = json.loads(output.read_text(encoding="utf-8"))
    assert merged["status"] == "captured_real_flow_smoke_passed"
    assert merged["claimBoundary"]["flowSmokePassed"] is True
    assert merged["claimBoundary"]["realComponentConfigured"] is True
    assert merged["connectionReference"]["connectionConfigured"] is True
    assert merged["results"]["successfulRunIds"] == [
        "run-validate-input-001",
        "run-calculate-request-001",
        "run-evidence-export-001",
        "run-deployment-smoke-001",
    ]
    assert merged["realNswRunEvidence"][0]["flowId"] == (
        "11111111-1111-1111-1111-111111111111"
    )
    assert merged["realNswRunEvidence"][0]["runUrl"] == (
        "https://example.com/runs/validate-input-001"
    )
    assert all(
        entry["runStatus"] == "succeeded" for entry in merged["realNswRunEvidence"]
    )
