from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "end_to_end_validated_canary_20260512"
EVIDENCE = TRACK / "canary_lifecycle_evidence.json"
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
CANARY_DOC = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "end-to-end-validated-canary.mdx"
)
CANARY_TEMPLATE = TRACK / "template.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_validated_canary_track_is_complete_with_gaps_not_overclaimed():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "end_to_end_validated_canary_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert (TRACK / "review.md").exists()


def test_validated_canary_claims_match_source_only_bundle():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    bundle = json.loads(_read(CANARY_BUNDLE))
    spec = _read(TRACK / "validated_canary_spec.md")
    evidence = json.loads(_read(EVIDENCE))

    assert bundle["status"] == "source-only"
    assert bundle["validation"]["parity_claim"] is False
    assert evidence["validation_status"] == "complete-with-gaps"
    assert evidence["official_sas_parity"]["status"] == "blocked"
    assert evidence["official_excel_parity"]["status"] == "source-formula-only"
    assert evidence["fixture_parity"]["status"] == "pass"
    assert evidence["python_rust_parity"]["status"] == "pass"
    assert evidence["arrow_parquet_bundle"]["status"] == "pass"
    assert "SAS parity record" not in metadata["completion_evidence"]
    assert "Official SAS/Excel parity not recorded" in spec
    assert "Starlight canary page committed" in spec
    assert "Reusable canary template committed" in spec


def test_validated_canary_docs_and_template_are_committed():
    spec = _read(TRACK / "validated_canary_spec.md")
    doc = _read(CANARY_DOC)
    template = _read(CANARY_TEMPLATE)

    assert CANARY_DOC.exists()
    assert CANARY_TEMPLATE.exists()
    assert "Official SAS parity remains blocked" in doc
    assert "Do not claim full official parity" in template
    assert "no canary page is currently committed" not in spec
    assert "no reusable canary template is currently" not in spec


def test_validated_canary_gap_register_is_specific():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    gaps = {gap["id"]: gap for gap in metadata["gap_register"]}

    assert gaps["official-sas-parity-missing"]["status"] == "blocked"
    assert gaps["official-sas-parity-missing"]["blocking_scope"] == "official-parity"
    assert gaps["local-canary-docs-template"]["status"] == "complete"
    assert gaps["cli-arrow-output-parity"]["status"] == "complete-local-fixture"


def test_validated_canary_missing_official_parity_is_gap_recorded():
    spec = _read(TRACK / "validated_canary_spec.md")

    assert "Official SAS/Excel parity not recorded" in spec
    assert "Arrow/Parquet output parity not recorded" in spec
    assert "Validated | Blocked" in spec
