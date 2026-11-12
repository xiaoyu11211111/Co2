"""Turn a customer's cart into the amount they have to pay.

The web layer calls :func:`checkout` and stores the returned dictionary as an
order.  Keep the public functions in this module small and free of I/O so they
stay easy to unit test.
"""

from cart import Cart

#: Orders at or above this amount are shipped for free.
FREE_SHIPPING_THRESHOLD = 50.00

#: Flat shipping fee charged for smaller orders.
SHIPPING_FEE = 4.99


class Customer:
    """A customer who places an order."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Customer({self.name!r})"


def shipping_cost(subtotal):
    """Shipping fee for an order whose goods are worth ``subtotal``."""
    if subtotal >= FREE_SHIPPING_THRESHOLD:
        return 0.0
    return SHIPPING_FEE


def calculate_total(cart, customer):
    """Amount payable by ``customer`` for ``cart``.

    The result is the goods subtotal plus shipping, rounded to cents.
    """
    if not isinstance(cart, Cart):
        raise TypeError("cart must be a Cart instance")
    if not isinstance(customer, Customer):
        raise TypeError("customer must be a Customer instance")

    subtotal = cart.subtotal()
    return round(subtotal + shipping_cost(subtotal), 2)


def checkout(cart, customer):
    """Checkout entry point used by the web layer.

    Returns an order summary dictionary instead of writing to a database, so
    that the pricing rules can be tested in isolation.
    """
    return {
        "customer": customer.name,
        "items": len(cart),
        "total": calculate_total(cart, customer),
    }
