from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "ahpcs_costing_process_model_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
MODEL_DOC = TRACK / "ahpcs_model.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ahpcs_model_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        MODEL_DOC,
    ]:
        assert path.exists(), path


def test_ahpcs_model_tracks_md_is_open():
    registry = _read_text(TRACKS)
    assert "AHPCS Costing Process Model" in registry
    assert "- [x] **Track: AHPCS Costing Process Model**" in registry
    assert "./archive/ahpcs_costing_process_model_20260512/" in registry


def test_model_doc_defines_cost_ledger():
    text = _read_text(MODEL_DOC)
    assert "Cost Ledger" in text
    assert "cost centre" in text.lower()


def test_model_doc_covers_production_cost_centres():
    text = _read_text(MODEL_DOC)
    assert "Production Cost Centres" in text
    assert "direct costs" in text.lower()


def test_model_doc_covers_overhead_cost_centres():
    text = _read_text(MODEL_DOC)
    assert "Overhead Cost Centres" in text
    assert "allocation" in text.lower()


def test_model_doc_defines_products():
    text = _read_text(MODEL_DOC)
    for phrase in ["Final Products", "Intermediate Products", "AR-DRG"]:
        assert phrase in text


def test_model_doc_covers_line_items_offsets_and_rvus():
    text = _read_text(MODEL_DOC)
    for phrase in ["Line Items", "Offsets", "Recoveries", "Relative Value Units"]:
        assert phrase in text


def test_model_doc_includes_allocation_model():
    text = _read_text(MODEL_DOC)
    assert "Allocation Model" in text
    assert "allocation keys" in text.lower()


def test_model_doc_relates_to_nwau_calculation():
    text = _read_text(MODEL_DOC)
    assert "NWAU Calculation" in text
    assert "cost buckets" in text.lower()


def test_model_doc_has_validation_guidance():
    text = _read_text(MODEL_DOC)
    assert "Validation Model" in text
    assert "cost ledger schema" in text.lower()


def test_model_doc_includes_caveats():
    text = _read_text(MODEL_DOC)
    for phrase in [
        "local costing policy",
        "compliance certification",
        "data governance",
        "not a replacement",
    ]:
        assert phrase in text.lower()


def test_ahpcs_model_metadata_is_conservative():
    import json

    metadata = json.loads(_read_text(TRACK / "metadata.json"))

    assert metadata["track_id"] == "ahpcs_costing_process_model_20260512"
    assert metadata["track_class"] == "costing"
    assert metadata["current_state"] == "complete"
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "cost" in metadata["description"].lower()
