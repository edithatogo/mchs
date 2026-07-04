from __future__ import annotations

from pathlib import Path

import pytest


def test_public_dataset_inventory_selects_mimic_iv_demo() -> None:
    from nwau_py.public_clinical_datasets import (
        list_public_dataset_candidates,
        select_initial_worked_example,
    )

    candidates = list_public_dataset_candidates()
    candidate_ids = {candidate.dataset_id for candidate in candidates}

    assert {
        "mimic-iv-demo-2.2",
        "mimic-iv-ed-demo-2.2",
        "mimic-iv-demo-meds-0.0.1",
        "mimic-iv-fhir-demo-2.1.0",
        "synthea",
    }.issubset(candidate_ids)

    selected = select_initial_worked_example(candidates)
    assert selected.dataset_id == "mimic-iv-demo-2.2"
    assert selected.initial_role == "primary"
    assert selected.access_policy == "open-access"
    assert selected.license_name == "Open Data Commons Open Database License v1.0"
    assert "admissions" in selected.clinical_fields
    assert "icu_stays" in selected.clinical_fields
    assert selected.fit_for_nwau_examples == "admitted-episode-staging"


def test_public_dataset_inventory_records_deferrals_and_risks() -> None:
    from nwau_py.public_clinical_datasets import list_public_dataset_candidates

    candidates = {
        candidate.dataset_id: candidate
        for candidate in list_public_dataset_candidates()
    }

    assert candidates["mimic-iv-ed-demo-2.2"].initial_role == "deferred-ed-track"
    assert candidates["mimic-iv-demo-meds-0.0.1"].initial_role == "deferred-interop"
    assert candidates["mimic-iv-fhir-demo-2.1.0"].initial_role == "deferred-interop"
    assert candidates["synthea"].initial_role == "comparison-synthetic"

    for candidate in candidates.values():
        assert candidate.url.startswith("https://")
        assert candidate.citation
        assert candidate.download_path
        assert candidate.file_size
        assert candidate.redistribution_rules
        assert candidate.pros
        assert candidate.cons
        assert candidate.risks
        assert candidate.to_dict()["dataset_id"] == candidate.dataset_id


def test_dataset_assessment_document_records_candidate_table() -> None:
    assessment = Path(
        "conductor/tracks/public_clinical_dataset_worked_example_20260704/"
        "dataset_assessment.md"
    )
    assert assessment.exists()
    text = assessment.read_text(encoding="utf-8")
    assert "MIMIC-IV Clinical Database Demo v2.2" in text
    assert "Open Data Commons Open Database License v1.0" in text
    assert "selected initial worked example" in text
    assert "not authoritative Australian AR-DRG" in text


def test_public_dataset_inventory_rejects_empty_selection() -> None:
    from nwau_py.public_clinical_datasets import select_initial_worked_example

    with pytest.raises(ValueError, match="no public dataset candidates"):
        select_initial_worked_example(())
