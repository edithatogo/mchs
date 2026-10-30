"""Preflight for raw AECC inputs, separate from already-grouped AECC feeds."""

from collections.abc import Mapping
from dataclasses import dataclass

AECC_INPUTS = frozenset(
    {
        "principal_diagnosis",
        "age",
        "episode_end_status",
        "triage_category",
        "arrival_transport",
        "clinical_care_commencement",
    }
)


@dataclass(frozen=True)
class GroupingReadiness:
    """An input inventory, never proof of official grouper parity."""

    missing_inputs: tuple[str, ...]
    mapping_unresolved: bool
    input_inventory_complete: bool
    official_grouping_qualified: bool = False


def assess_aecc_inputs(
    values: Mapping[str, object], *, diagnosis_mapping_qualified: bool
) -> GroupingReadiness:
    """Preserve missingness and reject lookalike field-name substitutions.

    Zero is an observed value here, not missing. Value domains, editions,
    chronology and a qualified grouper still require separate validation.
    """
    missing = tuple(
        sorted(
            key
            for key in AECC_INPUTS
            if values.get(key) is None
            or (isinstance(values.get(key), str) and not str(values[key]).strip())
        )
    )
    return GroupingReadiness(
        missing,
        not diagnosis_mapping_qualified,
        not missing and diagnosis_mapping_qualified,
    )
