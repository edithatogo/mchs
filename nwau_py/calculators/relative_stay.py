"""Indirect relative stay index for a caller-defined, versioned benchmark."""

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class StayStratum:
    """One separation or disjoint aggregate. Actual days are the TOTAL."""

    stratum: str
    separations: int
    actual_days: float
    exclusion_reason: str | None = None


@dataclass(frozen=True)
class RelativeStayResult:
    benchmark: str
    eligible_separations: int
    excluded_by_reason: dict[str, int]
    actual_days: float
    expected_days: float
    index: float


def relative_stay_index(
    rows: Iterable[StayStratum],
    expected_days_per_separation: Mapping[str, float],
    *,
    benchmark: str,
) -> RelativeStayResult:
    """Apply reference mean days to local eligible counts and return actual/expected.

    Callers define disjoint strata, apply the benchmark eligibility and patient-day
    conventions, and identify its version, period and population in benchmark.
    Missing eligible strata fail the calculation rather than reducing coverage.
    """
    if not benchmark.strip():
        raise ValueError("A benchmark identifier is required")
    count = 0
    actual = expected = 0.0
    excluded: Counter[str] = Counter()
    for row in rows:
        if type(row.separations) is not int or row.separations <= 0:
            raise ValueError("Separations must be a positive integer")
        if row.exclusion_reason is not None:
            if not row.exclusion_reason.strip():
                raise ValueError("An exclusion reason cannot be blank")
            excluded[row.exclusion_reason] += row.separations
            continue
        mean = expected_days_per_separation.get(row.stratum)
        if mean is None or not isfinite(mean) or mean <= 0:
            raise ValueError(
                f"Missing or invalid expected days for stratum {row.stratum!r}"
            )
        if not isfinite(row.actual_days) or row.actual_days < 0:
            raise ValueError("Actual patient days must be finite and nonnegative")
        count += row.separations
        actual += row.actual_days
        expected += row.separations * mean
    if not count or not isfinite(actual) or not isfinite(expected):
        raise ValueError("A nonempty eligible cohort with finite totals is required")
    return RelativeStayResult(
        benchmark, count, dict(excluded), actual, expected, actual / expected
    )
