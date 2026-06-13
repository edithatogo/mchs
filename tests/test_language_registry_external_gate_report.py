from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "language_registry_external_gate_report.py"


def _module():
    spec = importlib.util.spec_from_file_location(
        "language_registry_external_gate_report", SCRIPT
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_vscode_live_probe_requires_target_version_on_both_registries():
    module = _module()
    registry = {
        "id": "vscode_openvsx",
        "version": "0.1.1",
    }

    assert (
        module.vscode_target_version_visible(
            registry,
            {
                "openvsx_probe": {
                    "http_status": 200,
                    "body": '"version":"0.1.1"',
                },
                "marketplace_probe": {
                    "http_status": 200,
                    "body": '"version":"0.1.0"',
                },
            },
        )
        is False
    )

    assert (
        module.vscode_target_version_visible(
            registry,
            {
                "openvsx_probe": {
                    "http_status": 200,
                    "body": '"version":"0.1.1"',
                },
                "marketplace_probe": {
                    "http_status": 200,
                    "body": '"version":"0.1.1"',
                },
            },
        )
        is True
    )
