"""Synthetic algebraic contracts, without pricing data or clinical assertions."""

import os
from decimal import Decimal

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from nwau_py.calculators.nep26_equation import TERMS, evaluate
from nwau_py.calculators.relative_stay import StayStratum, relative_stay_index

_EXAMPLES = int(os.environ.get("CALCULATION_PROPERTY_EXAMPLES", "100"))
if not 1 <= _EXAMPLES <= 1000:
    raise ValueError("CALCULATION_PROPERTY_EXAMPLES must be between 1 and 1000")
_BOUNDED = settings(max_examples=_EXAMPLES, deadline=1000)
_DECIMALS = st.integers(-100, 100).map(Decimal)
_TERMS = st.fixed_dictionaries({name: _DECIMALS for name in sorted(TERMS)})


@_BOUNDED
@given(terms=_TERMS, multiplier=st.integers(0, 100))
def test_currency_scaling_cannot_change_activity(
    terms: dict[str, Decimal], multiplier: int
) -> None:
    before = evaluate(terms)
    changed = {**terms, "NEP": terms["NEP"] * multiplier}
    after = evaluate(changed)
    assert after.activity_nwau == before.activity_nwau
    assert after.amount_aud == before.amount_aud * multiplier
    assert after.formula_version == "NEP26-section-2.3-pre-floor-v1"


@_BOUNDED
@given(weight=st.integers(-10000, 10000), price=st.integers(1, 10000))
def test_neutral_adjustments_retain_signed_activity(weight: int, price: int) -> None:
    terms = dict.fromkeys(TERMS, Decimal(0))
    terms.update(PW=Decimal(weight), APaed=Decimal(1), NEP=Decimal(price))
    result = evaluate(terms)
    assert result.activity_nwau == weight
    assert result.amount_aud == weight * price


@_BOUNDED
@given(terms=_TERMS, delta=st.integers(-100, 100))
def test_shadow_adjustment_has_exact_signed_marginal_effect(
    terms: dict[str, Decimal], delta: int
) -> None:
    before = evaluate(terms)
    changed = {**terms, "AHAC": terms["AHAC"] + delta}
    after = evaluate(changed)
    expected_change = -terms["PW"] * delta
    assert after.activity_nwau - before.activity_nwau == expected_change
    assert after.amount_aud - before.amount_aud == expected_change * terms["NEP"]


@_BOUNDED
@given(terms=_TERMS, missing=st.sampled_from(sorted(TERMS)))
def test_missing_terms_cannot_silently_become_zero(
    terms: dict[str, Decimal], missing: str
) -> None:
    terms.pop(missing)
    with pytest.raises(ValueError, match="Supply every NEP26 term as a finite Decimal"):
        evaluate(terms)


@_BOUNDED
@given(
    terms=_TERMS,
    key=st.sampled_from(sorted(TERMS)),
    nonfinite=st.sampled_from(["NaN", "sNaN", "Infinity", "-Infinity"]),
)
def test_nonfinite_terms_fail_before_decimal_arithmetic(
    terms: dict[str, Decimal], key: str, nonfinite: str
) -> None:
    terms[key] = Decimal(nonfinite)
    with pytest.raises(ValueError, match="Supply every NEP26 term as a finite Decimal"):
        evaluate(terms)


@_BOUNDED
@given(
    first=st.integers(1, 100),
    second=st.integers(1, 100),
    days_first=st.integers(0, 10000),
    days_second=st.integers(0, 10000),
    reference_mean=st.integers(1, 100),
)
def test_relative_stay_preserves_disjoint_aggregation_and_order(
    first: int,
    second: int,
    days_first: int,
    days_second: int,
    reference_mean: int,
) -> None:
    rows = [
        StayStratum("synthetic", first, days_first),
        StayStratum("synthetic", second, days_second),
    ]
    reference = {"synthetic": float(reference_mean)}
    merged = [StayStratum("synthetic", first + second, days_first + days_second)]
    actual = relative_stay_index(rows, reference, benchmark="synthetic-v1")
    assert actual == relative_stay_index(merged, reference, benchmark="synthetic-v1")
    assert actual == relative_stay_index(
        reversed(rows), reference, benchmark="synthetic-v1"
    )
    assert actual.eligible_separations == first + second
    assert actual.index == (days_first + days_second) / (
        (first + second) * reference_mean
    )


@_BOUNDED
@given(
    eligible=st.integers(1, 100),
    excluded=st.integers(1, 100),
    days=st.integers(0, 10000),
    excluded_days=st.integers(0, 10000),
    mean=st.integers(1, 100),
)
def test_exclusion_count_never_enters_the_eligible_denominator(
    eligible: int, excluded: int, days: int, excluded_days: int, mean: int
) -> None:
    result = relative_stay_index(
        [
            StayStratum("eligible", eligible, days),
            StayStratum(
                "no-reference-needed", excluded, excluded_days, "synthetic exclusion"
            ),
        ],
        {"eligible": float(mean)},
        benchmark="synthetic-v1",
    )
    assert result.eligible_separations == eligible
    assert result.excluded_by_reason == {"synthetic exclusion": excluded}
    assert result.actual_days == days
    assert result.expected_days == eligible * mean
    assert result.index == days / (eligible * mean)


@_BOUNDED
@given(count=st.integers(1, 100), days=st.integers(0, 10000))
def test_missing_eligible_reference_cannot_reduce_cohort_coverage(
    count: int, days: int
) -> None:
    with pytest.raises(ValueError, match="Missing or invalid expected days"):
        relative_stay_index(
            [StayStratum("known", 1, 1), StayStratum("missing", count, days)],
            {"known": 1.0},
            benchmark="synthetic-v1",
        )
