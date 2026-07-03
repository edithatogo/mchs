"""Static classification-mapping registry rows used by the public registry.

The rows in this module are intentionally metadata-only. They describe
supported systems, stream bindings, version matrices, and local-only hook
placeholders without embedding any proprietary mapping tables or grouping
logic.
"""

from __future__ import annotations

from typing import Final


def _hook(
    *,
    hook_id: str,
    reference_type: str,
    command: str | None,
    reference_uri: str | None,
    local_path_hint: str | None,
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "hook_id": hook_id,
        "reference_type": reference_type,
        "status": "placeholder",
        "license_boundary": "local-only",
        "command": command,
        "reference_uri": reference_uri,
        "local_path_hint": local_path_hint,
        "notes": notes,
    }


CLASSIFICATION_MAPPING_ROWS: Final[tuple[dict[str, object], ...]] = (
    {
        "system": "ar_drg",
        "display_name": "AR-DRG",
        "aliases": ("ar-drg", "ar_drg", "ar drg"),
        "stream": "admitted_acute",
        "licensed": True,
        "restriction": "Licensed product; source artefacts may be restricted.",
        "support_status": "blocked_licensed",
        "required_fields": ("DRG",),
        "source_refs": (
            "https://www.ihacpa.gov.au/health-care/classification/admitted-acute-care",
            "https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system",
            "nwau_py/docs/calculators.md",
        ),
        "versions": (
            ("2013", "v7.0"),
            ("2014", "v7.0"),
            ("2015", "v7.0"),
            ("2016", "v8.0"),
            ("2017", "v8.0"),
            ("2018", "v9.0"),
            ("2019", "v9.0"),
            ("2020", "v10.0"),
            ("2021", "v10.0"),
            ("2022", "v10.0"),
            ("2023", "v11.0"),
            ("2024", "v11.0"),
            ("2025", "v11.0"),
            ("2026", "v12.0"),
        ),
        "public_asset": {
            "kind": "public-metadata",
            "source_refs": (
                "https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system",
                "nwau_py/docs/calculators.md",
                "reference-data/2025/manifest.yaml",
                "reference-data/2026/manifest.yaml",
            ),
            "local_path_hint": None,
            "restricted": False,
            "notes": (
                "Public metadata only; licensed AR-DRG tables are not bundled.",
                "The registry records the classification boundary without "
                "grouping logic.",
            ),
        },
        "local_hooks": (
            _hook(
                hook_id="ar-drg-local-command",
                reference_type="local_command",
                command="ar-drg-grouper --input in.json --output out.json",
                reference_uri=None,
                local_path_hint="archive/ihacpa/raw/2026/licensed/ar_drg/grouper/",
                notes=(
                    "Placeholder for a user-supplied local grouping command.",
                    "The repository does not ship the command or grouping tables.",
                ),
            ),
            _hook(
                hook_id="ar-drg-local-service",
                reference_type="local_service",
                command=None,
                reference_uri="http://localhost:8791/ar-drg-grouper",
                local_path_hint="archive/ihacpa/raw/2026/licensed/ar_drg/service/",
                notes=(
                    "Placeholder for a locally hosted licensed grouper service.",
                    "The service contract stays local-only.",
                ),
            ),
            _hook(
                hook_id="ar-drg-file-exchange",
                reference_type="file_exchange",
                command=None,
                reference_uri=None,
                local_path_hint="archive/ihacpa/raw/2026/licensed/ar_drg/file-exchange/",
                notes=(
                    "Placeholder for offline file exchange with a licensed provider.",
                    "The repo only records the exchange boundary.",
                ),
            ),
        ),
        "notes": (
            "AR-DRG remains licensed and should not be treated as redistributable.",
            "Local hook placeholders allow the deployed tool to describe the "
            "boundary without bundling proprietary logic.",
        ),
    },
    {
        "system": "aecc",
        "display_name": "AECC",
        "aliases": ("aecc",),
        "stream": "emergency_department",
        "licensed": False,
        "restriction": None,
        "support_status": "source_available",
        "required_fields": ("AECC",),
        "source_refs": (
            "https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc",
            "https://www.ihacpa.gov.au/health-care/classification/emergency-care",
            "nwau_py/docs/calculators.md",
        ),
        "versions": (
            ("2013", None),
            ("2014", None),
            ("2015", None),
            ("2016", None),
            ("2017", None),
            ("2018", None),
            ("2019", None),
            ("2020", "v1.0_shadow"),
            ("2021", "v1.0"),
            ("2022", "v1.1"),
            ("2023", "v1.1"),
            ("2024", "v1.1"),
            ("2025", "v1.1"),
            ("2026", "v1.1"),
        ),
        "public_asset": {
            "kind": "public-metadata",
            "source_refs": (
                "https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc",
                "nwau_py/docs/calculators.md",
            ),
            "local_path_hint": None,
            "restricted": False,
            "notes": (
                "Public metadata only; no licensed AECC payload is bundled.",
                "The registry records support without reimplementing any "
                "grouper logic.",
            ),
        },
        "local_hooks": (),
        "notes": (
            "AECC is public metadata in this repository and does not require "
            "local licensed assets.",
        ),
    },
    {
        "system": "udg",
        "display_name": "UDG",
        "aliases": ("udg",),
        "stream": "emergency_service",
        "licensed": False,
        "restriction": None,
        "support_status": "source_available",
        "required_fields": ("UDG",),
        "source_refs": (
            "https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg",
            "https://www.ihacpa.gov.au/health-care/classification/emergency-care",
            "nwau_py/docs/calculators.md",
        ),
        "versions": (
            ("2013", "URG_v1.4"),
            ("2014", "URG_v1.4"),
            ("2015", "URG_v1.4"),
            ("2016", "URG_v1.4"),
            ("2017", "URG_v1.4"),
            ("2018", "URG_v1.4"),
            ("2019", "URG_v1.4"),
            ("2020", "URG_v1.4"),
            ("2021", "UDG_v1.3"),
            ("2022", "UDG_v1.3"),
            ("2023", "UDG_v1.3"),
            ("2024", "UDG_v1.3"),
            ("2025", "UDG_v1.3"),
            ("2026", "UDG_v1.3"),
        ),
        "public_asset": {
            "kind": "public-metadata",
            "source_refs": (
                "https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg",
                "nwau_py/docs/calculators.md",
            ),
            "local_path_hint": None,
            "restricted": False,
            "notes": (
                "Public metadata only; no UDG code table is bundled here.",
                "The registry keeps the emergency-service boundary explicit.",
            ),
        },
        "local_hooks": (),
        "notes": ("UDG remains public metadata in this repository.",),
    },
    {
        "system": "tier_2",
        "display_name": "Tier 2",
        "aliases": ("tier-2", "tier_2", "tier 2"),
        "stream": "admitted_non_acute",
        "licensed": False,
        "restriction": None,
        "support_status": "source_available",
        "required_fields": ("TIER2_CLINIC",),
        "source_refs": (
            "https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27",
            "nwau_py/docs/calculators.md",
        ),
        "versions": (
            ("2013", None),
            ("2014", None),
            ("2015", None),
            ("2016", None),
            ("2017", None),
            ("2018", None),
            ("2019", None),
            ("2020", None),
            ("2021", None),
            ("2022", "v7"),
            ("2023", "v7"),
            ("2024", "v7"),
            ("2025", "v7"),
            ("2026", "v10.0"),
        ),
        "public_asset": {
            "kind": "public-metadata",
            "source_refs": (
                "https://www.ihacpa.gov.au/resources/national-efficient-price-determination-2026-27",
                "nwau_py/docs/calculators.md",
            ),
            "local_path_hint": None,
            "restricted": False,
            "notes": (
                "Public metadata only; Tier 2 support is recorded without "
                "bundling tables.",
                "The registry keeps the non-admitted boundary explicit.",
            ),
        },
        "local_hooks": (),
        "notes": ("Tier 2 remains public metadata in this repository.",),
    },
    {
        "system": "amhcc",
        "display_name": "AMHCC",
        "aliases": ("amhcc",),
        "stream": "community_mental_health",
        "licensed": False,
        "restriction": None,
        "support_status": "source_available",
        "required_fields": ("AMHCC",),
        "source_refs": (
            "https://www.ihacpa.gov.au/health-care/classification/mental-health-care",
            "nwau_py/docs/calculators.md",
        ),
        "versions": (
            ("2013", None),
            ("2014", None),
            ("2015", None),
            ("2016", None),
            ("2017", None),
            ("2018", None),
            ("2019", None),
            ("2020", None),
            ("2021", "v1"),
            ("2022", "v1"),
            ("2023", "v1"),
            ("2024", "v1"),
            ("2025", "v1"),
            ("2026", "v1"),
        ),
        "public_asset": {
            "kind": "public-metadata",
            "source_refs": (
                "https://www.ihacpa.gov.au/health-care/classification/mental-health-care",
                "nwau_py/docs/calculators.md",
            ),
            "local_path_hint": None,
            "restricted": False,
            "notes": (
                "Public metadata only; AMHCC support is recorded without "
                "bundling licensed assets.",
                "The registry preserves the community mental health boundary "
                "explicitly.",
            ),
        },
        "local_hooks": (),
        "notes": ("AMHCC remains public metadata in this repository.",),
    },
)
