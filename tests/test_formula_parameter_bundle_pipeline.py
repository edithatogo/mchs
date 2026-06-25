from __future__ import annotations

import json
import sys
import types
from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PYREADSTAT: Any = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

import nwau_py.calculators.acute as acute  # noqa: E402
from nwau_py.formula_parameter_bundle import (  # noqa: E402
    FormulaParameterBundle,
    bundle_diff,
    bundle_sha256,
    bundle_to_canonical_json,
    load_acute_2025_canary_bundle,
    load_formula_parameter_bundle,
    resolve_formula_parameter_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "formula_parameter_bundle_pipeline_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
DOCS_PAGE = (
    ROOT
    / "docs-site"
    / "src"
    / "content"
    / "docs"
    / "governance"
    / "formula-parameter-bundle-pipeline.mdx"
)
GOVERNANCE_INDEX = (
    ROOT / "docs-site" / "src" / "content" / "docs" / "governance" / "index.mdx"
)
CONTRACT = (
    ROOT
    / "contracts"
    / "formula-parameter-bundle"
    / "formula-parameter-bundle.contract.json"
)
CONTRACT_EXAMPLE = (
    ROOT / "contracts" / "formula-parameter-bundle" / "examples" / "bundle.json"
)
CONTRACT_DIFF_EXAMPLE = (
    ROOT / "contracts" / "formula-parameter-bundle" / "examples" / "bundle-diff.json"
)
CANARY = (
    ROOT
    / "reference-data"
    / "2025"
    / "parameter-bundles"
    / "acute"
    / "acute-2025-canary"
    / "v1"
    / "bundle.json"
)


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_formula_parameter_bundle_track_docs_and_contract_are_current() -> None:
    metadata = _read_json(TRACK / "metadata.json")
    tracks = TRACKS.read_text(encoding="utf-8")
    docs_page = DOCS_PAGE.read_text(encoding="utf-8")
    governance_index = GOVERNANCE_INDEX.read_text(encoding="utf-8")
    contract = _read_json(CONTRACT)

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "not-ready"
    assert metadata["gap_blockers"]
    assert metadata["completion_policy"].startswith("complete-with-gaps means")
    assert "[x] **Track: Formula and Parameter Bundle Pipeline**" in tracks
    assert "source-only" in docs_page.lower()
    index = (TRACK / "index.md").read_text(encoding="utf-8")
    assert "not parity-validated" in index
    assert "publication blockers" in index
    assert "formula-parameter-bundle-pipeline" in governance_index
    assert contract["tool"]["name"] == "nwau_py.formula_parameter_bundle"
    assert contract["tool"]["package"] == "nwau_py"
    assert contract["bundle"]["status"] == "source-only"


def test_canary_bundle_loads_strictly_and_preserves_provenance() -> None:
    resolved = load_formula_parameter_bundle(CANARY)
    bundle = resolved.bundle

    assert bundle.schema_version == "1.0"
    assert bundle.bundle_id == "acute-2025-canary"
    assert bundle.bundle_version == "v1"
    assert bundle.calculator == "acute"
    assert bundle.pricing_year == "2025"
    assert bundle.stream == "acute"
    assert bundle.status == "source-only"
    assert bundle.validation.status == "source-only"
    assert bundle.validation.parity_claim is False
    assert resolved.manifest_path == CANARY
    assert resolved.bundle_dir == CANARY.parent

    source_ids = {e.evidence_id for e in bundle.source_evidence}
    assert {
        "ihacpa-nep25-acute-page",
        "nep25-acute-weight-fixture",
        "excel-2025-formula-fixture",
    } <= source_ids

    weights = resolved.weights_frame()
    assert isinstance(weights, pd.DataFrame)
    assert list(weights["DRG"]) == ["801A", "801B", "801C"]
    assert weights.loc[weights["DRG"] == "801A", "drg_pw_inlier"].item() > 0


def test_resolved_bundle_serialization_hash_and_diff_are_stable() -> None:
    resolved = resolve_formula_parameter_bundle(
        ROOT,
        year="2025",
        stream="acute",
        bundle_id="acute-2025-canary",
        bundle_version="v1",
    )

    assert resolved.manifest_path == CANARY
    assert load_acute_2025_canary_bundle(ROOT).bundle.bundle_id == "acute-2025-canary"
    assert bundle_to_canonical_json(resolved) == bundle_to_canonical_json(resolved)
    assert len(bundle_sha256(resolved)) == 64
    assert bundle_diff(resolved, resolved) == ""

    mutated_payload = deepcopy(resolved.bundle.model_dump(mode="json"))
    mutated_payload["weights"][0]["parameters"]["drg_pw_inlier"] = 9.999
    mutated = FormulaParameterBundle.model_validate(mutated_payload)

    diff = bundle_diff(resolved.bundle, mutated, from_name="before", to_name="after")
    assert "--- before" in diff
    assert "+++ after" in diff
    assert "9.999" in diff


def test_bundle_rejects_unknown_evidence_and_status_overclaim() -> None:
    payload = _read_json(CANARY)
    payload["weights"][0]["source_evidence_ids"] = ["missing-evidence"]

    with pytest.raises(ValueError, match="unknown evidence"):
        FormulaParameterBundle.model_validate(payload)

    overclaim = _read_json(CANARY)
    overclaim["validation"]["source_only"] = True
    overclaim["validation"]["status"] = "schema-complete"
    overclaim["status"] = "schema-complete"

    with pytest.raises(ValueError, match="source-only"):
        FormulaParameterBundle.model_validate(overclaim)


def test_acute_2025_canary_reference_bundle_uses_bundle_weights() -> None:
    reference_bundle = acute.load_acute_2025_canary_reference_bundle()

    assert reference_bundle.year == "2025"
    assert reference_bundle.ref_dir == CANARY.parent
    assert reference_bundle.weights is not None
    assert list(reference_bundle.weights["DRG"]) == ["801A", "801B", "801C"]


def test_formula_parameter_bundle_contract_examples_are_conservative() -> None:
    contract = _read_json(CONTRACT)
    example = _read_json(CONTRACT_EXAMPLE)
    diff_example = _read_json(CONTRACT_DIFF_EXAMPLE)

    assert contract["privacy"]["contains_phi"] is False
    assert example["status"] == "source-only"
    assert "validated" not in json.dumps(example).lower()
    assert diff_example["changes"][-1]["after"] == "schema-complete"
    assert diff_example["summary"]["status_changes"] == 1
