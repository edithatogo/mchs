"""Apply versioned Australian financial-year stay benchmarks to disjoint cohorts."""

import csv
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from math import isfinite
from pathlib import Path
from typing import Literal

from .relative_stay import RelativeStayResult, StayStratum, relative_stay_index

Kind = Literal["pricing_alos", "rsi"]


@dataclass(frozen=True)
class Benchmark:
    edition: str
    source: str
    means: dict[str, float]


@dataclass(frozen=True)
class DatedStay:
    separation_date: date
    edition: str
    stay: StayStratum


@dataclass(frozen=True)
class StayReport:
    kind: Kind
    annual: dict[int, RelativeStayResult]
    pooled: RelativeStayResult


def load_benchmarks(path: Path) -> dict[tuple[str, int], Benchmark]:
    """Read one named series per kind. Year is the four-digit FY starting year."""
    registry: dict[tuple[str, int], Benchmark] = {}
    fields = {"kind", "start_year", "edition", "stratum", "expected_days", "source"}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if set(reader.fieldnames or ()) != fields or len(
            reader.fieldnames or ()
        ) != len(fields):
            raise ValueError("Unexpected benchmark CSV header")
        for row in reader:
            if None in row or any(not (value or "").strip() for value in row.values()):
                raise ValueError(f"Incomplete benchmark at line {reader.line_num}")
            kind, year, edition, stratum, days, source = (
                row[key].strip()
                for key in (
                    "kind",
                    "start_year",
                    "edition",
                    "stratum",
                    "expected_days",
                    "source",
                )
            )
            if (
                kind not in ("pricing_alos", "rsi")
                or len(year) != 4
                or not year.isdecimal()
            ):
                raise ValueError("Invalid benchmark kind or financial year")
            mean = float(days)
            if not isfinite(mean) or mean <= 0:
                raise ValueError("Expected days must be finite and positive")
            ref = registry.setdefault((kind, int(year)), Benchmark(edition, source, {}))
            if (ref.edition, ref.source) != (edition, source) or stratum in ref.means:
                raise ValueError("Conflicting benchmark metadata or duplicate stratum")
            ref.means[stratum] = mean
    if not registry:
        raise ValueError("Empty benchmark file")
    return registry


def calculate_stay_report(
    rows: Iterable[DatedStay], registry: dict[tuple[str, int], Benchmark], *, kind: Kind
) -> StayReport:
    """Each row represents separations with the same FY, edition and stratum."""
    groups: dict[int, list[StayStratum]] = defaultdict(list)
    for row in rows:
        d = row.separation_date
        year = d.year if d.month >= 7 else d.year - 1
        ref = registry.get((kind, year))
        if ref is None or (
            row.stay.exclusion_reason is None and ref.edition != row.edition
        ):
            raise ValueError(
                f"No matching {kind} benchmark for FY {year} and edition {row.edition}"
            )
        groups[year].append(row.stay)
    annual = {}
    pooled_rows = []
    pooled_means = {}
    for year, stays in sorted(groups.items()):
        ref = registry[kind, year]
        label = f"{kind} | FY {year} | {ref.edition} | {ref.source}"
        annual[year] = relative_stay_index(stays, ref.means, benchmark=label)
        for stay in stays:
            key = f"{year}:{stay.stratum}"
            pooled_rows.append(
                StayStratum(
                    key, stay.separations, stay.actual_days, stay.exclusion_reason
                )
            )
            if stay.exclusion_reason is None:
                pooled_means[key] = ref.means[stay.stratum]
    pooled = relative_stay_index(
        pooled_rows,
        pooled_means,
        benchmark="; ".join(result.benchmark for result in annual.values()) or kind,
    )
    return StayReport(kind, annual, pooled)
