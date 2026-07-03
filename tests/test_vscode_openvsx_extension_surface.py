from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VSCODE_ROOT = ROOT / "integrations" / "vscode"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
TRACK_METADATA = (
    ROOT
    / "conductor"
    / "archive"
    / "vscode_openvsx_registry_submission_20260524"
    / "metadata.json"
)
PACKAGE_JSON = VSCODE_ROOT / "package.json"
EXTENSION_JS = VSCODE_ROOT / "extension.js"
README = VSCODE_ROOT / "README.md"
SYNC_VSIX = VSCODE_ROOT / "mchs-tools-0.1.1.vsix"
SYNC_VSIX_SHA256 = "bfbeca13497f21489c532e58af3b1e10df9fe60ae5eab4c721e632baee9b5dd6"


def test_vscode_extension_exposes_concrete_registry_gate_commands():
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    extension_source = EXTENSION_JS.read_text(encoding="utf-8")

    command_ids = {command["command"] for command in package["contributes"]["commands"]}
    expected_commands = {
        "mchs.showRegistryStatus",
        "mchs.openLanguageRegistryContract",
        "mchs.openExternalGateRoadmap",
        "mchs.copyOpenVsxPublishCommand",
    }

    assert expected_commands <= command_ids
    assert {
        event.removeprefix("onCommand:") for event in package["activationEvents"]
    } == command_ids
    for command_id in expected_commands:
        assert command_id in extension_source

    assert "language-registry-submissions.contract.json" in extension_source
    assert "language-registry-external-gates.md" in extension_source
    assert "mchs-tools-0.1.1.vsix" in extension_source
    assert (
        "publication evidence is recorded in the contract" in extension_source.lower()
    )


def test_vscode_extension_metadata_and_docs_record_current_publication_boundary():
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    package_text = json.dumps(package).lower()
    readme = README.read_text(encoding="utf-8").lower()

    assert package["version"] == "0.1.1"
    assert "scaffold" not in package_text
    assert "scaffold" not in readme
    assert "verified on visual studio marketplace and open vsx" in readme
    assert (
        "published on visual studio marketplace as `edithatogo.mchs-tools@0.1.1`"
        in readme
    )
    assert "open vsx also exposes `edithatogo.mchs-tools@0.1.0`" in readme
    assert "latest public version is `0.1.1`" in readme
    assert "local package metadata and copied publish command target `0.1.1`" in readme
    assert "mchs-tools-0.1.1.vsix" in readme
    assert "marketplace gallery api also reports `0.1.1`" in readme
    assert "marketplace still reports latest version `0.1.0`" not in readme
    assert "requires a `vsce_pat` publish session" not in readme
    assert "open vsx publication remains gated" not in readme


def test_vscode_marketplace_sync_artifact_is_prepared():
    assert SYNC_VSIX.exists()
    digest = hashlib.sha256(SYNC_VSIX.read_bytes()).hexdigest()

    assert digest == SYNC_VSIX_SHA256


def test_vscode_openvsx_surface_is_deprecated_and_cancelled():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    registry = next(
        item for item in contract["registries"] if item["id"] == "vscode_openvsx"
    )
    metadata = json.loads(TRACK_METADATA.read_text(encoding="utf-8"))

    assert registry["current_status"] == "deprecated_cancelled_publication_retained"
    assert registry["cancelled_at"] == "2026-07-03"
    assert "Deprecated and cancelled" in registry["blocker"]
    assert "historical" in registry["blocker"].lower()
    assert metadata["current_status"] == "deprecated_cancelled_publication_retained"
    assert metadata["publication_status"] == "deprecated_cancelled_publication_retained"
    assert metadata["cancelled_at"] == "2026-07-03"
    assert metadata["publication_claimed"] is True
