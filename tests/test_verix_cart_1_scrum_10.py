from datetime import date
from decimal import Decimal

import pytest

from shopcart import Cart, apply_coupon


# ---------------------------------------------------------------------------
# SCRUM-10 AC1
# ---------------------------------------------------------------------------

def test_add_new_sku_sets_quantity():
    # AC: SCRUM-10 AC1
    c = Cart()
    c.add_item("PEN", 10, 2)
    assert c.items["PEN"]["qty"] == 2


def test_bug_ac1_repeated_sku_increases_quantity():
    """BUG SCRUM-10 AC1: adding an existing SKU overwrites the quantity instead of increasing it (PEN x2 then PEN x3 must give 5)."""
    c = Cart()
    c.add_item("PEN", 10, 2)
    c.add_item("PEN", 10, 3)
    assert c.items["PEN"]["qty"] == 5


# ---------------------------------------------------------------------------
# SCRUM-10 AC2
# ---------------------------------------------------------------------------

def test_quantity_of_one_is_valid():
    # AC: SCRUM-10 AC2
    c = Cart()
    c.add_item("PEN", 10, 1)
    assert c.items["PEN"]["qty"] == 1


def test_negative_quantity_raises_value_error():
    # AC: SCRUM-10 AC2
    c = Cart()
    with pytest.raises(ValueError):
        c.add_item("PEN", 10, -1)


def test_bug_ac2_zero_quantity_raises_value_error():
    """BUG SCRUM-10 AC2: a quantity of 0 is accepted, but a quantity of 0 or below must raise ValueError."""
    c = Cart()
    with pytest.raises(ValueError):
        c.add_item("PEN", 10, 0)


def test_bug_ac2_fractional_quantity_raises_value_error():
    """BUG SCRUM-10 AC2: a non-whole quantity (1.5) is accepted, but the quantity must be a whole number."""
    c = Cart()
    with pytest.raises(ValueError):
        c.add_item("PEN", 10, 1.5)


# ---------------------------------------------------------------------------
# SCRUM-10 AC3
# ---------------------------------------------------------------------------

def test_remove_existing_sku():
    # AC: SCRUM-10 AC3
    c = Cart()
    c.add_item("PEN", 10, 2)
    c.remove_item("PEN")
    assert "PEN" not in c.items


def test_bug_ac3_removing_missing_sku_raises_key_error():
    """BUG SCRUM-10 AC3: removing a SKU that is not in the cart silently does nothing, but must raise KeyError."""
    c = Cart()
    with pytest.raises(KeyError):
        c.remove_item("NOPE")


# ---------------------------------------------------------------------------
# SCRUM-10 AC4
# ---------------------------------------------------------------------------

def test_total_is_subtotal_plus_gst():
    # AC: SCRUM-10 AC4
    c = Cart()
    c.add_item("BOOK", 100, 1)
    assert c.total() == Decimal("118.00")


def test_bug_ac4_total_rounded_half_up_as_decimal():
    """BUG SCRUM-10 AC4: total() uses float round() and returns a float instead of a Decimal rounded half-up to 2 decimals; subtotal 10.25 must give Decimal('12.10')."""
    c = Cart()
    c.add_item("A", Decimal("10.25"), 1)
    assert c.total() == Decimal("12.10")


# ---------------------------------------------------------------------------
# SCRUM-10 AC5
# ---------------------------------------------------------------------------

def test_flat50_above_min_spend():
    # AC: SCRUM-10 AC5
    assert apply_coupon(Decimal("600"), "FLAT50") == Decimal("550")


def test_flat50_below_min_spend_raises_value_error():
    # AC: SCRUM-10 AC5
    with pytest.raises(ValueError):
        apply_coupon(Decimal("499.99"), "FLAT50")


def test_bug_ac5_flat50_qualifies_at_exactly_500():
    """BUG SCRUM-10 AC5: FLAT50 must take 50 off when the subtotal is exactly 500, but the code rejects exactly 500 with ValueError."""
    assert apply_coupon(Decimal("500"), "FLAT50") == Decimal("450")


# ---------------------------------------------------------------------------
# SCRUM-10 AC6
# ---------------------------------------------------------------------------

def test_fixed_discount_on_large_subtotal():
    # AC: SCRUM-10 AC6
    assert apply_coupon(Decimal("200"), "WELCOME100") == Decimal("100")


def test_bug_ac6_discount_never_makes_amount_negative():
    """BUG SCRUM-10 AC6: WELCOME100 on a subtotal of 60 must be clamped to 0, but the code returns -40."""
    assert apply_coupon(Decimal("60"), "WELCOME100") == Decimal("0")


# ---------------------------------------------------------------------------
# SCRUM-10 AC7
# ---------------------------------------------------------------------------

def test_save10_uppercase_code_works():
    # AC: SCRUM-10 AC7
    assert apply_coupon(Decimal("200"), "SAVE10") == Decimal("180.00")


def test_bug_ac7_coupon_codes_are_case_insensitive():
    """BUG SCRUM-10 AC7: coupon codes must not be case-sensitive, but the lookup is an exact match so lowercase "save10" is not found."""
    assert apply_coupon(Decimal("200"), "save10") == Decimal("180.00")


# ---------------------------------------------------------------------------
# SCRUM-10 AC8
# ---------------------------------------------------------------------------

def test_diwali25_works_before_expiry():
    # AC: SCRUM-10 AC8
    assert apply_coupon(Decimal("200"), "DIWALI25", today=date(2026, 11, 14)) == Decimal("150.00")


def test_bug_ac8_diwali25_works_on_expiry_date():
    """BUG SCRUM-10 AC8: DIWALI25 must work on its expiry date 2026-11-15, but the code rejects it as expired on that day."""
    assert apply_coupon(Decimal("200"), "DIWALI25", today=date(2026, 11, 15)) == Decimal("150.00")


def test_diwali25_fails_day_after_expiry():
    # AC: SCRUM-10 AC8
    with pytest.raises(ValueError):
        apply_coupon(Decimal("200"), "DIWALI25", today=date(2026, 11, 16))
