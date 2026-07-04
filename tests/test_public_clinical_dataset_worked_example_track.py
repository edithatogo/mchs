from __future__ import annotations

from pathlib import Path
from typing import Any, cast

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
    classification_boundary = cast(
        dict[str, Any],
        provenance["classification_boundary"],
    )
    assert classification_boundary["support_state"] == "blocked_licensed"
    assert quality["row_count"] == 2
    assert quality["classification_provenance_state"] == "missing"
    assert disclosure["commit_safe"] is False
    risk_reasons = cast(list[str], disclosure["risk_reasons"])
    assert "admission IDs" in " ".join(risk_reasons)


def test_mimic_demo_staging_preserves_episode_lineage() -> None:
    from nwau_py.public_clinical_datasets import stage_mimic_demo_episodes

    staged = stage_mimic_demo_episodes(Path("examples/mimic_demo/fixtures"))

    assert list(staged["episode_id"]) == ["mimic-1001-2001", "mimic-1002-2002"]
    assert list(staged["los_days"]) == [2.0, 1.0]
    assert list(staged["icu_hours"]) == [12.0, 0.0]
    assert staged.loc[0, "mimic_drg_code"] == "001"
    assert staged.loc[0, "diagnosis_codes"] == "I10;E119"
    assert staged.loc[0, "procedure_codes"] == "5A1955Z"
    assert "hosp/admissions.csv" in staged.loc[0, "lineage_source_files"]


def test_mimic_demo_calculator_input_fails_closed_without_ar_drg() -> None:
    from nwau_py.public_clinical_datasets import (
        PublicDatasetClassificationError,
        prepare_mimic_demo_calculator_input,
        stage_mimic_demo_episodes,
    )

    staged = stage_mimic_demo_episodes(Path("examples/mimic_demo/fixtures"))

    with pytest.raises(
        PublicDatasetClassificationError,
        match="Australian AR-DRG provenance",
    ):
        prepare_mimic_demo_calculator_input(staged)


def test_mimic_demo_synthetic_overlay_prepares_acute_input() -> None:
    from nwau_py.public_clinical_datasets import (
        prepare_mimic_demo_calculator_input,
        stage_mimic_demo_episodes,
    )

    staged = stage_mimic_demo_episodes(Path("examples/mimic_demo/fixtures"))
    calculator_input = prepare_mimic_demo_calculator_input(
        staged,
        synthetic_overlay_path=Path("examples/mimic_demo/fixtures/synthetic_overlay.csv"),
        allow_synthetic_overlay=True,
    )

    assert list(calculator_input["DRG"]) == ["801A", "801B"]
    assert list(calculator_input["LOS"]) == [2.0, 1.0]
    assert list(calculator_input["ICU_HOURS"]) == [12.0, 0.0]
    assert set(calculator_input["classification_provenance"]) == {
        "synthetic_demo_overlay"
    }
    assert calculator_input["overlay_is_synthetic"].all()


def test_mimic_demo_local_precomputed_overlay_requires_provenance(
    tmp_path: Path,
) -> None:
    from nwau_py.public_clinical_datasets import (
        prepare_mimic_demo_calculator_input,
        stage_mimic_demo_episodes,
    )

    overlay_path = tmp_path / "local_ar_drg.csv"
    pd.DataFrame(
        {
            "episode_id": ["mimic-1001-2001", "mimic-1002-2002"],
            "australian_ar_drg": ["801A", "801B"],
            "classification_provenance": ["local_precomputed_ar_drg"] * 2,
        }
    ).to_csv(overlay_path, index=False)
    staged = stage_mimic_demo_episodes(Path("examples/mimic_demo/fixtures"))

    calculator_input = prepare_mimic_demo_calculator_input(
        staged,
        local_ar_drg_path=overlay_path,
    )

    assert list(calculator_input["DRG"]) == ["801A", "801B"]
    assert set(calculator_input["classification_provenance"]) == {
        "local_precomputed_ar_drg"
    }
    assert not calculator_input["overlay_is_synthetic"].any()


def test_mimic_demo_worked_example_bundle_exercises_core_surfaces() -> None:
    from nwau_py.public_clinical_datasets import run_mimic_demo_worked_example

    bundle = run_mimic_demo_worked_example(
        Path("examples/mimic_demo/fixtures"),
        synthetic_overlay_path=Path("examples/mimic_demo/fixtures/synthetic_overlay.csv"),
        reference_weights_path=Path("tests/data/nep25_aa_price_weights.csv"),
    )

    assert list(bundle.staged["episode_id"]) == [
        "mimic-1001-2001",
        "mimic-1002-2002",
    ]
    assert "NWAU25" in bundle.calculated.columns
    assert bundle.support_status_summary["validated"] == [
        "python_api_acute_runtime_with_fixture_weights"
    ]
    assert bundle.support_status_summary["blocked_licensed"] == [
        "authoritative_australian_ar_drg_from_mimic_alone"
    ]
    mcp_report = cast(dict[str, Any], bundle.surface_contract_report["mcp"])
    assert mcp_report["status"] == "boundary_validated"
    assert mcp_report["runtime_formula_execution"] == "not_claimed"
    scenario_names = [
        scenario["scenario"]
        for scenario in cast(list[dict[str, Any]], bundle.scenario_sensitivity_report)
    ]
    assert scenario_names == ["missing_australian_ar_drg", "synthetic_overlay"]
    assert bundle.disclosure_risk_summary["safe_output_class"] == "local-only"


def test_mimic_demo_worked_example_reports_local_precomputed_scenario(
    tmp_path: Path,
) -> None:
    from nwau_py.public_clinical_datasets import run_mimic_demo_worked_example

    overlay_path = tmp_path / "local_ar_drg.csv"
    pd.DataFrame(
        {
            "episode_id": ["mimic-1001-2001", "mimic-1002-2002"],
            "australian_ar_drg": ["801A", "801B"],
            "classification_provenance": ["local_precomputed_ar_drg"] * 2,
        }
    ).to_csv(overlay_path, index=False)

    bundle = run_mimic_demo_worked_example(
        Path("examples/mimic_demo/fixtures"),
        synthetic_overlay_path=Path("examples/mimic_demo/fixtures/synthetic_overlay.csv"),
        local_ar_drg_path=overlay_path,
        reference_weights_path=Path("tests/data/nep25_aa_price_weights.csv"),
    )

    scenario_names = [
        scenario["scenario"]
        for scenario in cast(list[dict[str, Any]], bundle.scenario_sensitivity_report)
    ]
    assert scenario_names == [
        "missing_australian_ar_drg",
        "synthetic_overlay",
        "local_precomputed_ar_drg",
    ]


def test_mimic_demo_worked_example_writes_local_outputs(tmp_path: Path) -> None:
    from nwau_py.public_clinical_datasets import run_mimic_demo_worked_example

    bundle = run_mimic_demo_worked_example(
        Path("examples/mimic_demo/fixtures"),
        synthetic_overlay_path=Path("examples/mimic_demo/fixtures/synthetic_overlay.csv"),
        reference_weights_path=Path("tests/data/nep25_aa_price_weights.csv"),
        output_dir=tmp_path,
    )

    assert {
        "staged",
        "calculator_input",
        "calculated",
        "provenance_report",
        "data_quality_report",
        "disclosure_risk_summary",
        "support_status_summary",
        "surface_contract_report",
        "mcp_boundary_validation",
        "scenario_sensitivity_report",
    }.issubset(bundle.written_files)
    for output_path in bundle.written_files.values():
        assert Path(output_path).exists()
