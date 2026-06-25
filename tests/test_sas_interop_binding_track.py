from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast


ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "sas_interop_binding_20260512"
ROADMAP = ROOT / "docs" / "roadmaps" / "audience-language-strategy.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return cast(dict[str, Any], payload)


def _track_text() -> str:
    return "\n".join(
        _read_text(path)
        for path in [
            TRACK / "spec.md",
            TRACK / "plan.md",
            TRACK / "binding_strategy.md",
            TRACK / "validation_evidence.md",
        ]
    )


def test_sas_interop_is_private_no_new_development_policy_not_adapter():
    for path in [
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "binding_strategy.md",
        TRACK / "validation_evidence.md",
        ROADMAP,
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    text = _track_text()
    roadmap = _read_text(ROADMAP)

    assert metadata["track_id"] == "sas_interop_binding_20260512"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "private-no-new-development"
    assert metadata["publication_status"] == "private-not-published"
    assert metadata["primary_contract"] == "Private/local SAS reference comparison policy"
    assert metadata["completion_evidence"] == [
        "docs",
        "private-reference-policy",
        "tests",
    ]
    assert "cli_file_interop_binding_20260512" in metadata["dependencies"]
    assert "source_archive_provenance_20260504" in metadata["dependencies"]

    for phrase in [
        "private/no-new-development",
        "does not publish a SAS adapter",
        "not a dual implementation",
        "no public SAS interop contract bundle",
        "private/local reference evidence",
        "Do not claim adapter readiness",
    ]:
        assert phrase in text

    assert (
        "Private/no new development - no public adapter; retain existing SAS-read workflows only"
        in roadmap.replace("—", "-")
    )


def test_sas_interop_keeps_public_contract_and_formula_logic_out_of_track():
    text = _track_text().lower()

    assert not (ROOT / "bindings" / "sas").exists()
    assert not (ROOT / "contracts" / "sas-interop-binding").exists()

    for forbidden_claim in [
        "current_state\": \"adapter-ready",
        "publication_status\": \"published",
        "module_readiness",
        "public sas adapter has adapter-ready status",
        "sas formula implementation",
        "formula port implementation",
        "copied_sas_formula",
    ]:
        assert forbidden_claim not in text

    for required in [
        "no sas source code",
        "formula logic is copied",
        "archived sas material is treated as reference input only",
        "shared cli/file contract",
        "local/licensed",
        "synthetic fixtures",
    ]:
        assert required in text
