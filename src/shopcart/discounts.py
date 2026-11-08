"""Coupon codes."""
from datetime import date
from decimal import Decimal

COUPONS = {
    "SAVE10": {"kind": "percent", "value": Decimal("10"), "min_spend": Decimal("0"), "expires": date(2099, 12, 31)},
    "FLAT50": {"kind": "fixed", "value": Decimal("50"), "min_spend": Decimal("500"), "expires": date(2099, 12, 31)},
    "WELCOME100": {"kind": "fixed", "value": Decimal("100"), "min_spend": Decimal("0"), "expires": date(2099, 12, 31)},
    "DIWALI25": {"kind": "percent", "value": Decimal("25"), "min_spend": Decimal("0"), "expires": date(2026, 11, 15)},
}


def apply_coupon(subtotal, code, today=None):
    """Return the subtotal after applying the coupon code."""
    today = today or date.today()
    subtotal = Decimal(str(subtotal))
    c = COUPONS.get(code.upper() if isinstance(code, str) else code)
    if c is None:
        raise ValueError(f"unknown coupon {code}")
    if today > c["expires"]:
        raise ValueError(f"coupon {code} has expired")
    if subtotal < c["min_spend"] and c["min_spend"] > 0:
        raise ValueError(f"{code} needs a minimum spend of {c['min_spend']}")
    if c["kind"] == "percent":
        return (subtotal * (100 - c["value"]) / 100).quantize(Decimal("0.01"))
    return max(subtotal - c["value"], Decimal("0"))
