import pytest

from nwau_py.calculators.relative_stay import StayStratum, relative_stay_index


@pytest.mark.parametrize(
    ("n", "observed_mean", "expected_mean", "published"),
    [(174, 7.67, 7.24, 1.06), (44, 5.91, 7.69, 0.77)],
)
def test_published_table_4(n, observed_mean, expected_mean, published):
    # Kamaraju et al., Table 4. Totals reconstructed from rounded subgroup means.
    result = relative_stay_index(
        [StayStratum("group", n, n * observed_mean)],
        {"group": expected_mean},
        benchmark="Kamaraju et al., Table 4, published rounded means",
    )
    assert round(result.index, 2) == published


def test_weighted_cohort_and_exclusion():
    result = relative_stay_index(
        [
            StayStratum("a", 2, 6),
            StayStratum("b", 1, 2),
            StayStratum("x", 3, 12, "out of scope"),
        ],
        {"a": 2, "b": 6},
        benchmark="synthetic v1",
    )
    assert (result.actual_days, result.expected_days, result.index) == (8, 10, 0.8)
    assert result.eligible_separations == 3
    assert result.excluded_by_reason == {"out of scope": 3}


@pytest.mark.parametrize("reference", [{}, {"a": 0}, {"a": float("nan")}])
def test_missing_or_invalid_reference(reference):
    with pytest.raises(ValueError):
        relative_stay_index([StayStratum("a", 1, 2)], reference, benchmark="test")


def test_empty_denominator():
    with pytest.raises(ValueError):
        relative_stay_index([], {}, benchmark="test")
