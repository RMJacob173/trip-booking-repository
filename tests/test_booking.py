# tests/test_booking.py — Trip Booking Calculator Tests
# Existing test suite from Lecture 6.6

import pytest
from booking import (
    calculate_total_price,
    apply_seasonal_discount,
    calculate_tax,
    get_price_category,
    format_booking_summary,
    calculate_final_price,
)


# ── Happy Path Tests ──────────────────────────────────────────────────────────

def test_calculate_total_price_returns_correct_value():
    """Normal case: 3 nights, 2 guests at $100/night = $600."""
    assert calculate_total_price(100, 3, 2) == 600.0


def test_apply_seasonal_discount_january():
    """January has 15% discount — $1000 becomes $850."""
    assert apply_seasonal_discount(1000, 1) == 850.0


def test_calculate_tax_france():
    """France has 20% tax — $500 tax = $100."""
    assert calculate_tax(500, "france") == 100.0


def test_get_price_category_budget():
    """Under $500 should be 'budget'."""
    assert get_price_category(400) == "budget"


def test_get_price_category_mid_range():
    """$1000 should be 'mid-range'."""
    assert get_price_category(1000) == "mid-range"


def test_get_price_category_luxury():
    """Over $2000 should be 'luxury'."""
    assert get_price_category(2500) == "luxury"


def test_format_booking_summary_contains_trip_name():
    """Summary string must contain the trip name."""
    result = format_booking_summary("Paris Adventure", "france", 1200.0, 2)
    assert "Paris Adventure" in result


def test_calculate_final_price_basic():
    """Calculate final price: $100/night × 3 nights × 2 guests, June, France.

    Calculation: 600 (base) → 600 (no discount in June) → 600 + 120 (tax) = 720.
    """
    result = calculate_final_price(100, 3, 2, 6, "france")
    assert result == 720.0


def test_calculate_final_price_with_seasonal_discount():
    """Verify seasonal discount is applied: January has 15% off.

    Calculation: 600 (base) → 510 (15% off) → 510 + 51 (10% japan tax) = 561.
    """
    result = calculate_final_price(100, 3, 2, 1, "japan")
    assert result == 561.0


# ── Edge Case Tests ───────────────────────────────────────────────────────────

def test_calculate_total_price_zero_nights_raises():
    """nights=0 must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_total_price(100, 0, 2)


def test_calculate_total_price_zero_guests_raises():
    """guests=0 must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_total_price(100, 3, 0)


def test_apply_seasonal_discount_month_zero_raises():
    """month=0 is invalid and must raise ValueError."""
    with pytest.raises(ValueError):
        apply_seasonal_discount(1000, 0)


def test_apply_seasonal_discount_month_13_raises():
    """month=13 is invalid and must raise ValueError."""
    with pytest.raises(ValueError):
        apply_seasonal_discount(1000, 13)


def test_get_price_category_negative_price_raises():
    """Negative price must raise ValueError."""
    with pytest.raises(ValueError):
        get_price_category(-100)


def test_calculate_tax_unknown_country_raises():
    """Unknown country must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_tax(500, "mars")


def test_calculate_final_price_zero_nights_raises():
    """calculate_final_price must raise ValueError for zero nights."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 0, 2, 6, "france")


def test_calculate_final_price_zero_guests_raises():
    """calculate_final_price must raise ValueError for zero guests."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 0, 6, "france")


def test_calculate_final_price_invalid_month_raises():
    """calculate_final_price must raise ValueError for invalid month."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 2, 13, "france")


def test_calculate_final_price_unsupported_country_raises():
    """calculate_final_price must raise ValueError for unsupported country."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 2, 6, "mars")
