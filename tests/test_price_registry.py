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


def test_national_price_uses_packaged_nep_constants():
    record = price_registry.get_national_price("2026")

    assert record.jurisdiction == "National"
    assert record.year == "2026"
    assert record.price_per_hwau == 7418
    assert record.schedule_type is price_registry.PriceScheduleType.NATIONAL
    assert record.support_status is price_registry.PriceSourceStatus.PUBLIC
    assert record.effective_period == ("2025-07-01", "2026-06-30")


def test_state_local_and_discounted_price_lookups_are_explicitly_synthetic():
    state = price_registry.get_state_price("nsw", 2025)
    local = price_registry.get_local_price("Sydney_LHN", "2025")
    discounted = price_registry.get_discounted_price("NSW_rural_multiplier", "2025")

    assert state.price_per_hwau == 7300
    assert state.schedule_type is price_registry.PriceScheduleType.STATE
    assert state.support_status is price_registry.PriceSourceStatus.LOCAL_ONLY
    assert "Synthetic state price fixture" in state.provenance_notes[0]

    assert local.price_per_hwau == 7100
    assert local.schedule_type is price_registry.PriceScheduleType.LOCAL
    assert local.support_status is price_registry.PriceSourceStatus.LOCAL_ONLY

    assert discounted.price_per_hwau == 8395.0
    assert discounted.schedule_type is price_registry.PriceScheduleType.DISCOUNTED
    assert discounted.discount_rule is not None
    assert discounted.discount_rule.rule_type == "multiplier"
    assert discounted.discount_rule.value == 1.15


def test_registry_facade_lists_and_resolves_schedules():
    registry = price_registry.PriceRegistry()

    assert registry.list_years() == ["2025", "2026"]
    assert "NSW" in registry.list_jurisdictions(price_registry.PriceScheduleType.STATE)
    assert "Sydney_LHN" in registry.list_jurisdictions("local")
    assert registry.national("2025").price_per_hwau == 7434
    assert registry.state("VIC", "2026").price_per_hwau == 7550
    assert registry.local("Brisbane_LHN", "2026").price_per_hwau == 7000
    assert registry.discounted("VIC_fixed_discount", "2025").price_per_hwau == 6800.0


def test_invalid_price_registry_requests_fail_closed():
    for call in [
        lambda: price_registry.get_national_price("1999"),
        lambda: price_registry.get_state_price("TAS", "2025"),
        lambda: price_registry.get_local_price("Missing_LHN", "2025"),
        lambda: price_registry.get_discounted_price("missing_rule", "2025"),
    ]:
        try:
            call()
        except price_registry.PriceRegistryError:
            continue
        raise AssertionError("expected PriceRegistryError")
