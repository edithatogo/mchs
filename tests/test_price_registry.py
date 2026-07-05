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


def test_price_registry_lists_available_years_and_jurisdictions():
    registry = price_registry.PriceRegistry.default()

    assert registry.list_available_years() == ["2025", "2026"]
    assert set(registry.list_available_jurisdictions("2025")) >= {
        "Brisbane_LHN",
        "National",
        "NSW",
        "Sydney_LHN",
        "VIC",
    }


def test_price_registry_returns_public_national_price_with_provenance():
    record = price_registry.get_national_price("2026")

    assert record.jurisdiction == "National"
    assert record.price_per_hwau == 7418
    assert record.schedule_type is price_registry.PriceScheduleType.NATIONAL
    assert record.support_status is price_registry.PriceSourceStatus.PUBLIC
    assert any("IHACPA NEP" in note for note in record.provenance_notes)
    assert record.checksum


def test_price_registry_returns_state_and_local_prices():
    state = price_registry.get_state_price("NSW", "2025")
    local = price_registry.get_local_price("Sydney_LHN", "2025")

    assert state.price_per_hwau == 7300
    assert state.support_status is price_registry.PriceSourceStatus.LOCAL_ONLY
    assert state.schedule_type is price_registry.PriceScheduleType.STATE
    assert local.price_per_hwau == 7100
    assert local.schedule_type is price_registry.PriceScheduleType.LOCAL


def test_price_registry_applies_discount_rules():
    multiplier = price_registry.get_discounted_price("NSW_rural_multiplier", "2025")
    fixed = price_registry.get_discounted_price("VIC_fixed_discount", "2025")
    percentage = price_registry.get_discounted_price("QLD_percentage_discount", "2025")

    assert multiplier.price_per_hwau == 8395
    assert multiplier.discount_rule is not None
    assert multiplier.discount_rule.rule_type == "multiplier"
    assert fixed.price_per_hwau == 6800
    assert fixed.discount_rule is not None
    assert fixed.discount_rule.rule_type == "fixed_price"
    assert percentage.price_per_hwau == 6840
    assert percentage.discount_rule is not None
    assert percentage.discount_rule.rule_type == "percentage_discount"


def test_price_registry_fails_closed_for_missing_and_blocked_schedules():
    registry = price_registry.PriceRegistry.default()

    assert registry.get_price("ACT", "2025") is None
    blocked = registry.require_price("WA_blocked_local_source", "2025")
    assert blocked.support_status is price_registry.PriceSourceStatus.BLOCKED

    try:
        registry.require_price("ACT", "2025")
    except price_registry.PriceRegistryError as exc:
        assert "No price schedule available" in str(exc)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("missing price schedule should fail closed")

    try:
        price_registry.get_state_price("WA", "2025")
    except price_registry.PriceRegistryError as exc:
        assert "not available" in str(exc)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("unavailable state price should fail closed")
