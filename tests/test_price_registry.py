from __future__ import annotations

from datetime import date

from nwau_py import price_registry


def test_price_schedule_record_serializes_discount_and_status():
    rule = price_registry.PriceDiscountRule(
        rule_type="multiplier",
        value=1.15,
        description="Rural loading multiplier",
    )
    record = price_registry.PriceScheduleRecord(
        jurisdiction="NSW",
        year="2025",
        price_per_hwau=7300,
        currency="AUD",
        effective_period=("2024-07-01", "2025-06-30"),
        source_url="https://example.test/prices/nsw-2025",
        retrieval_date=date(2026, 6, 12),
        checksum="abc123",
        licence="synthetic-test-fixture",
        schedule_type=price_registry.PriceScheduleType.STATE,
        discount_rule=rule,
        support_status=price_registry.PriceSourceStatus.LOCAL_ONLY,
        provenance_notes=("synthetic fixture", "no licensed payload"),
    )

    payload = record.to_dict()

    assert payload == {
        "jurisdiction": "NSW",
        "year": "2025",
        "price_per_hwau": 7300,
        "currency": "AUD",
        "effective_period": {"start": "2024-07-01", "end": "2025-06-30"},
        "source_url": "https://example.test/prices/nsw-2025",
        "retrieval_date": "2026-06-12",
        "checksum": "abc123",
        "licence": "synthetic-test-fixture",
        "schedule_type": "state",
        "support_status": "local_only",
        "provenance_notes": ["synthetic fixture", "no licensed payload"],
        "discount_rule": {
            "rule_type": "multiplier",
            "value": 1.15,
            "description": "Rural loading multiplier",
        },
    }


def test_price_schedule_record_omits_absent_discount_rule():
    record = price_registry.PriceScheduleRecord(
        jurisdiction="National",
        year="2025",
        price_per_hwau=None,
        currency="AUD",
        effective_period=("2024-07-01", "2025-06-30"),
        source_url="https://example.test/prices/national-2025",
        retrieval_date=date(2026, 6, 12),
        checksum="def456",
        licence="public",
        schedule_type=price_registry.PriceScheduleType.NATIONAL,
        support_status=price_registry.PriceSourceStatus.PUBLIC,
    )

    payload = record.to_dict()

    assert payload["price_per_hwau"] is None
    assert payload["schedule_type"] == "national"
    assert payload["support_status"] == "public"
    assert "discount_rule" not in payload
