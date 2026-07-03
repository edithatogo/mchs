from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "r_binding_20260512"
PUBLIC_API = ROOT / "conductor" / "public-api-contract.md"
DOWNSTREAM_PACKAGING = ROOT / "conductor" / "downstream-packaging-plans.md"
FIXTURE_MANIFEST = (
    ROOT / "tests" / "fixtures" / "golden" / "acute_2025" / "manifest.json"
)
R_BINDING = ROOT / "r-binding"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def test_r_binding_track_files_and_shared_contract_docs_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "strategy.md",
        TRACK / "ci_notes.md",
        R_BINDING / "DESCRIPTION",
        R_BINDING / "NAMESPACE",
        R_BINDING / "R" / "nwau.R",
        R_BINDING / "tests" / "testthat.R",
        R_BINDING / "tests" / "testthat" / "test-wrapper-contract.R",
        PUBLIC_API,
        DOWNSTREAM_PACKAGING,
        FIXTURE_MANIFEST,
    ]:
        assert path.exists(), path


def test_r_binding_strategy_records_the_selected_non_duplicative_path():
    strategy = _read(TRACK / "strategy.md").lower()
    downstream = _read(DOWNSTREAM_PACKAGING).lower()

    assert "thin r wrapper over the shared cli plus file interchange" in strategy
    assert "csv is the executable prototype" in strategy
    assert "arrow/parquet is the target exchange format" in strategy
    assert "least duplicative option" in strategy
    assert "formula logic" in strategy
    assert (
        "works well for large costing-study batches and quarto/r markdown pipelines"
        in strategy
    )
    assert "recommended evaluation path: `extendr`" in downstream
    assert (
        "release readiness is claimable only after fixture-backed parity is recorded"
        in downstream
    )


def test_r_binding_docs_expose_the_batch_api_boundary():
    public_api = _read(PUBLIC_API).lower()
    spec = _read(TRACK / "spec.md").lower()
    strategy = _read(TRACK / "strategy.md").lower()

    assert "runtime-neutral and batch-first" in public_api
    assert "calculator core, not in adapters" in public_api
    assert (
        "define an r package api for batch calculation and validation diagnostics"
        in spec
    )
    assert "document installation and use from r markdown/quarto" in spec
    assert "repeatable batch runs" in strategy
    assert "quarto/r markdown pipelines" in strategy


def test_r_binding_reuses_shared_fixtures_and_synthetic_examples():
    spec = _read(TRACK / "spec.md").lower()
    plan = _read(TRACK / "plan.md").lower()
    manifest = _load_json(FIXTURE_MANIFEST)
    source_basis = _as_mapping(manifest["source_basis"])
    provenance = _as_mapping(manifest["provenance"])
    notes = provenance["notes"]
    assert isinstance(notes, list)

    assert "reuse shared golden fixtures and synthetic costing-study examples" in spec
    assert "r examples run against synthetic fixtures" in spec
    assert "include r markdown or quarto costing-study examples" in plan
    assert "validate outputs against golden fixtures" in plan
    assert manifest["privacy_classification"] == "synthetic"
    assert source_basis["kind"] == "synthetic_sample"
    assert "synthetic fixture pack for cross-language parity checks." in (
        str(notes[0]).lower()
    )
    assert str(source_basis["input_source"]).endswith("acute_input.csv")
    assert str(source_basis["expected_output_source"]).endswith("acute_expected.csv")


def test_r_binding_package_is_wrapper_only_and_has_testthat_guardrails():
    source = _read(R_BINDING / "R" / "nwau.R").lower()
    readme = _read(R_BINDING / "README.md").lower()
    testthat = _read(
        R_BINDING / "tests" / "testthat" / "test-wrapper-contract.R"
    ).lower()

    for forbidden in [
        "nwau25 =",
        "nwau25 <-",
        "private_service_adjustment",
        "long_stay_per_diem",
        "same_day_base_weight",
        "icu_rate",
    ]:
        assert forbidden not in source

    assert "system2" in source
    assert "nwau_cli_contract" in source
    assert "validate_nwau_input" in source
    assert "nwau_assert_output_file" in source
    assert "`python3` and the module `nwau_py.cli.main`" in readme
    assert "formula logic stays in python" in readme
    assert "successful cli runs must produce a non-empty output csv" in readme
    assert "diagnose reports cli failures without formula fallback" in testthat
    assert "input validation enforces concrete csv handoff" in testthat
    assert "cli contract probe reports command failures without formula fallback" in (
        testthat
    )
