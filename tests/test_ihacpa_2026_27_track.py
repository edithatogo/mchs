from __future__ import annotations

import json
from pathlib import Path

from nwau_py.pricing_constants import (
    NEC26,
    NEC_BY_YEAR,
    NEP26,
    NEP_BY_YEAR,
    PRICING_CONSTANTS_SCHEMA_VERSION,
    get_nec,
    get_nep,
    get_supported_pricing_years,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "ihacpa_2026_27_support_20260512"
TRACK = ROOT / "conductor" / "tracks" / TRACK_ID
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / TRACK_ID
TRACKS = ROOT / "conductor" / "tracks.md"
SOURCE_INVENTORY = TRACK / "source_inventory.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ihacpa_2026_27_support_track_scaffold_is_present():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        SOURCE_INVENTORY,
        TRACKS,
    ]:
        assert path.exists(), path


def test_ihacpa_2026_27_support_track_metadata_is_completed_but_conservative():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    track_index = _read_text(TRACK / "index.md")
    registry = _read_text(TRACKS)

    assert metadata["track_id"] == "ihacpa_2026_27_support_20260512"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "governance"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert metadata["support_scope"]["state"] == "complete-with-gaps"
    assert "does not claim calculator parity" in metadata["support_scope"]["summary"]
    assert {gap["id"] for gap in metadata["gap_register"]} >= {
        "nep26-calculator-parity",
        "nep26-sas-extraction",
        "nep26-excel-internal-audit",
        "hac-ahr-companion-hashes",
    }

    assert "ihacpa_2026_27_support_20260512" in track_index
    assert "IHACPA 2026-27 Support" in registry
    assert (
        "Gate: add current 2026-27 NEP, technical specification, "
        "price-weight, calculator, and classification-version support with "
        "explicit validation status."
    ) in registry
    assert "explicit validation status" in registry
    assert "calculator parity is not claimed" in track_index
    assert "Remaining gaps are explicit" in track_index


def test_ihacpa_2026_27_phase_1_source_inventory_is_complete_and_gap_explicit():
    inventory = _read_text(SOURCE_INVENTORY)
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")

    for phrase in [
        (
            "Scope: official IHACPA sources for 2026-27 NEP, NEC, technical "
            "specifications, NWAU calculators, and price-weight downloads."
        ),
        "## Inventory",
        "## Explicit gaps",
        "## Source notes",
        "National Efficient Price Determination 2026",
        "National Efficient Cost Determination 2026",
        "National Pricing Model Technical Specifications 2026",
        "NWAU calculators",
        "Price weights",
        "$7,418 per NWAU(26)",
        "AR-DRG v12.0",
        "Tier 2 Version 10.0",
        "Determination and technical specification downloads",
        "2162d941f5b75548b1bbf82377e20b0a63c215afefbb8e9b920b85dac5611aab",
        "cca4212fccca2e40b741ee4279d8cf67c2b35a277049865c8453d485f6086fc3",
        "29f2f526aa54d09d5cf7a98a83598ef23ee4f5774fb66b6648ab49ec0a624836",
        "ff6d8e34dd56633559de0a4e58c6d0a563e62ca317f737b8439783111c86aa98",
        "47f28004b9b47050d921e5090a690d041126543ca436d051b20af75b5fcadc40",
        "calculator parity",
        "no standalone open license",
        "the SAS `.7Z` archive has not been extracted.",
        "separate standalone NEC price-weight table file",
    ]:
        assert phrase in inventory or phrase in inventory.lower()

    assert (
        "Do not claim calculator parity until verified against official IHACPA "
        "calculator outputs or source logic."
    ) in spec
    assert "health-care/pricing/national-pricing-model-technical-specifications" in spec
    assert "health-care/pricing/nwau-calculators" in spec
    assert "what-we-do/pricing" not in spec
    assert "what-we-do/national-weighted-activity-unit" not in spec
    assert "Keep validation conservative and auditable." in spec
    assert "source inventory records official NEP, NEC" in _read_text(
        TRACK / "index.md"
    )

    for phrase in [
        (
            "Record 2026-27 NEP, NEC, technical specifications, calculator, "
            "and price-weight source entries."
        ),
        (
            "Mark unavailable calculator artifacts as explicit gaps rather "
            "than inferred support."
        ),
        "Capture URLs, publication dates, checksums, and licensing/provenance notes.",
    ]:
        assert phrase in plan

    assert "**Captured:** SHA-256 hashes are recorded above" in inventory
    assert "Checksum status: captured for the XLSX download" in inventory
    assert "Checksum status: not yet captured for the XLSX download" not in inventory
    assert (
        "explicit gaps rather than being silently implied as support" in inventory
        or "Explicit gaps" in inventory
    )


def test_ihacpa_2026_27_phase_2_pricing_constants_api_exposes_nep26():
    assert PRICING_CONSTANTS_SCHEMA_VERSION == "1.0"
    assert tuple(get_supported_pricing_years()) == ("2025", "2026")
    assert NEP26 == 7418
    assert NEP_BY_YEAR == {"2025": 7434, "2026": 7418}
    assert NEC_BY_YEAR == {"2025": None, "2026": NEC26}
    assert get_nep("2026") == 7418
    assert get_nep("2025") == 7434
    assert get_nep("2024") is None
    assert get_nec("2026") == NEC26
    assert NEC26.fixed_cost_dollars == 3_127_000
    assert NEC26.variable_cost_per_nwau == 8_003
    assert NEC26.in_scope_hospitals == 364
    assert get_nec("2024") is None


def test_ihacpa_2026_27_phase_3_validation_status_stays_conservative():
    spec = _read_text(TRACK / "spec.md")
    index = _read_text(TRACK / "index.md")
    inventory = _read_text(SOURCE_INVENTORY)
    registry = _read_text(TRACKS)

    for phrase in [
        (
            "Do not claim calculator parity until verified against official "
            "IHACPA calculator outputs or source logic."
        ),
        "Keep validation conservative and auditable.",
        "explicit validation status",
        "calculator parity is not claimed",
        "NEP26 compiled/Python reference files from IHACPA",
        "NEP26 user guides or calculator documentation",
    ]:
        assert (
            phrase in spec
            or phrase in index
            or phrase in inventory
            or phrase in registry
        )

    assert (
        "parity validation is not claimed" in inventory
        or "not yet validated" in inventory
    )
