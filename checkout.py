"""Turn a customer's cart into the amount they have to pay.

The web layer calls :func:`checkout` and stores the returned dictionary as an
order.  Keep the public functions in this module small and free of I/O so they
stay easy to unit test.
"""

from decimal import Decimal, ROUND_HALF_UP

from cart import Cart

#: Orders at or above this amount are shipped for free.
FREE_SHIPPING_THRESHOLD = 50.00

#: Flat shipping fee charged for smaller orders.
SHIPPING_FEE = 4.99

#: Fraction taken off the goods total for eligible student customers.
STUDENT_DISCOUNT_RATE = 0.10

#: Money is always rounded to two decimal places, half up.
CENTS = Decimal("0.01")


def _money(value):
    """Round ``value`` to cents, half up, and return it as a float.

    Prices are computed with :class:`~decimal.Decimal` so that a discount never
    introduces binary floating point noise such as ``17.990000000000002``.
    """
    return float(Decimal(str(value)).quantize(CENTS, rounding=ROUND_HALF_UP))


class Customer:
    """A customer who places an order.

    ``is_student`` marks a customer as eligible for the student discount.  It
    defaults to ``False`` so that existing call sites keep working.
    """

    def __init__(self, name, is_student=False):
        self.name = name
        self.is_student = bool(is_student)

    def __repr__(self):
        return f"Customer({self.name!r}, is_student={self.is_student!r})"


def apply_student_discount(total, is_student):
    """Return ``total`` after the 10% student discount, if applicable.

    Only eligible customers (``is_student`` is true) get the discount; every
    other customer pays the original amount.  The result is rounded to cents
    so an order never ends up with fractions of a penny.
    """
    if is_student:
        rate = Decimal(str(STUDENT_DISCOUNT_RATE))
        return _money(Decimal(str(total)) * (Decimal("1") - rate))
    return total


def shipping_cost(subtotal):
    """Shipping fee for an order whose goods are worth ``subtotal``.

    The free-shipping threshold is decided on the full goods value, before the
    student discount, so a student does not lose free shipping by using the
    discount.
    """
    if subtotal >= FREE_SHIPPING_THRESHOLD:
        return 0.0
    return SHIPPING_FEE


def calculate_total(cart, customer):
    """Amount payable by ``customer`` for ``cart``.

    The goods subtotal is discounted when the customer is a student, shipping
    is added on top, and the result is rounded to cents.
    """
    if not isinstance(cart, Cart):
        raise TypeError("cart must be a Cart instance")
    if not isinstance(customer, Customer):
        raise TypeError("customer must be a Customer instance")

    subtotal = cart.subtotal()
    payable_goods = apply_student_discount(subtotal, customer.is_student)
    return _money(payable_goods + shipping_cost(subtotal))


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
