from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from nwau_py.pricing_constants import (
    NEP26,
    NEP_BY_YEAR,
    _build_nep_by_year,
    get_nep,
    get_supported_pricing_years,
)
from nwau_py.reference_manifest import ReferenceManifestError, load_reference_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_2025 = ROOT / "reference-data" / "2025" / "manifest.yaml"
MANIFEST_2026 = ROOT / "reference-data" / "2026" / "manifest.yaml"


def _load_manifest_dict(year: str) -> dict[str, object]:
    payload = yaml.safe_load(
        (ROOT / "reference-data" / year / "manifest.yaml").read_text(encoding="utf-8")
    )
    assert isinstance(payload, dict)
    return payload


def test_pricing_constants_are_loaded_from_reference_data_manifests() -> None:
    manifest_2025 = load_reference_manifest(MANIFEST_2025)
    manifest_2026 = load_reference_manifest(MANIFEST_2026)

    assert manifest_2025.constants["nep"]["value"] == 7258
    assert manifest_2026.constants["nep"]["value"] == 7418
    assert NEP_BY_YEAR == {"2025": 7258, "2026": 7418}
    assert get_supported_pricing_years() == ["2025", "2026"]
    assert get_nep("2025") == 7258
    assert get_nep("2026") == 7418
    assert NEP26 == 7418


def test_pricing_constants_fail_closed_when_manifest_missing_nep_value(
    tmp_path: Path,
) -> None:
    payload = deepcopy(_load_manifest_dict("2025"))
    payload["pricing_year"] = "2028"
    payload["financial_year"] = "2028-29"
    payload["current_pricing_year"] = False
    payload["validation_status"] = "source-only"
    payload["validation"]["status"] = "source-only"
    payload["validation"]["parity_claim"] = False
    payload["validation"]["source_only"] = True
    payload["constants"].pop("nep")

    manifest_path = tmp_path / "reference-data" / "2028" / "manifest.yaml"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    with pytest.raises(ReferenceManifestError, match=r"constants\.nep"):
        _build_nep_by_year(repo_root=tmp_path)
