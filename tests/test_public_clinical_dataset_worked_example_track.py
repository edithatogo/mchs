from __future__ import annotations

from pathlib import Path

import pandas as pd
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


def test_public_dataset_manifest_loads_cache_policy() -> None:
    from nwau_py.public_clinical_datasets import load_public_dataset_manifest

    manifest = load_public_dataset_manifest(
        Path("reference-data/public-datasets/mimic-iv-demo/manifest.yaml")
    )

    assert manifest.dataset_id == "mimic-iv-demo-2.2"
    assert manifest.license_name == "Open Data Commons Open Database License v1.0"
    assert manifest.raw_data_git_policy == "forbidden"
    assert manifest.local_cache_policy.cache_root_env == "MCHS_MIMIC_IV_DEMO_DIR"
    assert {
        "hosp/admissions.csv.gz",
        "hosp/diagnoses_icd.csv.gz",
        "hosp/procedures_icd.csv.gz",
        "hosp/drgcodes.csv.gz",
        "icu/icustays.csv.gz",
    }.issubset({file.path for file in manifest.expected_files})


def test_public_dataset_guard_blocks_raw_patient_level_paths() -> None:
    from nwau_py.public_clinical_datasets import (
        PublicDatasetPolicyError,
        scan_public_dataset_paths_for_restricted_assets,
    )

    with pytest.raises(PublicDatasetPolicyError, match="raw public clinical dataset"):
        scan_public_dataset_paths_for_restricted_assets(
            [
                "reference-data/public-datasets/mimic-iv-demo/raw/hosp/"
                "admissions.csv.gz"
            ]
        )

    assert scan_public_dataset_paths_for_restricted_assets(
        [
            "reference-data/public-datasets/mimic-iv-demo/manifest.yaml",
            "examples/mimic_demo/fixtures/admissions.csv",
        ]
    ) == []


def test_public_dataset_cache_diagnostics_report_missing_files(tmp_path: Path) -> None:
    from nwau_py.public_clinical_datasets import (
        diagnose_public_dataset_cache,
        load_public_dataset_manifest,
    )

    manifest = load_public_dataset_manifest(
        Path("reference-data/public-datasets/mimic-iv-demo/manifest.yaml")
    )
    cache_dir = tmp_path / "mimic"
    (cache_dir / "hosp").mkdir(parents=True)
    (cache_dir / "hosp" / "admissions.csv.gz").write_text("synthetic", encoding="utf-8")

    diagnostic = diagnose_public_dataset_cache(manifest, cache_dir)

    assert diagnostic.status == "missing-files"
    assert "hosp/admissions.csv.gz" in diagnostic.present_files
    assert "hosp/diagnoses_icd.csv.gz" in diagnostic.missing_files
    assert diagnostic.to_dict()["cache_root"] == str(cache_dir)


def test_public_dataset_reports_are_machine_readable() -> None:
    from nwau_py.public_clinical_datasets import (
        build_public_dataset_data_quality_report,
        build_public_dataset_disclosure_risk_summary,
        build_public_dataset_provenance_report,
        load_public_dataset_manifest,
    )

    manifest = load_public_dataset_manifest(
        Path("reference-data/public-datasets/mimic-iv-demo/manifest.yaml")
    )
    staged = pd.DataFrame(
        {
            "episode_id": ["e1", "e2"],
            "subject_id": [1001, 1002],
            "hadm_id": [2001, 2002],
            "admittime": ["2120-01-01", "2120-01-02"],
            "dischtime": ["2120-01-02", "2120-01-03"],
            "los_days": [1.0, 1.0],
            "icu_hours": [4.0, 0.0],
            "mimic_drg_code": ["001", "002"],
            "australian_ar_drg": ["", ""],
        }
    )

    provenance = build_public_dataset_provenance_report(
        manifest,
        local_files=("hosp/admissions.csv.gz",),
        derivation_steps=("stage_admissions",),
        overlay_status="none",
        support_state="blocked_licensed",
    )
    quality = build_public_dataset_data_quality_report(staged)
    disclosure = build_public_dataset_disclosure_risk_summary(staged)

    assert provenance["dataset_id"] == "mimic-iv-demo-2.2"
    assert provenance["classification_boundary"]["support_state"] == "blocked_licensed"
    assert quality["row_count"] == 2
    assert quality["classification_provenance_state"] == "missing"
    assert disclosure["commit_safe"] is False
    assert "admission IDs" in " ".join(disclosure["risk_reasons"])
