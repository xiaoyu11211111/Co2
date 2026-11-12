"""Shopping cart objects for the online shopping application.

A cart only knows which products a customer picked.  All pricing rules
(shipping, discounts, taxes) live in :mod:`checkout`.
"""


class CartItem:
    """One product line inside a cart."""

    def __init__(self, name, unit_price, quantity=1):
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        self.name = name
        self.unit_price = float(unit_price)
        self.quantity = int(quantity)

    @property
    def line_total(self):
        """Price of this line, rounded to cents."""
        return round(self.unit_price * self.quantity, 2)

    def __repr__(self):
        return (
            f"CartItem({self.name!r}, {self.unit_price!r}, {self.quantity!r})"
        )


class Cart:
    """An ordered collection of :class:`CartItem` objects."""

    def __init__(self, items=None):
        self.items = list(items or [])

    def add(self, item):
        """Append ``item`` to the cart and return the cart (chainable)."""
        self.items.append(item)
        return self

    def subtotal(self):
        """Sum of every line total, before shipping and discounts."""
        return round(sum(item.line_total for item in self.items), 2)

    def __len__(self):
        return len(self.items)
