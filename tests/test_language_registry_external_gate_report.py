from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "language_registry_external_gate_report.py"
CONTRACT = (
    ROOT
    / "contracts/language-registry-submissions"
    / "language-registry-submissions.contract.json"
)


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


def test_classify_uses_multi_probe_target_version_visibility():
    module = _module()
    registry = {
        "id": "vscode_openvsx",
        "current_status": "openvsx_0_1_1_verified_marketplace_republish_blocked",
        "version": "0.1.1",
        "publicationEvidence": {"type": "partial_publication_verified"},
    }

    assert (
        module.classify(registry, {"target_version_visible": True})
        == "completion_candidates"
    )
    assert (
        module.classify(registry, {"target_version_visible": False})
        == "partial_publications"
    )


def test_vscode_registry_contract_records_marketplace_0_1_1_completion():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    registry = next(
        item for item in contract["registries"] if item["id"] == "vscode_openvsx"
    )

    assert registry["current_status"] == "published_verified"
    assert registry["blocker"] is None
    assert registry["publication_claimed"] is True
    assert (
        registry["publicationEvidence"]["type"]
        == "open_vsx_and_visual_studio_marketplace_publication"
    )
    assert registry["publicationEvidence"]["visualStudioMarketplaceVersion"] == "0.1.1"
    assert (
        registry["publicationEvidence"]["visualStudioMarketplaceVsixSha256"]
        == "1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad"
    )
