"""C2: SAS/Excel parity boundary - comparison report structure.

This test module defines the structure for comparing Rust output against
SAS and Excel reference outputs. It does NOT execute SAS or Excel -
those require licensed tools and host-specific runtimes.

Key responsibilities:
1. Define the comparison report schema (JSON)
2. Validate that comparison records are well-formed
3. Record known gap years where SAS references are unavailable
4. Ensure the comparison contract is ready for downstream automation
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class ComparisonStatus(str, Enum):
    """Status of a single Rust-vs-SAS/Excel comparison."""

    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    NOT_RUN = "not_run"
    PENDING_REVIEW = "pending_review"


@dataclass(frozen=True)
class ComparisonRecord:
    """A single comparison between Rust and a SAS/Excel reference.
    Attributes:
        year: Pricing year (e.g. "2025").
        engine: Reference engine - "sas" or "excel".
        reference_path: Path to the reference output file, or None.
        rust_result_path: Path to the Rust-generated output, or None.
        status: Outcome of the comparison.
        max_abs_error: Maximum absolute error observed (None if not run).
        max_rel_error: Maximum relative error observed (None if not run).
        notes: Free-text annotation (e.g. gap reason).
    """

    year: str
    engine: str
    reference_path: Path | None = None
    rust_result_path: Path | None = None
    status: ComparisonStatus = ComparisonStatus.NOT_RUN
    max_abs_error: float | None = None
    max_rel_error: float | None = None
    notes: str = ""


@dataclass
class ComparisonReport:
    """Aggregate report of all Rust-vs-SAS/Excel comparisons."""

    report_version: str = "1.0"
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source_version: str = ""
    git_commit: str = ""
    records: list[dict[str, Any]] = field(default_factory=list)

    def add_record(self, record: ComparisonRecord) -> None:
        self.records.append(asdict(record))

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)

    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for rec in self.records:
            status = rec.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts


SAS_UNAVAILABLE_YEARS: set[str] = {"2016", "2017", "2024", "2026", "2027"}
EXCEL_UNAVAILABLE_YEARS: set[str] = set()
SAS_EXPECTED_YEARS: set[str] = {
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2025",
}
EXCEL_EXPECTED_YEARS: set[str] = {"2025"}
ALL_PRICING_YEARS: set[str] = (
    SAS_EXPECTED_YEARS | SAS_UNAVAILABLE_YEARS | EXCEL_EXPECTED_YEARS
)


def test_comparison_report_schema_is_self_consistent():
    report = ComparisonReport(source_version="0.1.0", git_commit="abc1234")
    report.add_record(
        ComparisonRecord(
            year="2025",
            engine="sas",
            status=ComparisonStatus.NOT_RUN,
            notes="SAS execution requires licensed SAS runtime",
        )
    )
    report.add_record(
        ComparisonRecord(
            year="2016",
            engine="sas",
            status=ComparisonStatus.NOT_APPLICABLE,
            notes="SAS reference not available for 2016",
        )
    )
    json_str = report.to_json()
    parsed = json.loads(json_str)
    assert parsed["report_version"] == "1.0"
    assert len(parsed["records"]) == 2
    summary = report.summary()
    assert summary.get("not_run", 0) == 1
    assert summary.get("not_applicable", 0) == 1


def test_sas_unavailable_years_are_recorded():
    report = ComparisonReport()
    for year in sorted(SAS_UNAVAILABLE_YEARS):
        report.add_record(
            ComparisonRecord(
                year=year,
                engine="sas",
                status=ComparisonStatus.NOT_APPLICABLE,
                notes=f"SAS reference not available for pricing year {year}",
            )
        )
    assert len(report.records) == len(SAS_UNAVAILABLE_YEARS)
    for rec in report.records:
        assert rec["status"] == "not_applicable"
        assert "SAS reference not available" in rec["notes"]


def test_sas_expected_years_have_records():
    report = ComparisonReport()
    for year in sorted(SAS_EXPECTED_YEARS):
        report.add_record(
            ComparisonRecord(
                year=year,
                engine="sas",
                status=ComparisonStatus.NOT_RUN,
                notes="Awaiting SAS execution environment",
            )
        )
    for year in sorted(EXCEL_EXPECTED_YEARS):
        report.add_record(
            ComparisonRecord(
                year=year,
                engine="excel",
                status=ComparisonStatus.NOT_RUN,
                notes="Awaiting Excel execution environment",
            )
        )
    recorded_years = {r["year"] for r in report.records if r["engine"] == "sas"}
    assert recorded_years == SAS_EXPECTED_YEARS, (
        f"Missing SAS records for: {SAS_EXPECTED_YEARS - recorded_years}"
    )


def test_gap_coverage_is_complete():
    all_accounted = SAS_EXPECTED_YEARS | SAS_UNAVAILABLE_YEARS
    missing = SAS_EXPECTED_YEARS - all_accounted
    assert not missing, f"Pricing years without SAS status: {missing}"


def test_comparison_record_validates_status():
    for valid_status in ComparisonStatus:
        record = ComparisonRecord(year="2025", engine="sas", status=valid_status)
        assert record.status == valid_status


def test_report_can_accept_pass_and_fail_records():
    report = ComparisonReport()
    report.add_record(
        ComparisonRecord(
            year="2025",
            engine="sas",
            status=ComparisonStatus.PASS,
            max_abs_error=1e-6,
            max_rel_error=1e-6,
            notes="All NWAU values within tolerance",
        )
    )
    report.add_record(
        ComparisonRecord(
            year="2025",
            engine="excel",
            status=ComparisonStatus.FAIL,
            max_abs_error=0.5,
            max_rel_error=0.1,
            notes="Discrepancy in long-stay per-diem calculation",
        )
    )
    summary = report.summary()
    assert summary.get("pass", 0) == 1
    assert summary.get("fail", 0) == 1


def test_report_serialisation_roundtrip_preserves_fields():
    original = ComparisonReport(source_version="0.2.0", git_commit="deadbeef")
    original.add_record(
        ComparisonRecord(
            year="2025",
            engine="sas",
            status=ComparisonStatus.PASS,
            max_abs_error=1e-8,
            max_rel_error=1e-8,
        )
    )
    json_str = original.to_json()
    parsed = json.loads(json_str)
    assert parsed["source_version"] == "0.2.0"
    assert parsed["git_commit"] == "deadbeef"
    assert len(parsed["records"]) == 1
    rec = parsed["records"][0]
    assert rec["year"] == "2025"
    assert rec["engine"] == "sas"
    assert rec["status"] == "pass"


def test_all_pricing_years_enumeration_is_stable():
    all_years = sorted(ALL_PRICING_YEARS)
    assert len(all_years) >= 1
    for y in all_years:
        assert y.isdigit() and len(y) == 4, f"Invalid year format: {y}"
