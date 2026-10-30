"""Explicit NEP26 section 2.3 equation; not a grouper or full funding calculator.

Source: IHACPA National Pricing Model Technical Specifications 2026-27,
section 2.3 (March 2026). NWAU is activity; multiplying by NEP yields AUD.
"""

from dataclasses import dataclass
from decimal import Decimal

TERMS = frozenset(
    {
        "PW",
        "APaed",
        "AInd",
        "ARes",
        "ART",
        "ADia",
        "ATreat",
        "AICU",
        "ICU_hours",
        "APPS",
        "LOS",
        "AAcc",
        "AHAC",
        "PWAHR",
        "AAHR",
        "NEP",
    }
)


@dataclass(frozen=True)
class EquationResult:
    """Separate pre-floor activity and currency, with explicit scope."""

    activity_nwau: Decimal
    amount_aud: Decimal
    formula_version: str = "NEP26-section-2.3-pre-floor-v1"


def evaluate(terms: dict[str, Decimal]) -> EquationResult:
    """Evaluate explicit finite Decimal terms without missing-to-zero defaults.

    ART is radiotherapy; ATreat is treatment remoteness. AICU must be the
    applicable eligible hourly adjustment, not a bundled-ICU Boolean. AHAC
    and AAHR are shadow adjustments: callers must choose their treatment.
    No COVID multiplier exists in this year's equation. Negative pre-floor
    values are retained; official funding flooring is a separate policy.
    """
    if set(terms) != TERMS or not all(
        isinstance(value, Decimal) and value.is_finite() for value in terms.values()
    ):
        raise ValueError("Supply every NEP26 term as a finite Decimal")
    t = terms
    activity = (
        t["PW"]
        * t["APaed"]
        * (1 + t["ARes"] + t["AInd"] + t["ART"] + t["ADia"])
        * (1 + t["ATreat"])
        + t["AICU"] * t["ICU_hours"]
        - (t["PW"] + t["AICU"] * t["ICU_hours"]) * t["APPS"]
        - t["LOS"] * t["AAcc"]
        - t["PW"] * t["AHAC"]
        - t["PWAHR"] * t["AAHR"]
    )
    return EquationResult(activity, activity * t["NEP"])
