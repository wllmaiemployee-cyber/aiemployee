from decimal import Decimal

from shopcart import Cart, apply_coupon


def test_subtotal_of_two_items():
    c = Cart()
    c.add_item("PEN", 10, 2)
    c.add_item("BOOK", 250)
    assert c.subtotal() == Decimal("270.00")


def test_save10():
    assert apply_coupon(200, "SAVE10") == Decimal("180.00")
