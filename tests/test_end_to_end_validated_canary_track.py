from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "end_to_end_validated_canary_20260512"
CANARY_BUNDLE = (
    ROOT
    / "reference-data"
    / "2025"
    / "parameter-bundles"
    / "acute"
    / "acute-2025-canary"
    / "v1"
    / "bundle.json"
)
MISSING_DOC = ROOT / "docs-site" / "src" / "content" / "docs" / "validated-canary" / "acute-2025.mdx"
MISSING_TEMPLATE = TRACK / "template.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_validated_canary_track_is_blocked_not_archived():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "end_to_end_validated_canary_20260512"
    assert metadata["status"] == "blocked"
    assert metadata["current_state"] == "overclaim-remediated-blocked"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert (TRACK / "review.md").exists()


def test_validated_canary_claims_match_source_only_bundle():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    bundle = json.loads(_read(CANARY_BUNDLE))
    spec = _read(TRACK / "validated_canary_spec.md")

    assert bundle["status"] == "source-only"
    assert bundle["validation"]["parity_claim"] is False
    assert "SAS parity record" not in metadata["completion_evidence"]
    assert "Excel formula parity record" not in metadata["completion_evidence"]
    assert "Starlight documentation page" not in metadata["completion_evidence"]
    assert "Official SAS/Excel parity not recorded" in spec
    assert "Arrow/Parquet output parity not recorded" in spec
    assert "Validated | Blocked" in spec


def test_validated_canary_missing_docs_are_gap_recorded():
    spec = _read(TRACK / "validated_canary_spec.md")

    assert not MISSING_DOC.exists()
    assert not MISSING_TEMPLATE.exists()
    assert "no canary page is currently committed" in spec
    assert "no reusable canary template is currently" in spec
