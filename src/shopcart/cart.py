"""Shopping cart: items keyed by SKU, prices in rupees."""
from decimal import ROUND_HALF_UP, Decimal

GST_RATE = Decimal("0.18")


class Cart:
    def __init__(self):
        self.items = {}  # sku -> {"price": Decimal, "qty": int}

    def add_item(self, sku, price, qty=1):
        if qty <= 0:
            raise ValueError("quantity must be positive")
        if sku in self.items:
            self.items[sku]["qty"] += qty
        else:
            self.items[sku] = {"price": Decimal(str(price)), "qty": qty}

    def remove_item(self, sku):
        self.items.pop(sku)

    def subtotal(self):
        total = sum((i["price"] * i["qty"] for i in self.items.values()), Decimal("0"))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def total(self):
        sub = self.subtotal()
        return (sub * (1 + GST_RATE)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
